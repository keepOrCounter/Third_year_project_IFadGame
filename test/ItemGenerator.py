from interactionSys import Gpt3

systemRole = """You are an item generator for an RPG game and need to generate some food according to the json format and following requirements. Here is the reqirement form:
{
    "name": <name of the food>,
    "category": "food",
    "appear_possibility": <the possibility of this food can be picked up(if the food is human processed, please set all the possibility into 0): sea, land, forest and beach, in dictionary form, each possibility is between 0-20>,
    "weight": <The weight of the food, player can take totally 20 units weight items>,
    "item_energy_recovery": <how many action point player can recovery after eat this food>,
    "edible": <true or false, whether food is edible, the food like "rotten apple" or "raw kidney bean" are not edible>,
    "freshness": <How many turns the food can be store in general case>,
    "thirst": <the sense of thirst player will change after eat this food>
}
Please note that the production of food must be logical. Here are some expected results:
{
    "name": "apple",
    "category": "food",
    "appear_possibility": {"sea": 0, "land": 1, "forest": 10, "beach": 0},
    "weight": 2,
    "item_energy_recovery": 5,
    "edible": true,
    "freshness": 72,
    "thirst": 5
},
{
    "name": "bread",
    "category": "food",
    "appear_possibility": {"sea": 0, "land": 0, "forest": 0, "beach": 0},
    "weight": 1,
    "item_energy_recovery": 25,
    "edible": true,
    "freshness": 50,
    "thirst": -10
},
{
    "name": "grilled fish",
    "category": "food",
    "appear_possibility": {"sea": 0, "land": 0, "forest": 0, "beach": 0},
    "weight": 3,
    "item_energy_recovery": 25,
    "edible": true,
    "freshness": 50,
    "thirst": -10
}"""

# prompt = 'Please generate a new item similar to the following:\
#             Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 1, \
#             item_energy_recovery = 15, state = 2, freshness = 72, satiety = 30, thirst = -20), \
#             Food("raw fish", {"sea": 18, "land": 0, "forest": 0, "beach": 10}, weight = 2, \
#             item_energy_recovery = 5, state = 1, freshness = 24, satiety = 15, thirst = 20),\
#             Food("grilled fish", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 2, \
#                  item_energy_recovery = 15, state = 2, freshness = 24, satiety = 15, thirst = 10),\
#              Food("berry", {"sea": 0, "land": 5, "forest": 20, "beach": 0}, weight = 1, \
#                  item_energy_recovery = 5, state = 2, freshness = 72, satiety = 5, thirst = 10),\
#              Food("potato", {"sea": 0, "land": 15, "forest": 10, "beach": 0}, weight = 1, \
#                  item_energy_recovery = 10, state = 1, freshness = 120, satiety = 10, thirst = -5),\
#              Food("grilled potato", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 1, \
#                  item_energy_recovery = 10, state = 2, freshness = 72, satiety = 10, thirst = -10),\
#              Food("raw venison", {"sea": 0, "land": 5, "forest": 10, "beach": 0}, weight = 5, \
#                  item_energy_recovery = 20, state = 1, freshness = 36, satiety = 80, thirst = 50),\
#              Food("grilled venison", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 5, \
#                  item_energy_recovery = 30, state = 2, freshness = 48, satiety = 80, thirst = 20),\
#              Food("vegetable soup", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 5, \
#                  item_energy_recovery = 30, state = 2, freshness = 36, satiety = 30, thirst = 50),\
#              Food("stew", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 10, \
#                  item_energy_recovery = 50, state = 2, freshness = 36, satiety = 100, thirst = 30)\
# Please note that in the state, 0 means unusable, 1 means raw, 2 means edible, and 3 means rotten. Please analyze the category according to the actual situation of the generated items. Generate items in dictionary form'
prompt = "Generate a food please."

GptWarpper = Gpt3("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")

print(GptWarpper.inquiry(prompt, systemRole, 1))