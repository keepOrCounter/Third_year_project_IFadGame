from status_record import Player_status, Map_information, EventsTriggered, globalInfo
from PCGsys import PCGController
from interactionSys import OutputGenerator, InputTranslator, Gpt3
from Pre_definedContent import DefininedSys, Commands, character_effectSys
import sys

# from status_record import Location
class rule_system():
    def __init__(self, player : Player_status, map_info: Map_information, worldStatus: globalInfo, \
        defininedContent: DefininedSys, buffEffect: character_effectSys) -> None:
        self.__player = player
        self.__map_info = map_info
        self.__worldStatus = worldStatus
        self.__defininedContent = defininedContent
        self.__buffEffect = buffEffect
        
    def buff_triggered(self):
        buffDict = self.__defininedContent.get_buff()
        for x in buffDict.keys():
            if buffDict[x].trigerred_Condition(self.__player, self.__map_info, self.__worldStatus):
                self.__buffEffect.add_buff(buffDict[x], buffDict[x].start_level)
            elif buffDict[x].end_Condition(self.__player, self.__map_info, self.__worldStatus):
                self.__buffEffect.remove_buff(buffDict[x].buff_name)
        
    def buffHandler(self):
        self.buff_triggered()
        buffs = self.__player.get_buffs()
        counter = 0
        buffName = buffs.keys()
        while counter < len(buffName):
            # dynamic_exe_args = [buffs[buffName[counter]].buff_name, buffs[buffName[counter]].timeLimit, buffs[buffName[counter]].startedTime]
            # result_exe_args = tuple(dynamic_exe_args + list(buffs[buffName[counter]].exe_args))
            # TODO add end condition
            buffs[buffName[counter]].exe_function(*buffs[buffName[counter]].exe_args)
            buffs[buffName[counter]].startedTime += 1
            if buffs[buffName[counter]].timeLimit != -1 and \
                buffs[buffName[counter]].startedTime >= buffs[buffName[counter]].timeLimit:
                # result_end_args = tuple(dynamic_exe_args + list(buffs[buffName[counter]].end_args))
                
                buffs[buffName[counter]].end_Function(*buffs[buffName[counter]].end_args)
                buffs.pop(buffName[counter])
                # counter -= 1
            counter += 1
        
    def naturalChange(self):
        freshnessList = self.__worldStatus.freshNessChangedItems
        for x in freshnessList:
            x.freshness -= 1
        AP_change = self.__worldStatus.naturalAP_reduce
        thirst_change = self.__worldStatus.naturalThirst_reduce
        
        self.__player.set_action_point(self.__player.get_action_point() - AP_change)
        self.__player.set_thirst(self.__player.get_thirst() - thirst_change)
        
    def eachTurn_handler(self):
        """Need to be called each turn
        """
        self.buffHandler()
        self.naturalChange()
        # self.__worldStatus.current_description = dict()
        
        if not self.player_active():
            self.__player.set_hp(self.__player.get_hp() + self.__player.get_action_point())
            self.__player.set_action_point(0)
        if not self.player_alive():
            print("Game over.")
            sys.exit(0)
        if not self.player_thirst():
            
            self.__player.set_thirst(0)
        
        if self.__map_info.currentLocation != None:
            currentPlace = self.__map_info.currentLocation.location_name
            if self.__worldStatus.lastPlace != None:
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
        
    def turnInfoClear(self):
        self.__worldStatus.player_dangerAction = dict()
        self.__worldStatus.NPC_action_toPlayer = dict()
        
    def player_alive(self):
        return self.__player.get_hp() > 0
    
    def player_active(self):
        return self.__player.get_action_point() > 0
    
    def player_thirst(self):
        return self.__player.get_thirst() > 0
    
    def debug_information(self):
        print("current_location:", self.__player.get_currentLocation())
        print("last_location:", self.__player.get_lastLocation())
        print("current Action_point:", self.__player.get_action_point())
        print("current maximum action_point:", self.__player.get_maximum_action_point())
        print("current thirst:", self.__player.get_thirst())
        print("current maximum thirst:", self.__player.get_maximum_thirst())
        if self.__player.get_currentAction() != None:
            print("Current action:", self.__player.get_currentAction().actionName)
        else:
            print("Current action:", None)
        print("visited place:", self.__map_info.get_visitedPlace())
        print("player hp:", self.__player.get_hp())
        print("--------------------------------------")
    
    # def 

if __name__ == "__main__":
    worldStatus = globalInfo()
    player_info = Player_status(action_point = 30)
    # player_info = Player_status()
    map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
    # mapPCG = MapGenerator(player_info, map_record)
    defined_command = Commands(player_info, map_record, worldStatus)
    buffEffect = character_effectSys(player_info, defined_command, worldStatus)
    game_content = DefininedSys(defined_command, map_record, buffEffect)
    # objectPCG = objectsGenerator(game_content)
    # event_Engage = eventGenerator(game_content)
    
    user_input = input("To start the game, please provide an openai key>>>")
    gpt = Gpt3(user_input)
    descriptionGenerator = OutputGenerator(gpt, player_info, map_record, worldStatus)
    inputAdapter = InputTranslator(gpt, player_info, map_record, game_content)
    eventHandler = EventsTriggered()
    
    pcgSystem = PCGController(game_content, player_info, map_record, descriptionGenerator, eventHandler, worldStatus)
    
    game_rule = rule_system(player_info, map_record, worldStatus, game_content)
    
    begin = True
    while begin:
        if not worldStatus.skipTurn:
            game_rule.eachTurn_handler()
            game_rule.debug_information()
            pcgSystem.locationPCG_each_turn()
            game_rule.turnInfoClear()
        else:
            worldStatus.skipTurn = False
        # print(map_record.get_currentMap())

        # print(map_record.currentLocation.description)
        user_input = input("What would you do?>>>")
        if user_input == "__exit":
            begin = False
        else:
            # inputAdapter.command_translator(user_input)
            inputAdapter.tem_translater()