import cv2
import noise
import numpy as np

cv2.namedWindow("Perlin Noise Experiment")
cv2.createTrackbar("Octaves", "Perlin Noise Experiment", 1, 8, lambda x: None)
cv2.createTrackbar("Persistence", "Perlin Noise Experiment", 10, 100, lambda x: None)
cv2.createTrackbar("Scale", "Perlin Noise Experiment", 1, 100, lambda x: None)
cv2.createTrackbar("Width", "Perlin Noise Experiment", 800, 1920, lambda x: None)
cv2.createTrackbar("Height", "Perlin Noise Experiment", 600, 1080, lambda x: None)

while True:
    # Get the current slider values
    octaves = cv2.getTrackbarPos("Octaves", "Perlin Noise Experiment")
    persistence = cv2.getTrackbarPos("Persistence", "Perlin Noise Experiment") / 10.0
    scale = cv2.getTrackbarPos("Scale", "Perlin Noise Experiment") / 100.0
    width = cv2.getTrackbarPos("Width", "Perlin Noise Experiment")
    height = cv2.getTrackbarPos("Height", "Perlin Noise Experiment")

    world = np.zeros((height, width), dtype=np.float32)
    for i in range(height):
        for j in range(width):
            world[i][j] = noise.pnoise2(i * scale, j * scale, octaves=octaves+int(octaves==0), persistence=persistence, lacunarity=2.0, base=57)


    # print(world)
    # print(world)
    min_value = np.min(world)
    max_value = np.max(world)
    normalized_scale = (max_value - min_value) / 2
    world = np.round(world / normalized_scale).astype(int)
    # print(normalized_array)
    # print(np.where(normalized_array == 0))
    # print(world)
    # for x in list(world):
    #     print(set(x))
    world = cv2.normalize(world, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the noise map to a grayscale image
    world_image = cv2.cvtColor(world.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    # Show the generated Perlin noise
    cv2.imshow("Perlin Noise Experiment", world_image)

    key = cv2.waitKey(1)
    # break
    if key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()
