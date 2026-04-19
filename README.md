# AUV Software Subsystem Recruitment Tasks

This repository contains my submissions for the AUV Software Subsystem recruitment. The workspace is built using ROS 2 Humble on Ubuntu 22.04 and includes custom Python nodes, topics, and computer vision pipelines.

## 🛠️ Workspace Setup & Build Instructions

To run these packages, you need to have ROS 2 Humble installed. 

**1. Clone the repository:**
bash
git clone https://github.com/YOUR_USERNAME/auv_recruitment.git
cd auv_recruitment/auv_ws


**2. Build the workspace:**
bash
colcon build


**3. Source the installation:**
You must source the workspace in every new terminal before running a node.
bash
source install/setup.bash


---

## 🚀 Task Execution Guide

### Task 1: The Comm-Link (ROS 2 Pub/Sub)
A single Python node that allows bidirectional chatting between two users over the `/chat` topic.

**Execution:**
Open two separate terminals, navigate to `auv_ws`, and source the setup file in both.

*Terminal 1:*
bash
ros2 run comm_link chat_node Invictus

*Terminal 2:*
bash
ros2 run comm_link chat_node Hawcker


---

## Issues Faced & Resolutions

**Task 1: The Comm-Link**
This was a moderate task. It helped me to learn the basics ofhow nodes and topics work in ROS2 and How Subscription and Publishing tasks are done. Also, since getting input using Python and rclpy spin are both infinite tasks that cannot be run simultaneously,the interesting concept of threading was introduced in which rclpy spin was run on a different thread and python input run normally. I did not face any great challenges in this task but setting up git with the username and token on a VM took some time. Otherwise this was a great starting point of a task.


### Task 2: Signal Processing Pipeline
The second task is a multi-node mathematical pipeline demonstrating timer-based execution and sequential topic processing. An even number has to published by a node and one middleman node subscribes to the node and performs an operation and then publishes it which is captured by another node to give a final output. I loved the sequential processing, and it was very satisying to see unfold. 

**Execution:**
Open three separate terminals, navigate to `auv_ws`, and source the setup file in all of them.

*Terminal 1 (The Source - 1 Hz Timer):*
bash
ros2 run signal_pipeline publisher_node

*Terminal 2 (The Multiplier):*
bash
ros2 run signal_pipeline processor_node

*Terminal 3 (The Output Logger):*
bash
ros2 run signal_pipeline output_node


You can visualize the active data flow between these nodes by opening a fourth terminal and running:
bash
rqt_graph

### Task 3: Dead Reckoning System (Custom Interfaces & State Machine)
This task simulates basic submarine movement tracking using a completely custom ROS 2 message (`BotPose.msg`) and a Python-based finite state machine to calculate directional heading. 

**Structure:**
* `auv_interfaces`: A CMake package containing the custom message definition.
* `dead_reckoning`: A Python package containing the Commander and Navigator nodes.

**Execution:**
Open two separate terminals, navigate to `auv_ws`, and source the setup file in both.

*Terminal 1 (The Commander):*
\`\`\`bash
ros2 run dead_reckoning commander_node
\`\`\`
*Terminal 2 (The Navigator):*
\`\`\`bash
ros2 run dead_reckoning navigator_node
\`\`\`

Type commands such as `forward`, `backward`, `turn left`, or `turn right` into Terminal 1 to see the Navigator dynamically update the bot's coordinates and heading in Terminal 2.
