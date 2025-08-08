import cv2
import numpy as np
import time
import random
import rclpy
from rknnlite.api import RKNNLite
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from cv_bridge import CvBridge
from multiprocessing import Process, Manager
from PIL import ImageFont, ImageDraw, Image

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy

# 跨进程通信队列
manager = Manager()
IMG_QUEUE = manager.Queue()
INFO_QUEUE = manager.Queue()
WORKING = manager.Value('b', False)

# 定义类别中文映射及颜色（BGR）
CLASS_INFO = {
    0: {"name": "纸巾",   "color": (255, 0, 0)},    # Blue
    1: {"name": "瓶子",   "color": (0, 255, 0)},    # Green
    2: {"name": "药物",   "color": (0, 0, 255)},    # Red
    3: {"name": "塑料",   "color": (255, 255, 0)},  # Cyan
    4: {"name": "口罩",   "color": (255, 0, 255)},  # Magenta
    5: {"name": "烟雾",   "color": (0, 255, 255)},  # Yellow
}

# 替换为系统中可用支持中文的字体路径
FONT_PATH = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
FONT_SIZE = 20
CHINESE_FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# def plot_one_box(box, img, class_id, score, line_thickness=2):
#     """
#     在图像 img 上绘制单个检测框并标注中文类别及置信度
#     box: [x1, y1, x2, y2]
#     class_id: 类别索引
#     score: 置信度
#     """
#     c1 = (int(box[0]), int(box[1]))
#     c2 = (int(box[2]), int(box[3]))
#     info = CLASS_INFO.get(class_id, {})
#     color = info.get("color", (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
#     label = f"{info.get('name','未知')} {score:.2f}"
#     # 绘制矩形框
#     cv2.rectangle(img, c1, c2, color, thickness=line_thickness, lineType=cv2.LINE_AA)
#     # 计算文字背景大小并绘制
#     tf = max(line_thickness - 1, 1)
#     t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, line_thickness / 3, tf)[0]
#     c2_label = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
#     cv2.rectangle(img, c1, c2_label, color, -1, cv2.LINE_AA)
#     cv2.putText(img, label, (c1[0], c1[1] - 2),
#                 cv2.FONT_HERSHEY_SIMPLEX, line_thickness / 3, (255, 255, 255), thickness=tf, lineType=cv2.LINE_AA)

def plot_one_box(box, img, class_id, score, line_thickness=2):
    """
    在图像上绘制检测框：
      - 左上角：中文类别（PIL 绘制，白字 + 深蓝灰底）
      - 右上角：英文数字置信度（OpenCV 绘制，白字 + 同色底）
    """
    x1, y1 = int(box[0]), int(box[1])
    x2, y2 = int(box[2]), int(box[3])

    info = CLASS_INFO.get(class_id, {"name": "未知", "color": (0, 255, 255)})
    name = info["name"]
    color = info["color"]

    # --- 绘制主框 ---
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=line_thickness, lineType=cv2.LINE_AA)

    # === 左上角：PIL 绘制中文类别 ===
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    padding = 6
    text_w, text_h = draw.textsize(name, font=CHINESE_FONT)
    name_bg_x1 = x1
    name_bg_y1 = max(0, y1 - text_h - 2 * padding)
    name_bg_x2 = x1 + text_w + 2 * padding
    name_bg_y2 = y1

    bg_color = (40, 50, 70)  # 深蓝灰

    # 背景+文字
    draw.rectangle([name_bg_x1, name_bg_y1, name_bg_x2, name_bg_y2], fill=bg_color)
    draw.text((name_bg_x1 + padding, name_bg_y1 + padding), name, font=CHINESE_FONT, fill=(255, 255, 255))

    # 转回 BGR 图像
    img[:, :, :] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # === 右上角：OpenCV 绘制置信度 ===
    conf_text = f"{score:.2f}"
    tf = max(line_thickness - 1, 1)
    font_scale = 0.6
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 计算文本尺寸
    (tw, th), baseline = cv2.getTextSize(conf_text, font, font_scale, tf)
    padding = 6
    conf_bg_x2 = x2
    conf_bg_x1 = x2 - tw - 2 * padding
    conf_bg_y1 = max(0, y1 - th - 2 * padding)
    conf_bg_y2 = y1

    # 画填充背景框（颜色为检测框色）
    cv2.rectangle(img, (conf_bg_x1, conf_bg_y1), (conf_bg_x2, conf_bg_y2), color, thickness=-1, lineType=cv2.LINE_AA)

    # 绘制文本（居中）
    text_org = (conf_bg_x1 + padding, conf_bg_y2 - padding - 1)
    cv2.putText(img, conf_text, text_org, font, font_scale, (255, 255, 255), tf, lineType=cv2.LINE_AA)




    
def post_process_opencv(outputs, model_h, model_w, img_h, img_w, nms_thresh, conf_thresh):
    """
    输出解码、NMS 返回框、置信度及类别
    """
    # outputs: [N, 5+num_classes] 格式：[cx,cy,w,h,conf,cls1,cls2...]
    outputs = outputs.reshape(-1, outputs.shape[-1])
    # 提取信息
    conf = outputs[:, 4]
    cls_scores = outputs[:, 5:]
    cls_ids = np.argmax(cls_scores, axis=1)
    # 转换到原图坐标
    cx = outputs[:, 0] / model_w * img_w
    cy = outputs[:, 1] / model_h * img_h
    w  = outputs[:, 2] / model_w * img_w
    h  = outputs[:, 3] / model_h * img_h
    x1 = cx - w / 2
    y1 = cy - h / 2
    x2 = cx + w / 2
    y2 = cy + h / 2
    boxes = np.stack([x1, y1, x2, y2], axis=1).tolist()
    # 执行 NMS
    idxs = cv2.dnn.NMSBoxes(boxes, conf.tolist(), conf_thresh, nms_thresh)
    if len(idxs) > 0:
        idxs = idxs.flatten()
        return [boxes[i] for i in idxs], conf[idxs], cls_ids[idxs]
    else:
        return [], [], []

def _make_grid(nx, ny):
    xv, yv = np.meshgrid(np.arange(ny), np.arange(nx))
    return np.stack((xv, yv), 2).reshape(-1, 2).astype(np.float32)

def cal_outputs(outs, nl, na, model_w, model_h, anchor_grid, stride):
    """
    还原 YOLO 输出到边框格式
    """
    row = 0
    for i in range(nl):
        h, w = model_h // int(stride[i]), model_w // int(stride[i])
        length = na * h * w
        if outs[row:row+length, :].shape[0] != length:
            break
        grid = np.tile(_make_grid(w, h), (na, 1))
        # xy
        outs[row:row+length, 0:2] = (outs[row:row+length, 0:2] * 2 - 0.5 + grid) * stride[i]
        # wh
        outs[row:row+length, 2:4] = (outs[row:row+length, 2:4] * 2) ** 2 * np.repeat(anchor_grid[i], h*w, axis=0)
        row += length
    return outs

def inference_process(img_q, info_q, working_flag):
    working_flag.value = True
    # 模型和参数初始化
    # model_path = '/home/uboot/data/xyc/yolov5_320.rknn'
    model_path = '/home/uboot/data/xyc/730.rknn'
    model_h, model_w = 320, 320
    nl, na = 3, 3
    stride = [8., 16., 32.]
    anchors = [[10,13,16,30,33,23], [30,61,62,45,59,119], [116,90,156,198,373,326]]
    anchor_grid = np.asarray(anchors, np.float32).reshape(nl, -1, 2)

    # 加载并初始化 RKNN 模型
    rknn = RKNNLite()
    rknn.load_rknn(model_path)
    rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_2)
    print('[IMG NODE] RKNN 初始化完成')

    cap = cv2.VideoCapture('/dev/video21')
    if not cap.isOpened():
        print('[ERROR] 摄像头打开失败')
        working_flag.value = False
        return

    counter, start_time, fps = 0, time.time(), 0
    while working_flag.value:
        ret, img0 = cap.read()
        if not ret:
            continue

        # 推理前处理
        img = cv2.resize(img0, (model_w, model_h))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        outputs = rknn.inference(inputs=[np.expand_dims(img_rgb.astype(np.uint8), 0)])
        if outputs is None:
            continue

        # 后处理
        raw = outputs[0].squeeze(0).astype(np.float32)
        processed = cal_outputs(raw, nl, na, model_w, model_h, anchor_grid, stride)
        boxes, confs, cls_ids = post_process_opencv(processed, model_h, model_w, img0.shape[0], img0.shape[1], 0.4, 0.5)

        # 绘制结果并收集信息
        detect_msgs = []
        # for box, score, cid in zip(boxes, confs, cls_ids):
        #     plot_one_box(box, img0, cid, score, line_thickness=2)
        #     info = CLASS_INFO.get(cid, {})
        #     cx, cy = int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)
        #     detect_msgs.append(f"{info.get('name','未知')} {score:.2f} 坐标:({cx},{cy})")
        CONFIDENCE_THRESHOLD = 0.6

        for box, score, cid in zip(boxes, confs, cls_ids):
            if score < CONFIDENCE_THRESHOLD:
                continue  # 不绘制低置信度目标
            plot_one_box(box, img0, cid, score, line_thickness=2)
            info = CLASS_INFO.get(cid, {})
            cx, cy = int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)
            # detect_msgs.append(f"{info.get('name','未知')} {score:.2f} 坐标:({cx},{cy})")
            detect_msgs.append(f"{info.get('name','未知')}")


        # 计算并绘制 FPS
        counter += 1
        if time.time() - start_time >= 1:
            fps = counter / (time.time() - start_time)
            start_time, counter = time.time(), 0
        cv2.putText(img0, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # 发布信息到队列
        info_q.put("\n".join(detect_msgs) if detect_msgs else "无目标")
        img_q.put(img0)

    cap.release()

class MultiProcPublisher(Node):
    def __init__(self, img_q, info_q, working_flag):
        super().__init__('yolo_multiproc_publisher')
        # self.comp_pub = self.create_publisher(CompressedImage, 'yolo/result_image/compressed', 10)

        video_qos = QoSProfile(depth=1)
        video_qos.reliability = QoSReliabilityPolicy.BEST_EFFORT
        video_qos.durability = QoSDurabilityPolicy.VOLATILE

        self.comp_pub = self.create_publisher(CompressedImage, 'yolo/result_image/compressed', video_qos)

        self.detect_pub = self.create_publisher(String, 'yolo/detect_info', 10)
        self.bridge = CvBridge()
        self.img_q = img_q
        self.info_q = info_q
        self.working_flag = working_flag
        self.create_timer(0.01, self.timer_callback)
        print('[IMG NODE] 节点初始化完成')

    def timer_callback(self):
        if not self.working_flag.value:
            return
        # 发布图像
        if not self.img_q.empty():
            img = self.img_q.get()
            ok, buf = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY),70])
            if ok:
                msg = CompressedImage()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.format = 'jpeg'
                msg.data = buf.tobytes()
                self.comp_pub.publish(msg)
        # 发布检测文字信息
        if not self.info_q.empty():
            info_msg = String()
            info_msg.data = self.info_q.get()
            self.detect_pub.publish(info_msg)

if __name__ == '__main__':
    # 启动推理子进程
    p_inf = Process(target=inference_process, args=(IMG_QUEUE, INFO_QUEUE, WORKING))
    p_inf.start()
    # 初始化 ROS2
    rclpy.init()
    node = MultiProcPublisher(IMG_QUEUE, INFO_QUEUE, WORKING)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    # 停止推理
    WORKING.value = False
    p_inf.join()
    print('[IMG NODE] 退出')
    node.destroy_node()
    rclpy.shutdown()
