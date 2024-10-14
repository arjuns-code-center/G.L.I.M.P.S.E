# Navigation Nodes

Below is a brief description of what each node does to help with our navigation system. 

| Node Name | Description |
| --------- | ----------- |
| [```nav2pose.py```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/navigator/navigator/nav2pose.py) | Goal publishing node given target pose information | 
| [```sens2odom.py```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/navigator/navigator/sens2odom.py) | Converting encoder and IMU serial readings into odometry messages | 
| [```searchtargets.py```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/navigator/navigator/search_targets.py) | Search behavior for our target tracking to find or reacquire the targets | 
| [```filterlidar.py```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/navigator/navigator/filter_lidar.py) | Filtering LiDAR readings to void out the beams on Holly, or anything within Holly's perimeter | 
| [```camerasearch.py```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/navigator/navigator/camera_search.py) | Additional camera only search to find or reacquire targets | 

We found out that adding a camera search on top of a robot body search increases the likelihood and smoothness of searching for a target, making it as if a human were searching for a target. 

We have also implemented Velocity-of-target based navigation, to tackle with the stop-start behavior when a target is moving. What this does is take into account the velocity of the target and increase or decrease our goal poses accordingly, so there is smooth consistent motion to the goal. 

![image](https://github.com/user-attachments/assets/43d6dac3-b1e2-405c-b296-e737dcab511d)
