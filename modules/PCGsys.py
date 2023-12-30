import numpy as np
import cellpylib as cpl
from status_record import *
from Pre_definedContent import *
import cv2
import random


class MapGenerator():
    def __init__(self, player : Player_status, map_info: Map_information) -> None:
        # self.textual_map = {}  # {x_coordinate : [Location_names(whose indices are y cordinate)]}
        # self.current_coord = {"x" : player.get_currentLocation()[0], "y" : player.get_currentLocation()[1]} # a copy of coord
        # self.current_main_terrain = 0 # land pattern, main terrain would be land mass
        self.terrain_type = np.array(["sea", "land"])
        self.__player = player
        self.__map_info = map_info

    def generate_random_map(self, rows: int, cols: int, land_prob: float=0.65): # rows, cols = y, x
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
        
    def game_map_generation(self, cellular_timesteps: int, convert_threshold: int, \
        mode="8_neighbours"): # rows, cols = y, x

        self.map_info_update()
        rows, cols = self.__map_info.get_map_size()
        if self.__map_info.get_current_area_type() == 1:
            random_map = self.generate_random_map(rows, cols, land_prob=0.65)
            random_map[0, :] = np.zeros((cols,))
            random_map[rows - 1, :] = np.zeros((cols,))
            
            random_map[:, 0] = np.zeros((rows,))
            random_map[:, cols - 1] = np.zeros((rows,))
            
        else:
            random_map = self.generate_random_map(rows, cols, land_prob=0.35)
            
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
        # print(random_map)
        # print(updated_map[-1])

        self.__map_info.set_currentMap(self.terrain_type[updated_map[-1]])
        
        return random_map, updated_map[-1] # for debug use
        # return updated_map[-1]
        
        
    def debug(self, cellular_timesteps: int, convert_threshold: int, \
        mode="8_neighbours"): # rows, cols = y, x

        random_map, updated_map = self.game_map_generation(cellular_timesteps, \
            convert_threshold, mode)

        # print(updated_map)
        print(random_map)
        print(updated_map)
        print(self.terrain_type[updated_map].tolist())

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


        array = updated_map

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
        
    def map_info_update(self) -> None:
        x, y = self.__player.get_currentLocation()
        rows, cols = self.__map_info.get_map_size() # row, cols = y, x

        x_areaType = (x + int(cols/2)) /cols
        y_areaType = (y + int(rows/2)) /rows
        if x_areaType == y_areaType:
            self.__map_info.set_current_area_type = 1
        else:
            self.__map_info.set_current_area_type = 0


class objectsGenerator():
    def __init__(self, defininedContent: DefininedSys) -> None:
        self.__defininedContent = defininedContent
        
    def objectGeneration(self, lowest_amount: int, highest_amount: int) -> list[Items]:
        """
        Args:
            `lowest_amount` (int): lower bound of number of objects generated (includ end point)\n
            `highest_amount` (int): upper bound of number of objects generated (includ end point)\n
        """
        objectList = self.__defininedContent.get_items()
        generateResult = random.choices(objectList, k=random.randint(lowest_amount, highest_amount))
        
        return generateResult


class eventGenerator():
    def __init__(self, defininedContent: DefininedSys) -> None:
        self.__defininedContent = defininedContent
        
    def eventGeneration(self) -> list[Events]:
        eventList = self.__defininedContent.get_events()
        generateResult = random.choice(eventList)
        
        return generateResult


# class PCGController():
#     def __init__(self, mapPCG: MapGenerator, objectsPCG: objectsGenerator, \
#         eventPCG: eventGenerator) -> None:
#         self.__mapPCG = mapPCG
#         self.__objectsPCG = objectsPCG
#         self.__eventPCG = eventPCG
    


if __name__ == "__main__":
    # test = MapGenerator(Player_status(), Map_information(1))
    # test.debug(5, 4)
    test = objectsGenerator(DefininedSys())
    test.objectGeneration(1, 6)