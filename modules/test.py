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
# # import numpy as np
# # terrain_type = np.array([1,2,3])
# # print(np.shape(terrain_type)[0])
# # Your JSON formatted string
# json_string = '''
# {
#     "successful": false,
#     "fail": "True",
#     "reward": [], 
#     "penalty": [1]
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
# print(data["successful"])
# print(int(-0.1))

    # def visualized(self, random_map, updated_map, mode="8_neighbours"): # rows, cols = y, x

    #     # random_map, updated_map = self.game_map_generation(cellular_timesteps, \
    #     #     convert_threshold, mode)

    #     # print(updated_map)
    #     print(random_map)
    #     print(updated_map)
    #     print(self.terrain_type[updated_map].tolist())

    #     array = random_map

    #     # Convert the array to a grayscale image
    #     # image = np.uint8(array * 255)
    #     colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
    #     colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
    #     colored_image[array == 1] = [0, 255, 0]  # Green for 1s

    #     # Optionally, scale the image to make it visually better
    #     scale_factor = 5
    #     scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

    #     # Display the image
    #     cv2.imshow('Visualized Image', scaled_image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()


    #     array = updated_map

    #     # Convert the array to a grayscale image
    #     # image = np.uint8(array * 255)
    #     colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
    #     colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
    #     colored_image[array == 1] = [0, 255, 0]  # Green for 1s

    #     # Optionally, scale the image to make it visually better
    #     scale_factor = 5
    #     scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

    #     # Display the image
    #     cv2.imshow('Visualized Image', scaled_image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
# for y in range(1, -2, -1):
#     print(y)
# import numpy as np

# def random_replace(arr, replace_prob):
#     """
#     Randomly replaces some of the 1s in a 2D numpy array with 3s.

#     Parameters:
#         arr (numpy.ndarray): Input 2D numpy array.
#         replace_prob (float): Probability of replacing a 1 with a 3.

#     Returns:
#         numpy.ndarray: New array with replacements.
#     """
#     replaced_arr = np.copy(arr)  # Create a copy of the input array
#     np.random.seed(100)
#     a = np.random.randint(0, 100, arr.shape)
#     print(a)
#     np.random.seed(100)
#     mask = np.random.rand(*arr.shape)  # Create a mask of True/False values based on probability
#     print(mask)
#     # replaced_arr[arr == 1] = np.where(mask[arr == 1], 3, 1)  # Replace 1s with 3s where the mask is True
#     # replaced_arr[np.logical_and(arr == 1, mask)] = 3  # Replace 1s with 3s where the mask is True
#     # return replaced_arr

# # Example usage:
# # Create a 2D numpy array
# original_array = np.array([[1, 0, 1, 1],
#                            [1, 1, 1, 1],
#                            [1, 1, 5, 1]])

# # Probability of replacing 1s with 3s
# replace_probability = 0.3

# # Perform random replacements
# modified_array = random_replace(original_array, replace_probability)

# print("Original Array:")
# print(original_array)
# print("\nModified Array:")
# print(modified_array)
# print(modified_array[(0,1)])
# import nltk
# from nltk.corpus import wordnet
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag

# def get_word_meaning_in_phrase(phrase, word):
#     tokens = word_tokenize(phrase)
#     tagged_tokens = pos_tag(tokens)
    
#     # 找到目标单词在短语中的词性标签
#     word_pos = None
#     for token, pos in tagged_tokens:
#         if token.lower() == word.lower():
#             word_pos = pos
#             break
    
#     if word_pos:
#         # 根据词性标签在WordNet中找到对应的含义
#         synsets = wordnet.synsets(word, pos=word_pos[0].lower())
#         print(synsets)
#         if synsets:
#             # 获取短语中其他单词的同义词集合
#             other_words_synsets = []
#             for token, pos in tagged_tokens:
#                 if token.lower() != word.lower():
#                     synsets2 = wordnet.synsets(token, pos=pos[0].lower())
#                     other_words_synsets.extend(synsets2)
            
#             meanings = [synset.definition() for synset in synsets]
#             return meanings, synsets, other_words_synsets
#         else:
#             return None, None, None
#     else:
#         return None, None, None

# # 示例短语和目标单词
# phrase = "move forward"
# word = "move"

# # 获取目标单词在短语中的意思和相应的同义词集合
# meanings, synsets, other_words_synsets = get_word_meaning_in_phrase(phrase, word)
# if meanings:
#     print(f"Meanings of '{word}' in the context of the phrase:")
#     for i, meaning in enumerate(meanings, 1):
#         print(f"{i}. {meaning}")

#     # 显示与给定含义相关的同义词集合
#     for synset in synsets:
#         print(f"\nSynonyms for '{word}' in the context of the phrase (Synset: {synset.name()}):")
#         for lemma in synset.lemmas():
#             print(lemma.name())
    
#     # 显示短语中其他单词的同义词集合
#     print("\nOther words' synonyms in the context of the phrase:")
#     for other_word_synsets in other_words_synsets:
#         for lemma in other_word_synsets.lemmas():
#             print(lemma.name())
# else:
#     print(f"No meanings found for '{word}' in the context of the phrase")


# # import nltk
# # from nltk.tokenize import word_tokenize

# def get_word_meaning_in_context(phrase, target_word):
#     tokens = word_tokenize(phrase)
#     tagged_tokens = nltk.pos_tag(tokens)  # 进行词性标注
#     print(tagged_tokens)
#     for token, tag in tagged_tokens:
#         if token == target_word:
#             return tag

# print("--------------------------------------")
# phrase = "play game"
# target_word = "play"
# meaning = get_word_meaning_in_context(phrase, target_word)
# print(f"Part of speech of '{target_word}' in '{phrase}': {meaning}")

# print(meaning)
# import nltk
# import time
# # import sys
# from os.path import expanduser
# begin = time.time()
# home = expanduser("~")
# from nltk.tag.hunpos import HunposTagger
# _path_to_bin = home + '\\hunpos-1.0-win\\hunpos-tag.exe'
# _path_to_model = home + '\\hunpos-1.0-win\\english.model'
# ht = HunposTagger(path_to_model=_path_to_model, path_to_bin=_path_to_bin)
# text = "move forward"
# print(ht.tag(text.split()))
# print(time.time()-begin)
# ht.close()
# print("----------------------------------")
# sys.exit(0)
# print("----------------------------------")
class Location():
    def __init__(self, location_name) -> None:
        """`location_name:` name of current terrain\n
            `objects:` items at current place\n
            `description:` description generated by GPT, only for visited places, in this format: \n
{
    "location name": <location name>,
    "Description of current and surrounding locations": <What is surrounding and where player at>,
    "Landscape Features description": <Any specific Landscape>, 
    "Items description": <Any items>
}\n
            `x\y: ` locations' coordinate
        """
        self.location_name = location_name

t = Location(0)
a = lambda player: player.location_name > 1

print(a(t))
t.location_name +=10
print(a(t))
a=[1,2,3]
b = a
b.pop()
print(a)