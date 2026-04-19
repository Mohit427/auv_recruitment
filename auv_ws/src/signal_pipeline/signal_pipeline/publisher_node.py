import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class SignalPublisher(Node):
    def __init__(self):
        super().__init__('signal_publisher')
        self.publisher_ = self.create_publisher(Int32, '/raw_signal', 10)
        # Timer calls the timer_callback function every 1.0 seconds (1 Hz)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.current_value = 2 # Starting value

    def timer_callback(self):
        msg = Int32()
        msg.data = self.current_value
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')
        self.current_value += 2 # Increment by 2 for the next cycle

def main(args=None):
    rclpy.init(args=args)
    node = SignalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
