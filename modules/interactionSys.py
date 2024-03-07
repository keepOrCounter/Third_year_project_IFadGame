import openai
# import copy
import time
import Levenshtein
from status_record import *
from Pre_definedContent import *
import json
from autocorrect import Speller
from numpy import inf
import inspect

class IOSys():
    def __init__(self) -> None:
        """
        This class is just a log system for debugging
        """
        pass
    
    def inquery_response_log_recorder(self,systemRole:str, inquiry:str, response:str) -> None:
        f3 = open('log.txt', 'a')
        f3.write("[" + str(time.asctime(time.localtime(time.time()))) +"]\n" \
            +"systemRole: \n" + systemRole + "\n\ninquiry: \n" + inquiry + \
            "\n\nresponse by gpt3.5-turbo: \n" + response\
            + "\n////////////////////////////////////////////////////\n")
        f3.close()

class Gpt3():
    def __init__(self, api_key) -> None:
        # Set up the OpenAI API client
        openai.api_key = api_key

    def inquiry(self, prompt:str, systemRole: str, temperature = 0.5) -> str:
        # Generate a response
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
        messages=[
        {"role": "system", "content": systemRole},
        {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    
class OutputGenerator():
    def __init__(self, gptAPI: Gpt3, playerStatus: Player_status, mapInfo: Map_information, \
        worldStatus: globalInfo) -> None:
        self.__gptAPI = gptAPI
        self.__OuterData = IOSys()
        self.__playerStatus = playerStatus
        self.__mapInfo = mapInfo
        self.__worldStatus = worldStatus
        self.__locationDiscriptionSysRole = """You are writing a description about current location \
player is at for a text-based adventure game program, you will receive a game details from game \
program like this "{Current location: End Of Road, Front: brick building, Back: Forest, \
Right hand side: Forest, Left hand side: Forest, Landscape Features: [small stream], \
Items: [keyA, keyB, keyC]}". Here is the example of expected result: "
End Of Road
You are standing at the end of a road before a small brick building. Around you is a forest. A small stream flows out of the building and down a gully. 
There are some keys on the ground here." """

        self.__eventDescriptionSysRole = """You are creating a event for a text-based adventure game, you should create event in following form based on game information(Mainly the triggered reason) provided in later:
{
	"event_name": <event name here>,
	"event_discription": <possible discription in third person and first person view>
}, Here is an example:
	game information:
	{
		"event type": "survival crisis",
		"triggered reason": "low action point",
		"Current location": "End Of Road",
		"Current action": "moving",
		"Tool(s) assist with moving": [],
		"player current status": "Normal",
		"description needed to be modified": "
End Of Road
You are standing at the end of a road before a small brick building. Around you is a forest. A small stream flows out of the building and down a gully. 
There are some keys on the ground here."
	}
	
	expected result:
	{
		"event_name": "starting feeling tired",
		"event_description": "
End Of Road
You stand at the end of a road before a small brick building. The dense forest surrounds you, its looming trees casting shadows. A weary sensation seeps through your limbs, accentuating the fatigue in your bones. A small stream trickles from the building, and amidst the weariness, you notice a glint—keys scattered on the ground, waiting to be claimed."
	}"""
        
        self.__eventDevelopmentSysRole = """You are determine the development of an event in a text-based adventure game, you should tell the program the development in following form of event based on (Mainly based on the triggered reason and player information) the game information provided later:
{
	"successful": <true if succeed, false if not>,
	"fail": <true if failed, false if not>,
	"reward": <select the indices of zero or more of reward like a python list (You may make this with an empty list if you decide to choose no reward) from possible reward list in game information provided based on player action in game information>, 
	"penalty": <select the indices of zero or more of penalty like a python list (You may make this with an empty list if you decide to choose no penalty) from possible penalty list in game information provided based on player action in game information>,
	"development description": <A description to tell how the event developed, please describe implicitly like following example>
}, Here is an example(the event is not necessary be succeed or failed immediately, it won't failed as long as in the time limit, we will tell you if times up), the following example has select a penalty which is the third one in "possible penalty":
	game information:
	{
		"event_name": "Venomous Encounter",
		"event type": "poisoning potential",
		"triggered reason": "attacked by snake",
		"player current status": "normal",
		"player action": "suck the attcked part",
		"times up": False,
		"possible reward": ["increase maximum hp", "increase maximum action point", "obtain a poison"],
		"possible penalty": ["decrease hp", "decrease action point", "add poisoning status"],
		"event description": "You find yourself deep in the wilderness, navigating through dense foliage and treacherous terrain. Suddenly, without warning, a venomous snake lunges at you, its fangs sinking into your flesh."
	}
	
	expected result:
	{
		"successful": false,
		"fail": false,
		"reward": [], 
		"penalty": [2],
		"development description": "You decide to suck the wound, hoping to extract the poison. Unfortunately, your efforts prove in vain. The venom takes hold. Nausea and weakness grip you, making the journey ahead more challenging."
}"""
    
        self.__foodGenerateSystemRole = """You are an item generator for an RPG game and need to generate some food according to the json format and following requirements. Here is the reqirement form:
{
	"name": <name of the food>,
	"category": "food",
	"appear_possibility": <the possibility of this food can be picked up(if the food is human processed, please set all the possibility into 0 or 1 like the bread in following examples): sea, land, forest and beach, in dictionary form, each possibility is between 0-20>,
	"weight": <The weight of the food, player can take totally 20 units weight items>,
	"AP_recovery": <how many action point player can recovery after eat this food>,
	"edible": <true or false, whether food is edible, the food like "rotten apple" or "raw kidney bean" are not edible>,
	"freshness": <How many turns the food can be store in general case>,
	"thirst_satisfied": <the sense of thirst player will change after eat this food>
}
Please note that the production of food must be logical. Here are some expected results:
{
	"name": "apple",
	"category": "food",
	"appear_possibility": {"sea": 0, "land": 1, "forest": 10, "beach": 0},
	"weight": 2,
	"AP_recovery": 5,
	"edible": true,
	"freshness": 72,
	"thirst_satisfied": 5
},
{
	"name": "bread",
	"category": "food",
	"appear_possibility": {"sea": 0, "land": 0, "forest": 0, "beach": 0},
	"weight": 1,
	"AP_recovery": 25,
	"edible": true,
	"freshness": 50,
	"thirst_satisfied": -10
}"""
    
        self.__generalized_promt = """You are writing the game description for a text-based adventure game program, you will receive a game details from game program like this in form of json:
{
	"player_information":{
		"HP": "100/100",
		"AP": "100/100",
		"player_current_status": "normal",
		"thirst_satisfied": "90/100",
		"player_current_action": "consumed 2 bread",
	},
	"environment_information": {
		"Current location": "End Of Road",
		"Front": "brick building",
		"Back": "Forest",
		"Right hand side": "Forest",
		"Left hand side": "Forest",
		"Landscape Features": ["small stream"],
		"Items": ["keyA", "keyB", "keyC"]
	}
	"information_need_to_be_desctipt": {
		"player_current_action": "have 2 bread",
		"used/comsumed_items/consumable_detial":{
			"items_name": ["bread", "bread"],
			"weight": [1, 1],
			"AP_recovery": [15, 15],
			"freshness": [-5, -30],
			"eatable": [false, false],
			"thirst_satisfied": [-20, -20]
		}
		"description_target": "player current feeling"
	}
}, you need to write the description for "description_target" with the details in "information_need_to_be_desctipt" and the basic information given in other two keys. Please note that all the information should only be implicit in natural language(i.e. no explicit game value or number appear in output) Here is the expected result according to above example:
{
	"title_of_description": "comsumed uneatable bread",
	"description": "You are trying to have two slices of stale bread. The bread is dry and hard, its texture reminiscent of chewing on ancient parchment. Its taste is a blend of mustiness and decay, assaulting your palate with a bitter, stale flavor that lingers uncomfortably on your tongue. Your stomach churns uncomfortably, protesting against the foreign and indigestible substance. "
}""" # TODO improve this prompt
    
    def locationDescription(self, locationList: dict[str, Location]) -> None:
        """
        Args:
            `locationList (dict[str, Location])`: {current: <Location>, Front: \
                <Location>, Back: <Location>, Right hand side: <Location>, \
                    Left hand side: <Location>}
        """
        inputDictionary = {"Current location": locationList["Current location"].location_name, \
            "Front": locationList["Front"].location_name, "Back": locationList["Back"].location_name,\
                "Right hand side": locationList["Right hand side"].location_name, \
                    "Left hand side": locationList["Left hand side"].location_name}
        for current_object in locationList["Current location"].objects:
            if current_object.category not in inputDictionary.keys():
                inputDictionary[current_object.category] = [current_object.item_name]
            else:
                inputDictionary[current_object.category].append(current_object.item_name)
        
        inquiry = str(inputDictionary)
        # print(inquiry)
        # print("=======================================\n")
        gpt_response = self.__gptAPI.inquiry(inquiry, self.__locationDiscriptionSysRole)
        # print(gpt_response)
        self.__OuterData.inquery_response_log_recorder(self.__locationDiscriptionSysRole, inquiry, gpt_response)
        
        # result = json.loads(gpt_response, strict=False)
        
        locationList["Current location"].description = gpt_response
        
        return gpt_response
    
    
    def eventDescription(self, event: PassivityEvents) -> None:
        inputDictionary = {"event type": event.eventType, "triggered reason": event.triggered_reason, \
            "Current location": event.current_location, "Current action": event.currentAction, \
                "Tool(s) assist with moving": event.moving_tool, "player current status": event.play_current_status, \
                    "description needed to be modified": event.description}
        
        inquiry = str(inputDictionary)
        # print(inquiry)
        # print("=======================================\n")
        gpt_response = self.__gptAPI.inquiry(inquiry, self.__eventDescriptionSysRole)
        # print(gpt_response)
        self.__OuterData.inquery_response_log_recorder(self.__eventDescriptionSysRole, inquiry, gpt_response)
        
        result = json.loads(gpt_response, strict=False)

        # Extract the value of the "event_name" key and "event_description" key
        # result = {"event_name": str(data.get("event_name")), "event_description": str(data.get("event_description"))}
        event.eventName = result["event_name"]
        event.description = result["event_description"]

        return result
        
    def eventDevelopment(self, event: PassivityEvents) -> dict:
        # TODO
        inputDictionary = {"event_name": event.eventName, "event type": event.eventType, \
            "triggered reason": event.triggered_reason, "player current status": event.play_current_status,\
                "player action": event.currentAction, "times up": (event.triggered_time \
                    > event.time_limit and event.time_limit >= 0), \
                    "possible reward": event.possible_reward, "possible penalty": event.possible_penalty, \
                        "event description": event.description
                }
        
        inquiry = str(inputDictionary)
        # print(inquiry)
        # print("=======================================\n")
        gpt_response = self.__gptAPI.inquiry(inquiry, self.__eventDevelopmentSysRole)
        # print(gpt_response)
        self.__OuterData.inquery_response_log_recorder(self.__eventDevelopmentSysRole, inquiry, gpt_response)
        
        result = json.loads(gpt_response, strict=False)

        # print(result)
        return result
    
    def foodGenerate(self) -> Food:
        inquiry = "Please generate a food please."
        gpt_response = self.__gptAPI.inquiry(inquiry, self.__foodGenerateSystemRole)
        self.__OuterData.inquery_response_log_recorder(self.__eventDevelopmentSysRole, inquiry, gpt_response)
        
        result = json.loads(gpt_response, strict=False)
        print("=======================================\n")
        print(result)
        foodGenerated = Food(result["name"], result["appear_possibility"], result["weight"], \
            result["AP_recovery"], result["edible"], result["freshness"], result["thirst_satisfied"])
        
        return foodGenerated
    
    def generalDescription(self, target) -> None:
        """
        Args:
            `locationList (dict[str, Location])`: {current: <Location>, Front: \
                <Location>, Back: <Location>, Right hand side: <Location>, \
                    Left hand side: <Location>}
        """
        inputDictionary = {"player_information": vars(self.__playerStatus), \
            "environment_information": vars(self.__mapInfo.currentLocation), "information_need_to_be_desctipt": 
                vars(target)}
        # for current_object in locationList["Current location"].objects:
        #     if current_object.category not in inputDictionary.keys():
        #         inputDictionary[current_object.category] = [current_object.item_name]
        #     else:
        #         inputDictionary[current_object.category].append(current_object.item_name)
        
        # inquiry = str(inputDictionary)
        # # print(inquiry)
        # print("=======================================\n")
        # gpt_response = self.__gptAPI.inquiry(inquiry, self.__locationDiscriptionSysRole)
        # # print(gpt_response)
        # self.__OuterData.inquery_response_log_recorder(self.__locationDiscriptionSysRole, inquiry, gpt_response)
        
        # # result = json.loads(gpt_response, strict=False)
        
        # locationList["Current location"].description = gpt_response
        
    def text_output(self):
        for x in self.__worldStatus.current_description.keys():
            print(x)
            print(self.__worldStatus.current_description[x])
            
        print("=======================================\n")
        self.__worldStatus.current_description.clear()
    
class InputTranslator():
    def __init__(self, gptAPI: Gpt3, playerStatus: Player_status, mapInfo: Map_information, \
        defined_content: DefininedSys) -> None:
        self.__gptAPI = gptAPI
        self.__playerStatus = playerStatus
        self.__mapInfo = mapInfo
        self.__defined_content = defined_content
        
    def get_function_params_info(self, func):
        func_signature = inspect.signature(func)
        params_info = []
        for param_name, param in func_signature.parameters.items():
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else "No type annotation"
            params_info.append((param_name, param_type))
        return params_info
    
    def tem_translater(self):
        move_commands = list(self.__defined_content.get_Actions().keys())
        for x in range(len(move_commands)):
            print(x, ": ", move_commands[x])
        
        target = int(input(">>>"))
        action = self.__defined_content.get_Actions()[move_commands[target]]
        self.__playerStatus.set_currentAction(action)
        for commands in range(len(action.command_executed)):
            params_info = self.get_function_params_info(action.command_executed[commands])
            print(params_info)
            result = []
            for x in range(1, len(params_info)):
                target = input(str(x)+": ")
                result.append(target)
            action.command_executed[commands](*(action.command_args[commands]+result))

    def frequent_command (common_list:str) -> list:
        frequent_words_in_commands = []
        common_list.pop(-1)

        for i in range(len(common_list)):
            common_words = common_list[i].split()
            for i in range(len(common_words)):
                frequent_words_in_commands.append(common_words[i])

        clear_word_list = list(dict.fromkeys(frequent_words_in_commands))

        return clear_word_list

    def all_case_word_list (word_list:str) -> list:
        all_case_word_list = []

        for i in range(len(word_list)):
            all_case_word_list.append(word_list[i].lower())

        for i in range(len(word_list)):
            all_case_word_list.append(word_list[i].upper())

        return all_case_word_list
        
    def command_translator(self, user_input:str):
        move_commands = list(self.__defined_content.get_Actions().keys())
        move_commands.append("<Rejected>")
        print(move_commands)
        systemRole = "You are trying to translate the command in natual language \
from player to the command of text-based adventure game \
system, the game command are listed below: " + str(move_commands[:-1]) + "\nPlease do \
not reply something more than the command given above(Even if punctuation mark). If the player command is less likely to \
be any of the game command above, just reply a '<Rejected>'."

        clear_word_list_in_move_commands = InputTranslator.frequent_command(move_commands)
        all_case_word_list = InputTranslator.all_case_word_list(clear_word_list_in_move_commands)
        print(clear_word_list_in_move_commands)
        print(all_case_word_list)
        spell = Speller(lang = 'en')

        for i in range(len(all_case_word_list)):
            spell.nlp_data.update({all_case_word_list[i]:inf})

        corrected_user_input = spell(user_input)
        print(corrected_user_input)

        if (corrected_user_input != user_input):
            print("Wait, why I have that mind, is it\"", corrected_user_input, "\"?")
        else:
            command = self.__gptAPI.inquiry(user_input, systemRole)
            print(command)
            
            dis = Levenshtein.distance(move_commands[0], command)
            target = 0
            for x in range(1, len(move_commands)):
                tem_dis = Levenshtein.distance(move_commands[x], command)
                if tem_dis < dis:
                    target = x
                    dis = tem_dis
            print(move_commands[target])
            print(move_commands)
            if move_commands[target] != "<Rejected>":
                action = self.__defined_content.get_Actions()[move_commands[target]]
                self.__playerStatus.set_currentAction(action)
                for commands in range(len(action.command_executed)):
                    action.command_executed[commands](*action.command_args[commands])
                    # commands[0](*commands[1])
            else:
                print("Nothing happen...")
    
        
