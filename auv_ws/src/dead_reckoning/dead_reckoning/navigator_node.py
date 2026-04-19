import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from auv_interfaces.msg import BotPose # Importing the custom message

class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')
        self.subscription = self.create_subscription(String, '/cmd', self.cmd_callback, 10)
        self.publisher_ = self.create_publisher(BotPose, '/bot_pose', 10)
        
        # State Machine Initialization [cite: 23]
        self.x = 0.0
        self.y = 0.0
        self.directions = ['North', 'East', 'South', 'West']
        self.current_dir_index = 0 # 0 equates to 'North'

    def cmd_callback(self, msg):
        command = msg.data
        
        # State Transitions [cite: 24, 25, 27]
        if command == 'turn right':
            self.current_dir_index = (self.current_dir_index + 1) % 4
        elif command == 'turn left':
            self.current_dir_index = (self.current_dir_index - 1) % 4
        elif command == 'forward':
            self.move(1.0)
        elif command == 'backward':
            self.move(-1.0)
        
        facing = self.directions[self.current_dir_index]
        
        # Format Custom Message 
        pose_msg = BotPose()
        pose_msg.x = float(self.x)
        pose_msg.y = float(self.y)
        pose_msg.facing_direction = facing
        self.publisher_.publish(pose_msg)
        
        self.get_logger().info(f'State -> X: {self.x}, Y: {self.y}, Facing: {facing}')

    def move(self, step):
        # Determine axis movement based on current state
        facing = self.directions[self.current_dir_index]
        if facing == 'North':
            self.y += step
        elif facing == 'South':
            self.y -= step
        elif facing == 'East':
            self.x += step
        elif facing == 'West':
            self.x -= step

def main(args=None):
    rclpy.init(args=args)
    node = NavigatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
