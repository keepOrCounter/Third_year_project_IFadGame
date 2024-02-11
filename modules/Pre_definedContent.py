from status_record import Player_status, Map_information, globalInfo, Items, Events, \
    Actions, Terrain_type
import random
import copy
import numpy as np



class Commands():
    def __init__(self, player: Player_status, map: Map_information, worldStatus: globalInfo) -> None:
        """
        This class is pre-defined commands in methods form
        """
        self.__player = player
        self.__map = map
        self.__worldStatus = worldStatus
        # self.__executionTranslator
        
    def valueRetrieval(self, *value):
        valueProcessed = []
        for x in value:
            if x == "<random>":
                valueProcessed.append(random.randint(0, 5))
            else:
                valueProcessed.append(x)
        
        if len(valueProcessed) > 1:
            return valueProcessed
        else:
            return valueProcessed[0]
        
    def move(self, target) -> None:
        """
        Move to specific direction or target place
        """
        newTarget = self.valueRetrieval(target)
        x, y = self.__player.get_currentLocation()
        if newTarget == "North":
            self.__player.set_currentLocation(x, y+1)
        elif newTarget == "South":
            self.__player.set_currentLocation(x, y-1)
        elif newTarget == "East":
            self.__player.set_currentLocation(x+1, y)
        elif newTarget == "West":
            self.__player.set_currentLocation(x-1, y)
        else:
            self.__player.set_currentLocation(*newTarget)
            
        self.__player.set_action_point(self.__player.get_action_point() -\
            self.__worldStatus.move_APCost * self.__worldStatus.move_dLevel)
        
    def increase_action_point(self, value: int) -> None:
        """
        Recovery action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_action_point(self.__player.get_action_point() + newValue)
        
    def decrease_action_point(self, value: int) -> None:
        """
        consume action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_action_point(self.__player.get_action_point() - newValue)
        
    def increase_hp(self, value: int) -> None:
        """
        Recovery health point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_hp(self.__player.get_hp() + newValue)
        
    def decrease_hp(self, value: int) -> None:
        """
        reduce health point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_hp(self.__player.get_hp() - newValue)
        
    def add_items(self, items: list[Items]) -> None:
        """
        Add one or more items to player's package
        """
        currentItems = self.__player.get_items()
        for x in items:
            if x.item_name not in currentItems.keys():
                currentItems[x.item_name] = [copy.deepcopy(x)]
            else:
                currentItems[x.item_name].append(copy.deepcopy(x))
        self.__player.set_items(currentItems)
        
    def remove_items(self, items: dict[str, int]) -> None:
        """
        Remove one or more items to player's package
        """
        currentItems = self.__player.get_items()
        for x in items.keys():
            for y in range(items[x]):
                currentItems[x].pop()
        self.__player.set_items(currentItems)
        
    def increase_maximum_action_point(self, value: int) -> None:
        """
        Recovery action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(newValue)
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() + newValue)
        
    def decrease_maximum_action_point(self, value: int) -> None:
        """
        consume action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() - newValue)
    
    
    def rest(self):
        if self.__worldStatus.restPlace:
            self.increase_action_point(int(self.__player.get_APrecovery() / \
                self.__worldStatus.move_dLevel))
            print("You seat down, and have a short nap")
        else:
            print("You cannot have a rest now.")
    
    # def equalTo(self, value, target) -> bool:
    #     return value == target
    
    # def greaterThan(self, value, target) -> bool:
    #     return value > target
    
    # def greaterThanOrEqualTo(self, value, target) -> bool:
    #     return value >= target
    
    # def smallerThan(self, value, target) -> bool:
    #     return value < target
    
    # def smallerThanOrEqualTo(self, value, target) -> bool:
    #     return value <= target
    
    # def callableExecution(self, callablePosition, itsArguemts):
    #     pass
    
    
class MapPcgRule():
    def __init__(self, map: Map_information) -> None:
        self.__map = map
    
    def random_map_update_SIslands(self, cell_grid: np.ndarray, cellT, time_step, \
        death_limit = 4, birth_limit = 4, currentId = 0, seed: int= None):
        
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_1 = np.where(oneD == 1)[0].shape[0]
        number_of_0 = oneD.shape[0] - number_of_1

        if cell == 1:
            number_of_1 -= 1
        else:
            number_of_0 -= 1
            
        if number_of_1 > birth_limit:
            cell = 1
        elif number_of_1 < death_limit:
            cell = 0

        return cell
    
    def random_map_update_defult(self, cell_grid: np.ndarray, cellT, time_step, \
        death_limit = 4, birth_limit = 4, currentId = 0, seed: int= None):
        
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_target = np.where(oneD == currentId)[0].shape[0]
        number_of_0 = oneD.shape[0] - number_of_target
        # print(cellT)
        if cell == currentId:
            number_of_target -= 1
        else:
            number_of_0 -= 1
            
        if number_of_target > birth_limit:
            cell = copy.copy(currentId)
            # print("Changed!")
        elif number_of_target < death_limit:
            cell = -1

        return cell
    
    def random_map_update_sand(self, cell_grid: np.ndarray, cellT, time_step, \
        death_limit = 4, birth_limit = 4, currentId = 0, seed: int= None, \
            possibility: int= 0.5):
        
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_sea = np.where(oneD == 0)[0].shape[0]
        number_of_target = np.where(oneD == currentId)[0].shape[0]
        
        np.random.seed(seed)
        pTable = np.random.randint(0, 100, self.__map.get_map_size())
        # print(pTable)
        # print(seed)
        tranferP = possibility * 100

        if cell == 0:
            number_of_sea -= 1
        elif cell == currentId:
            number_of_target -= 1

            
        if number_of_sea > 0 or number_of_target > birth_limit:
            tranferP *= 2
        elif number_of_target < death_limit:
            tranferP = 0
            
        tranferP = int(tranferP)
        if cell!= 0 and cell != 2 and tranferP > pTable[cellT] and cell != -1:
            # print(cell)
            cell = copy.copy(currentId)
            # print("Changed!")
        # else:
        #     cell = -1

        return cell
    
class character_effectSys():
    def __init__(self, player: Player_status, preDefinedCommands: Commands) -> None:
        """
        This class is pre-defined buff function in methods form
        """
        self.__player = player
        self.__preDefinedCommands = preDefinedCommands
        
    def hp_recovery(self, amount):
        self.__preDefinedCommands.increase_hp(amount)
        
    def more_hp(self, amount):
        self.__player.set_maximum_hp(self.__player.get_maximum_hp() + amount)
        
    def action_point_recovery(self, amount):
        self.__preDefinedCommands.increase_action_point(amount)
        
    def more_ap(self, amount):
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() + amount)

class DefininedSys(): # 
    def __init__(self, preDefinedCommands: Commands, map_record: Map_information) -> None:
        """
        All the defined content stored here\n\n
        `__def_items:` All the objects with same or differnt type here\n
        `__def_actions:` Defined player action, contains the name of action and the command will be executed in method form,
        usage example>>> <method stored in Actions>(*<arguments of method>), this would call the method\n
        """
        self.__map_record = map_record
        self.__def_items = [
            # Items("Campfire", 20, "Items"),
            Items("Stream", 10, "Landscape Features"),
            Items("Bread", 15, "Items"),
            Items("Traps", 10, "Items"),
            Items("First Aid Kit", 25, "Items"),
            # Items("Toolkits", 15),
            # Items("Maps", 5),
            Items("Edible Plants", 10, "Items"),
            Items("Firewood", 0, "Items"),
            Items("Rocks", 0, "Landscape Features"),
            Items("Weapon Crafting Bench", 0, "Items")
        ]
        # """
        # fun1
        # """
        
        # self.__def_events = [
        #     Events("init_reward", [(preDefinedCommands.equalTo, (player.get_currentLocation(), (0,0)))], \
        #         [(preDefinedCommands.add_items, (None, random.choice, (self.__def_items, )))])
        # ]
        
        # self.__def_events = [
        #     Events("init_reward", [(preDefinedCommands.equalTo, (player.get_currentLocation(), (0,0)))], \
        #         [(preDefinedCommands.add_items, (None, random.choice, (self.__def_items, )))])
        # ]
        
        self.__pre_def_events_frameWork = {
            "survival crisis": {"action point": Events("", "survival crisis", \
                "low action point", ["increase action point", "increase maximum action point"], \
                    ["decrease action point", "decrease maximum action point"], -1, "")}
        }
        
        self.__pre_def_events = {
            "survival crisis": {"action point": Events("Exhausted","survival crisis", \
                "low action point in anywhere", ["increase action point", \
                    "increase maximum action point"], ["decrease action point", \
                    "decrease maximum action point"], 3, "I'm so tired, I need have a rest!")}
        }
        
        self.__def_actions = {
            "Move North": Actions("Move North", [(preDefinedCommands.move, ("North",))]),
            "Move South": Actions("Move South", [(preDefinedCommands.move, ("South",))]),
            "Move East": Actions("Move East", [(preDefinedCommands.move, ("East",))]),
            "Move West": Actions("Move West", [(preDefinedCommands.move, ("West",))]),
            "Rest": Actions("Rest", [(preDefinedCommands.rest, tuple())])
        }
        
        self.__eventCommandMap = {
            "increase action point": ("increase action point", "<random>"),
            "decrease action point": ("decrease action point", "<random>"),
            "increase maximum action point": ("increase maximum action point", "<random>"),
            "decrease maximum action point": ("decrease maximum action point", "<random>")
        }
        
        self.__commandTranslate = {
            "increase action point": preDefinedCommands.increase_action_point,
            "decrease action point": preDefinedCommands.decrease_action_point,
            "increase maximum action point": preDefinedCommands.increase_maximum_action_point,
            "decrease maximum action point": preDefinedCommands.decrease_maximum_action_point,
        }
        
        mapRule = MapPcgRule(map_record)
        
        self.__terrain_type= {
            "sea": Terrain_type("sea", 0, 0.7, 4, mapRule.random_map_update_SIslands, tuple(), [], [255, 0, 0]), 
            "land": Terrain_type("land", 1, 0.5, 1, mapRule.random_map_update_SIslands, tuple(), [0], [0, 255, 0]), 
            "forest": Terrain_type("forest", 2, 0.4, 1, mapRule.random_map_update_defult, tuple(), [1], [52, 137, 52]),
            "beach": Terrain_type("beach", 3, 0, 2, mapRule.random_map_update_sand, (0.3,), [1], [0, 255, 255])
            }
        
        # self.__terrain_type = ["sea", "land"]
        # self.__move_dLevel = [4, 1]
        
    def get_items(self) -> list[Items]:
        return self.__def_items
    
    # Setter method for def_items
    def set_items(self, new_items: list[Items]):
        self.__def_items = new_items

    def get_events(self) -> list[Events]:
        return self.__pre_def_events
    
    def get_events_frameWork(self) -> dict:
        return self.__pre_def_events_frameWork
    
    # Setter method for def_items
    # def set_events(self, new_events: list[Events]):
    #     self.__pre_def_events = new_events

    def get_Actions(self) -> dict[str,Actions]:
        return self.__def_actions
    
    # Setter method for def_items
    def set_Actions(self, new_Actions: dict[str,Actions]):
        self.__def_actions = new_Actions
        
    def get_eventCommandMap(self) -> dict:
        return self.__eventCommandMap
    
    def get_commandTranslate(self) -> dict:
        return self.__commandTranslate
    
    def get_terrain_type(self) -> dict[str, Terrain_type]:
        return self.__terrain_type
    
    
    # Setter method for def_items
    def set_terrain(self, new_terrain_name: str, new_terrain: Terrain_type):
        self.__terrain_type[new_terrain_name] = new_terrain
        self.__terrain_type[new_terrain_name].terrain_ID = len(self.__terrain_type.keys())
