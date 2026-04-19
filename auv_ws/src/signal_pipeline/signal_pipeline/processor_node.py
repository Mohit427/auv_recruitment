import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class SignalProcessor(Node):
    def __init__(self):
        super().__init__('signal_processor')
        self.subscription = self.create_subscription(
            Int32, '/raw_signal', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(Int32, '/processed_signal', 10)

    def listener_callback(self, msg):
        processed_msg = Int32()
        processed_msg.data = msg.data * 5 # Multiply by 5
        self.publisher_.publish(processed_msg)
        self.get_logger().info(f'Processed {msg.data} -> {processed_msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = SignalProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
