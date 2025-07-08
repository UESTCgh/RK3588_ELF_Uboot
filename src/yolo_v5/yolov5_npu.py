import cv2
import numpy as np
import random
import time
from rknnlite.api import RKNNLite

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from std_msgs.msg import String

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
        cv2.putText(img, label, (c1[0], c1[1] - 2),
                    0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def _make_grid(nx, ny):
    xv, yv = np.meshgrid(np.arange(ny), np.arange(nx))
    return np.stack((xv, yv), 2).reshape((-1, 2)).astype(np.float32)


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


def post_process_opencv(outputs, model_h, model_w, img_h, img_w, thred_nms, thred_conf):
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

    areas = areas.tolist()
    ids = cv2.dnn.NMSBoxes(areas, conf, thred_conf, thred_nms)
    if len(ids) > 0:
        ids = ids.flatten()
        return np.array(areas)[ids], np.array(conf)[ids], cls_id[ids]
    else:
        return [], [], []

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('yolo_image_publisher')
        self.raw_pub = self.create_publisher(Image, 'yolo/raw_image', 10)
        self.result_pub = self.create_publisher(Image, 'yolo/result_image', 10)
        self.detect_pub = self.create_publisher(String, 'yolo/detect_info', 10)  # 新增话题
        self.bridge = CvBridge()

def main():
    rclpy.init()
    image_node = ImagePublisher()
    # 模型路径
    model_path = 'yolov5_320.rknn'

    # 模型输入尺寸
    model_h = 320
    model_w = 320

    # YOLO 参数
    nl = 3
    na = 3
    stride = [8., 16., 32.]
    anchors = [[10, 13, 16, 30, 33, 23],
               [30, 61, 62, 45, 59, 119],
               [116, 90, 156, 198, 373, 326]]
    anchor_grid = np.asarray(anchors, dtype=np.float32).reshape(nl, -1, 2)

    # 类别字典（请根据模型训练标签修改）
    dic_labels = {0: 'tissue', 1: 'Bottle', 2: 'Medicine', 3: 'Plastic', 4: 'facemask', 5: 'smoke'}

    # 加载 RKNN 模型
    rknn = RKNNLite()
    print('[INFO] Loading RKNN model...')
    rknn.load_rknn(model_path)
    rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0)
    print('[INFO] RKNN model loaded.')

    # 打开摄像头
    cap = cv2.VideoCapture('/dev/video21')
    if not cap.isOpened():
        print("[ERROR] Failed to open camera.")
        return
    
    start_time = time.time()
    counter = 0
    fps = 0
    num = 0
    boxes, confs, ids = [],[],[]
    try:
        while rclpy.ok():
            ret, img0 = cap.read()
            if not ret:
                continue

            # raw_msg = image_node.bridge.cv2_to_imgmsg(img0, encoding="bgr8")
            # image_node.raw_pub.publish(raw_msg)

            img = cv2.resize(img0, (model_w, model_h))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            input_data = img_rgb.astype(np.uint8)
            input_data = np.expand_dims(input_data, axis=0)  # [1, H, W, C]

            # 推理
            outputs = rknn.inference(inputs=[input_data])
            if outputs is None:
                print("[ERROR] RKNN inference failed.")
                continue

            output = outputs[0].squeeze(axis=0).astype(np.float32)
            output = cal_outputs(output, nl, na, model_w, model_h, anchor_grid, stride)
            img_h, img_w, _ = img0.shape
            boxes, confs, ids = post_process_opencv(output, model_h, model_w, img_h, img_w, 0.4, 0.5)

            # 绘制结果
            for box, score, id in zip(boxes, confs, ids):
                label = '%s:%.2f' % (dic_labels.get(id, str(id)), score)
                plot_one_box(box.astype(np.int16), img0, color=(0, 0, 255), label=label)
            # 显示 FPS
            counter += 1
            if time.time()- start_time > 1:
                fps = counter / (time.time()- start_time)
                start_time = time.time()
                counter = 0
            cv2.putText(img0, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 显示图像
            # cv2.imshow("RKNN YOLOv5 Detection", img0)

            result_msg = image_node.bridge.cv2_to_imgmsg(img0, encoding="bgr8")
            image_node.result_pub.publish(result_msg)

            # print(f'fps:{fps}')
            if cv2.waitKey(1) == ord('q'):
                break
            
            rclpy.spin_once(image_node, timeout_sec=0.0)
    except KeyboardInterrupt:
        print('[INFO] exit!')
    finally:
        cap.release()
        cv2.destroyAllWindows()
        rknn.release()
        rclpy.shutdown()
    


if __name__ == '__main__':
    main()
