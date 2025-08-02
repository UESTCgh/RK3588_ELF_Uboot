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

# 使用 Manager 创建可跨进程通信的队列
manager = Manager()
IMG_QUEUE = manager.Queue()
INFO_QUEUE = manager.Queue()
WORKING = manager.Value('b', False)

def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)
        cv2.putText(
            img,
            label,
            (c1[0], c1[1] - 2),
            0,
            tl / 3,
            [225, 255, 255],
            thickness=tf,
            lineType=cv2.LINE_AA,
        )

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

# 包含推理逻辑，将结果放入队列
def inference_process(img_q, info_q, working_flag):
    working_flag.value = True
    # 初始化模型
    model_path = '/home/uboot/data/xyc/yolov5_320.rknn'
    dic_labels = {0: 'tissue', 1: 'Bottle', 2: 'Medicine', 3: 'Plastic', 4: 'facemask', 5: 'smoke'}
    model_h, model_w = 320, 320
    nl, na = 3, 3
    stride = [8., 16., 32.]
    anchors = [[10,13,16,30,33,23], [30,61,62,45,59,119], [116,90,156,198,373,326]]
    anchor_grid = np.asarray(anchors, np.float32).reshape(nl, -1, 2)
    # 加载 RKNN
    rknn = RKNNLite()
    rknn.load_rknn(model_path)
    rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_2)
    print('[IMG NODE] RKNN success...')
    # 打开摄像头            
    # cap = cv2.VideoCapture('/dev/video25')
    cap = cv2.VideoCapture('/dev/video21')
    if not cap.isOpened():
        print("[ERROR] Failed to open camera.")
        working_flag.value = False
        return

    counter = 0
    start_time = time.time()
    fps = 20
    while working_flag.value:
        ret, img0 = cap.read()
        if not ret:
            continue
        # 推理
        img = cv2.resize(img0, (model_w, model_h))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(img_rgb.astype(np.uint8), axis=0)
        outputs = rknn.inference(inputs=[input_data])
        if outputs is None:
            continue
        output = outputs[0].squeeze(0).astype(np.float32)
        # 这里简化调用 cal_outputs、post_process
        boxes, confs, ids = post_process_opencv(
            cal_outputs(output, nl, na, model_w, model_h, anchor_grid, stride),
            model_h, model_w, img0.shape[0], img0.shape[1], 0.4, 0.5
        )
        # 绘制并生成信息
        detect_msgs = []
        for box, score, cid in zip(boxes, confs, ids):
            label = f"{dic_labels[cid]} ({score:.2f})"
            plot_one_box(box.astype(int), img0, color=(0,0,255), label=label)
            cx, cy = int((box[0]+box[2])/2), int((box[1]+box[3])/2)
            detect_msgs.append(f"{dic_labels[cid]} ({score:.2f}) at ({cx},{cy})")
            print(f"[DETECT] {label} at ({cx},{cy}) confidence: {score:.2f}")
            
        # 显示 FPS
        counter += 1
        if time.time()- start_time > 1:
            fps = counter / (time.time()- start_time)
            start_time = time.time()
            counter = 0
        cv2.putText(img0, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        info_q.put("\n".join(detect_msgs) if detect_msgs else "No objects detected")
        img_q.put(img0)

    cap.release()

# ROS 节点：从队列读取并发布
class MultiProcPublisher(Node):
    def __init__(self, img_q, info_q, working_flag):
        super().__init__('yolo_multiproc_publisher')
        self.comp_pub = self.create_publisher(CompressedImage, 'yolo/result_image/compressed', 10)
        self.detect_pub = self.create_publisher(String, 'yolo/detect_info', 10)
        self.bridge = CvBridge()
        self.img_q = img_q
        self.info_q = info_q
        self.working_flag = working_flag
        self.create_timer(0.01, self.timer_callback)
        print('[IMG NODE] Loading model...')

    def timer_callback(self):
        if not self.working_flag.value:
            return
        # 发布图片
        if not self.img_q.empty():
            img = self.img_q.get()
            # small = cv2.resize(img, (480,360))
            ok, buf = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY),90])
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
