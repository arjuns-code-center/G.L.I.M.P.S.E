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

