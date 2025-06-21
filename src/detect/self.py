import cv2
import numpy as np
import random
import time

# 绘制识别框的函数
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
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

# 后处理函数（优化的NMS）
def post_process_opencv(outputs, model_h, model_w, img_h, img_w, thred_nms=0.2, thred_conf=0.4):
    conf = outputs[:, 4]
    valid_indices = np.where(conf > thred_conf)[0]

    if len(valid_indices) == 0:
        return [], [], []

    boxes = outputs[valid_indices, :4]
    scores = conf[valid_indices]
    cls_ids = outputs[valid_indices, 5:].argmax(axis=1)

    boxes[:, 0] = boxes[:, 0] * img_w
    boxes[:, 1] = boxes[:, 1] * img_h
    boxes[:, 2] = boxes[:, 2] * img_w
    boxes[:, 3] = boxes[:, 3] * img_h

    p_x1 = boxes[:, 0] - (boxes[:, 2] / 2)
    p_y1 = boxes[:, 1] - (boxes[:, 3] / 2)
    p_x2 = boxes[:, 0] + (boxes[:, 2] / 2)
    p_y2 = boxes[:, 1] + (boxes[:, 3] / 2)

    final_boxes = np.stack([p_x1, p_y1, p_x2, p_y2], axis=-1)

    # 增强 NMS：基于类别进行过滤
    unique_classes = np.unique(cls_ids)
    final_boxes_list, final_scores_list, final_cls_ids_list = [], [], []

    for cls in unique_classes:
        cls_indices = np.where(cls_ids == cls)[0]
        cls_boxes = final_boxes[cls_indices]
        cls_scores = scores[cls_indices]

        indices = cv2.dnn.NMSBoxes(cls_boxes.tolist(), cls_scores.tolist(), thred_conf, thred_nms)

        if len(indices) > 0:
            indices = indices.flatten()
            final_boxes_list.extend(cls_boxes[indices])
            final_scores_list.extend(cls_scores[indices])
            final_cls_ids_list.extend([cls] * len(indices))

    return np.array(final_boxes_list), np.array(final_scores_list), np.array(final_cls_ids_list)

    boxes = outputs[valid_indices, :4]
    scores = conf[valid_indices]
    cls_ids = outputs[valid_indices, 5:].argmax(axis=1)

    boxes[:, 0] = boxes[:, 0] * img_w
    boxes[:, 1] = boxes[:, 1] * img_h
    boxes[:, 2] = boxes[:, 2] * img_w
    boxes[:, 3] = boxes[:, 3] * img_h

    p_x1 = boxes[:, 0] - (boxes[:, 2] / 2)
    p_y1 = boxes[:, 1] - (boxes[:, 3] / 2)
    p_x2 = boxes[:, 0] + (boxes[:, 2] / 2)
    p_y2 = boxes[:, 1] + (boxes[:, 3] / 2)

    final_boxes = np.stack([p_x1, p_y1, p_x2, p_y2], axis=-1)

    indices = cv2.dnn.NMSBoxes(final_boxes.tolist(), scores.tolist(), thred_conf, thred_nms)

    if len(indices) > 0:
        indices = indices.flatten()
        return final_boxes[indices], scores[indices], cls_ids[indices]

    return [], [], []

# 推理函数
def infer_img(img0, net, model_h, model_w, thred_nms=0.15, thred_conf=0.7):
    img = cv2.resize(img0, (model_h, model_w), interpolation=cv2.INTER_AREA)
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (model_h, model_w), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward().squeeze(0)

    img_h, img_w, _ = img0.shape
    boxes, confs, cls_ids = post_process_opencv(outputs, model_h, model_w, img_h, img_w, thred_nms, thred_conf)

    return boxes, confs, cls_ids

if __name__ == "__main__":
    model_path = "best_320.onnx"
    net = cv2.dnn.readNetFromONNX(model_path)

    dic_labels = {0: 'tissue', 1: 'Bottle', 2: 'Medicine', 3: 'Plastic', 4: 'facemask', 5: 'smoke'}

    cap = cv2.VideoCapture(0)
    flag_det = False

    while True:
        success, img0 = cap.read()
        if not success:
            break

        start_time = time.time()

        if flag_det:
            boxes, scores, cls_ids = infer_img(img0, net, 320, 320)
            for box, score, cls_id in zip(boxes, scores, cls_ids):
                label = dic_labels.get(cls_id, "Unknown")
                plot_one_box(box, img0, color=(255, 0, 0), label=f"{label}: {score:.2f}")

        # 计算FPS（优化）
        end_time = time.time()
        fps = 1 / (end_time - start_time + 1e-6)  # 防止除0
        cv2.putText(img0, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("video", img0)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            flag_det = not flag_det
            print("Detection ON" if flag_det else "Detection OFF")

    cap.release()
    cv2.destroyAllWindows()
