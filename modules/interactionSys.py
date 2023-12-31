import openai
import copy
import time
import Levenshtein
from status_record import *
from Pre_definedContent import *

class IOSys():
    def __init__(self) -> None:
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
    def __init__(self, gptAPI: Gpt3, playerStatus: Player_status, mapInfo: Map_information, \
        OuterData: IOSys) -> None:
        self.__gptAPI = gptAPI
        self.__OuterData = OuterData
        self.__playerStatus = playerStatus
        self.__mapInfo = mapInfo
        self.__locationDiscriptionSysRole = """You are writing a description about current location \
player is at for a text-based adventure game program, you will receive a game details from game \
program like this "{Current location: End Of Road, Front: brick building, Back: Forest, \
Right hand side: Forest, Left hand side: Forest, Landscape Features: [flat ground, small stream], \
Items: [keyA, keyB, keyC]}". You should write a description in this style: "

End Of Road

You are standing at the end of a road before a small brick building. Around you is a forest. A small stream flows out of the building and down a gully. 
There are some keys on the ground here." """
        
    
    def locationDescription(self, locationList: dict[str, Location]):
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
        print(gpt_response)
        self.__OuterData.inquery_response_log_recorder(self.__locationDiscriptionSysRole, inquiry, gpt_response)
    
    
    
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
            for commands in action.command_executed:
                commands[0](*commands[1])
        else:
            print("Nothing happen...")
    
        
