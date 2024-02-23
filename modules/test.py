import numpy as np
# from typing import Callable
from Pre_definedContent import *


# for x in result:
#     print(x)
# print(len(result) == len(def_items) == len(updated))

min_val = -60
max_val = 300
value = 280
result = 0

#128 is mapped by zero, so 128 is 0, and 0~128 is possible negative value, 128~255 is possible positive value

if value < 0:
    result = 128 - (128 - 0) * (value / min_val) # <boundary between positive and negative> - class width * (actual value/min)
elif value == 0:
    result = 128
else:
    result = 128 + (255 - 128) * (value / max_val) # <boundary between positive and negative> + class width * (actual value/max)

print(result)

worldStatus = globalInfo()
# player_info = Player_status(action_point = 30)
player_info = Player_status()
map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
# mapPCG = MapGenerator(player_info, map_record)
defined_command = Commands(player_info, map_record, worldStatus)
game_content = DefininedSys(defined_command, map_record)
a = np.array(["12nb","ttt"])
b = np.array(["a","35"])
c= np.append(a, b)
d = np.array([19, 15,1, 10])
choice = np.random.choice(c, size=(2,), p=(np.divide(d, np.sum(d))))
print(choice)
print(np.divide(d, np.sum(d)))
# print(np.append(a, b)[np.array([1,2])])
# import numpy as np
# import copy

# # Original array with mutable objects
# original_array = np.array([[1, 2, 3], [4, 5, 6]])
# print(np.divide(original_array, 5))
# # Shallow copy
# shallow_copy = np.copy(original_array)

# # Modify the shallow copy
# shallow_copy[0][0] = 100

# # Original array is also modified because it's a shallow copy
# print(original_array)
# print(shallow_copy)

# # Deep copy
# deep_copy = copy.deepcopy(original_array)

# # Modify the deep copy
# deep_copy[1][1] = 500

# # Original array remains unchanged because it's a deep copy
# print(original_array)
# print(deep_copy)
