import sys
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class CommLinkNode(Node):
    def __init__(self, username):
        # We append the username to make the node name unique for the ROS graph
        super().__init__('comm_link_node_' + username.lower())
        self.username = username
        
        # Publish and subscribe to the exact same ROS topic 
        self.publisher_ = self.create_publisher(String, '/chat', 10)
        self.subscription = self.create_subscription(
            String,
            '/chat',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        # Ignore our own messages so we don't see double
        if not msg.data.startswith(f"[{self.username}]"):
            # Print the incoming message from the other user
            print(f"\n{msg.data}")

    def publish_message(self, text):
        msg = String()
        # Format the message to include the user identifier 
        msg.data = f"[{self.username}]: {text}" 
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    # Ensure a user identifier is passed via the terminal 
    if len(sys.argv) < 2:
        print("Usage: ros2 run comm_link chat_node <Invictus/Hawcker>")
        return

    username = sys.argv[1]
    
    # Validate the user identifier 
    if username not in ["Invictus", "Hawcker"]: 
        print("Error: User identifier must be either Invictus or Hawcker.")
        return

    node = CommLinkNode(username)

    # Run ROS spin in a separate thread so input() doesn't block incoming messages
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,))
    spin_thread.start()

    print(f"Comm-Link established as {username}. Type your message and press Enter.")
    
    try:
        while True:
            text = input()
            if text:
                node.publish_message(text)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join()

if __name__ == '__main__':
    main()
