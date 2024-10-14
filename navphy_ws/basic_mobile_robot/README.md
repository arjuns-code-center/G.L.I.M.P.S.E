## Behind the scenes: Navigation
The navigation stack is the most complicated part of our design project. The list of things involved, in order, goes as follows:
- Robot Localisation
- Simultaneous Localization And Mapping (SLAM)
- Coordinate Transforms
- Nav2 Servers

## Robot Localisation
The robot is localized using an Extended Kalman Filter (EKF). This node will take in all sources of odometry we provide it, and fuse them together into an odometry topic. This topic's information is read in by the navigation modules to accurately place the robot in the environment. Sources we use are:
- LiDAR ranges
- Wheel encoders
- Inertial Management Unit (IMU)

Suppose you know the starting point of an object. You wish to know where the object will be in the future. To do this, you will make an estimate. But how do you make that estimate? You will need to know something about the system, like the dynamics of it. If you know how the object is moving, you will be able to mathematically obtain its location in the future, given you know how long into the future you are extrapolating. But in the real world, this measure of the object's movement is noisy. As the time into the future increases, so does the uncertainty associated with the location of the object. 

But, it is still possible to make an estimate of the object's location using probability and odometry measurements. This is what the Kalman Filter does. It makes the assumption of linear motion model and environment, both modelled by a Gaussian. It uses the covariances associated with each source of odometry, and models the object's future locations using a probabilistic approach. This process does involve some level of noise, but will be accurate to a margin. 

An extended Kalman filter is used when the measurement and motion model are not linear. Since our wheel encoders do not account for wheel slippage, and our IMU can be noisy, and our LiDAR is not the best quality, it is possible that one or more of these readings are wrong. Additionally, our motion may not be linear at times, so we will not have a way to model that using the Kalman Filter. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/ba99deaf-5d88-48d2-91d7-bec8f73e0685)

Shown below is a connected tree showing the flow of information for our localization using EKF. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/33ba2bae-2a5e-466b-9848-0de6fb2b136f)

We have the configuration file for EKF in the [```ekf.yaml```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/basic_mobile_robot/config/ekf.yaml) file. This file allows you to define the topics used for each source of odometry and the values you are taking from each source to fuse together. It outputs the fused data to the ```odom``` frame and the ```/odometry/filtered``` topic. 

## SLAM
SLAM uses LiDAR ranges to localize the robot and navigate while mapping. It is a particle filter that probabilistically approximates the robot location using the measurements it receives. Our robot performs SLAM to generate the map and uses the joint odometry information from EKF to localize itself. Shown below is a SLAM generated map of the UMass Amherst M5! 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/688b8ccc-6d9e-4b77-b894-d1b22d476c36)

Our SLAM config file can be found in the [```doslam.yaml```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/basic_mobile_robot/config/doslam.yaml) file. This contains important information about the algorithm we are using, how many samples we are collecting, and what topic we are reading in ```LaserScan``` data from. We take this file from the [```ROS2 SLAM Toolbox GitHub repository```](https://github.com/SteveMacenski/slam_toolbox). 

## Coordinate Transforms
Coordinate Transforms are how ROS understands movement. When the robot moves in the real world, ROS needs to know that is happening too. It does so by mapping the coordinates of each component of the robot and the environment relative to each other. In our robot description file, we have joints and links. Joints are pieces of the robot that can move and rotate. They connect links together (eg: Left wheel joint, Right wheel joint). Links are pieces of the robot that cannot move (eg: Base, LiDAR, Wheel). Each link and joint is mapped together using the ```robot_state_publisher``` and ```joint_state_publisher``` nodes provided by ROS. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/32681a65-1e49-4259-8362-fd9fdf01dd2e)

But we also need a coordinate transform from the odometry of the robot to the base of the robot. This tells us where the robot is. So a transform is published by EKF. Same way, we need to know where the robot is in the map generated, so another transform is published from SLAM. Shown below is the complete coordinate transform tree. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/f7c0b655-bd9a-48ee-a253-f3ebd0e7bf9d)

So this now connects each part of the environment with everything else in ROS. 

## Nav2 Servers
So the robot is initialized, the transforms are set, and SLAM + EKF are working. Now how does the navigation work? First, Nav2 sets up a Behavior Tree. This contains all the behaviors the robot will perform. First, it tries to compute a path to the goal and smooth it. This happens at a rate of 1 Hz. As soon as the path is computed, the follow instructions are given. Now, let's say the navigation is unsuccessful, due to some obstacle or noise. There are recovery behaviors that will be executed in a Round Robin fashion. First, the global and local costmaps are set. Then, ROS tries to navigate again. If that fails, then the robot is spun 90 degrees, and ROS tries navigating again. If that fails, it waits 5 seconds and tries again. If that too fails, it backs up about 30 cm and tries again. If everything fails, it reruns the whole sequence of navigation and recovery up to 6 times before aborting navigation. 

With this tree, Nav2 launches the ```behavior_server``` and ```smoother_server```. The behavior server handles all the behaviors specified in the tree defined above, while the smoother server intelligently smooths the paths it receives to avoid any obstacles to some radius. This is done using the ```ConstrainedSmoother``` from the Nav2 API. With all this, the simplified Nav2 block diagram looks like below:

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/1ee7b45f-0c73-4795-837a-6b310e492032)

Next, the ```planner_server``` and ```controller_server``` are launched. The planner uses the ```SmacHybridPlanner``` from Nav2 API and runs A* search to find the fastest path to goal. The controller computes the ```cmd_vel``` Twist messages and publishes to the ```/cmd_vel_nav``` topic. This is used by the serial communication node. So the block diagram updates like so:

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/b6bfc5bb-e685-439f-bf84-2fd3a542b197)

Next, the certerpiece of the navigation system comes online. This is the ```bt_navigator``` node, which takes in all the outputs and goal pose information and keeps track of the navigation. It uses the ```bond``` timer to sync all the servers together and run navigation smoothly. The final block diagram is as follows: 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/4a87bee6-890b-4f12-bda9-f1737b721793)

More information about the different servers and the parameters associated with them can be found in the [```nav2_params.yaml```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/basic_mobile_robot/params/nav2_params.yaml) file. You can find all the information about each server in the [```Nav2 Configuration Guide```](https://docs.nav2.org/configuration/index.html), which describes each and every parameter we used. 
