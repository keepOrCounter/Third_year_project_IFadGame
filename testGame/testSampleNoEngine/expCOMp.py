import numpy as np
import cv2
import noise

def generate_perlin_noise_2d(shape, resolution):
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i / resolution, j / resolution)
    return world

def generate_random_noise_2d(shape):
    return np.random.rand(shape[0], shape[1])

# 设置地图大小
map_shape = (100, 100)
# 设置柏林噪声函数的分辨率
perlin_resolution = 15.0
# 生成柏林噪声地图
perlin_map = generate_perlin_noise_2d(map_shape, perlin_resolution)
# 生成随机地图
random_map = generate_random_noise_2d(map_shape)

print(np.where(perlin_map<-0.8))
# 展示和保存柏林噪声地图
cv2.imshow('Perlin Noise Map', perlin_map)
cv2.imwrite('perlin_noise_map.png', (perlin_map * 255).astype(np.uint8))

# 展示和保存随机地图
cv2.imshow('Random Noise Map', random_map)
cv2.imwrite('random_noise_map.png', (random_map * 255).astype(np.uint8))

cv2.waitKey(0)
cv2.destroyAllWindows()
