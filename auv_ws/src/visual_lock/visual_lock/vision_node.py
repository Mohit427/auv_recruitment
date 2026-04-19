import rclpy
from rclpy.node import Node
import cv2
import numpy as np

class VisualLockNode(Node):
    def __init__(self):
        super().__init__('visual_lock_node')
        
        # Open the default laptop webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Could not open webcam!")

        # Get frame width to divide into thirds
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.left_bound = self.width / 3
        self.right_bound = (self.width / 3) * 2

        # Create a timer to run the vision loop at ~30 FPS
        self.timer = self.create_timer(0.033, self.vision_callback)
        self.current_state = "INITIALIZING"

    def vision_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 1. Convert to HSV and create a mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # NOTE: This range is for a bright BLUE object. 
        # You will need to tune these values if you use a red cup or green pen.
        lower_bound = np.array([100, 150, 0])
        upper_bound = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # 2. Find the object's center (X-coordinate)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        object_x = None
        if contours:
            # Grab the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            # Only track if it's reasonably sized (ignore tiny noise)
            if cv2.contourArea(largest_contour) > 500:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    object_x = int(M["m10"] / M["m00"])
                    # Draw a circle at the center for debugging
                    cv2.circle(frame, (object_x, int(M["m01"] / M["m00"])), 5, (0, 255, 0), -1)

        # 3. State Machine & Visual Filters
        output_frame = frame.copy()
        new_state = ""

        if object_x is None:
            new_state = "LOST - SEARCHING"
            # Filter: Invert colors (Negative)
            output_frame = cv2.bitwise_not(frame)
            
        elif object_x < self.left_bound:
            new_state = "STATE 1 - ALIGNING LEFT"
            # Filter: Grayscale (Convert to gray, then back to BGR to keep channel depth same for display)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            output_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
        elif object_x > self.right_bound:
            new_state = "STATE 3 - ALIGNING RIGHT"
            # Filter: Edge Detection (Canny)
            edges = cv2.Canny(frame, 100, 200)
            output_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
        else:
            new_state = "STATE 2 - LOCKED ON (CENTRE)"
            # Filter: Normal color (Do nothing to output_frame)
            pass 

        # Log state changes to the terminal
        if new_state != self.current_state:
            self.get_logger().info(f"Target Status: {new_state}")
            self.current_state = new_state

        # 4. Display the result
        cv2.putText(output_frame, self.current_state, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("Operation Visual Lock", output_frame)
        
        # Crucial for OpenCV to update the window
        cv2.waitKey(1) 

    def destroy_node(self):
        # Clean up the camera when the node dies
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = VisualLockNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
