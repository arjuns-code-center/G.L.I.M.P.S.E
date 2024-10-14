## Serial Communication
On the serial side, the ```/cmd_vel_nav``` topic is subscribed to and the Twist messages are converted into a linear and linear-rotational vector. This vector is then sent to the Nav Pico, which will then communicate with the motors and set their velocities accordingly. It will then read the wheel and IMU odometry data, and send it back to ROS. And thus, we have navigation with the physical robot. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/f5d28e58-e7bc-4cf5-89b7-cca8e2596e42)

For target tracking, we take the marker location, published in ```/marker_location``` topic, as an offset from the center, and send that to our target tracking Pico. This will then command the servos to center the camera at the center of the marker. We predict the motion of the marker using the offset's velocity and position to allow smooth camera movement. This allows us to perform target tracking when CPU resources are constrained, and we cannot calculate the pose of the marker fast (under 20 Hz). With our computer, however, we are able to calculate the pose at 30 Hz and above easily. 

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/ab3f6ce5-edd7-491d-afe9-5e546c6bcd06)
