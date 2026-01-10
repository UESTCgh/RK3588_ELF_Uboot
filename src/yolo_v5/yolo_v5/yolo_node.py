import cv2
import numpy as np
import time
import random
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from cv_bridge import CvBridge
from multiprocessing import Process, Manager
from PIL import ImageFont, ImageDraw, Image
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy

# 使用 Manager 创建可跨进程通信的队列
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

# def plot_one_box(x, img, color=None, label=None, line_thickness=None):
#     tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
#     color = color or [random.randint(0, 255) for _ in range(3)]
#     c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
#     cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
#     if label:
#         tf = max(tl - 1, 1)
#         t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
#         c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
#         cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)
#         cv2.putText(
#             img,
#             label,
#             (c1[0], c1[1] - 2),
#             0,
#             tl / 3,
#             [225, 255, 255],
#             thickness=tf,
#             lineType=cv2.LINE_AA,
#         )

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


def post_process_opencv(outputs, model_h, model_w, img_h, img_w, thred_nms, thred_cond):
    conf = outputs[:, 4].tolist()
    c_x = outputs[:, 0] / model_w * img_w
    c_y = outputs[:, 1] / model_h * img_h
    w = outputs[:, 2] / model_w * img_w
    h = outputs[:, 3] / model_h * img_h
    p_cls = outputs[:, 5:]
    if len(p_cls.shape) == 1:
        p_cls = np.expand_dims(p_cls, 1)
    cls_id = np.argmax(p_cls, axis=1)

    p_x1 = np.expand_dims(c_x - w / 2, -1)
    p_y1 = np.expand_dims(c_y - h / 2, -1)
    p_x2 = np.expand_dims(c_x + w / 2, -1)
    p_y2 = np.expand_dims(c_y + h / 2, -1)
    areas = np.concatenate((p_x1, p_y1, p_x2, p_y2), axis=-1)

    if areas.size == 0:
        return [], [], []
    
    areas = areas.tolist()
    ids = cv2.dnn.NMSBoxes(areas, conf, thred_cond, thred_nms)
    if len(ids) > 0:
        ids = ids.flatten()
        return np.array(areas)[ids], np.array(conf)[ids], cls_id[ids]
    else:
        return [], [], []

def cal_outputs(outs, nl, na, model_w, model_h, anchor_grid, stride):
    row_ind = 0
    grid = [np.zeros(1)] * nl
    for i in range(nl):
        h, w = int(model_w / stride[i]), int(model_h / stride[i])
        length = int(na * h * w)
        if grid[i].shape[0] != length:
            grid[i] = _make_grid(w, h)
        outs[row_ind:row_ind + length, 0:2] = (outs[row_ind:row_ind + length, 0:2] * 2. - 0.5 + np.tile(
            grid[i], (na, 1))) * int(stride[i])
        outs[row_ind:row_ind + length, 2:4] = (outs[row_ind:row_ind + length, 2:4] * 2) ** 2 * np.repeat(
            anchor_grid[i], h * w, axis=0)
        row_ind += length
    return outs

def _make_grid(nx, ny):
    xv, yv = np.meshgrid(np.arange(ny), np.arange(nx))
    return np.stack((xv, yv), 2).reshape((-1, 2)).astype(np.float32)

# 推理核心代码
def infer_img(img0, net, model_h, model_w, nl, na, stride, anchor_grid):
    # 1. 缩放、归一化、RGB 转置
    img = cv2.resize(img0, (model_w, model_h))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    blob = np.transpose(img, (2,0,1))[None, ...]
    # 2. 前向推理
    net.setInput(blob)
    outs = net.forward().squeeze(0)
    # 3. 解码预测框
    outs = cal_outputs(outs, nl, na, model_w, model_h, anchor_grid, stride)
    # 4. 后处理 NMS，转换回原图尺寸
    h0, w0 = img0.shape[:2]
    boxes, confs, ids = post_process_opencv(
        outs, model_h, model_w, img0.shape[0], img0.shape[1],
        thred_nms=0.4, thred_cond=0.5
    )
    return boxes, confs, ids


# 包含推理逻辑，将结果放入队列
def inference_process(img_q, info_q, working_flag):
    working_flag.value = True
    # 初始化模型

    model_pb_path = "/home/user/ros2_uboot/src/yolo_v5/models/730_best.onnx"
    net = cv2.dnn.readNetFromONNX(model_pb_path)

    dic_labels = {0: 'tissue', 1: 'Bottle', 2: 'Medicine', 3: 'Plastic', 4: 'facemask', 5: 'smoke'}

    model_h, model_w = 320, 320
    nl, na = 3, 3
    stride = [8., 16., 32.]
    anchors = [[10,13,16,30,33,23], [30,61,62,45,59,119], [116,90,156,198,373,326]]
    anchor_grid = np.asarray(anchors, np.float32).reshape(nl, -1, 2)
    print("[INFO] load model success.")
    # 打开摄像头            
    # cap = cv2.VideoCapture('/dev/video25')
    video = 0
    cap = cv2.VideoCapture(video)
    
    if not cap.isOpened():
        print("[ERROR] Failed to open camera.")
        working_flag.value = False
        return

    counter = 0
    start_time = time.time()
    while time.time()-start_time < 3:
        ret, img0 = cap.read()
        counter += 1
    camera_fps = counter/(time.time()-start_time)
    counter = 0
    start_time = time.time()
    fps = 5
    input_counter = 0
    lock_fps = 5+1
    lock_fps_counter = 0
    lock_fps_current_avg_fps = 3
    boxes, confs, ids = [], [], []
    detect_msgs = []
    while working_flag.value:
        ret, img0 = cap.read()
        if not ret:
            continue
        if input_counter < camera_fps/(lock_fps+1):
            input_counter += 1
            continue
        input_counter = 0
        # 推理
        lock_fps_counter += 1
        if lock_fps_counter > (lock_fps/lock_fps_current_avg_fps):
            
            s1 = time.time()
            boxes, confs, ids = infer_img(img0, net, model_h, model_w, nl, na, stride, anchor_grid)
            s2 = time.time()
            lock_fps_current_avg_fps = lock_fps_current_avg_fps/3 + (1 / (s2-s1))*2/3
            
            # 绘制并生成信息
            detect_msgs = []
            # for box, score, cid in zip(boxes, confs, ids):
            #     label = f"{dic_labels[cid]} ({score:.2f})"
            #     plot_one_box(box.astype(int), img0, color=(0,0,255), label=label)
            #     cx, cy = int((box[0]+box[2])/2), int((box[1]+box[3])/2)
            #     detect_msgs.append(f"{dic_labels[cid]} ({score:.2f}) at ({cx},{cy})")
            #     print(f"[DETECT] {label} at ({cx},{cy}) confidence: {score:.2f}")
            lock_fps_counter = 0
        cls_ids_in_frame = []
        CONFIDENCE_THRESHOLD = 0.8
        for box, score, cid in zip(boxes, confs, ids):
            if score < CONFIDENCE_THRESHOLD:
                continue  # 不绘制低置信度目标
            plot_one_box(box, img0, cid, score, line_thickness=2)
            if cid not in cls_ids_in_frame:
                cls_ids_in_frame.append(cid)
            
        # 显示 FPS
        counter += 1
        if time.time()- start_time > 1:
            fps = counter / (time.time()- start_time)
            start_time = time.time()
            counter = 0
            # print(f"[INFO] FPS: {fps:.2f}")
        cv2.putText(img0, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if cls_ids_in_frame:
            info_q.put(" ".join(str(i) for i in cls_ids_in_frame))
        else:
            info_q.put("")  # 不发送“0”，用空串表示没检测到
        # info_q.put("\n".join(detect_msgs) if detect_msgs else "No objects detected")
        img_q.put(img0)

    cap.release()
    working_flag.value = False

# ROS 节点：从队列读取并发布
class MultiProcPublisher(Node):
    def __init__(self, img_q, info_q, working_flag):
        super().__init__('yolo_multiproc_publisher')
        # 配置 BEST_EFFORT & VOLATILE QoS
        video_qos = QoSProfile(depth=1)
        video_qos.reliability = QoSReliabilityPolicy.BEST_EFFORT
        video_qos.durability = QoSDurabilityPolicy.VOLATILE
        # 图像发布者
        self.comp_pub = self.create_publisher(
            CompressedImage,
            'yolo/result_image/compressed',
            video_qos
        )
        # 检测结果发布者
        self.detect_pub = self.create_publisher(String, 'yolo/detect_info', 10)
        self.bridge = CvBridge()
        self.img_q = img_q
        self.info_q = info_q
        self.working_flag = working_flag
        self.create_timer(0.01, self.timer_callback)
        print('[IMG NODE] 节点初始化完成，使用BEST_EFFORT QoS')

    def timer_callback(self):
        if not self.working_flag.value:
            return
        # 发布图像
        if not self.img_q.empty():
            img = self.img_q.get()
            ok, buf = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            if ok:
                msg = CompressedImage()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.format = 'jpeg'
                msg.data = buf.tobytes()
                self.comp_pub.publish(msg)
        # 发布检测信息
        if not self.info_q.empty():
            info_text = self.info_q.get()
            info_msg = String()
            info_msg.data = info_text
            self.detect_pub.publish(info_msg)


# 主入口：启动多进程和 ROS spin
if __name__ == '__main__':
    # 启动推理进程
    p_inf = Process(target=inference_process, args=(IMG_QUEUE, INFO_QUEUE, WORKING))
    p_inf.start()
    # ROS2 初始化
    rclpy.init()
    node = MultiProcPublisher(IMG_QUEUE, INFO_QUEUE, WORKING)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    # 停止推理
    WORKING.value = False
    p_inf.join()
    print('[IMG NODE] EXIT.')
    node.destroy_node()
    rclpy.shutdown()
