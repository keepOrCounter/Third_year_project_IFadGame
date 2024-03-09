import openai
import copy
import time
import Levenshtein

location_names = [
    "Forest Entrance", "Clearing",
    "Riverbank", "Mysterious Cave",
    "Forest Path", "Old Ruins", "Dark Forest",
    "Mountain Base", "Dragon's Lair"
]
interactable_objects = {
    "Forest Entrance": ["Tree Stump", "Wildflowers"],
    "Clearing": ["Campfire", "Backpack"],
    "Riverbank": ["Fishing Rod", "Broken Bridge", "Rocks"],
    "Mysterious Cave": ["Glowing Crystals", "Ancient Inscriptions"],
    "Forest Path": ["Map", "Mushrooms", "Trees"],
    "Old Ruins": ["Crumbling Statues", "Hidden Passage"],
    "Dark Forest": ["Giant Spiderweb", "Mysterious Glowing Eyes"],
    "Mountain Base": ["Climbing Gear", "Campsite"],
    "Dragon's Lair": ["Dragon Egg", "Treasure Chest"]
}
objects_type = {
    "unportable": {
        "Tree Stump", "Campfire", "Fishing Rod", "Broken Bridge",
        "Glowing Crystals", "Ancient Inscriptions", "Map",
        "Crumbling Statues", "Hidden Passage", "Giant Spiderweb", "Mysterious Glowing Eyes",
        "Climbing Gear", "Campsite", "Dragon Egg", "Treasure Chest", "Trees"
    },
    "portable": {
        "Wildflowers", "Backpack", "Mushrooms", "Rocks"
    }
}

move_commands = [
    "Move North", "Move South", "Move East", "Move West", "<Rejected>"
]
# textual_map = {
#     0: ["Forest Entrance", "Clearing"],
#     1: ["Riverbank", "Mysterious Cave"],
#     2: ["Forest Path", "Old Ruins", "Dark Forest"],
#     3: ["Mountain Base", "Dragon's Lair"]
# } # {x_coordinate : [Location_names(whose indices are y cordinate)]}
textual_map = {} # {x_coordinate : [Location_names(whose indices are y cordinate)]}

class Location():
    def __init__(self, location_name:str, x:int, y:int, objects:list = []) -> None:
        self.location_name = location_name
        self.objects = objects
        self.x = x
        self.y = y

class Player_status():
    def __init__(self, currentLocation:list[int,int] = [0,0], items:list[str] = []) -> None:
        self.__currentLocation = currentLocation
        self.items = items
    
    def x_coordinate(self) -> int:
        
        return self.__currentLocation[0]
    
    def y_coordinate(self) -> int:
        
        return self.__currentLocation[1]
    
    def location_adder(self, delta_x:int, delta_y:int) -> None:
        self.__currentLocation[0] += delta_x
        self.__currentLocation[1] += delta_y
class Gpt3():
    def __init__(self, api_key, output_systemRole:str, command_translator_systemRole:str) -> None:
        # Set up the OpenAI API client
        openai.api_key = api_key
        self.output_systemRole = output_systemRole
        self.command_translator_systemRole = command_translator_systemRole

    def inquiry(self, prompt:str) -> str:
        # Generate a response
        response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0125:3rdprojectgroup:generaltest2:90cz1xIx",#gpt-3.5-turbo-0301
        messages=[
        {"role": "system", "content": self.output_systemRole},
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
    
    def command_translator(self, user_command):
        # Generate a response
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
        messages=[
        {"role": "system", "content": self.command_translator_systemRole},
        {"role": "user", "content": user_command}
        ],
        temperature=0.5,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    
class UserInterface():
    def __init__(self, gptAPI:Gpt3) -> None:
        self.gptAPI = gptAPI
    
    def output(self, textual_map: dict[int, list[Location]], objects_type: dict[str, set[str]], \
        current_location: tuple[int,int] = (0,0)):
        map_size = 3 # only for fixed map
        print("current_location", current_location)
        
        current_location_details = textual_map[current_location[0] % map_size][current_location[1] % map_size]
        shortCut_map = ""
        maxLength = 0
        shortCut_locations_list = []
        for y in range(3):
            tem = []
            # print("print(y_coor)", y_coor)
            y_coor = (current_location_details.y + y - 1) % map_size
            # if y_coor >= map_size:
            #     y_coor = y_coor - map_size
            # elif y_coor < 0:
            #     y_coor = y_coor + map_size
            print("y_coor", y_coor)
            for x in range(3):
                # print("print(x_coor)", x_coor)
                x_coor = (current_location_details.x + x - 1) % map_size
                # if x_coor >= map_size:
                #     x_coor = x_coor - map_size
                # elif x_coor < 0:
                #     x_coor = x_coor + map_size
                print("x_coor", x_coor)
                
                maxLength = max(maxLength, len(textual_map[x_coor][y_coor].location_name))
                tem.append(textual_map[x_coor][y_coor].location_name)
                print(tem)
                print(x_coor, y_coor)
                print(current_location_details.x, current_location_details.y)
                print("-------------------------")
            shortCut_locations_list = tem + shortCut_locations_list
        changeLine = 3
        for x in range(1, len(shortCut_locations_list) + 1):
            shortCut_map += "[" + shortCut_locations_list[x - 1] + (" " * (maxLength - len(shortCut_locations_list[x - 1]))) + "]"
            if x != 0 and x != len(shortCut_locations_list) and x % 3 == 0:
                shortCut_map += "\n"
                for y in range(3):
                    shortCut_map += (" " * int(maxLength / 2 + 1)) + "|" + (" " * int(maxLength / 2 + 1 - int(maxLength % 2 == 0)))
                    if y < 2:
                        shortCut_map += "  "
                    else:
                        shortCut_map += "\n"
            elif x == len(shortCut_locations_list):
                pass
            else:
                shortCut_map += "--"
        print(shortCut_map)
        inquiry = "game information(Notice: the place around current location is \
just to make sure that there is not contradiction between your writting and the \
game map, please do not tell player about the place around current location): {\n\
Map(Lines or slashes represent connections between different places):\n" + \
        shortCut_map + "\nCurrent location: " + current_location_details.location_name + \
        "\nObjects at current location(All possible objects and scene in here, \
please don't write something doesn't in this list. For example, if tree is not in \
list, don't tell about tree in description even if the Current location is a forest):" \
    + str(current_location_details.objects) + "}"
        print(inquiry)
        print("=======================================\n")
        gpt_response = self.gptAPI.inquiry(inquiry)
        print(gpt_response)
        self.inquery_response_log_recorder(self.gptAPI.output_systemRole, inquiry, gpt_response)
        
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
        
    def inquery_response_log_recorder(self,systemRole:str, inquiry:str, response:str) -> None:
        f3 = open('log.txt', 'a')
        f3.write("[" + str(time.asctime(time.localtime(time.time()))) +"]\n" \
            +"systemRole: \n" + systemRole + "\n\ninquiry: \n" + inquiry + \
            "\n\nresponse by gpt3.5-turbo: \n" + response\
            + "\n////////////////////////////////////////////////////\n")
        f3.close()


    
def testMapCovertFunction():
    changeLine = pow(len(location_names), 0.5)
    x_coordinate = 0
    textual_map[x_coordinate] = []
    for x in range(1, len(location_names) + 1):
        print(location_names[x - 1], x_coordinate, \
            len(textual_map[x_coordinate]), interactable_objects[location_names[x - 1]])
        textual_map[x_coordinate].append(Location(location_names[x - 1], x_coordinate, \
            len(textual_map[x_coordinate]), interactable_objects[location_names[x - 1]]))

        if x % changeLine == 0:
            x_coordinate += 1
            textual_map[x_coordinate] = []
    del textual_map[x_coordinate]
    
if __name__ == "__main__":
    testMapCovertFunction()
    print(textual_map)
    changeLine = pow(len(location_names), 0.5)
    currentLocation = [int((1+changeLine)/2) - 1, int((1+changeLine)/2) - 1]
    player_current_state = Player_status(currentLocation, [])
    print(currentLocation)
    systemRole = "You are an author of a text-based adventure game, \
and you need to write one short description(Only for current location) \
for player base on game information, here \
is an example:{Map: \n[Forest      ]--[brick building]--[Forest     ]\n\
        |            |               |\n\
[Forest      ]--[End Of Road   ]--[Deep forest]\n\
        |            |               |\n\
[Not Known   ]--[Forest        ]--[Not Known  ]\nCurrent location: End Of Road\nObjects at current location:[stream, keyA, keyB, keyC]} \
According to th example above, you should author the game text in this style: You are standing \
at the end of a road before a small brick building. Around you is a forest. \
A small stream flows out of the building and down a gully. \n\
There are some keys on the ground here."

    translate_system = "You are trying to translate the command in natual language \
from player to the command of text-based adventure game \
system, the game command are listed below(Notice: player always face to north in game, which means forward=north, \
right=east, left=west, south=backward): " + str(move_commands[:-1]) + "\nPlease do \
not reply something more than the command given above(Even if punctuation mark). If the player command is less likely to \
be any of the game command above, just reply a '<Rejected>.'"

    GptWarpper = Gpt3("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", systemRole, translate_system)
    playerSurface = UserInterface(GptWarpper)
    while True:
        playerSurface.output(textual_map, objects_type, (player_current_state.x_coordinate(), \
            player_current_state.y_coordinate()))
        user_input = input("What would you do?>>>")
        playerSurface.command_translator(user_input, player_current_state, move_commands)