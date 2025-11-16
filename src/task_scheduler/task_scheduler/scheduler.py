import os.path
import sys

# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(current_file_path)
sys.path.append(current_dir)

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Twist
from queue import Queue
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus
from time import time,sleep


class TaskScheduler(Node):
    def __init__(self):
        super().__init__('TaskScheduler_server')
        self.publisher_initialPose = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.publisher_goal = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.publisher_uboot = self.create_publisher(String, '/uboot', 10)
        self.publisher_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription1 = self.create_subscription(String, '/chat', self.listener_chat_callback, 10)

        #导航
        self._client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.nav_start_time = 0
        self.nav_time = 0

        #模块检测
        self.check = self.create_timer(0.5, self.check_callback)
        self.chat_msgs = Queue()
        self.check_dict = {'chat':[self.chat_msgs, 3]}

        with open('/home/uboot/data/ros2_uboot/src/task_scheduler/task_scheduler/room.pos', 'r') as file:
            self.room_pos = eval(file.readline())

        # 是否在进行目标房间导航任务
        self.is_task = False

        # print(self.room_pos)
        print('<-TaskScheduler working...->')
        self.start()

    def start(self):
        pose_cov_stamped = PoseWithCovarianceStamped()
        # 设置 Header
        pose_cov_stamped.header.stamp = self.get_clock().now().to_msg()  # 当前时间
        pose_cov_stamped.header.frame_id = "map"     # 参考坐标系（如 "map"）

        # 设置位置（x, y, z）
        pose_cov_stamped.pose.pose.position.x = self.room_pos[0][0]
        pose_cov_stamped.pose.pose.position.y = self.room_pos[0][1]
        pose_cov_stamped.pose.pose.position.z = 0.0

        # 设置姿态（四元数，表示无旋转）
        pose_cov_stamped.pose.pose.orientation.x = 0.0
        pose_cov_stamped.pose.pose.orientation.y = 0.0
        pose_cov_stamped.pose.pose.orientation.z = 0.0
        pose_cov_stamped.pose.pose.orientation.w = 1.0  # w=1 表示无旋转

        # 设置协方差矩阵（示例：仅设置 x 和 yaw 的不确定性）
        # 协方差矩阵是 6×6，按行优先存储（共 36 个 float64）
        pose_cov_stamped.pose.covariance = [0.0] * 36  # 初始化为 0

        for i in range(3):
            self.publisher_initialPose.publish(pose_cov_stamped)
            sleep(0.1)
    
    def send_goal(self, x, y):
        print('<-TaskScheduler: wait for server->')
        self._client.wait_for_server()
        print('<-TaskScheduler: server success->')

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0  # Facing forward

        self.get_logger().info(f'发送导航目标: x={x}, y={y}')

        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

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
                self.send_goal(self.room_pos[0][0], self.room_pos[0][1])
        else:
            self.get_logger().error(f'❌ 导航失败，状态码: {status}')

    def check_callback(self):
        for key in self.check_dict.keys():
            if self.check_dict[key][0].empty():
                self.check_dict[key][1] -= 1
            else:
                self.check_dict[key][0].get()
                if self.check_dict[key][1]==0:
                    self.check_dict[key][1] =3
                    print(f'<-TaskScheduler: module {key} online!->')
        
        for key, value in self.check_dict.items():
            if value[1]<=0:
                print(f'<-TaskScheduler: module {key} offline!->')
                self.check_dict[key][1] = 0

    def listener_chat_callback(self, msg: String):
        self.chat_msgs.put(msg.data)
        room = int (msg.data)
        if room != 0:
            if (room in self.room_pos):
                self.is_task = True
                self.send_goal(self.room_pos[room][0], self.room_pos[room][1])
    
    def end(self):
        self._client.destroy()
        self.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    TaskScheduler_node = TaskScheduler()
    try:
        rclpy.spin(TaskScheduler_node) # 启动节点的事件循环
    except KeyboardInterrupt:
        TaskScheduler_node.end()
    finally:
        rclpy.shutdown() # 关闭ROS2

    
if __name__ == '__main__':
    main()
