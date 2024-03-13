from sample import Gpt3
import time

def inquery_response_log_recorder(systemRole:str, inquiry:str, response:str, model:str) -> None:
    f3 = open('log.txt', 'a')
    f3.write("[" + str(time.asctime(time.localtime(time.time()))) +"]\n" \
        +"systemRole: \n" + systemRole + "\n\ninquiry: \n" + inquiry + \
        "\n\nresponse by "+ model +": \n" + response\
        + "\n////////////////////////////////////////////////////\n")
    f3.close()
# systemRole = "You are writting the description about 'description_target' for a survival text-based adventure game based on game information given" #put your test system config here, which is use to tell gpt about \
    #context and define the style of response
systemRole = "You are writting the description about 'description_target' for a survival \
text-based adventure game based on game information given"
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
prompt = "{'player_current_action': 'monitor all', 'player_equipment': 'none', 'NPCs': [{'NPC_name': 'wolf', 'NPC_id': 'wolf_1', 'NPC_category': 'animal', 'current_action': 'monitor player', 'equipment': ['buckteeth', 'claws'], 'relationship_with_player': 'cautious, on guard'}], 'information_need_to_be_described': {'player_action_result': 'none', 'wolf_1_action_result': 'none', 'description_target': ['player_current_action', 'player_equipment', \"NPCs in player's view\", 'wolf_1_action_result', 'player_action_result']}}" # put your test prompt here

GptWarpper = Gpt3("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", systemRole, "")
result = GptWarpper.inquiry(prompt)
print(result) # gpt response will be printed here
inquery_response_log_recorder(systemRole, prompt, result, "ft:gpt-3.5-turbo-0125:3rdprojectgroup:generaltest3:91haHqhT")