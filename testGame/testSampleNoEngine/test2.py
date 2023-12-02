import cv2
import noise
import numpy as np

scale = 0.01
width = 400
height = 300
# Create a window with sliders for controlling Perlin noise parameters
# cv2.namedWindow("Perlin Noise Experiment")
world = np.zeros((height, width), dtype=np.float32)

for i in range(height):
    for j in range(width):
        world[i][j] = noise.pnoise2(i * scale, j * scale, octaves=6, persistence=0.4)
print(list(world))