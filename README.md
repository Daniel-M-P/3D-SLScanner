# 3D-SLScanner
Python program for recreating a 3D model of an object using Structured Light Scanning, from the use of two cameras and a projector.

Code written with the help of AI.

## Files:

pattern_creator.py: Creates gray patterns given a width and height of pixels to give each pixel an x and y gray binary value.

cameras_set_properties.py: Allows to change the properties of the camera and see the changes in real time.

capture_pattern.py: Projects the gray patterns made and captures an image for each pattern in both cameras, then waits until you rotate the object to repeat the process.

cameras_key_capture.py: Show the cameras in real time and captures the image when you press the 's' key until you reach 10 images.

image_seer.py: Slide through all the images inside the parent_folder created in capture pattern by pressing the 'D' key. Useful for verifying the images.

deca.py: Module with the deca class for obtaining the correspondance of pixels between camaras and the camara class for calculating the intrinsic and extrinsinc parameters.

reconstruction.py: Given the intrinsic and extrinsinc parameter of the camaras calculate the corresponding 3D point and saves it in a point_cloud, ply file.

ply_to_3D: Converts a cloud point file in to a 3D model (stl file)

### Note

Be aware of the threshold used for masking the images.
The rotation matrix and translation vector of the camaras have not been verified if they were calculated correctly.

## Referencias:
https://www.instructables.com/DIY-3D-scanner-based-on-structured-light-and-stere/
https://arxiv.org/pdf/1406.6595v1
https://fpcv.cs.columbia.edu

Código para la calibración:
https://github.com/niconielsen32/ComputerVision/tree/master/stereoVisionCalibration

