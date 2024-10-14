# ArUco Detection and Pose Estimation
Below is our documentation on how we perform our computer vision for marker detection. Firstly, we calibrate the camera using 10 images of a checkerboard that we took, with different distances and angles. Using this, we run a [```MATLAB calibration script```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/blob/main/navphy_ws/calibration/camera_calibrator_script.m) to get our camera matrix parameters and distortion coefficients. This saves a parameters.mat file in our [```calibration```](https://github.com/arjuns-code-center/G.L.I.M.P.S.E/tree/main/navphy_ws/calibration) directory. We then use this .mat file in our code to perform detection and pose estimation. 

# The Translational Vector
We are interested in the translational vector for our project. It is as follows:

``tvec = [x, y, d]`` where

``x``: vertical position of the center of the marker with respect to the center of the frame

``y``: horizontal position of the center of the marker with respect to the center of the frame

``d``: distance to the center of the marker from the camera.

# Output
Here is what the console output is.

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/87d7b692-d8ad-4f8e-a7d1-e9cf463e3aaa)

# Smooth Target Tracking
A major challenge we faced was the servo speed being reliant on the update rate of the target pose. In order to have smooth movement, we needed an update rate > 30 Hz, but this took up more than 50% of the computer processing power. This slowed down our other systems.

To deal with this, we take the vector heading of the target we see, and predict where the target will be next. We know the target motion is relatively linear, so we can do a linear interpolation on the next position. THis allows us to slow down the update rate to 10 Hz while still keeping the target in frame.

Eventually, we were able to get the CPU utilization to ~35% with a higher update rate (~20 Hz). Shown below is a representation of how this works. 

![image](https://github.com/user-attachments/assets/1d103505-9851-4fdb-865a-d0424601c409)
