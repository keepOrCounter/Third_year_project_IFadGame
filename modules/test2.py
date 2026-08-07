import ast

# 这是你提供的字符串形式的字典
dict_str = """{'title_of_description': 'River Environment', 'description': 'You find yourself in the heart of a majestic river, its tranquil waters flowing gently around you. \n\nTo the front, a sandy beach stretches invitingly, while to your back and sides, the river's current meanders steadily. \n\nThe landscape is adorned with lush green grass, adding a touch of vibrancy to the serene waters. \n\nThe river teems with life, offering a bountiful source of sustenance in the form of fish. \n\nNavigating through this aquatic expanse is a formidable task, requiring a significant expenditure of energy and determination due to the strong currents.'}"""
print("\\n" in dict_str)
print("\n" in dict_str)
print(dict_str)
dict_str = dict_str.replace("\\n", "\n")
dict_str = dict_str.replace("\n", "\\n")
print(dict_str)
# 使用 ast.literal_eval 来解析字符串形式的字典
parsed_dict = ast.literal_eval(dict_str)

# 现在你可以像操作普通字典一样访问值
print(parsed_dict['title_of_description'])
print(parsed_dict['description'])
