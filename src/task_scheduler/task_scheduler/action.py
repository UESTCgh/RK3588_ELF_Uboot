import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus


class NavigationClient(Node):

    def __init__(self):
        super().__init__('navigation_client')
        self._client = ActionClient(self, NavigateToPose, '/navigate_to_pose')

    def send_goal(self, x, y):
        self._client.wait_for_server()

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
            rclpy.shutdown()
            return

        self.get_logger().info('✅ 目标被接受，等待结果...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'📍 正在导航中，已用时间: {feedback.navigation_time.sec} 秒')

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('🎯 成功到达目标！')
        else:
            self.get_logger().error(f'❌ 导航失败，状态码: {status}')

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = NavigationClient()
    node.send_goal(x=2.0, y=2.0)  # 可以根据地图调整坐标
    rclpy.spin(node)

if __name__ == '__main__':
    main()

