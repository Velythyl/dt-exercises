#!/bin/bash
sed -i "s/agent/${VEHICLE_NAME}/g" /opt/ros/noetic/share/rviz/viscontrol.rviz
rviz -d /opt/ros/noetic/share/rviz/viscontrol.rviz &
python3 /root/Documents/VLS-control-tool.py &
rostopic pub --latch "/${VEHICLE_NAME}/vls_node/action" std_msgs/String "data: init_vc"