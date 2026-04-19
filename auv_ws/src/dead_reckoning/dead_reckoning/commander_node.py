import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading

class CommanderNode(Node):
    def __init__(self):
        super().__init__('commander_node')
        self.publisher_ = self.create_publisher(String, '/cmd', 10)

    def send_command(self, cmd_text):
        msg = String()
        msg.data = cmd_text
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CommanderNode()
    
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,))
    spin_thread.start()

    print("Commander ready. Valid inputs: 'forward', 'backward', 'turn left', 'turn right'")
    
    try:
        while True:
            cmd = input().strip().lower()
            if cmd in ['forward', 'backward', 'turn left', 'turn right']:
                node.send_command(cmd)
            else:
                print("Invalid command.")
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join()

if __name__ == '__main__':
    main()
