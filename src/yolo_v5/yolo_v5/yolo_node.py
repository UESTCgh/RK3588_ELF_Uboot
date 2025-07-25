import cv2
import numpy as np
import time
import random
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage 
from cv_bridge import CvBridge
import threading
from std_msgs.msg import String
import queue

IMG_QUEUE = queue.Queue() 
INFO_QUEUE = queue.Queue() 
WORKING = False

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

    areas = areas.tolist()
    ids = cv2.dnn.NMSBoxes(areas, conf, thred_cond, thred_nms)
    if len(ids) > 0:
        ids = ids.flatten()
        return np.array(areas)[ids], np.array(conf)[ids], cls_id[ids]
    else:
        return [], [], []

def infer_img(img0, net, model_h, model_w, nl, na, stride, anchor_grid, thred_nms=0.4, thred_cond=0.5):
    img = cv2.resize(img0, [model_w, model_h], interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    blob = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)

    net.setInput(blob)
    outs = net.forward()
    outs = outs.squeeze(axis=0)

    outs = cal_outputs(outs, nl, na, model_w, model_h, anchor_grid, stride)

    img_h, img_w, _ = np.shape(img0)
    boxes, confs, ids = post_process_opencv(outs, model_h, model_w, img_h, img_w, thred_nms, thred_cond)

    return boxes, confs, ids
    
def predict():
    global WORKING, IMG_QUEUE, INFO_QUEUE
    WORKING = True
    #print("[INFO] YOLO 图像节点启动")

    model_pb_path = "/home/uboot/data/ros2_uboot/src/yolo_v5/models/best_320.onnx"
    net = cv2.dnn.readNetFromONNX(model_pb_path)

    dic_labels = {0: 'tissue', 1: 'Bottle', 2: 'Medicine', 3: 'Plastic', 4: 'facemask', 5: 'smoke'}

    model_h = 320
    model_w = 320
    nl = 3
    na = 3
    stride = [8., 16., 32.]
    anchors = [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119], [116, 90, 156, 198, 373, 326]]
    anchor_grid = np.asarray(anchors, dtype=np.float32).reshape(nl, -1, 2)
    
    cap = cv2.VideoCapture('/dev/video21')

    counter = 0
    start_time = time.time()
    fps = 5
    num = 0
    det_boxes, scores, ids = [], [], []
    while WORKING:
        try:
            success, img0 = cap.read()
            if success:
                # 发布原始图像
                # raw_msg = image_node.bridge.cv2_to_imgmsg(img0, encoding="bgr8")
                # image_node.raw_pub.publish(raw_msg)
                
                img_copy = img0  # .copy
                detect_msgs = []
                num += 1
                if num<8:
                    det_boxes, scores, ids = infer_img(
                        img_copy, net, model_h, model_w, nl, na, stride, anchor_grid,
                        thred_nms=0.4, thred_cond=0.5
                    )
                else:
                    num = 0
                for box, score, id in zip(det_boxes, scores, ids):
                    label = '%s:%.2f' % (dic_labels[id], score)
                    plot_one_box(box.astype(np.int16), img_copy, color=(255, 0, 0), label=label)
                    x1, y1, x2, y2 = box.astype(np.int32)
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    detect_msgs.append(f"{dic_labels[id]} ({score:.2f}) at ({center_x},{center_y})")
                    print(f"[DETECT] {label} at ({center_x},{center_y}) confidence: {score:.2f}")

                # FPS 信息
                counter += 1
                if time.time() - start_time > 1:
                    fps = counter / (time.time() - start_time)
                    start_time = time.time()
                    counter = 0
                cv2.putText(img_copy, f"FPS: {fps:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # 发布识别信息
                if detect_msgs:
                    detect_info = "\n".join(detect_msgs)
                else:
                    detect_info = "No objects detected"
                INFO_QUEUE.put(String(data=detect_info))

                # 发布处理后图像
                # image_node.result_pub.publish(result_msg)
                # result_msg = image_node.bridge.cv2_to_imgmsg(img_copy, encoding="bgr8")
                IMG_QUEUE.put(img_copy)
                # cv2.imshow("Detection Result", img_copy)
        except KeyboardInterrupt:
            cap.release()
            WORKING = False
    cap.release()
    

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('yolo_image_publisher')
        # self.raw_pub = self.create_publisher(Image, 'yolo/raw_image', 10)
        # self.result_pub = self.create_publisher(Image, 'yolo/result_image', 10)
        self.detect_pub = self.create_publisher(String, 'yolo/detect_info', 10)  # 新增话题
        # 压缩后 JPEG 发布者
        self.comp_pub = self.create_publisher(CompressedImage, 'yolo/result_image/compressed', 10)
        self.timer_ = self.create_timer(0.01, self.timer_callback)
        self.bridge = CvBridge()
        self.detect = threading.Thread(target=predict)
        self.detect.start()
        self.counter = 0
        print('[IMG NODE] WORK.')
    
    def timer_callback(self):
        global IMG_QUEUE, INFO_QUEUE, WORKING
        # print('[IMG NODE]:working...')
        if not IMG_QUEUE.empty() and WORKING:
            img = IMG_QUEUE.get()
            if len(IMG_QUEUE) > 10:
                self.counter += 1:
                if self.counter > 1:
                    self.counter = 0
                    result_msg = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")
                    # self.result_pub.publish(result_msg)
                    # —— 压缩发布 —— #
                    # 1. 用 OpenCV 编码成 JPEG（二进制）
                    img_small = cv2.resize(img, (480, 360), interpolation=cv2.INTER_AREA)
                    success, buffer = cv2.imencode('.jpg', img_small, [int(cv2.IMWRITE_JPEG_QUALITY),80])
                    if success:
                        comp_msg = CompressedImage()
                        comp_msg.header.stamp = self.get_clock().now().to_msg()
                        comp_msg.format = "jpeg"
                        comp_msg.data = np.array(buffer).tobytes()
                        self.comp_pub.publish(comp_msg)
                    else:
                        self.get_logger().warn("JPEG 编码失败")

        if not INFO_QUEUE.empty() and WORKING:
            info = INFO_QUEUE.get()
            self.detect_pub.publish(info)
    
    def end(self):
        global WORKING
        WORKING = False
        self.detect.join()
        print('[IMG NODE] EXIT.')


def main():
    rclpy.init()
    image_node = ImagePublisher()
    try:
        rclpy.spin(image_node) # 启动节点的事件循环
    except KeyboardInterrupt:
        image_node.end()
        image_node.destroy_node() # 清理并关闭节点
    finally:
        rclpy.shutdown() # 关闭ROS2


if __name__ == "__main__":
    main()