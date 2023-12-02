import numpy as np
import cellpylib as cpl
from status_record import *
import cv2


class MapGenerator():
    def __init__(self, player : Player_status) -> None:
        self.textual_map = {}  # {x_coordinate : [Location_names(whose indices are y cordinate)]}
        self.current_coord = {"x" : player.x_coordinate, "y" : player.y_coordinate}
        self.current_main_terrain = 0 # land pattern, main terrain would be land mass

    def generate_random_map(self, rows: int, cols: int, land_prob: float=None): # rows, cols = y, x
        if land_prob == None:
            if self.current_main_terrain == 0:
                land_prob = 0.65
            else:
                land_prob = 0.35
        return np.random.choice([0, 1], size=(rows, cols), p=[1-land_prob, land_prob])


    def random_map_update_8n_rule(self, cell_grid: np.ndarray, threshold: int):
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_1 = np.where(oneD == 1)[0].shape[0]
        number_of_0 = oneD.shape[0] - number_of_1

        if cell == 1:
            number_of_1 -= 1
        else:
            number_of_0 -= 1
        # print(cell_grid)
        # print(number_of_1)
        # print(number_of_0)
        # print(cell)
        # print("-------------------")
        if number_of_1 > threshold:
            cell = 1
        elif number_of_1 < threshold:
            cell = 0

        return cell
    
    def rule(self, grid, cell, time_step, mode="8_neighbours", threshold = 4):
        # print(grid, c, t)
        if mode == "8_neighbours":
            return self.random_map_update_8n_rule(grid, threshold)
        
    def game_map_generation(self, rows: int, cols: int, land_prob: float, \
        cellular_timesteps: int, convert_threshold: int, mode="8_neighbours"): # rows, cols = y, x

        random_map = self.generate_random_map(rows, cols, land_prob=land_prob)
        cellular_automaton = cpl.init_simple2d(rows, cols)
        cellular_automaton[0] = random_map
        # print(cellular_automaton)
        # print(np.where(np.array([0, 0, 1, 0, 1, 0, 0, 1, 1, 1]) == 1)[0].shape[0])

        # The rule function must return a scalar for each cell


        # print(cpl.nks_rule(np.array([[0, 0, 0],[0, 1, 0],[0, 0, 0]]), 30))
        updated_map = cpl.evolve2d(cellular_automaton, timesteps=cellular_timesteps, \
            apply_rule=lambda grid, cell, time_step: \
                self.rule(grid, cell, time_step, mode, convert_threshold))

        # print(updated_map)
        print(random_map)
        print(updated_map[-1])

        array = random_map

        # Convert the array to a grayscale image
        # image = np.uint8(array * 255)
        colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
        colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
        colored_image[array == 1] = [0, 255, 0]  # Green for 1s

        # Optionally, scale the image to make it visually better
        scale_factor = 5
        scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

        # Display the image
        cv2.imshow('Visualized Image', scaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        array = updated_map[-1]

        # Convert the array to a grayscale image
        # image = np.uint8(array * 255)
        colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
        colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
        colored_image[array == 1] = [0, 255, 0]  # Green for 1s

        # Optionally, scale the image to make it visually better
        scale_factor = 5
        scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

        # Display the image
        cv2.imshow('Visualized Image', scaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test = MapGenerator(Player_status())
    test.game_map_generation(50, 50, 0.65, 5, 4)