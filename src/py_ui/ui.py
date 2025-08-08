import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool, String
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Bool as BoolMsg
import threading
import os
import signal
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout, QFrame, QToolBar, QStatusBar,
    QWidgetAction ,QOpenGLWidget,QStackedLayout
)

from PyQt5.QtCore import QTimer, Qt, QSize, QDateTime ,QMutex,pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QPainter,QMovie
import cv2
import numpy as np

from rclpy.action import ActionClient                        
from nav2_msgs.action import NavigateToPose                 
from action_msgs.msg import GoalStatus                      
from geometry_msgs.msg import PoseStamped,Twist,PoseWithCovarianceStamped

from time import time,sleep

# 导航用
class ROSListener(Node):
    def __init__(self):
        super().__init__('qt_ros_listener')
        self.temperature = None
        self.humidity = None
        self.mq2 = None
        self.compressed_frame = None
        self.server_wait_count = 0

        os.system("xset s off")
        os.system("xset -dpms")
        os.system("xset s noblank")

        # 订阅者
        self.create_subscription(Float32, '/temp', self.temp_callback, 10)
        self.create_subscription(Float32, '/hum', self.hum_callback, 10)
        self.create_subscription(Bool, '/mq2', self.mq2_callback, 10)
        self.subtitle = ""        # 存储最新字幕文本
        self.create_subscription(
            String,
            '/subtitle',
            self.subtitle_callback,
            10
        )

        qos = QoSProfile(depth=1)
        qos.reliability = QoSReliabilityPolicy.BEST_EFFORT
        qos.durability  = QoSDurabilityPolicy.VOLATILE
        self.create_subscription(CompressedImage, '/yolo/result_image/compressed', self.image_callback, qos)
        # 发布者
        self.mode_pub = self.create_publisher(String, '/robot_mode', 10)
        self.publisher_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.publisher_uboot = self.create_publisher(String, '/uboot', 10)
        self.led_pub = self.create_publisher(BoolMsg, '/led', 10)

        print('<-UI working...->')

        # 导航用
        self._client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.publisher_initialPose = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.nav_start_time = 0
        self.nav_time = 0
        self.is_task = False
        self.start()

    def start(self):
        pose_cov_stamped = PoseWithCovarianceStamped()
        # 设置 Header
        pose_cov_stamped.header.stamp = self.get_clock().now().to_msg()  # 当前时间
        pose_cov_stamped.header.frame_id = "map"     # 参考坐标系（如 "map"）

        ############################ 设置起始位置（x, y, z）######################################
        pose_cov_stamped.pose.pose.position.x = 0.0
        pose_cov_stamped.pose.pose.position.y = 0.0
        pose_cov_stamped.pose.pose.position.z = 0.0

        # 设置姿态（四元数，表示无旋转）
        pose_cov_stamped.pose.pose.orientation.x = 0.0
        pose_cov_stamped.pose.pose.orientation.y = 0.0
        pose_cov_stamped.pose.pose.orientation.z = 0.0
        pose_cov_stamped.pose.pose.orientation.w = 1.0  # w=1 表示无旋转

        # 设置协方差矩阵（示例：仅设置 x 和 yaw 的不确定性）
        # 协方差矩阵是 6×6，按行优先存储（共 36 个 float64）
        pose_cov_stamped.pose.covariance = [0.0] * 36  # 初始化为 0

        for i in range(5):
            self.publisher_initialPose.publish(pose_cov_stamped)
            sleep(0.1)

    def subtitle_callback(self, msg: String):
        self.subtitle = msg.data

    def temp_callback(self, msg):
        self.temperature = msg.data

    def hum_callback(self, msg):
        self.humidity = msg.data

    def mq2_callback(self, msg):
        self.mq2 = msg.data

    def image_callback(self, msg):
        np_arr = np.frombuffer(msg.data, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.compressed_frame = frame

    def publish_mode(self, mode: str):
        msg = String()
        msg.data = mode
        self.mode_pub.publish(msg)

    def send_goal(self, x, y):
        self.nav_start_time = time()
        self.nav_time = 0
        self.goal_x = x
        self.goal_y = y

        # 启动定时器，每100ms检查一次服务器状态
        self.server_check_timer = self.create_timer(1, self.check_server_and_send_goal)

    def check_server_and_send_goal(self):
        if self._client.wait_for_server(timeout_sec=0.0):  # 非阻塞检测
            print('<-UI: server success->')
            self.server_check_timer.cancel()

            goal_msg = NavigateToPose.Goal()
            goal_msg.pose = PoseStamped()
            goal_msg.pose.header.frame_id = 'map'
            goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
            goal_msg.pose.pose.position.x = self.goal_x
            goal_msg.pose.pose.position.y = self.goal_y
            goal_msg.pose.pose.orientation.w = 1.0

            self.get_logger().info(f'发送导航目标: x={self.goal_x}, y={self.goal_y}')

            self._send_goal_future = self._client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback
            )
            self._send_goal_future.add_done_callback(self.goal_response_callback)
        else:
            print('<-UI: 等待导航服务器...->')
            self.server_wait_count += 1
            if self.server_wait_count > 10:  # 最多等10秒（0.1*100）
                print('<-UI: 等待服务器超时->')
                self.server_check_timer.cancel()

    # def send_goal(self, x, y):
    #     self.nav_start_time = time()
    #     self.nav_time = 0
    #     print('<-UI: wait for server->')
    #     self._client.wait_for_server()
    #     print('<-UI: server success->')

    #     goal_msg = NavigateToPose.Goal()
    #     goal_msg.pose = PoseStamped()
    #     goal_msg.pose.header.frame_id = 'map'
    #     goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
    #     goal_msg.pose.pose.position.x = x
    #     goal_msg.pose.pose.position.y = y
    #     goal_msg.pose.pose.orientation.w = 1.0  # Facing forward

    #     self.get_logger().info(f'发送导航目标: x={x}, y={y}')

    #     self._send_goal_future = self._client.send_goal_async(
    #         goal_msg,
    #         feedback_callback=self.feedback_callback
    #     )
    #     self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('⚠️ 目标被拒绝！')
            return

        self.get_logger().info('✅ 目标被接受，等待结果...')
        self.nav_start_time = time()
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        used_time = int(time() - self.nav_start_time)
        if used_time != self.nav_time:
            self.get_logger().info(f'📍 正在导航中，已用时间: {used_time} 秒')
            self.nav_time = used_time

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('🎯 成功到达目标！')
            twist_msg = Twist()
            twist_msg.angular.x = 0.0
            twist_msg.angular.y = 0.0
            twist_msg.angular.z = 0.0
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.linear.z = 0.0

            for i in range(3):
                self.publisher_cmd_vel.publish(twist_msg)
                sleep(0.3)
            if self.is_task:
                self.is_task = False
                msg = String()
                msg.data = 'back'
                sleep(2)
                self.publisher_uboot.publish(msg)
                self.send_goal(0.0, 0.0)
        else:
            self.get_logger().error(f'❌ 导航失败，状态码: {status}')

# 显示图像
class GLCameraWidget(QOpenGLWidget):
    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node
        self.frame = None
        self.mutex = QMutex()
        self.setFixedSize(600, 450)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~30 FPS

    def update_frame(self):
        frame = self.ros_node.compressed_frame
        if frame is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            self.mutex.lock()
            self.frame = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()
            self.mutex.unlock()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.mutex.lock()
        if self.frame:
            pix = QPixmap.fromImage(self.frame).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(self.rect().center() - pix.rect().center(), pix)
        self.mutex.unlock()
        painter.end()


class CameraWidget(QLabel):
    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node
        self.setFixedSize(320, 240)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px solid #2c3e50; background-color: #000;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame = self.ros_node.compressed_frame
        if frame is None:
            return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qt_image).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pix)

# 传感器
class SensorWidget(QFrame):
    def __init__(self, ros_node, show_gas=True):
        super().__init__()
        self.ros_node = ros_node
        self.show_gas = show_gas
        self.setFixedHeight(80)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame { background-color: rgba(255,255,255,0.8); border-radius: 8px; padding: 6px; border: 1px solid #bdc3c7; }
            QLabel { color: #2c3e50; font: 14pt 'Segoe UI'; }
        """)
        layout = QHBoxLayout()
        self.temp_label = QLabel("温度: -- °C")
        self.humi_label = QLabel("湿度: -- %")
        layout.addWidget(self.temp_label)
        layout.addStretch(1)
        layout.addWidget(self.humi_label)
        layout.addStretch(1)
        if self.show_gas:
            self.mq2_label = QLabel("可燃气体: --")
            layout.addWidget(self.mq2_label)
            layout.addStretch(1)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sensor)
        self.timer.start(1000)

    def update_sensor(self):
        if self.ros_node.temperature is not None:
            self.temp_label.setText(f"温度: {self.ros_node.temperature:.1f} °C")
        if self.ros_node.humidity is not None:
            self.humi_label.setText(f"湿度: {self.ros_node.humidity:.1f} %")
        if self.show_gas and self.ros_node.mq2 is not None:
            self.mq2_label.setText(f"可燃气体: {'有' if self.ros_node.mq2 else '无'}")

# UI界面
class MainWindow(QMainWindow):
    def __init__(self, ros_node):
        super().__init__()
        self.ros = ros_node
        self.active_mode = None

        # 模式到页面索引的映射
        self.mode_index = {
            'navigation': 1,
            'garbage': 2,
            'dialog': 3,
        }

        self.prev_subtitle = ""
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.typewriter_tick)
        self.full_text = ""
        self.current_index = 0

        with open('/home/uboot/data/gh/py_ui/room.pos', 'r') as file:
            self.room_pos = eval(file.readline())

        self.setWindowTitle("酒店机器人交互界面")
        self.showFullScreen()
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #e0f7fa, stop:1 #80deea); }
            QLabel { font: 20pt 'Segoe UI'; color: #2c3e50; }
            QPushButton { font: 16pt 'Segoe UI'; }
        """)

        def add_feedback(btn, normal, pressed):
            btn.setCheckable(False)
            btn.pressed.connect(lambda b=btn: b.setStyleSheet(pressed))
            btn.released.connect(lambda b=btn: b.setStyleSheet(normal))

        ################# 顶部工具栏 #################
        toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(10, 0, 10, 0)
        toolbar_layout.setSpacing(20)

        ################# 左侧模式按钮区 #################
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self.mode_buttons = {}
        def add_mode_button(text, mode):
            idx = self.mode_index[mode]
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            btn.setMinimumWidth(150)
            btn.clicked.connect(lambda _, m=mode: self.on_mode_selected(self.mode_index[m], m))
            self.mode_buttons[mode] = btn
            button_layout.addWidget(btn)

        add_mode_button("领航", 'navigation')
        add_mode_button("巡查", 'garbage')
        add_mode_button("交互", 'dialog')

        ################## 右侧信息区 #################
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(10)
        self.temp_label = QLabel("温度: -- °C")
        self.humi_label = QLabel("湿度: -- %")
        self.time_label = QLabel("")
        for lbl in (self.temp_label, self.humi_label, self.time_label):
            lbl.setStyleSheet("color: white; font: 14pt 'Segoe UI'; padding: 0 10px;")
            info_layout.addWidget(lbl)

        toolbar_layout.addWidget(button_container)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(info_container)
        toolbar_action = QWidgetAction(self)
        toolbar_action.setDefaultWidget(toolbar_container)
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(32, 32))
        self.toolbar.setStyleSheet("background-color: rgba(44,62,80,0.8);")
        self.toolbar.setFixedHeight(80)
        self.toolbar.addAction(toolbar_action)
        self.toolbar.hide()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # 定时更新状态
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)

        # 页面堆栈
        self.pages = QStackedWidget()

        # 欢迎页
        page_welcome = QWidget()
        w_layout = QVBoxLayout(page_welcome)
        w_layout.setAlignment(Qt.AlignCenter)
        label_w = QLabel("<h1>欢迎使用机器人系统</h1><p>点击屏幕开始</p>")
        label_w.setAlignment(Qt.AlignCenter)
        w_layout.addWidget(label_w)
        page_welcome.mousePressEvent = lambda e: self.show_toolbar_and_switch()

        ####################### 领航页 #################
        page_nav = QWidget()
        nav_layout = QVBoxLayout(page_nav)
        nav_layout.setContentsMargins(20, 20, 20, 20)
        nav_layout.setSpacing(20)

        # 标题
        nav_label = QLabel("<b>领航模式</b><br>让我带你去房间吧！")
        nav_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(nav_label)

        # --- 创建水平主容器 ---
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(50, 0, 50, 0)  # 整体左右留白，避免贴边
        content_layout.setSpacing(100)  # 地图与按钮之间的间距（可调）

        # ---- 地图部分 ----
        map_label = QLabel()
        map_pix = QPixmap("hotel.png").scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        map_label.setPixmap(map_pix)
        map_label.setAlignment(Qt.AlignCenter)

        map_container = QWidget()
        map_layout = QVBoxLayout(map_container)
        map_layout.setAlignment(Qt.AlignCenter)
        map_layout.addWidget(map_label)

        content_layout.addWidget(map_container)

        # ---- 按钮部分 ----
        btn1 = QPushButton("房间1")
        btn2 = QPushButton("房间2")
        nav_normal  = "background-color:#4CAF50; color:white; border-radius:8px;"
        nav_pressed = "background-color:#45a049; color:white; border-radius:8px;"
        for b in (btn1, btn2):
            add_feedback(b, nav_normal, nav_pressed)
            b.setFixedSize(300, 100)
            b.setStyleSheet(nav_normal)

        btn_container = QWidget()
        btn_layout = QVBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)

        content_layout.addWidget(btn_container)

        # ---- 添加到主页面布局 ----
        nav_layout.addWidget(content_container)

        # ---- 按钮回调 ----
        btn1.clicked.connect(self.on_goto_room1)
        btn2.clicked.connect(self.on_goto_room2)

        ################################# 垃圾巡查页 #################
        page_garbage = QWidget()
        g_layout = QVBoxLayout(page_garbage)
        g_layout.setContentsMargins(20, 10, 20, 20)
        g_layout.setSpacing(10)
        g_label = QLabel("<b>垃圾巡查模式</b>")
        g_label.setAlignment(Qt.AlignCenter)
        g_layout.addWidget(g_label)
        g_layout.addStretch(1)
        cam = GLCameraWidget(self.ros)
        # cam = CameraWidget(self.ros)
        cam.setFixedSize(760, 570)
        g_layout.addWidget(cam, alignment=Qt.AlignCenter)
        g_layout.addStretch(2)

        ############################## 服务交互页 #################
        page_dialog = QWidget()
        d_layout = QVBoxLayout(page_dialog)
        d_layout.setContentsMargins(20, 20, 20, 20)
        d_layout.setSpacing(16)

        d_label = QLabel("<b>服务交互模式</b><br>语音交互与灯光")
        d_label.setAlignment(Qt.AlignCenter)
        d_layout.addWidget(d_label)


        #### ====== 聊天行容器 (GIF + 字幕) ====== ####
        chat_row = QWidget()
        chat_layout = QHBoxLayout(chat_row)
        chat_layout.setContentsMargins(150, 0, 0, 0)
        chat_layout.setSpacing(15)
        chat_layout.setAlignment(Qt.AlignLeft)

        # 左侧 GIF
        self.chat_gif = QLabel()
        self.chat_gif.setFixedSize(300, 300)
        self.chat_gif.setStyleSheet("background: transparent;")
        self.chat_gif.setAlignment(Qt.AlignCenter)
        movie = QMovie("pig.gif")  # 确保 chat.gif 在你的工作目录中
        self.chat_gif.setMovie(movie)
        movie.start()

        # 右侧 字幕气泡
        self.subtitle_label = QLabel("我是酒店机器人！")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.subtitle_label.setMaximumWidth(1600)
        self.subtitle_label.setMaximumHeight(200)
        self.subtitle_label.setStyleSheet("""
            color: white;
            background-color: rgba(52, 152, 219, 0.85);
            font: 18pt 'Segoe UI';
            padding: 8px 20px;
            border-radius: 20px;
            border: 2px solid rgba(41, 128, 185, 0.8);
        """)

        chat_layout.addWidget(self.chat_gif)
        chat_layout.addWidget(self.subtitle_label)
        d_layout.addWidget(chat_row)

        #### ====== 灯光控制按钮区域 ====== ####
        on_btn = QPushButton("开灯")
        off_btn = QPushButton("关灯")
        interact_normal = "background-color:#3498db; color:white; border-radius:10px;"
        interact_pressed = "background-color:#2980b9; color:white; border-radius:10px;"

        # 设置按钮样式、尺寸
        for b in (on_btn, off_btn):
            add_feedback(b, interact_normal, interact_pressed)
            b.setFixedSize(300, 100)
            b.setStyleSheet(interact_normal)

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(60)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(on_btn)
        btn_layout.addWidget(off_btn)

        # 添加按钮区到主布局
        d_layout.addWidget(btn_container)


        # 连接回调
        on_btn.clicked.connect(self.on_light_on)
        off_btn.clicked.connect(self.on_light_off)

        # 将各页加入堆栈
        self.pages.addWidget(page_welcome)
        self.pages.addWidget(page_nav)
        self.pages.addWidget(page_garbage)
        self.pages.addWidget(page_dialog)

        central = QWidget()
        c_layout = QVBoxLayout(central)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.addWidget(self.pages)
        self.setCentralWidget(central)

        ################ 初始显示欢迎页，并在 3 秒后切换 #################
        self.pages.setCurrentIndex(0)
        # QTimer.singleShot(3000, self.show_toolbar_and_switch)

        # 状态栏
        status = QStatusBar()
        status.setStyleSheet("font-size:12pt; background:rgba(255,255,255,0.6);")
        status.showMessage("系统就绪")
        self.setStatusBar(status)

    ########################### 各按钮回调###################################3
    def on_goto_room1(self):
        print('房间1 按钮被按下')

        # 先广播机器人模式
        self.ros.publish_mode('goto_room101')
        # 再发送导航目标点，假设房间101在地图坐标 (2.0, 3.5)
        self.ros.send_goal(self.room_pos[1][0], self.room_pos[1][1])
        # 切换界面
        self.on_mode_selected(self.mode_index['navigation'], 'navigation')

    def on_goto_room2(self):
        print('房间2 按钮被按下')
        self.ros.publish_mode('goto_room102')
        # 假设房间102坐标 (4.0, 1.0)
        self.ros.send_goal(self.room_pos[2][0], self.room_pos[2][1])
        self.on_mode_selected(self.mode_index['navigation'], 'navigation')

    def on_light_on(self):
        print('开灯按钮被按下')
        self.ros.publish_mode('light_on')
        self.ros.led_pub.publish(BoolMsg(data=True))
        self.on_mode_selected(self.mode_index['dialog'], 'dialog')

    def on_light_off(self):
        print('关灯按钮被按下')
        self.ros.publish_mode('light_off')
        self.ros.led_pub.publish(BoolMsg(data=False))
        self.on_mode_selected(self.mode_index['dialog'], 'dialog')

    def on_mode_selected(self, index, mode):
        self.pages.setCurrentIndex(index)
        self.ros.publish_mode(mode)
        self.statusBar().showMessage(f"当前模式: {mode}")
        self.active_mode = mode
        self.update_mode_button_styles()

    def update_mode_button_styles(self):
        for mode, btn in self.mode_buttons.items():
            if mode == self.active_mode:
                btn.setStyleSheet("background-color:#e67e22; color:white; border-radius:10px;")
            else:
                btn.setStyleSheet("background-color:#34495e; color:white; border-radius:10px;")

    def update_status(self):
        if self.ros.temperature is not None:
            self.temp_label.setText(f"温度: {self.ros.temperature:.1f} °C")
        if self.ros.humidity is not None:
            self.humi_label.setText(f"湿度: {self.ros.humidity:.1f} %")
        if self.ros.subtitle and self.ros.subtitle != self.prev_subtitle:
            self.prev_subtitle = self.ros.subtitle
            self.start_typewriter_effect(self.ros.subtitle)

        now = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
        self.time_label.setText(now)
    
    def start_typewriter_effect(self, text):
        self.full_text = text
        self.current_index = 0
        self.subtitle_label.setText("")
        self.typing_timer.start(100)  # 每 50ms 显示一个字符，可调节速度

    def typewriter_tick(self):
        if self.current_index < len(self.full_text):
            current_char = self.full_text[self.current_index]
            self.subtitle_label.setText(self.subtitle_label.text() + current_char)
            self.current_index += 1
        else:
            self.typing_timer.stop()

    def show_toolbar_and_switch(self):
        self.toolbar.show()
        # 默认切换到领航模式
        self.on_mode_selected(self.mode_index['navigation'], 'navigation')

    def closeEvent(self, event):
        self.ros.destroy_node()
        rclpy.shutdown()
        QApplication.quit()
        event.accept()


if __name__ == '__main__':
    os.environ['DISPLAY'] = ':0'
    rclpy.init()
    ros_node = ROSListener()
    threading.Thread(target=rclpy.spin, args=(ros_node,), daemon=True).start()
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    signal.signal(signal.SIGINT, lambda s, f: app.quit())
    window = MainWindow(ros_node)
    window.show()
    sys.exit(app.exec_())
