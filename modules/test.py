# import numpy as np
# import random

# def generate_random_map(rows, cols, wall_prob=0.4):
#     """Generates a random map represented as a 2D array.
    
#     Args:
#     rows (int): Number of rows in the map.
#     cols (int): Number of columns in the map.
#     wall_prob (float): Probability of a cell being a wall.

#     Returns:
#     numpy.ndarray: The generated map.
#     """
#     return np.random.choice([0, 1], size=(rows, cols), p=[1-wall_prob, wall_prob])

# def get_neighbors(matrix, row, col):
#     """Get the values of all neighbors of a cell in a 2D matrix.

#     Args:
#     matrix (numpy.ndarray): The 2D array representing the map.
#     row (int): Row index of the cell.
#     col (int): Column index of the cell.

#     Returns:
#     list: Values of the neighbors.
#     """
#     neighbors = []
#     rows, cols = matrix.shape
#     for i in range(max(0, row-1), min(rows, row+2)):
#         for j in range(max(0, col-1), min(cols, col+2)):
#             if (i, j) != (row, col):
#                 neighbors.append(matrix[i, j])
#     return neighbors

# def apply_rules(matrix, n, m):
#     """Apply the given rules to the map for m iterations.

#     Args:
#     matrix (numpy.ndarray): The 2D array representing the map.
#     n (int): Threshold for the number of walls among neighbors.
#     m (int): Number of iterations to apply the rules.

#     Returns:
#     numpy.ndarray: The updated map.
#     """
#     for _ in range(m):
#         new_matrix = matrix.copy()
#         rows, cols = matrix.shape
#         for row in range(rows):
#             for col in range(cols):
#                 neighbors = get_neighbors(matrix, row, col)
#                 if sum(neighbors) > n:
#                     new_matrix[row, col] = 1  # Become a wall
#                 elif sum(neighbors) < n:
#                     new_matrix[row, col] = 0  # Become empty space
#         matrix = new_matrix
#     return matrix

# # Example usage
# rows, cols = 10, 10  # Size of the map
# wall_prob = 0.4     # Probability of a cell being a wall initially
# n = 4               # Threshold for the number of walls among neighbors
# m = 3               # Number of iterations to apply the rules

# # Generate a random map
# random_map = generate_random_map(rows, cols, wall_prob)
# # Apply the rules to the map
# updated_map = apply_rules(random_map, n, m)

# # Displaying the initial and final maps
# print(random_map)
# print(updated_map)

# import numpy as np
# import cellpylib as cpl
# import cv2

# def generate_random_map(rows, cols, land_prob=0.6):
#     np.random.seed(0)
#     return np.random.choice([0, 1], size=(rows, cols), p=[1-land_prob, land_prob])

# # def get_neighbors(cell_grid, row, col):
# #     neighbors = []
# #     rows, cols = cell_grid.shape
# #     for i in range(max(0, row-1), min(rows, row+2)):
# #         for j in range(max(0, col-1), min(cols, col+2)):
# #             if (i, j) != (row, col):
# #                 neighbors.append(cell_grid[i, j])
# #     return neighbors

# def cellular_automaton_rule(cell_grid, n):
#     rows, cols = cell_grid.shape
#     cell = cell_grid[int(rows/2), int(cols/2)]
#     oneD = cell_grid.copy().flatten()
#     number_of_1 = np.where(oneD == 1)[0].shape[0]
#     number_of_0 = oneD.shape[0] - number_of_1

#     if cell == 1:
#         number_of_1 -= 1
#     else:
#         number_of_0 -= 1
#     # print(cell_grid)
#     # print(number_of_1)
#     # print(number_of_0)
#     # print(cell)
#     # print("-------------------")
#     if number_of_1 > n:
#         cell = 1
#     elif number_of_1 < n:
#         cell = 0
#     # new_grid = np.zeros_like(cell_grid)
#     # print(cell_grid)
#     # rows, cols = cell_grid.shape
#     # for row in range(rows):
#     #     for col in range(cols):
#     #         neighbors = get_neighbors(cell_grid, row, col)
#     #         if sum(neighbors) > n:
#     #             new_grid[row, col] = 1
#     #         elif sum(neighbors) <= n:
#     #             new_grid[row, col] = 0
#     # print(new_grid)
#     return cell

# rows, cols = 100, 100
# land_prob = 0.65
# n = 4
# m = 5

# random_map = generate_random_map(rows, cols, land_prob=land_prob)
# cellular_automaton = cpl.init_simple2d(rows, cols)
# cellular_automaton[0] = random_map
# # print(cellular_automaton)
# # print(np.where(np.array([0, 0, 1, 0, 1, 0, 0, 1, 1, 1]) == 1)[0].shape[0])

# # The rule function must return a scalar for each cell
# def rule(grid, c, t):
#     # print(grid, c, t)
#     return cellular_automaton_rule(grid, n)

# # print(cpl.nks_rule(np.array([[0, 0, 0],[0, 1, 0],[0, 0, 0]]), 30))
# updated_map = cpl.evolve2d(cellular_automaton, timesteps=m, apply_rule=lambda n, c, t: rule(n, c, t))

# # print(updated_map)
# print(random_map)
# print(updated_map[-1])


# # Your 2D NumPy array
# array = random_map

# # Convert the array to a grayscale image
# # image = np.uint8(array * 255)
# colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
# colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
# colored_image[array == 1] = [0, 255, 0]  # Green for 1s

# # Optionally, scale the image to make it visually better
# scale_factor = 5
# scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

# # Display the image
# cv2.imshow('Visualized Image', scaled_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# array = updated_map[-1]

# # Convert the array to a grayscale image
# # image = np.uint8(array * 255)
# colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
# colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
# colored_image[array == 1] = [0, 255, 0]  # Green for 1s

# # Optionally, scale the image to make it visually better
# scale_factor = 5
# scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

# # Display the image
# cv2.imshow('Visualized Image', scaled_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(np.zeros((50,)))
# def ttt(t):
#     print(t)

# v = ttt
# print(str(v))
# b = (2, )
# print(type(b))
# v(*b)

# import json

# # Your JSON formatted string
# json_string = '''
# {
#     "event_name": "discovering an abandoned camp",
#     "event_description": "Land\n\nYou find yourself standing in the middle of a vast, open land. The desolation of the surroundings weighs heavily on your spirit, as if the land itself is sapping away your strength. There is no sign of civilization as far as the eye can see, leaving you feeling isolated and vulnerable.\n\nAmidst the barren landscape, you spot a few weapon crafting benches scattered around. They stand as silent reminders of a presence that once inhabited this desolate place. The mystery of who left them behind and why lingers in the air, adding an eerie touch to the already somber atmosphere. These benches hold the potential to create formidable weapons, if you possess the necessary materials."
# }
# '''

# # Parse the JSON string
# data = json.loads(json_string, strict=False)
# print(type(data))
# a = dict()
# print(type(a))

# # Extract the value of the "event_name" key
# event_name = data.get("event_name")

# # Extract the value of the "event_description" key
# event_description = data.get("event_description")

# # Print the extracted values
# print("Event Name:", event_name)
# print("Event Description:", event_description)


    def visualized(self, random_map, updated_map, mode="8_neighbours"): # rows, cols = y, x

        # random_map, updated_map = self.game_map_generation(cellular_timesteps, \
        #     convert_threshold, mode)

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