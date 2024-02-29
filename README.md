# Virtual Painter Project

[Source Link](https://www.youtube.com/watch?v=01sAkU_NvOY&t=17575s)

The repository is mainly built upon MediaPipe, OpenCV. While MediaPipe offers a number of functionalities to perform hand tracking, OpenCV helps users to interact with these models. 

This repo lets users paint using their index finger. There are 2 available modes: 
* Selection Mode: This lets users select one of the 3 colors available or the eraser. This action is performed by bringing the index and middle fingers together and pointing to one of the 4 images at the top.
* Drawing Mode: This action is performed by only using the index finger and closing all other fingers. This lets you draw with one of the colors or erase as well.

To run:
```
python VirtualPainter.py
```
