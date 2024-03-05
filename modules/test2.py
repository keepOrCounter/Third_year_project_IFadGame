import json

# Read the JSON file
with open("tem.json", "r") as file:
    data = json.load(file)

# Print the loaded JSON data
print(data)
# result = json.loads("tem.json", strict=False)
# print(result)