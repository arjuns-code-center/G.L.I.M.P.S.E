# Physical Navigation using ROS2 Navigation Stack
This branch contains a number of packages, listed below:
| Package Name | Description |
| ------------ | ----------- |
| [```basic_mobile_robot```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/basic_mobile_robot) | all the navigation necessities. Contains URDF file for the robot, SLAM and EKF configuration files, and navigation launch script |
| [```navigator```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/navigator) | navigation nodes to work with target tracking, search behaviors, and publishing odometry |
| [```py_img_stream```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/py_img_stream) | performs our core computer vision to recognize targets and perform pose estimation on them |
| [```py_serial```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/py_serial) | handles all serial communication between ROS2 and our hardware |
| [```gui```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/gui) | an interactive Graphical User Interface (GUI) for the user |
| [```obs_nodes```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/obs_nodes) | Open Broadcast Service (OBS) websocket node that launches with our navigation to live stream camera feed |
| [```rpi_pico```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/rpi_pico) | backup code for our navigation and target tracking Picos |
| [```scripts```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/scripts) | contains Bash scripts to start our robot processes. Used by our GUI |

## Starting the Robot
After flipping the switch on and turning on the computer on Holly, you are able to Secure Shell (SSH) in using the command below:
```
ssh -Y sdpteam12@IPADDR
```
The ```IPADDR``` field is what shows up when the computer is connected to your private network (mobile hotspot or other private network). Note that this will not work on eduroam. 

Then, type the following into the terminal:
```
./run.sh
```
This script is located in the home directory of the on-board computer of the robot. This will launch the GUI. From here, clicking on ```Launch Navigation``` will launch all required nodes for navigation and tracking. You will be able to enter targets into the GUI as follows:

```[[ID, side length, time in seconds], [ID, side length, time in seconds]]```

This allows the user to specify a target ID of variable size for variable time of tracking. Larger targets can be seen from further away. 

## Serial Communication
On the serial side, the ```/cmd_vel_nav``` topic is subscribed to and the Twist messages are converted into a linear and linear-rotational vector. This vector is then sent to the Nav Pico, which will then communicate with the motors and set their velocities accordingly. It will then read the wheel and IMU odometry data, and send it back to ROS. And thus, we have navigation with the physical robot. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/f5d28e58-e7bc-4cf5-89b7-cca8e2596e42)

For target tracking, we take the marker location, published in ```/marker_location``` topic, as an offset from the center, and send that to our target tracking Pico. This will then command the servos to center the camera at the center of the marker. We predict the motion of the marker using the offset's velocity and position to allow smooth camera movement. This allows us to perform target tracking when CPU resources are constrained, and we cannot calculate the pose of the marker fast (under 20 Hz). With our computer, however, we are able to calculate the pose at 30 Hz and above easily. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/ab3f6ce5-edd7-491d-afe9-5e546c6bcd06)

