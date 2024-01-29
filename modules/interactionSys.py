import openai
import copy
import time
import Levenshtein
from status_record import *
from Pre_definedContent import *
import json

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

    def inquiry(self, prompt:str, systemRole: str) -> str:
        # Generate a response
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
        messages=[
        {"role": "system", "content": systemRole},
        {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    
class OutputGenerator():
    def __init__(self, gptAPI: Gpt3, playerStatus: Player_status, mapInfo: Map_information) -> None:
        self.__gptAPI = gptAPI
        self.__OuterData = IOSys()
        self.__playerStatus = playerStatus
        self.__mapInfo = mapInfo
        self.__locationDiscriptionSysRole = """You are writing a description about current location player is at for a text-based adventure game program, you will receive a game details from game program like this: 
{
	"Current location": "End Of Road", 
	"Front": "brick building", 
	"Back": "Forest", 
	"Right hand side": "Forest", 
	"Left hand side": "Forest", 
	"Landscape Features": "[small stream]", 
	"Items": "[keyA, keyB, keyC]"
} 
And the expected result would be: 
{
	"location name": "End Of Road",
	"Description of current and surrounding locations": "You are standing at the end of a road before a small brick building. Around you is a forest.",
	"Landscape Features description": "A small stream flows out of the building and down a gully.", 
	"Items description": "There are some keys on the ground."
} """

        self.__eventDiscriptionSysRole = """You are creating a event for a text-based adventure game, you should create an event name and refine the location description that triggers when the event occurs. Ensure the modified description aligns seamlessly with the current in-game circumstances, drawing on relevant game information. Use the following format: based on game information in following form:
{
	"event_name": <event name here>,
	"Description_of_locations": <Description of current and surrounding locations>, 
	"Landscape_description": <Description of any Landscape Features in original description>, 
	"Items_description": <Description of any items in original description>,
	"event_discription": <Additional description due to the event>
}, Here is an example:
	game information:
	{
		"event type": "survival crisis",
		"triggered reason": "low action point",
		"Current location": "End Of Road",
		"Current action": "moving",
		"Tool(s) assist with moving": [],
		"player current status": "normal",
		"Description of current and surrounding locations": "You are standing at the end of a road before a small brick building. Around you is a forest.",
		"Landscape Features description": "A small stream flows out of the building and down a gully.", 
		"Items description": "There are some keys on the ground here."
	}
	
	expected result:
	{
		"event_name": "starting to feel tired",
		"Description_of_locations": "You are standing at the end of a road before a small brick building. Around you is a forest.",
		"Landscape_description": "A small stream flows out of the building and down a gully.", 
		"Items_description": "There are some keys on the ground here."
		"event_discription": "You feel a weariness settling in, your steps heavier than before. The journey has taken its toll on you."
	}"""
        
    
    def locationDescription(self, locationList: dict[str, Location]) -> None:
        # TODO change function make it allowed for structured description
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
        print(inquiry)
        print("=======================================\n")
        gpt_response = self.__gptAPI.inquiry(inquiry, self.__locationDiscriptionSysRole)
        # print(gpt_response)
        self.__OuterData.inquery_response_log_recorder(self.__locationDiscriptionSysRole, inquiry, gpt_response)
        
        result = json.loads(gpt_response, strict=False)
        
        locationList["Current location"].description = result
    
    
    def eventDescription(self, event: Events) -> dict[str]:
        # TODO change the eventDescription to make it description all current events
        inputDictionary = {"event type": event.eventType, "triggered reason": event.triggered_reason, \
            "Current location": event.current_location, "Current action": event.currentAction, \
                "Tool(s) assist with moving": event.moving_tool, "player current status": event.play_current_status, \
                    "description needed to be modified": event.description}
        
        inquiry = str(inputDictionary)
        print(inquiry)
        print("=======================================\n")
        gpt_response = self.__gptAPI.inquiry(inquiry, self.__eventDiscriptionSysRole)
        # print(gpt_response)
        self.__OuterData.inquery_response_log_recorder(self.__eventDiscriptionSysRole, inquiry, gpt_response)
        
        result = json.loads(gpt_response, strict=False)

        # Extract the value of the "event_name" key and "event_description" key
        # result = {"event_name": str(data.get("event_name")), "event_description": str(data.get("event_description"))}


        return result
    
class InputTranslator():
    def __init__(self, gptAPI: Gpt3, playerStatus: Player_status, mapInfo: Map_information, \
        defined_content: DefininedSys) -> None:
        self.__gptAPI = gptAPI
        self.__playerStatus = playerStatus
        self.__mapInfo = mapInfo
        self.__defined_content = defined_content
        
    def command_translator(self, user_input:str):
        move_commands = list(self.__defined_content.get_Actions().keys())
        move_commands.append("<Rejected>")
        systemRole = "You are trying to translate the command in natual language \
from player to the command of text-based adventure game \
system, the game command are listed below: " + str(move_commands[:-1]) + "\nPlease do \
not reply something more than the command given above(Even if punctuation mark). If the player command is less likely to \
be any of the game command above, just reply a '<Rejected>'."
        
        command = self.__gptAPI.inquiry(user_input, systemRole)
        
        dis = Levenshtein.distance(move_commands[0], command)
        target = 0
        for x in range(1, len(move_commands)):
            tem_dis = Levenshtein.distance(move_commands[x], command)
            if tem_dis < dis:
                target = x
                dis = tem_dis
        if move_commands[target] != "<Rejected>":
            action = self.__defined_content.get_Actions()[move_commands[target]]
            self.__playerStatus.set_currentAction(action)
            for commands in action.command_executed:
                commands[0](*commands[1])
        else:
            print("Nothing happen...")
    
        
