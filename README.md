# Face_recognition
This Python program utilizes the OpenCV library for detecting faces in images or video streams. After processing, any changes made to the content, such as marked bounding boxes, are saved as a file. This file is then transferred to the same server over a Wi-Fi network using HTTP. The program is an efficient solution for scenarios requiring real-time face detection and seamless file sharing, such as in IoT applications, smart home devices, or cloud-based analysis systems.

## Installion

- install requirement's: `pip install -r requirements.py`

## Introduction of files
- `image_comparison.py`:file for comparing images.
- `main.py`:the main program file to run.
- `simple_facerec`:the simple_facerec library for the main file.

**note**:you can put your photo in `images` folder and see the name of the file(the name you gave to your photo)above the red square in the middle of your camera if it reconizes you well.after that it'll write "(your name) is present" in the terminal and also in the txt file(`text`) and sends it to a local server network like WI_FI.

I will appreciate your help  in improving this code and solving my problem.
