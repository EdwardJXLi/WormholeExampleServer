import cv2
import math
import numpy as np

# Code stolen from: https://github.com/codegiovanni/Webcam_Effect/blob/main/webcam_effect.py
# Just needed a random example of a computationally heavy video effect.
def circle_video_filter(video):
    output = np.zeros(video._frame.shape, dtype=np.int8)
    
    cell_width, cell_height = 12, 12
    new_width, new_height = int(video.width / cell_width), int(video.height / cell_height)
    small_image = cv2.resize(video._frame, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

    for i in range(new_height):
        for j in range(new_width):
            color = small_image[i, j]
            B = int(color[0])
            G = int(color[1])
            R = int(color[2])

            coord = (j * cell_width + cell_width, i * cell_height)

            cv2.circle(output, coord, 5, (B, G, R), 2)
            
    video._frame = output

# Image Warping Effect
def wavy_image_filter(video):
    import time
    output = np.zeros(video._frame.shape, dtype=np.int8)
    height, width, _ = video._frame.shape
    img = np.copy(video._frame)
 
    for i in range(height): 
        for j in range(width): 
            offset_y = int(16.0 * math.sin((2 * 3.14 * j / 150) + video.frame_controller.frames_rendered)) 
            if i+offset_y < height: 
                output[i,j] = img[(i+offset_y)%height,j] 
            else: 
                output[i,j] = 0 
        time.sleep(0.000001)  # some stupid hack to get cpu intensive tasks to not hog cpu
    
    video._frame = output
