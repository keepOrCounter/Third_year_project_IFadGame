from status_record import Player_status, Map_information, EventsTriggered, globalInfo, \
    Food, Location, LandscapeFeature, Container, Tool, Actions, Weapon
from PCGsys import PCGController
from interactionSys import OutputGenerator, InputTranslator, Gpt3
from Pre_definedContent import DefininedSys, Commands, character_effectSys
import sys
import unittest
import copy

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
    
            


class TestStringMethods(unittest.TestCase):

    def test_move(self):
        worldStatus = copy.deepcopy(globalInfo())
        # player_info = Player_status(action_point = 30)
        player_info = copy.deepcopy(Player_status(action_point = 30))
        map_record = copy.deepcopy(Map_information(current_area_type = 1, map_size=(20, 20))) # land type
        # mapPCG = MapGenerator(player_info, map_record)
        defined_command = Commands(player_info, map_record, worldStatus)
        buffEffect = character_effectSys(player_info, defined_command, worldStatus)
        game_content = DefininedSys(defined_command, map_record, buffEffect)
        action = copy.deepcopy(game_content.get_Actions()["Move"])
        action.command_args[0].append("North")
        defined_command.move(action, "North")
        x, y = player_info.get_currentLocation()
        
        self.assertEqual(worldStatus.move_dLevel, 1.0)
        self.assertEqual(player_info.get_action_point(), 30)
        self.assertEqual(player_info.get_thirst(), 100)
        # # objectPCG = objectsGenerator(game_content)
        # # event_Engage = eventGenerator(game_content)

        # user_input = input("To start the game, please provide an openai key>>>")
        # gpt = Gpt3(user_input)
        # descriptionGenerator = OutputGenerator(gpt, player_info, map_record, worldStatus)
        # inputAdapter = InputTranslator(gpt, player_info, map_record, game_content)
        # eventHandler = EventsTriggered()

        # pcgSystem = PCGController(game_content, player_info, map_record, descriptionGenerator, eventHandler, worldStatus)

        # game_rule = rule_system(player_info, map_record, worldStatus, game_content, buffEffect)
        self.assertEqual(y, 1)
        
        # action.command_args[0].append("south")
        # moving and AP/thirst cost test
        defined_command.move(action, "south")
        x, y = player_info.get_currentLocation()
        self.assertEqual(y, 0)
        self.assertEqual(worldStatus.move_dLevel, 1.0)
        
        defined_command.ActionCost(action)
        self.assertEqual(player_info.get_action_point(), 25)
        self.assertEqual(player_info.get_thirst(), 96)
        
        # action.command_args[0].append("east")
        defined_command.move(action, "east")
        x, y = player_info.get_currentLocation()
        self.assertEqual(x, 1)
        self.assertEqual(worldStatus.move_dLevel, 1.0)
        
        defined_command.ActionCost(action)
        self.assertEqual(player_info.get_action_point(), 20)
        self.assertEqual(player_info.get_thirst(), 92)
        
        # action.command_args[0].append("east")
        defined_command.move(action, "east")
        x, y = player_info.get_currentLocation()
        self.assertEqual(x, 2)
        self.assertEqual(worldStatus.move_dLevel, 1.0)
        
        defined_command.ActionCost(action)
        self.assertEqual(player_info.get_action_point(), 15)
        self.assertEqual(player_info.get_thirst(), 88)
        
        # action.command_args[0].append("east")
        defined_command.move(action, (10, 20))
        x, y = player_info.get_currentLocation()
        self.assertEqual(x, 10)
        self.assertEqual(y, 20)
        self.assertEqual(worldStatus.move_dLevel, 1.0)
        
        del worldStatus
        del player_info
        del map_record
        del defined_command
        del buffEffect
        del game_content

    def test_add_itemsOR_drop_items(self):
        worldStatus = copy.deepcopy(globalInfo())
        # player_info = Player_status(action_point = 30)
        player_info = Player_status()
        map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
        defined_command = Commands(player_info, map_record, worldStatus)
        buffEffect = character_effectSys(player_info, defined_command, worldStatus)
        game_content = DefininedSys(defined_command, map_record, buffEffect)
        
        self.assertEqual(player_info.get_maximum_package_weight(), 20)
        self.assertEqual(player_info.get_package_weight(), 0)
        self.assertEqual(player_info.get_items(), dict())
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two legal items
        currentItem = copy.deepcopy(player_info.get_items()["bread"])
        for food in range(len(items)):
            attributes1 = vars(items[food])
            attributes2 = vars(currentItem[food])
            for attribute1, value1 in attributes1.items():
                for attribute2, value2 in attributes2.items():
                    if attribute1 == attribute2:
                        if attribute1 == "codeName":
                            self.assertNotEqual(value1, value2)
                        else:
                            self.assertEqual(value1, value2)
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(currentItem), 2)
        
        defined_command.remove_items(None, None, currentItem, "code name")
        # testing remove all items in code name
        
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        # print(player_info.get_items()["bread"][0].codeName)
        
        failAdd = defined_command.add_items(None, items)
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 2)
        
        defined_command.remove_items(None, {"bread": 2}, None)
        # testing remove all items in items name
        
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        
        failAdd = defined_command.add_items(None, items)
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 2)
        
        defined_command.remove_items(None, {"bread": 1}, None)
        # testing remove part of items in items name
        
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 1)
        
        
        defined_command.remove_items(None, {"bread": 2}, None)
        # testing remove items more than expected in items name
        
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        
        defined_command.remove_items(None, {"bread": 2}, None)
        # testing remove items more than expected in items name
        
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        
        map_record.currentLocation = Location("land", 0, 0, copy.deepcopy(items))
        
        defined_command.remove_items(None, {"bread": 2}, None, place="location")
        # testing remove items in current location
        
        self.assertEqual(len(map_record.currentLocation.objects), 0)
        
        
        defined_command.remove_items(None, {"bread": 2}, None, place="location")
        # testing remove items in current location more than expected
        self.assertEqual(len(map_record.currentLocation.objects), 0)
        
        
        map_record.currentLocation = Location("land", 0, 0, copy.deepcopy(items))
        
        defined_command.remove_items(None, {"bread": 1}, None, place="location")
        # testing remove partial items in current location
        
        self.assertEqual(len(map_record.currentLocation.objects), 1)
        
        
        # map_record.currentLocation = Location("land", 0, 0, copy.deepcopy(items))
        
        defined_command.remove_items(None, {"bread": 1}, None, place="location")
        # testing remove partial items in current location
        
        self.assertEqual(len(map_record.currentLocation.objects), 0)
        
        
        items = [
            LandscapeFeature("stream", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=10, eatable=True, freshness=-1), 
            LandscapeFeature("stream", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=10, eatable=True, freshness=-1)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two illegal items
        # currentItem = copy.deepcopy(player_info.get_items()["stream"])
        for food in range(len(items)):
            attributes1 = vars(items[food])
            attributes2 = vars(failAdd[food])
            for attribute1, value1 in attributes1.items():
                for attribute2, value2 in attributes2.items():
                    if attribute1 == attribute2:
                        self.assertEqual(value1, value2)

        self.assertEqual(len(failAdd), 2)
        self.assertEqual(list(player_info.get_items().keys()), ["bread"])
        
        items = [
            Tool("weapon crafting bench", {"sea": 0, "land": 5, "forest": 5, "beach": 1, \
                "river": 3, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 10, "grassland": 0}, \
                weight=6, durability=10), 
            Container("glass water bottle", {"sea": 2, "land": 1, "forest": 1, "beach": 3, \
                "river": 2, "desert": 1, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 0}, \
                capacity=5)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two different legal items
        currentItem = copy.deepcopy(player_info.get_items())
        combined_list = [item for sublist in currentItem.values() for item in sublist]
        for food in range(len(items)):
            attributes1 = vars(items[food])
            attributes2 = vars(combined_list[food])
            for attribute1, value1 in attributes1.items():
                for attribute2, value2 in attributes2.items():
                    if attribute1 == attribute2:
                        if attribute1 == "codeName":
                            self.assertNotEqual(value1, value2)
                        else:
                            self.assertEqual(value1, value2)

        self.assertEqual(len(failAdd), 0)
        self.assertEqual(list(player_info.get_items().keys()), ["bread", \
            "weapon crafting bench", "glass water bottle"])
        
        del worldStatus
        del player_info
        del map_record
        del defined_command
        del buffEffect
        del game_content

    def test_consume(self):
        worldStatus = globalInfo()
        player_info = Player_status(action_point = 30)
        # player_info = Player_status()
        map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
        defined_command = Commands(player_info, map_record, worldStatus)
        buffEffect = character_effectSys(player_info, defined_command, worldStatus)
        game_content = DefininedSys(defined_command, map_record, buffEffect)
        
        player_info.set_currentAction(Actions("Consume", [defined_command.consume, defined_command.ActionCost], \
                [[],[]], 1, 1, ["eat", "drink"]))
        map_record.currentLocation = Location("land", 0, 0)
        
        defined_command.consume(None, 1, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["failed to consume bread"], "Although you have tried to find one bread, yet there is not such thing.")
        
        self.assertEqual(player_info.get_maximum_package_weight(), 20)
        self.assertEqual(player_info.get_package_weight(), 0)
        self.assertEqual(player_info.get_items(), dict())
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two legal items
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(currentItem), 2)
        
        worldStatus.descriptor_prompt = {
            "information_need_to_be_described": {
                "description_target": []
            }
        }
        print("1 or 2")
        defined_command.consume(None, 1, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(player_info.get_action_point(), 45)
        self.assertEqual(player_info.get_thirst(), 80)
        # self.assertEqual(worldStatus.current_description, "Although you have tried to find one bread, yet there is not such thing.")
        
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(len(worldStatus.descriptor_prompt), 3)
        self.assertEqual(worldStatus.descriptor_prompt["comsumed_items"], [{'item_name': 'bread', 'weight': 'light', 'AP_recovery': 'medium portion', 'freshness': 'fresh', 'edibility': 'edible', 'thirst_satisfied': 'cause a thirst'}])
        self.assertEqual(worldStatus.descriptor_prompt["information_need_to_be_described"], {'description_target': ['player_current_action', 'comsumed_items', 'player current feeling']})
        self.assertEqual(worldStatus.descriptor_prompt["player_current_action"], "")
        # print(worldStatus.descriptor_prompt)
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(currentItem), 1)
        
        defined_command.remove_items(None, {"bread": 1}, None)
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two legal items
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(currentItem), 2)
        
        worldStatus.descriptor_prompt = {
            "information_need_to_be_described": {
                "description_target": []
            }
        }
        print("1, 2")
        defined_command.consume(None, 1, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(player_info.get_action_point(), 75)
        self.assertEqual(player_info.get_thirst(), 40)
        # self.assertEqual(worldStatus.current_description, "Although you have tried to find one bread, yet there is not such thing.")
        
        currentItem = player_info.get_items()["bread"]
        # print(worldStatus.descriptor_prompt)
        self.assertEqual(len(worldStatus.descriptor_prompt), 3)
        self.assertEqual(worldStatus.descriptor_prompt["comsumed_items"], [{'item_name': 'bread', 'weight': 'light', 'AP_recovery': 'medium portion', 'freshness': 'fresh', 'edibility': 'edible', 'thirst_satisfied': 'cause a thirst'}, \
            {'item_name': 'bread', 'weight': 'light', 'AP_recovery': 'medium portion', 'freshness': 'fresh', 'edibility': 'edible', 'thirst_satisfied': 'cause a thirst'}])
        self.assertEqual(worldStatus.descriptor_prompt["information_need_to_be_described"], {'description_target': ['player_current_action', 'comsumed_items', 'player current feeling']})
        self.assertEqual(worldStatus.descriptor_prompt["player_current_action"], "")
        self.assertEqual(len(player_info.get_items()), 1)
        self.assertEqual(len(currentItem), 0)
        
        defined_command.remove_items(None, {"bread": 1}, None)
        
        
        items = [
            Tool("traps", {"sea": 0, "land": 8, "forest": 8, "beach": 2, "river": 6, \
                "desert": 2, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two legal items
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 2)
        self.assertEqual(len(currentItem), 1)
        self.assertEqual(len(player_info.get_items()["traps"]), 1)
        
        worldStatus.descriptor_prompt = {
            "information_need_to_be_described": {
                "description_target": []
            }
        }
        print("1")
        defined_command.consume(None, 1, "traps")
        self.assertEqual(player_info.get_action_point(), 75)
        self.assertEqual(player_info.get_thirst(), 40)
        # self.assertEqual(len(worldStatus.current_description), 1)
        # self.assertEqual(worldStatus.current_description, "Although you have tried to find one bread, yet there is not such thing.")
        
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(len(player_info.get_items()), 2)
        self.assertEqual(len(currentItem), 1)
        self.assertEqual(worldStatus.current_description["failed to consume traps"], "You cannot have that.")
        self.assertEqual(len(player_info.get_items()["traps"]), 1)
        
        defined_command.remove_items(None, {"bread": 1, "traps": 1}, None)
        self.assertEqual(len(player_info.get_items()["traps"]), 0)
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        
        
        items = [
            Tool("traps", {"sea": 0, "land": 8, "forest": 8, "beach": 2, "river": 6, \
                "desert": 2, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two legal items
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 2)
        self.assertEqual(len(currentItem), 1)
        self.assertEqual(len(player_info.get_items()["traps"]), 1)
        
        worldStatus.descriptor_prompt = {
            "information_need_to_be_described": {
                "description_target": []
            }
        }
        print("1")
        defined_command.consume(None, 1, "bread")
        self.assertEqual(player_info.get_action_point(), 90)
        self.assertEqual(player_info.get_thirst(), 20)
        # self.assertEqual(len(worldStatus.current_description), 1)
        # self.assertEqual(worldStatus.current_description, "Although you have tried to find one bread, yet there is not such thing.")
        
        currentItem = player_info.get_items()["bread"]
        self.assertEqual(len(player_info.get_items()), 2)
        self.assertEqual(len(currentItem), 0)
        self.assertEqual(len(player_info.get_items()["traps"]), 1)
        
        defined_command.remove_items(None, {"bread": 1, "traps": 1}, None)
        self.assertEqual(len(player_info.get_items()["traps"]), 0)
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            Food("grilled potato", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=20, eatable=True, freshness=72, thirst_satisfied=-10)
        ]
        
        worldStatus.current_description = dict()
        map_record.currentLocation.objects = copy.deepcopy(items)
        
        worldStatus.descriptor_prompt = {
            "information_need_to_be_described": {
                "description_target": []
            }
        }
        print("1")
        defined_command.consume(None, 1, "grilled potato")
        self.assertEqual(player_info.get_action_point(), 110)
        self.assertEqual(player_info.get_thirst(), 10)
        # self.assertEqual(len(worldStatus.current_description), 1)
        # self.assertEqual(worldStatus.current_description, "Although you have tried to find one bread, yet there is not such thing.")
        
        self.assertEqual(len(map_record.currentLocation.objects), 1)
        self.assertEqual(map_record.currentLocation.objects[0].item_name, "bread")
        self.assertEqual(map_record.currentLocation.objects[0].codeName, "bread")
        
        
        
        defined_command.remove_items(None, {"bread": 1}, None, place="location")
        self.assertEqual(len(map_record.currentLocation.objects), 0)
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            LandscapeFeature("stream", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=10, eatable=True, freshness=20, thirst_satisfied=20)
        ]
        
        worldStatus.current_description = dict()
        map_record.currentLocation.objects = copy.deepcopy(items)
        
        worldStatus.descriptor_prompt = {
            "information_need_to_be_described": {
                "description_target": []
            }
        }
        print("1")
        defined_command.consume(None, 1, "stream")
        self.assertEqual(player_info.get_action_point(), 120)
        self.assertEqual(player_info.get_thirst(), 30)
        # self.assertEqual(len(worldStatus.current_description), 1)
        # self.assertEqual(worldStatus.current_description, "Although you have tried to find one bread, yet there is not such thing.")
        
        self.assertEqual(len(map_record.currentLocation.objects), 2)
        self.assertEqual(map_record.currentLocation.objects[0].item_name, "bread")
        self.assertEqual(map_record.currentLocation.objects[0].codeName, "bread")
        self.assertEqual(map_record.currentLocation.objects[1].item_name, "stream")
        self.assertEqual(map_record.currentLocation.objects[1].codeName, "stream")
        
        
    def test_pickUp(self):
        worldStatus = globalInfo()
        player_info = Player_status(action_point = 30)
        # player_info = Player_status()
        map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
        defined_command = Commands(player_info, map_record, worldStatus)
        buffEffect = character_effectSys(player_info, defined_command, worldStatus)
        game_content = DefininedSys(defined_command, map_record, buffEffect)
        
        player_info.set_currentAction(Actions("Take", [defined_command.pickUp, defined_command.ActionCost], \
                [[],[]], 2, 1, ["take"]))
        map_record.currentLocation = Location("land", 0, 0)
        
        defined_command.pickUp(None, 1, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["failed to pick up bread"], \
            "It seems that there is not such things around, even if you try to find one.")
        
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        worldStatus.current_description = dict()
        map_record.currentLocation.objects = copy.deepcopy(items)
        
        print("1 or 2")
        defined_command.pickUp(None, 1, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["pick up bread"], \
            "You pick up 1 bread and drop them in your bag")
        self.assertEqual(len(map_record.currentLocation.objects), 1)
        
        
        items = [
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        worldStatus.current_description = dict()
        map_record.currentLocation.objects = copy.deepcopy(items)
        
        print("1, 2")
        defined_command.pickUp(None, 1, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["pick up bread"], \
            "You pick up 2 bread and drop them in your bag")
        self.assertEqual(len(map_record.currentLocation.objects), 0)
        
        
        items = [
            LandscapeFeature("stream", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 10, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=10, thirst_satisfied=30, eatable=True, freshness=2**10), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        worldStatus.current_description = dict()
        map_record.currentLocation.objects = copy.deepcopy(items)
        
        print("1")
        defined_command.pickUp(None, 1, "stream")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["pick up stream"], \
            "You pick up 0 stream and drop them in your bag")
        self.assertEqual(len(map_record.currentLocation.objects), 2)
    
    
    def test_equip(self):
        worldStatus = globalInfo()
        player_info = Player_status(action_point = 30)
        # player_info = Player_status()
        map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
        defined_command = Commands(player_info, map_record, worldStatus)
        buffEffect = character_effectSys(player_info, defined_command, worldStatus)
        game_content = DefininedSys(defined_command, map_record, buffEffect)
        
        player_info.set_currentAction(Actions("Take", [defined_command.pickUp, defined_command.ActionCost], \
                [[],[]], 2, 1, ["take"]))
        map_record.currentLocation = Location("land", 0, 0)
        
        defined_command.equip(None, "iron sword")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["failed to equip iron sword"], \
            "You cannot find one iron sword in your package")
        
        worldStatus.current_description = dict()
        
        items = [
            Weapon("iron sword", {"sea": 0, "land": 10, "forest": 5, "beach": 10, "river": 0, \
                "desert": 5, "mountain": 5, "highland snowfield": 2, "town": 0, "grassland": 10}, \
                    3, 10, 10), 
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20)
        ]
        
        failAdd = defined_command.add_items(None, items) # testing add two legal items
        currentItem = copy.deepcopy(player_info.get_items()["bread"])
        combined_list = [item for sublist in player_info.get_items().values() for item in sublist]
        for food in range(len(items)):
            attributes1 = vars(items[food])
            attributes2 = vars(combined_list[food])
            for attribute1, value1 in attributes1.items():
                for attribute2, value2 in attributes2.items():
                    if attribute1 == attribute2:
                        if attribute1 == "codeName":
                            self.assertNotEqual(value1, value2)
                        else:
                            self.assertEqual(value1, value2)
        self.assertEqual(failAdd, list())
        self.assertEqual(len(player_info.get_items()), 2)
        self.assertEqual(len(currentItem), 1)
        self.assertEqual(len(player_info.get_items()["iron sword"]), 1)
        
        defined_command.equip(None, "iron sword")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["equip iron sword"], \
            "You have equipped iron sword")
        self.assertEqual(len(player_info.get_items()["iron sword"]), 0)
        self.assertEqual(player_info.get_equipment().item_name, "iron sword")
        
        worldStatus.current_description = dict()
        defined_command.unequip(None)
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["unequip iron sword"], \
            "You have unequipped iron sword")
        self.assertEqual(len(player_info.get_items()["iron sword"]), 1)
        self.assertEqual(player_info.get_equipment(), None)
        
        worldStatus.current_description = dict()
        defined_command.equip(None, "bread")
        self.assertEqual(len(worldStatus.current_description), 1)
        self.assertEqual(worldStatus.current_description["equip bread"], \
            "You have equipped bread")
        self.assertEqual(len(player_info.get_items()["bread"]), 0)
        self.assertEqual(player_info.get_equipment().item_name, "bread")
        

if __name__ == '__main__':
    unittest.main()