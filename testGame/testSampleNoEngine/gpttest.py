from sample import Gpt3

systemRole = "You are writting the description about 'description_target' for a survival text-based adventure game based on game information given" #put your test system config here, which is use to tell gpt about \
    #context and define the style of response

prompt = "{'player_information': {'HP': '90/100', 'action_point': '40/100', 'player_current_status': 'normal', 'thirst_satisfied': '70/100', 'package_weight': '19/30', 'player_current_action': 'none', 'cash': 50, 'transportation': []}, 'environment_information': {'Current location': 'mountain', 'Front': 'beach', 'Back': 'highland snowfield', 'Right hand side': 'mountain', 'Left hand side': 'mountain'}, 'information_need_to_be_described': {'description_target': ['environment_information']}}" # put your test prompt here

GptWarpper = Gpt3("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", systemRole, "")

print(GptWarpper.inquiry(prompt)) # gpt response will be printed here
