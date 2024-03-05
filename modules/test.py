# import numpy as np
# # from typing import Callable
# from Pre_definedContent import *


# # for x in result:
# #     print(x)
# # print(len(result) == len(def_items) == len(updated))

# min_val = -60
# max_val = 300
# value = 280
# result = 0

# #128 is mapped by zero, so 128 is 0, and 0~128 is possible negative value, 128~255 is possible positive value

# if value < 0:
#     result = 128 - (128 - 0) * (value / min_val) # <boundary between positive and negative> - class width * (actual value/min)
# elif value == 0:
#     result = 128
# else:
#     result = 128 + (255 - 128) * (value / max_val) # <boundary between positive and negative> + class width * (actual value/max)

# print(result)

# worldStatus = globalInfo()
# # player_info = Player_status(action_point = 30)
# player_info = Player_status()
# map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
# # mapPCG = MapGenerator(player_info, map_record)
# defined_command = Commands(player_info, map_record, worldStatus)
# game_content = DefininedSys(defined_command, map_record)
# a = np.array(["12nb","ttt"])
# b = np.array(["a","35"])
# c= np.append(a, b)
# d = np.array([19, 15,1, 10])
# choice = np.random.choice(c, size=(2,), p=(np.divide(d, np.sum(d))))
# print(choice)
# print(np.divide(d, np.sum(d)))
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
# def tp(t):
#     print(t.buff_name)
# class Buff():
#     def __init__(self, fu) -> None:
        
#         self.buff_name = 1
#         self.T = (self,)
#         self.fu = fu

# a = Buff(tp)
# a.fu(*a.T)
# a.buff_name *= 10
# a.fu(*a.T)
# a = {"1":3, "2":13,"3":-3,"4":63,"5":10}
# print(list(a.values()))
# a.pop("2")
# print(a)
# class MyClass:
#     def __init__(self):
#         self.attr1 = 1
#         self.attr2 = 2
#         self.attr3 = 3

# obj = MyClass()

# # 使用 vars() 函数获取对象的属性字典
# attributes = vars(obj)
# print(type(attributes))
# for attribute, value in attributes.items():
#     print(attribute, '=', value)

# print(str(attributes))
# import openai
# class Gpt3():
#     def __init__(self, api_key) -> None:
#         # Set up the OpenAI API client
#         openai.api_key = api_key

#     def inquiry(self, prompt:str, systemRole: str, temperature = 0.5) -> str:
#         # Generate a response
#         response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
#         messages=[
#         {"role": "system", "content": systemRole},
#         {"role": "user", "content": prompt}
#         ],
#         temperature=temperature,
#         max_tokens=1000,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#         )

#         # print(response.choices)
#         # print(response.choices[0].message)
#         # print(response.model)
#         return response.choices[0].message.content
# a = """You are an food generator for an RPG game and need to generate some food according to the json format and following requirements. Here is the reqirement form:
# {
#     "name": <name of the food>,
#     "category": "food",
#     "appear_possibility": <the possibility of this food can be picked up(note if the food is not totally natural or processed by human, please set all the possibility into 0 like the bread, grilled fish...): sea, land, forest and beach, in dictionary form, each possibility is between 0-20>,
#     "weight": <The weight of the food, player can take totally 20 units weight items>,
#     "item_energy_recovery": <how many action point player can recovery after eat this food>,
#     "edible": <true or false, whether food is edible, the food like "rotten apple" or "raw kidney bean" are not edible>,
#     "freshness": <How many turns the food can be store in general case>,
#     "thirst": <the sense of thirst player will change after eat this food>
# }
# Please note that the production of food must be logical. You will receive the list like this: ["soup", "grilled potato", "raw fish"], which means the food already in the game, and you should generate a different food that is not in the list. Here are some expected results:
# {
#     "name": "apple",
#     "category": "food",
#     "appear_possibility": {"sea": 0, "land": 1, "forest": 10, "beach": 0},
#     "weight": 2,
#     "item_energy_recovery": 5,
#     "edible": true,
#     "freshness": 72,
#     "thirst": 5
# },
# {
#     "name": "bread",
#     "category": "food",
#     "appear_possibility": {"sea": 0, "land": 0, "forest": 0, "beach": 0},
#     "weight": 1,
#     "item_energy_recovery": 25,
#     "edible": true,
#     "freshness": 50,
#     "thirst": -10
# }"""
# test = Gpt3("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")
# t = ["soup", "grilled potato", "raw fish", "bread", "berry", "potato"]
# result = test.inquiry(str(t) + ", (note that the appear_possibility of human processed food should all be 0)", a)
# print(result)
# a = [5, 7, 9, 14, 18, 21, 24, 29, 34, 39, 40, 50, 58, 72, 76, 80, 81, 97, 102, 120, 122, 138, 150, 156, 172, 187, 193, 199, 212, 232, 243, 251, 279, 314, 365, 392, 414, 429, 449, 450, 480, 485, 498, 553, 577, 652, 657, 661, 670, 675, 680, 686, 688, 712, 745, 777, 808, 819, 820, 834, 857, 870, 880, 886, 901, 906, 924, 952, 961, 966, 976, 1003, 1046, 1055]
# print(len(a))


import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict

data_path = "eventTune.jsonl"

# Load the dataset
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

# Initial dataset stats
print("Num examples:", len(dataset))
print("First example:")
for message in dataset[0]["messages"]:
    print(message)

# Format error checks
format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue
        
    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue
        
    for message in messages:
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1
        
        if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
            format_errors["message_unrecognized_key"] += 1
        
        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1
            
        content = message.get("content", None)
        function_call = message.get("function_call", None)
        
        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1
    
    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")


encoding = tiktoken.get_encoding("cl100k_base")

# not exact!
# simplified from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

def num_assistant_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")




# Warnings and tokens counts
n_missing_system = 0
n_missing_user = 0
n_messages = []
convo_lens = []
assistant_message_lens = []

for ex in dataset:
    messages = ex["messages"]
    if not any(message["role"] == "system" for message in messages):
        n_missing_system += 1
    if not any(message["role"] == "user" for message in messages):
        n_missing_user += 1
    n_messages.append(len(messages))
    convo_lens.append(num_tokens_from_messages(messages))
    assistant_message_lens.append(num_assistant_tokens_from_messages(messages))
    
print("Num examples missing system message:", n_missing_system)
print("Num examples missing user message:", n_missing_user)
print_distribution(n_messages, "num_messages_per_example")
print_distribution(convo_lens, "num_total_tokens_per_example")
print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
n_too_long = sum(l > 4096 for l in convo_lens)
print(f"\n{n_too_long} examples may be over the 4096 token limit, they will be truncated during fine-tuning")


# Pricing and default n_epochs estimate
MAX_TOKENS_PER_EXAMPLE = 4096

TARGET_EPOCHS = 3
MIN_TARGET_EXAMPLES = 100
MAX_TARGET_EXAMPLES = 25000
MIN_DEFAULT_EPOCHS = 1
MAX_DEFAULT_EPOCHS = 25

n_epochs = TARGET_EPOCHS
n_train_examples = len(dataset)
if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
    n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
    n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

n_billing_tokens_in_dataset = sum(min(MAX_TOKENS_PER_EXAMPLE, length) for length in convo_lens)
print(f"Dataset has ~{n_billing_tokens_in_dataset} tokens that will be charged for during training")
print(f"By default, you'll train for {n_epochs} epochs on this dataset")
print(f"By default, you'll be charged for ~{n_epochs * n_billing_tokens_in_dataset} tokens")

















# import json

# # Read the JSON file
# with open("tem.json", "r") as file:
#     data = json.load(file)

# # Print the loaded JSON data
# print(data)
# # result = json.loads("tem.json", strict=False)
# # print(result)