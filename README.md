## Robot Follow The Line. 

This program runs alongside a maestro.py file to control a robot. For the execution of this code I have it flashed onto a MicroSD that runs on a Raspberry Pi3. Using OpenCV I capture an image from the camera mounted on the head of the robot. Pointing the head down I use a mixture of Bluring and Dilation functions to locate contrast on the ground (usually the line)while ignoring noise that might throw off the traversal of the robot. Based on where the majority of the contrasting pixels comes from the robot turns left or right. If the whole 
image is black the robot stops as there is no line to follow. 
