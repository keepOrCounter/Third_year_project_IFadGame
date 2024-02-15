from sample import Gpt3

systemRole = "You are an item generator for an RPG game and need to generate items according to the input format and requirements. Please note that the production of items must be logical."

prompt = 'Please generate a new item similar to the following format:\
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 1, \
            item_energy_recovery = 15, state = 2, freshness = 72, satiety = 30, thirst = -20), \
            Food("raw fish", {"sea": 18, "land": 0, "forest": 0, "beach": 10}, weight = 2, \
            item_energy_recovery = 5, state = 1, freshness = 24, satiety = 15, thirst = 20),\
            Food("grilled fish", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 2, \
                 item_energy_recovery = 15, state = 2, freshness = 24, satiety = 15, thirst = 10), \
             Food("berry", {"sea": 0, "land": 5, "forest": 20, "beach": 0}, weight = 1, \
                 item_energy_recovery = 5, state = 2, freshness = 72, satiety = 5, thirst = 10), \
             Food("potato", {"sea": 0, "land": 15, "forest": 10, "beach": 0}, weight = 1, \
                 item_energy_recovery = 10, state = 1, freshness = 120, satiety = 10, thirst = -5), \
             Food("grilled potato", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 1, \
                 item_energy_recovery = 10, state = 2, freshness = 72, satiety = 10, thirst = -10), \
             Food("raw venison", {"sea": 0, "land": 5, "forest": 10, "beach": 0}, weight = 5, \
                 item_energy_recovery = 20, state = 1, freshness = 36, satiety = 80, thirst = 50), \
             Food("grilled venison", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 5, \
                 item_energy_recovery = 30, state = 2, freshness = 48, satiety = 80, thirst = 20), \
             Food("vegetable soup", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 5, \
                 item_energy_recovery = 30, state = 2, freshness = 36, satiety = 30, thirst = 50), \
             Food("stew", {"sea": 0, "land": 0, "forest": 0, "beach": 0}, weight = 10, \
                 item_energy_recovery = 50, state = 2, freshness = 36, satiety = 100, thirst = 30) \
Please note that in the state, 0 means unusable, 1 means raw, 2 means edible, and 3 means rotten. Please analyze the category according to the actual situation of the generated items.'

GptWarpper = Gpt3("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", systemRole, "")

print(GptWarpper.inquiry(prompt))