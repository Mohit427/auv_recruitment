import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class SignalOutput(Node):
    def __init__(self):
        super().__init__('signal_output')
        self.subscription = self.create_subscription(
            Int32, '/processed_signal', self.listener_callback, 10)

    def listener_callback(self, msg):
        final_result = msg.data + 10 # Add 10
        self.get_logger().info(f'Final Result: {final_result}')

def main(args=None):
    rclpy.init(args=args)
    node = SignalOutput()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
