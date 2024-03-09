from sample import Gpt3

# systemRole = "You are writting the description about 'description_target' for a survival text-based adventure game based on game information given" #put your test system config here, which is use to tell gpt about \
    #context and define the style of response
systemRole = "You are writting the description about 'description_target' for a survival \
text-based adventure game based on game information given, every numerical attribute should be presented in \
implicit way(different level of perception) unless 'description_target' tell you not to do so, following dictionary show you how to transfer numerical attribute into implicit description: "
table = {"player_or_other_NPC": 
            {
                "HP": 
                {
                    "80%-100%": "little hurt",
                    "41%-79%": "median hurt",
                    "1%-40%": "intense damage"
                },
                "action_point(AP)": 
                {
                    "80%-100%": "normal",
                    "41%-79%": "a little bit tired",
                    "1%-40%": "exhausted"
                },
                "thirst_satisfied":
                {
                    "80%-100%": "normal",
                    "41%-79%": "a little bit thirst",
                    "1%-40%": "extremely thirst"
                },
                "package_weight":
                {
                    "0-10": "normal",
                    "11-15": "a little bit heavy",
                    "16-20": "heavy"
                },
                "action_AP_cost":
                {
                    "1 time": "normal",
                    "1.2 times": "a little bit strenuous",
                    "1.5 times": "strenuous",
                    "2 times": "extremely strenuous"
                }
            },
            "items":
            {
                "weight":
                {
                    "1": "light/small",
                    "2": "normal",
                    ">2": "heavy/large"
                },
                "AP_recovery":
                {
                    "1-10": "not enough/small",
                    "11-20": "normal",
                    ">20": "quite a filler"
                },
                "freshness": 
                {
                    "<=0": "not fresh",
                    ">0": "fresh"
                },
                "thirst_satisfied": 
                {
                    "<=0": "cause a thirst",
                    ">0": "quench a thirst"
                }
            },
            "environment_information":
            {
                "move_AP_cost":
                {
                    "1 time": "normal",
                    "2-4 times": "hard to travel through",
                    ">4 times": "extremely hard to travel through"
                }
            }
        }
prompt = "{'player_information': {'HP': '100/100', 'action_point(AP)': '80/100', 'player_current_status': ['thirst'], 'thirst_satisfied': '30/100', 'package_weight': '0/20', 'player_current_action': 'attack bob by hand', 'action_AP_cost': '1 time(s)', 'cash': 0, 'equipment': 'none', 'suit': 'old shirt', 'transportation_used': []}, 'package': [], 'information_need_to_be_described': {'description_target': ['player_information(except: [player_current_action, cash])', 'cash(explicit)', 'package']}}" # put your test prompt here

GptWarpper = Gpt3("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", systemRole + str(table), "")

print(GptWarpper.inquiry(prompt)) # gpt response will be printed here