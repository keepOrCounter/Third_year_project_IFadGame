from status_record import Player_status, Map_information, EventsTriggered, globalInfo
from PCGsys import PCGController
from interactionSys import OutputGenerator, InputTranslator, Gpt3
from Pre_definedContent import DefininedSys, Commands
import sys

# from status_record import Location
class rule_system():
    def __init__(self, player : Player_status, map_info: Map_information, worldStatus: globalInfo, \
        defininedContent: DefininedSys) -> None:
        self.__player = player
        self.__map_info = map_info
        self.__worldStatus = worldStatus
        self.__defininedContent = defininedContent
        
    def buffHandler(self):
        buffs = self.__player.get_buffs()
        counter = 0
        buffName = buffs.keys()
        while counter < len(buffName):
            # dynamic_exe_args = [buffs[buffName[counter]].buff_name, buffs[buffName[counter]].timeLimit, buffs[buffName[counter]].startedTime]
            # result_exe_args = tuple(dynamic_exe_args + list(buffs[buffName[counter]].exe_args))
            
            buffs[buffName[counter]].exe_function(*buffs[buffName[counter]].exe_args)
            buffs[buffName[counter]].startedTime += 1
            if buffs[buffName[counter]].timeLimit != -1 and \
                buffs[buffName[counter]].startedTime >= buffs[buffName[counter]].timeLimit:
                # result_end_args = tuple(dynamic_exe_args + list(buffs[buffName[counter]].end_args))
                
                buffs[buffName[counter]].end_Function(*buffs[buffName[counter]].end_args)
                buffs.pop(buffName[counter])
                # counter -= 1
            counter += 1
        
    def eachTurn_handler(self):
        """Need to be called each turn
        """
        self.buffHandler()
        if not self.player_active():
            self.__player.set_hp(self.__player.get_hp() + self.__player.get_action_point())
            self.__player.set_action_point(0)
        if not self.player_alive():
            print("Game over.")
            sys.exit(0)
            
        currentPlace = self.__map_info.currentLocation.location_name
        terrainDict = self.__defininedContent.get_terrain_type()
        mdLevelGradient = terrainDict[currentPlace].move_dLevel/ \
            terrainDict[self.__worldStatus.lastPlace].move_dLevel
            
        self.__worldStatus.move_dLevel *= mdLevelGradient
        self.__worldStatus.lastPlace = currentPlace
            
        if self.__map_info.get_current_area_type() == 1:
            # self.__worldStatus.move_APCost = 5
            pass
        elif self.__map_info.get_current_area_type() == 0:
            if False:
                pass
            else:
                # self.__worldStatus.move_APCost = 20 # determine the action point cost of each move
                pass
        
    def player_alive(self):
        return self.__player.get_hp() > 0
    
    def player_active(self):
        return self.__player.get_action_point() > 0
    
    def debug_information(self):
        print("current_location:", self.__player.get_currentLocation())
        print("last_location:", self.__player.get_lastLocation())
        print("current Action_point:", self.__player.get_action_point())
        print("current maximum action_point:", self.__player.get_maximum_action_point())
        print("Current action:", self.__player.get_currentAction())
        print("visited place:", self.__map_info.get_visitedPlace())
        print("player hp:", self.__player.get_hp())
    
    # def 

if __name__ == "__main__":
    worldStatus = globalInfo()
    # player_info = Player_status(action_point = 30)
    player_info = Player_status()
    map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
    # mapPCG = MapGenerator(player_info, map_record)
    defined_command = Commands(player_info, map_record, worldStatus)
    game_content = DefininedSys(defined_command, map_record)
    # objectPCG = objectsGenerator(game_content)
    # event_Engage = eventGenerator(game_content)
    
    user_input = input("To start the game, please provide an openai key>>>")
    gpt = Gpt3(user_input)
    descriptionGenerator = OutputGenerator(gpt, player_info, map_record)
    inputAdapter = InputTranslator(gpt, player_info, map_record, game_content)
    eventHandler = EventsTriggered()
    
    pcgSystem = PCGController(game_content, player_info, map_record, descriptionGenerator, eventHandler, worldStatus)
    
    game_rule = rule_system(player_info, map_record, worldStatus)
    
    begin = True
    while begin:
        game_rule.eachTurn_handler()
        # game_rule.debug_information()
        pcgSystem.locationPCG_each_turn()
        # print(map_record.get_currentMap())

        # print(map_record.currentLocation.description)
        user_input = input("What would you do?>>>")
        if user_input == "__exit":
            begin = False
        else:
            inputAdapter.command_translator(user_input)