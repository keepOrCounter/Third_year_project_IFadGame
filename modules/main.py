from status_record import Player_status, Map_information
from PCGsys import PCGController
from interactionSys import OutputGenerator, InputTranslator, Gpt3
from Pre_definedContent import DefininedSys, Commands
import sys

# from status_record import Location
class rule_system():
    def __init__(self, player : Player_status, map_info: Map_information) -> None:
        self.__player = player
        self.__map_info = map_info
        
    def eachTurn_handler(self):
        if not self.player_alive():
            print("Game over.")
            sys.exit(0)
        if self.player_active():
            pass
        
    def player_alive(self):
        return self.__player.get_hp() > 0
    
    def player_active(self):
        return self.__player.get_action_point() > 0
    
    
    # def 

if __name__ == "__main__":
    player_info = Player_status(action_point = 30)
    map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
    # mapPCG = MapGenerator(player_info, map_record)
    defined_command = Commands(player_info, map_record)
    game_content = DefininedSys(defined_command)
    # objectPCG = objectsGenerator(game_content)
    # event_Engage = eventGenerator(game_content)
    
    user_input = input("To start the game, please provide a openai key>>>")
    gpt = Gpt3(user_input)
    descriptionGenerator = OutputGenerator(gpt, player_info, map_record)
    inputAdapter = InputTranslator(gpt, player_info, map_record, game_content)
    
    pcgSystem = PCGController(game_content, player_info, map_record, descriptionGenerator)
    
    
    
    begin = True
    while begin:
        print(player_info.get_currentLocation())
        pcgSystem.locationPCG_each_turn()
        print(map_record.get_currentMap())

        # print(map_record.currentLocation.description)
        user_input = input("What would you do?>>>")
        if user_input == "__exit":
            begin = False
        else:
            inputAdapter.command_translator(user_input)