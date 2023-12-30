import openai
import copy
import time
import Levenshtein
from status_record import *

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
    def __init__(self) -> None:
        pass
    
    
class UserInterface():
    def __init__(self, gptAPI:Gpt3) -> None:
        self.gptAPI = gptAPI
    
#     def output(self, textual_map: dict[int, list[Location]], objects_type: dict[str, set[str]], \
#         current_location: tuple[int,int] = (0,0)):
#         map_size = 3 # only for fixed map
#         print("current_location", current_location)
        
#         current_location_details = textual_map[current_location[0] % map_size][current_location[1] % map_size]
#         shortCut_map = ""
#         maxLength = 0
#         shortCut_locations_list = []
#         for y in range(3):
#             tem = []
#             # print("print(y_coor)", y_coor)
#             y_coor = (current_location_details.y + y - 1) % map_size
#             # if y_coor >= map_size:
#             #     y_coor = y_coor - map_size
#             # elif y_coor < 0:
#             #     y_coor = y_coor + map_size
#             print("y_coor", y_coor)
#             for x in range(3):
#                 # print("print(x_coor)", x_coor)
#                 x_coor = (current_location_details.x + x - 1) % map_size
#                 # if x_coor >= map_size:
#                 #     x_coor = x_coor - map_size
#                 # elif x_coor < 0:
#                 #     x_coor = x_coor + map_size
#                 print("x_coor", x_coor)
                
#                 maxLength = max(maxLength, len(textual_map[x_coor][y_coor].location_name))
#                 tem.append(textual_map[x_coor][y_coor].location_name)
#                 print(tem)
#                 print(x_coor, y_coor)
#                 print(current_location_details.x, current_location_details.y)
#                 print("-------------------------")
#             shortCut_locations_list = tem + shortCut_locations_list
#         changeLine = 3
#         for x in range(1, len(shortCut_locations_list) + 1):
#             shortCut_map += "[" + shortCut_locations_list[x - 1] + (" " * (maxLength - len(shortCut_locations_list[x - 1]))) + "]"
#             if x != 0 and x != len(shortCut_locations_list) and x % 3 == 0:
#                 shortCut_map += "\n"
#                 for y in range(3):
#                     shortCut_map += (" " * int(maxLength / 2 + 1)) + "|" + (" " * int(maxLength / 2 + 1 - int(maxLength % 2 == 0)))
#                     if y < 2:
#                         shortCut_map += "  "
#                     else:
#                         shortCut_map += "\n"
#             elif x == len(shortCut_locations_list):
#                 pass
#             else:
#                 shortCut_map += "--"
#         print(shortCut_map)
#         inquiry = "game information(Notice: the place around current location is \
# just to make sure that there is not contradiction between your writting and the \
# game map, please do not tell player about the place around current location): {\n\
# Map(Lines or slashes represent connections between different places):\n" + \
#         shortCut_map + "\nCurrent location: " + current_location_details.location_name + \
#         "\nObjects at current location(All possible objects and scene in here, \
# please don't write something doesn't in this list. For example, if tree is not in \
# list, don't tell about tree in description even if the Current location is a forest):" \
#     + str(current_location_details.objects) + "}"
#         print(inquiry)
#         print("=======================================\n")
#         gpt_response = self.gptAPI.inquiry(inquiry)
#         print(gpt_response)
#         self.inquery_response_log_recorder(self.gptAPI.output_systemRole, inquiry, gpt_response)
        
    def command_translator(self, user_input:str, player_status:Player_status, move_commands:list[str]):
        command = self.gptAPI.command_translator(user_input)
        
        dis = Levenshtein.distance(move_commands[0], command)
        target = 0
        for x in range(1, len(move_commands)):
            tem_dis = Levenshtein.distance(move_commands[x], command)
            if tem_dis < dis:
                target = x
                dis = tem_dis
        if move_commands[target] == "Move North":
            player_status.location_adder(0, 1)
        elif move_commands[target] == "Move South":
            player_status.location_adder(0, -1)
        elif move_commands[target] == "Move East":
            player_status.location_adder(1, 0)
        elif move_commands[target] == "Move West":
            player_status.location_adder(-1, 0)
        else:
            print("Nothing happen...")
            
        print(command)
        
