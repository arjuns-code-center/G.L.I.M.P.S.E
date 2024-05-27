
![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/31cd0755-1891-4209-80e1-8882ec8a0141)

Finally, using scipy in Python again in the ``python aruco_video_detection.py`` file, we can read the .mat file as a dictionary object. The code shown below shows how you can extract the camera matrix and distortion coefficients calculated in the MATLAB script.

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/30e5c43d-8466-49cd-bc4b-374deefec767)

# Detection

Once the camera is calibrated and you have the necessary parameters, you can start detecting markers!

Next, to make the window size equal to the resolution, and have more pixels in the read image, we resize the window, and set the camera resolution as it reads. The default value will be 640x480.

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/baec31e8-b467-4534-87b8-2c8ac3404547)

The code starts reading frames from the camera chosen, and once it sees an ArUco marker, it will draw an outline on it, tell you its ID in the center of the marker, and also give you its distance from the camera in millimeters. The rotational and translational vectors are calculated with pose estimation using the camera calibration parameters.

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/a37714aa-beba-4843-b19a-d2f58ae1bedc)

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/8fa7bf18-5571-4064-b47d-8fb7ea7be4e1)

# The Translational Vector

``tvec = [x, y, d]`` where

``x``: vertical position of the center of the marker with respect to the center of the frame

``y``: horizontal position of the center of the marker with respect to the center of the frame

``d``: distance to the center of the marker from the camera.

# Output

Here is how the detected image looks like. You have the ability to save aruco detected images by pressing ``s`` on the keyboard.

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/31181203-7a5d-4ea5-ab4f-5fbfafec20a9)

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/b56cac42-61f8-4909-b5ae-4cb6107bcbe3)

Here is what the console output is.

![image](https://github.com/Samalmeida1028/sdp-team-12/assets/41523488/87d7b692-d8ad-4f8e-a7d1-e9cf463e3aaa)