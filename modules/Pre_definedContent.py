from status_record import Player_status, Map_information, globalInfo, Items, Events, \
    Actions, Terrain_type, LandscapeFeature, EnvironmentElement, Tool, Food, \
        Transportation, Weapon, Container, PassivityEvents
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
        if cell!= 0 and cell != 3 and tranferP > pTable[cellT] and cell != -1:
            # print(cell)
            cell = copy.copy(currentId)
            # print("Changed!")
        # else:
        #     cell = -1

        return cell
    
    def random_map_update_desert(self, cell_grid: np.ndarray, cellT, time_step, \
        death_limit = 4, birth_limit = 4, currentId = 0, seed: int= None):
        
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_sea = np.where(oneD == 0)[0].shape[0]
        number_of_target = np.where(oneD == currentId)[0].shape[0]
        

        if cell == 0:
            number_of_sea -= 1
        elif cell == currentId:
            number_of_target -= 1

        if number_of_target > birth_limit:
            cell = copy.copy(currentId)
            # print("Changed!")
        elif cell == currentId and (number_of_target < death_limit or number_of_sea>0):
            cell = -1
        
        if cell == 4 and number_of_sea <= 0:
            cell = 1
            # print("Changed!")
        # else:
        #     cell = -1

        return cell
    
    
    def random_map_update_highland_snowfield(self, cell_grid: np.ndarray, cellT, time_step, \
        death_limit = 4, birth_limit = 4, currentId = 0, seed: int= None, possibility = 0):
        
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_target = np.where(oneD == currentId)[0].shape[0]
        number_of_origin = np.where(oneD == -1)[0].shape[0]
        # print(cellT)
        np.random.seed(seed)
        pTable = np.random.randint(0, 50, self.__map.get_map_size())
        # print(seed)
        tranferP = possibility * 50

        if cell == currentId:
            number_of_target -= 1
            if number_of_origin + number_of_target < 8 and tranferP <= pTable[cellT]:
                cell = -1
                # print(pTable)
                # print(tranferP)

        return cell
    
    def random_map_update_town(self, cell_grid: np.ndarray, cellT, time_step, \
        death_limit = 4, birth_limit = 4, currentId = 0, seed: int= None):
        
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_target = np.where(oneD == currentId)[0].shape[0]
        number_of_other = np.where(oneD == -1)[0].shape[0]
        # print(cellT)
        if cell == currentId:
            number_of_target -= 1
            if number_of_target + number_of_other > 0:
                cell = -1

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
            # LandscapeFeature
            LandscapeFeature("stream", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                item_energy_recovery=10, eatable=True, freshness=-1), 
            LandscapeFeature("rocks", {"sea": 10, "land": 12, "forest": 12, "beach": 10, \
                "river": 8, "desert": 5, "mountain": 5, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                item_energy_recovery=10, eatable=True, freshness=72), 
            LandscapeFeature("grass", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 12}, \
                item_energy_recovery=2, eatable=False, freshness=20),
            LandscapeFeature("aloe vera", {"sea": 0, "land": 12, "forest": 5, "beach": 4, \
                "river": 2, "desert": 12, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                item_energy_recovery=2, eatable=True, freshness=20),
            
            # Tool
            Tool("traps", {"sea": 0, "land": 8, "forest": 8, "beach": 2, "river": 6, \
                "desert": 2, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}),
            Tool("weapon crafting bench", {"sea": 0, "land": 5, "forest": 5, "beach": 1, \
                "river": 3, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 10, "grassland": 0}, \
                weight=6, durability=10),
            Tool("fish rod", {"sea": 4, "land": 1, "forest": 1, "beach": 6, "river": 6, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}),
            
            # Container
            Container("glass water bottle", {"sea": 2, "land": 1, "forest": 1, "beach": 3, \
                "river": 2, "desert": 1, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 0}, \
                capacity=5),
            
            # Transportation
            Transportation("boat", {"sea": 2, "land": 0, "forest": 0, "beach": 8, "river": 5, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 0}, \
                suitablePlace={"sea"}, APReduce=0.5),
            
            # Food
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                item_energy_recovery=15, eatable=True, freshness=20, thirst=-20),
            Food("raw fish", {"sea": 15, "land": 0, "forest": 0, "beach": 1, "river": 12, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=2, \
                item_energy_recovery=5, eatable=False, freshness=24, thirst=20),
            Food("grilled fish", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=2, \
                item_energy_recovery=15, eatable=True, freshness=24, thirst=10),
            Food("berry", {"sea": 0, "land": 5, "forest": 10, "beach": 0, "river": 5, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 12}, weight=1, \
                item_energy_recovery=5, eatable=True, freshness=18, thirst=10),
            Food("potato", {"sea": 0, "land": 5, "forest": 2, "beach": 0, "river": 2, \
                "desert": 12, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 12}, weight=1, \
                item_energy_recovery=10, eatable=False, freshness=50, thirst=-5),
            Food("grilled potato", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                item_energy_recovery=10, eatable=True, freshness=72, thirst=-10),
            Food("raw venison", {"sea": 0, "land": 1, "forest": 2, "beach": 0, "river": 2, \
                "desert": 12, "mountain": 5, "highland snowfield": 5, "town": 0, "grassland": 15}, weight=5, \
                item_energy_recovery=20, eatable=False, freshness=19, thirst=50),
            Food("grilled venison", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=5, \
                item_energy_recovery=30, eatable=True, freshness=29, thirst=20),
            Food("vegetable soup", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=5, \
                item_energy_recovery=30, eatable=True, freshness=15, thirst=50),
            Food("stew", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, "desert": 0, \
                "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=10, \
                item_energy_recovery=50, eatable=True, freshness=15, thirst=30),
            
            # Item
            Items("wood", {"sea": 1, "land": 3, "forest": 20, "beach": 1, "river": 3, "desert": 0, \
                "mountain": 8, "highland snowfield": 5, "town": 0, "grassland": 15}, weight=5),
            Items("rock", {"sea": 10, "land": 12, "forest": 12, "beach": 10, "river": 8, \
                "desert": 5, "mountain": 15, "highland snowfield": 10, "town": 0, "grassland": 12}, weight=5),
            Items("stick", {"sea": 0, "land": 1, "forest": 20, "beach": 0, "river": 2, "desert": 0, \
                "mountain": 5, "highland snowfield": 5, "town": 0, "grassland": 15}, weight=2),
            Items("palm leave", {"sea": 1, "land": 0, "forest": 0, "beach": 19, "river": 2, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 15}, weight=1),
            Items("seed", {"sea": 1, "land": 10, "forest": 10, "beach": 1, "river": 3, "desert": 0, \
                "mountain": 3, "highland snowfield": 0, "town": 8, "grassland": 15}, weight=1),
            Items("coal", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, "desert": 0, \
                "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=2),
            Items("cloth", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, "desert": 0, \
                "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1),
            Items("glass bottle", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1),
            Items("a bottle of sand", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=3),
        ]

        # """
        # fun1
        # """
        
        # self.__def_events = [
        #     Events("init_reward", [(preDefinedCommands.equalTo, (player.get_currentLocation(), (0,0)))], \
        #         [(preDefinedCommands.add_items, (None, random.choice, (self.__def_items, )))])
        # ]
        
        # self.__def_events = [
        #     PassivityEvents("init_reward", [(preDefinedCommands.equalTo, (player.get_currentLocation(), (0,0)))], \
        #         [(preDefinedCommands.add_items, (None, random.choice, (self.__def_items, )))])
        # ]
        
        self.__pre_def_events_frameWork = {
            "survival crisis": [PassivityEvents("", "survival crisis", \
                "low action point", ["increase action point", "increase maximum action point"], \
                    ["decrease action point", "decrease maximum action point"], -1, "", \
                        lambda player, mapInfo, events, worldStatus: player.get_action_point() < 40), 
                        PassivityEvents("", "survival crisis", \
                "low health point", ["increase health point", "increase maximum health point"], \
                    ["decrease health point", "decrease maximum health point"], -1, "", \
                        lambda player, mapInfo, events, worldStatus: player.get_hp() < 40), 
                        PassivityEvents("", "survival crisis", \
                "low health point", ["increase health point", "increase maximum health point"], \
                    ["decrease health point", "decrease maximum health point"], -1, "", \
                        lambda player, mapInfo, events, worldStatus: player.get_hp() < 40)
            ]
        }
        
        # self.__pre_def_events = {
        #     "survival crisis": {"action point": PassivityEvents("Exhausted","survival crisis", \
        #         "low action point in anywhere", ["increase action point", \
        #             "increase maximum action point"], ["decrease action point", \
        #             "decrease maximum action point"], 3, "I'm so tired, I need have a rest!")}
        # }
        
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
        
        self.__terrain_type = {
            "sea": Terrain_type(terrain_name = "sea", terrain_ID = 0, possibilityOfGenerate = 0.7, \
                move_dLevel = 4, rules = mapRule.random_map_update_SIslands, extraArgs =  tuple(), \
                    allowedAppearUpon = [], visualizedColor = [128, 0, 0]), 
            "land": Terrain_type(terrain_name = "land", terrain_ID = 1, possibilityOfGenerate = 0.5, \
                move_dLevel = 1, rules = mapRule.random_map_update_SIslands, extraArgs =  tuple(), \
                    allowedAppearUpon = [0], visualizedColor = [0, 0, 128]), 
            "river": Terrain_type(terrain_name = "river", terrain_ID = 2, possibilityOfGenerate = 0, \
                move_dLevel = 4, rules = None, extraArgs =  tuple(), \
                    allowedAppearUpon = [0], visualizedColor = [255, 0, 0]),
            "forest": Terrain_type(terrain_name = "forest", terrain_ID = 3, possibilityOfGenerate = 0.4, \
                move_dLevel = 1, rules = mapRule.random_map_update_defult, extraArgs =  tuple(), \
                    allowedAppearUpon = [1], visualizedColor = [52, 137, 52]),
            "beach": Terrain_type(terrain_name = "beach", terrain_ID = 4, possibilityOfGenerate = 0, \
                move_dLevel = 2, rules = mapRule.random_map_update_sand, extraArgs = (0.3,), \
                    allowedAppearUpon = [1], visualizedColor = [0, 255, 255]),
            "desert": Terrain_type(terrain_name = "desert", terrain_ID = 5, possibilityOfGenerate = 0.3, \
                move_dLevel = 3, rules = mapRule.random_map_update_desert, extraArgs = tuple(), \
                    allowedAppearUpon = [1], visualizedColor = [175, 201, 237]), 
            "mountain": Terrain_type(terrain_name = "mountain", terrain_ID = 6, possibilityOfGenerate = 0.3, \
                move_dLevel = 4, rules = mapRule.random_map_update_defult, extraArgs =  tuple(), \
                    allowedAppearUpon = [1, 3, 4, 5], visualizedColor = [32, 96, 174]),
            "highland snowfield": Terrain_type(terrain_name = "highland snowfield", terrain_ID = 7, \
                possibilityOfGenerate = 1, move_dLevel = 5, rules = mapRule.random_map_update_highland_snowfield, \
                    extraArgs =  (0.2,), allowedAppearUpon = [6], visualizedColor = [255, 255, 255]),
            "town": Terrain_type(terrain_name = "town", terrain_ID = 8, \
                possibilityOfGenerate = 0.005, move_dLevel = 1, rules = mapRule.random_map_update_town, \
                    extraArgs =  tuple(), allowedAppearUpon = [1, 3, 4, 5, 6, 7], visualizedColor = [0, 0, 255]),
            "grassland": Terrain_type(terrain_name = "grassland", terrain_ID = 9, \
                possibilityOfGenerate = 0.6, move_dLevel = 1, rules = mapRule.random_map_update_defult, \
                    extraArgs =  tuple(), allowedAppearUpon = [1], visualizedColor = [0, 255, 0])
            }
        
        for terrain in self.__terrain_type.keys():
            # print("----------------------")
            # print(terrain)
            for item in self.__def_items:
                if item.possibleWeight[terrain] >= 20:
                    definitely_Object = self.__terrain_type[terrain].definitely_Object
                    definitely_Object = np.append(definitely_Object, item)
                    # print(definitely_Object[-1].item_name)
                    # self.__terrain_type[terrain].definitely_Object.append(item)
                elif item.possibleWeight[terrain] > 0:
                    possible_Object = self.__terrain_type[terrain].possible_Object
                    weight = self.__terrain_type[terrain].possible_Object_Weight
                    possible_Object = np.append(possible_Object, item)
                    weight = np.append(weight, item.possibleWeight[terrain])
                    # print(weight[-1])
                    # .append(item)
                    # .append(item.possibleWeight[terrain])
                # if len(self.__terrain_type[terrain].possible_Object)>0:
                #     print(self.__terrain_type[terrain].possible_Object[-1].item_name)
                #     print(self.__terrain_type[terrain].possible_Object_Weight[-1])
            
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
