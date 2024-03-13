import json

def convert_to_jsonl(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    with open(output_file, 'w') as f:
        for item in range(0, len(data), 2):
            # system_role = item.get('system_role', '')
            system_role = "You are writting the description about 'description_target' for a survival \
text-based adventure game based on game information given"
            table = {"player_or_other_NPC": 
                        {
                            "HP": 
                            {
                                "100%": "no hurt",
                                "80%-99%": "little hurt",
                                "41%-79%": "moderate hurt",
                                "1%-40%": "intense hurt"
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
                                "0-2": "light",
                                "3-10": "moderate",
                                "11-15": "a little bit heavy",
                                "16-20": "heavy"
                            },
                            "action_AP_cost":
                            {
                                "1 time": "normal",
                                "1.2 times": "a little bit strenuous",
                                "1.5 times": "strenuous",
                                "2 times": "extremely strenuous"
                            },
                            "relationship":
                            {
                                "<-10": "hostile",
                                "-10-(-1)": "cautious, on guard",
                                "0-10": "strange, not interested in",
                                "10-20": "friendly",
                                ">20": "acquainted"
                            }
                        },
                        "items":
                        {
                            "weight":
                            {
                                "1": "light/small",
                                "2": "moderate",
                                ">2": "heavy/large"
                            },
                            "AP_recovery":
                            {
                                "1-10": "insufficient portions",
                                "11-20": "moderate",
                                ">20": "quite a filler"
                            },
                            "freshness": 
                            {
                                "<=0": "stale",
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
                                "2-3 times": "hard to travel through",
                                ">3 times": "extremely hard to travel through"
                            }
                        },
                        "action":
                        {
                            "attack":
                            {
                                "0 hp": "no effect",
                                "1-5 hp": "light damage",
                                "6-20 hp": "moderate damage",
                                ">20 hp": "intense damage"
                            }
                        }
                    }
            user_role = data[item]
            assistant_role = data[item + 1]
            
            # Creating the JSONL format
            json_line = {
                "messages": [
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": str(user_role)},
                    {"role": "assistant", "content": str(assistant_role)}
                ]
            }
            
            # Writing each JSONL line to the file
            f.write(json.dumps(json_line) + '\n')

# Replace 'input.json' and 'output.jsonl' with your file names
convert_to_jsonl('backup.json', 'output.jsonl')
