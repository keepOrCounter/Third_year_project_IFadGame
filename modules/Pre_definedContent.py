from status_record import Player_status, Map_information, globalInfo, Items, Events, \
    Actions, Terrain_type, LandscapeFeature, EnvironmentElement, Tool, Food, \
        Transportation, Weapon, Container, PassivityEvents, Buff, DisasterEvents, humanNPC
import random
import copy
import numpy as np
import re



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
            elif x == "<median random>":
                valueProcessed.append(random.randint(6, 10))
            elif x == "<high random>":
                valueProcessed.append(random.randint(11, 20))
            else:
                valueProcessed.append(x)
        
        if len(valueProcessed) > 1:
            return valueProcessed
        else:
            return valueProcessed[0]
        
    def move(self, action: Actions, target) -> None:
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
            
        # self.__player.set_action_point(self.__player.get_action_point() -\
        #     action.actionPointCost * self.__worldStatus.move_dLevel)
        
    def increase_action_point(self, action: Actions, value: int) -> None:
        """
        Recovery action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_action_point(self.__player.get_action_point() + newValue)
        
    def decrease_action_point(self, _, value: int) -> None:
        """
        consume action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_action_point(self.__player.get_action_point() - newValue)
        
    def increase_hp(self, _, value: int) -> None:
        """
        Recovery health point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_hp(self.__player.get_hp() + newValue)
        
    def decrease_hp(self, _, value: int) -> None:
        """
        reduce health point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_hp(self.__player.get_hp() - newValue)
        
    def add_items(self, action: Actions, items: list[Items]) -> None:
        """
        Add one or more items to player's package
        """
        currentItems = self.__player.get_items()
        for x in items:
            if x.category == "food":
                self.__worldStatus.freshNessChangedItems.append(x)
            if x.item_name not in currentItems.keys():
                currentItems[x.item_name] = [copy.deepcopy(x)]
                # currentItems[x.item_name][-1].codeName = x.item_name + str(len(currentItems[x.item_name]))
            else:
                currentItems[x.item_name].append(copy.deepcopy(x))
                
            currentItems[x.item_name][-1].codeName = x.item_name + "(" + str(len(currentItems[x.item_name])) + ")"
                
        self.__player.set_items(currentItems)
        
    def remove_items(self, action: Actions, items: dict[str, Items]) -> None:
        """
        Remove one or more items to player's package
        """
        currentItems = self.__player.get_items()
        for x in items.keys():
            for y in range(items[x]):
                currentItems[x].pop()
        self.__player.set_items(currentItems)
        
    def increase_maximum_action_point(self, action: Actions, value: int) -> None:
        """
        Recovery action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(newValue)
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() + newValue)
        
    def decrease_maximum_action_point(self, action: Actions, value: int) -> None:
        """
        consume action point
        """
        # if value == "<random>":
        #     value = random.randint(0, 5)
        newValue = self.valueRetrieval(value)
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() - newValue)
    
    def findObject(self, action: Actions, target: str, place: str, mode = "real name"):
        """trying to find an object or an npc in player bag or current location

        Args:
            `target` (str): object name or code name
            `place` (str): 'package' or 'location'
            `mode` (str, optional): "real name" or "code name". Defaults to "real name".

        Returns:
            result, index, container
            `result` (bool): whether found in list or dictionary
            `index` (int): The position found in list or dictionary
            `container` (iterable): Target list or dictionary
        """
        if mode == "real name":
            if place == "package":
                bag = self.__player.get_items()
                container = bag
                if target in bag.keys() and len(bag[target])>0:
                    result = target in bag.keys()
                    amount = 0
                else:
                    result = False
                    amount = None
            else:
                currentPlace = self.__map.currentLocation
                itemList = currentPlace.objects
                npsList = currentPlace.npcs
                counter = 0
                for x in range(len(itemList)):
                    if itemList[x].item_name == target:
                        result = True
                        counter = x
                        container = itemList
                        return result, counter, container

                for x in range(len(npsList)):
                    if npsList[x].NPC_name == target:
                        result = True
                        counter = x
                        container = npsList

                amount = counter
                
            return result, amount, container
        else:
            result = False
            count = None
            container = None
            realName = re.sub(r'\(\d+\)', '', target)
            # print(realName)
            if place == "package":
                bag = self.__player.get_items()
                if realName in bag.keys() and len(bag[realName])>0:
                    for x in range(len(bag[realName])):
                        if bag[realName][x].codeName == target:
                            result = True
                            count = x
                            container = bag
                            break
            else:
                currentPlace = self.__map.currentLocation
                itemList = currentPlace.objects
                npsList = currentPlace.npcs
                for x in range(len(itemList)):
                    if itemList[x].codeName == target:
                        return True, x, itemList
                    

                for x in range(len(npsList)):
                    if npsList[x].NPC_name == target:
                        result = True
                        count = x
                        container = npsList

            return result, count, container
    
    def rest(self, action: Actions):
        if self.__worldStatus.restPlace:
            self.increase_action_point(action, int(self.__player.get_APrecovery() / \
                self.__worldStatus.move_dLevel))
            # print("You seat down, and have a short nap")
            self.__worldStatus.current_description["rest"] = \
                "You seat down, and have a short nap"
        else:
            # print("You cannot have a rest now.")
            self.__worldStatus.current_description["rest"] = \
                "You cannot have a rest now."
            
    def consume(self, action: Actions, items: Items):
        items = self.valueRetrieval(items)
        if items.category == "food":
            self.__player.set_action_point(self.__player.get_action_point() +\
                items.AP_recovery)
            self.__player.set_thirst(int(self.__player.get_thirst() -\
                items.thirst_satisfied))
            if not items.eatable:
                if "consume uneatable food" not in self.__worldStatus.player_dangerAction.keys():
                    self.__worldStatus.player_dangerAction["consume uneatable food"] = [items.item_name]
                else:
                    self.__worldStatus.player_dangerAction["consume uneatable food"].append(items.item_name)
            
            # print("You have your "+items.item_name+" and take a short break.")
            self.__worldStatus.current_description["consume "+items.item_name] = \
                "You have your "+items.item_name+" and take a short break."
            # TODO pass information to gpt to descript current player feeling
        else:
            self.__worldStatus.current_description["failed to consume "+items.item_name] = \
                "You cannot have that."
            
    def pickUp(self, action: Actions, amount: int, itemName: str): # TODO process weight
        itemName, amount = self.valueRetrieval(itemName, amount)
        itemsList = []
        count = 0
        for x in self.__map.currentLocation.objects:
            if itemName == x.item_name:
                itemsList.append(x)
                count += 1
                if count >= amount:
                    break
        if len(itemsList) > 0:
            self.add_items(action, itemsList)
            # print("You pick up "+str(count)+" "+itemName+" and drop them in your bag")
            self.__worldStatus.current_description["pick up "+itemName] = \
                "You pick up "+str(count)+" "+itemName+" and drop them in your bag"
        else:
            self.__worldStatus.current_description["pick up "+itemName] = \
                "It seems that there is not such things around, even if you try to find one."
            # print("It seems that there is not such things around, even if you try to find one.")
            
    def talk(self, action: Actions, npcs: humanNPC):
        pass
        
    def attack(self, action: Actions, target):
        item = self.__player.get_equipment()
        if item == None:
            target.set_hp(target.get_hp() - random.randint(0, 5))
            self.__worldStatus.current_description["attack"] = \
                "You give a punch at " + target.get_name()
        else:
            if item.category == "weapon":
                target.set_hp(target.get_hp() - random.randint(0, 5 + item.attack*item.weight))
            else:
                target.set_hp(target.get_hp() - random.randint(0, 5 + item.weight))
            action.actionPointCost += item.weight
            self.__worldStatus.current_description["attack with " + item.item_name] = \
                "You attack " + target.get_name() + " with " + item.item_name
        # TODO add different output for different level of attack
    
    def check(self, action: Actions, target):
        # if target == "myself":
            
        # self.__player.get_action_point()
        # self.__player.get_hp()
        # self.__player.get_cash()
        # self.__player.get_items()
        # pass
        attributes = vars(target)
        self.__worldStatus.current_description["checked"] = attributes
        # TODO pass information to gpt to descript current infomation
        
    def equip(self, action: Actions, target: str):
        bag = self.__player.get_items()
        if target in bag.keys() and len(bag[target]) > 0:
            equipment = self.__player.get_equipment()
            if equipment != None:
                self.add_items(action, [equipment])
            self.__player.set_equipment(bag[target][-1])
            self.remove_items(action, {target: 1})
            self.__worldStatus.current_description["equip " + target] = \
                "You have equipped " + target
        else:
            self.__worldStatus.current_description["fail to equip " + target] = \
                "You do not have " + target
                
                
    def unequip(self, action: Actions, target: str):
        equipment = self.__player.get_equipment()
        if equipment != None:
            self.add_items(action, [equipment])
            self.__player.set_equipment(None)
            self.__worldStatus.current_description["unequip " + target] = \
                "You have unequipped " + target
        else:
            self.__worldStatus.current_description["fail to equip " + target] = \
                "You do not have anything equipped"
    
    def filled(self, action: Actions, container: str, liquid: str):
        pass
    
    def ActionCost(self, action: Actions):
        if action.actionName == "Move":
            self.__player.set_action_point(int(self.__player.get_action_point() -\
                action.actionPointCost * self.__worldStatus.move_dLevel))
            self.__player.set_thirst(int(self.__player.get_thirst() -\
                action.thirstCost * self.__worldStatus.move_dLevel))
        else:
            self.__player.set_action_point(int(self.__player.get_action_point() -\
                action.actionPointCost * self.__player.get_action_dLevel()))
            self.__player.set_thirst(int(self.__player.get_thirst() -\
                action.thirstCost * self.__player.get_action_dLevel()))
    
    
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
    def __init__(self, player: Player_status, preDefinedCommands: Commands, \
        worldStatus: globalInfo) -> None:
        """
        This class is pre-defined buff function in methods form
        """
        self.__player = player
        self.__preDefinedCommands = preDefinedCommands
        self.__worldStatus = worldStatus
        
    # def __pack_buff(self, buff_name, exe_function, exe_args, timeLimit, trigerred_Condition = None, \
    #     end_Condition = None) -> None:
    #     currentBuffs = self.__player.get_buffs()
    #     currentBuffs.append(Buff(buff_name, exe_function, exe_args, timeLimit, trigerred_Condition, \
    #         trigerred_Condition))
    #     self.__player.set_buffs(currentBuffs)
        
    def add_buff(self, buff: Buff, level: str= "low") -> None:
        currentBuffs = self.__player.get_buffs()
        if buff.buff_name not in currentBuffs.keys():
            newBuff = copy.deepcopy(buff)
            if level == "potential":
                newBuff.level = 0
            elif level == "low":
                newBuff.level = 1
            elif level == "median":
                newBuff.level = 2
            else:
                newBuff.level = 3
            
            currentBuffs[newBuff.buff_name] = newBuff
            self.__player.set_buffs(currentBuffs)
            
    def upgrade_buff(self, buffName: str) -> None:
        currentBuffs = self.__player.get_buffs()
        if buffName in currentBuffs.keys():
            currentBuffs[buffName].level += 1
            
        self.__player.set_buffs(currentBuffs)
    
    def remove_buff(self, buffName: str) -> None:
        currentBuffs = self.__player.get_buffs()
        if buffName in currentBuffs.keys():
            currentBuffs[buffName].end_Function(*currentBuffs[buffName].end_args)
            currentBuffs.pop(buffName)
        
    def hp_recovery(self, buff: Buff, amount: int):
        self.__preDefinedCommands.increase_hp(None, amount)
        
    def more_hp(self, buff: Buff, amount: int):
        self.__player.set_maximum_hp(self.__player.get_maximum_hp() + amount)
        
    def action_point_recovery(self, buff: Buff, amount: int):
        self.__preDefinedCommands.increase_action_point(None, amount)
        
    def more_ap(self, buff: Buff, amount):
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() + amount)
        
    def thirsty(self, buff: Buff):
        if buff.startedTime == 0:
            if buff.level == 1:
                self.__player.set_action_dLevel(self.__player.get_action_dLevel()*1.2)
            elif buff.level == 2:
                self.__player.set_action_dLevel(self.__player.get_action_dLevel()*1.5)
            elif buff.level == 3:
                self.__player.set_action_dLevel(self.__player.get_action_dLevel()*2)
                
    def de_thirsty(self, buff: Buff):
        if buff.level == 1:
            self.__player.set_action_dLevel(self.__player.get_action_dLevel()/1.2)
        elif buff.level == 2:
            self.__player.set_action_dLevel(self.__player.get_action_dLevel()/1.5)
        elif buff.level == 3:
            self.__player.set_action_dLevel(self.__player.get_action_dLevel()/2)
            
            
    def poisoning(self, buff: Buff):
        if buff.level == 1:
            self.__preDefinedCommands.decrease_action_point(None, "<random>")
            self.__preDefinedCommands.decrease_hp(None, "<random>")
        elif buff.level == 2:
            self.__preDefinedCommands.decrease_action_point(None, "<median random>")
            self.__preDefinedCommands.decrease_hp(None, "<median random>")
        elif buff.level == 3:
            self.__preDefinedCommands.decrease_action_point(None, "<high random>")
            self.__preDefinedCommands.decrease_hp(None, "<high random>")
            
    def emptyFunc(self, _):
        pass
    

class DefininedSys(): # 
    def __init__(self, preDefinedCommands: Commands, map_record: Map_information, buffEffect: character_effectSys) -> None:
        """
        All the defined content stored here\n\n
        `__def_items:` All the objects with same or differnt type here\n
        `__def_actions:` Defined player action, contains the name of action and the command will be executed in method form,
        usage example>>> <method stored in Actions>(*<arguments of method>), this would call the method\n
        """
        self.__map_record = map_record
        self.__buffEffect = buffEffect
        
        self.__def_items = [
            # LandscapeFeature
            LandscapeFeature("stream", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=10, eatable=True, freshness=-1), 
            LandscapeFeature("rocks", {"sea": 10, "land": 12, "forest": 12, "beach": 10, \
                "river": 8, "desert": 5, "mountain": 5, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=10, eatable=True, freshness=72), 
            LandscapeFeature("grass", {"sea": 0, "land": 12, "forest": 15, "beach": 0, \
                "river": 8, "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 12}, \
                AP_recovery=2, eatable=False, freshness=20),
            LandscapeFeature("aloe vera", {"sea": 0, "land": 12, "forest": 5, "beach": 4, \
                "river": 2, "desert": 12, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, \
                AP_recovery=2, eatable=True, freshness=20),
            
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
            Transportation("wooden boat", {"sea": 2, "land": 0, "forest": 0, "beach": 8, "river": 5, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 0}, \
                suitablePlace={"sea"}, APReduce=0.5),
            
            # Food
            Food("bread", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=15, eatable=True, freshness=20, thirst_satisfied=-20),
            Food("raw fish", {"sea": 15, "land": 0, "forest": 0, "beach": 1, "river": 12, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=2, \
                AP_recovery=5, eatable=False, freshness=24, thirst_satisfied=20),
            Food("grilled fish", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=2, \
                AP_recovery=15, eatable=True, freshness=24, thirst_satisfied=10),
            Food("berries", {"sea": 0, "land": 5, "forest": 10, "beach": 0, "river": 5, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 5, "grassland": 12}, weight=1, \
                AP_recovery=5, eatable=True, freshness=18, thirst_satisfied=10),
            Food("potato", {"sea": 0, "land": 5, "forest": 2, "beach": 0, "river": 2, \
                "desert": 12, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 12}, weight=1, \
                AP_recovery=10, eatable=False, freshness=50, thirst_satisfied=-5),
            Food("grilled potato", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=1, \
                AP_recovery=10, eatable=True, freshness=72, thirst_satisfied=-10),
            Food("raw venison", {"sea": 0, "land": 1, "forest": 2, "beach": 0, "river": 0, \
                "desert": 12, "mountain": 5, "highland snowfield": 5, "town": 0, "grassland": 15}, weight=5, \
                AP_recovery=20, eatable=False, freshness=19, thirst_satisfied=50),
            Food("grilled venison", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=5, \
                AP_recovery=30, eatable=True, freshness=29, thirst_satisfied=20),
            Food("vegetable soup", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
                "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=5, \
                AP_recovery=30, eatable=True, freshness=15, thirst_satisfied=50, commandSuitable="have"),
            Food("stew", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, "desert": 0, \
                "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, weight=10, \
                AP_recovery=50, eatable=True, freshness=15, thirst_satisfied=30, commandSuitable="have"),
            
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

        
        self.__pre_def_events_frameWork = {
            "survival crisis": [PassivityEvents("", "survival crisis", \
                "low action point", ["increase action point", "increase maximum action point"], \
                    ["decrease action point", "decrease maximum action point"], -1, "", \
                        lambda player, mapInfo, events, worldStatus: player.get_action_point() < 40), 
                        PassivityEvents("", "survival crisis", \
                "low health point", ["increase health point", "increase maximum health point"], \
                    ["decrease health point", "decrease maximum health point"], -1, "", \
                        lambda player, mapInfo, events, worldStatus: player.get_hp() < 40), 
                        PassivityEvents("", "survival crisis", "high thirst level", \
                ["increase action point", "increase maximum action point", "remove thirsty status"], \
                    ["decrease action point", "decrease maximum action point", "add thirsty status(low)", "upgrade thirsty status"], -1, "", \
                        lambda player, mapInfo, events, worldStatus: player.get_thirst() < 40),
                        PassivityEvents("", "survival crisis", lambda player, mapInfo, events, worldStatus: "consume uneatable food" + str(worldStatus.player_dangerAction["consume uneatable food"]), \
                ["increase action point", "increase maximum action point", "remove thirsty status"], \
                    ["decrease health point", "add potential poisoning status", "add thirsty status(low)", "upgrade poisoning status"], 5, "", \
                        lambda player, mapInfo, events, worldStatus: "consume uneatable food" in worldStatus.player_dangerAction.keys())
            ],
            "disaster": [
                DisasterEvents("", "disaster", "dust storm occur", \
                ["decrease action point", "decrease health point", "decrease maximum health point"], 3, "", \
                    lambda player, mapInfo, events, worldStatus: ((mapInfo.currentLocation.location_name == "desert" and random.random() < 0.5) or \
                        (mapInfo.currentLocation.location_name == "land" and random.random() < 0.3)), 
                    lambda player, mapInfo, events, worldStatus: (mapInfo.currentLocation.location_name != "desert" and mapInfo.currentLocation.location_name != "land")),
            ]
        }
        
        # self.__pre_def_events = {
        #     "survival crisis": {"action point": PassivityEvents("Exhausted","survival crisis", \
        #         "low action point in anywhere", ["increase action point", \
        #             "increase maximum action point"], ["decrease action point", \
        #             "decrease maximum action point"], 3, "I'm so tired, I need have a rest!")}
        # }
        
        self.__def_actions = {
            "Move": Actions("Move", [preDefinedCommands.move, preDefinedCommands.ActionCost], \
                [[],[]], 5, 4, ["move"]),
            "Rest": Actions("Rest", [preDefinedCommands.rest, preDefinedCommands.ActionCost], \
                [[],[]], 0, 0, ["rest"]),
            "Take": Actions("Take", [preDefinedCommands.pickUp, preDefinedCommands.ActionCost], \
                [[],[]], 2, 1, ["take"]),
            "Equip": Actions("Equip", [preDefinedCommands.equip, preDefinedCommands.ActionCost], \
                [[],[]], 1, 0, ["equip"]),
            "Unequip": Actions("Unequip", [preDefinedCommands.unequip, preDefinedCommands.ActionCost], \
                [[],[]], 1, 0, ["unequip"]),
            "Check": Actions("Check", [preDefinedCommands.check, preDefinedCommands.ActionCost], \
                [[],[]], 2, 1, ["check"]),
            "Consume": Actions("Consume", [preDefinedCommands.consume, preDefinedCommands.ActionCost], \
                [[],[]], 1, 1, ["eat", "drink"]),
            "Fill": Actions("Fill", [preDefinedCommands.filled, preDefinedCommands.ActionCost], \
                [[],[]], 1, 0, ["fill"]),
            "Talk": Actions("Talk", [preDefinedCommands.talk, preDefinedCommands.ActionCost], \
                [[],[]], 1, 2, ["talk"])
        }
        ["Take all", "Take lamb leg", "Take glass water bottle", "Equip sword", "Unequip weapon crafting bench", "Check player", "Check all", "Check stream", "drink stream", "eat soup", "eat grilled fish", "fill glass water bottle with stream", "get on wooden boat", "get off wooden boat", "talk to Bob"]
        
        self.__def_buff = { # TODO add end condition
            "thirsty": Buff("thirsty", exe_function= self.__buffEffect.thirsty, \
                exe_args= list(), timeLimit= -1, end_Function= self.__buffEffect.de_thirsty, \
                    end_args=list(), trigerred_Condition=lambda player, mapInfo, worldStatus: player.get_thirst() <= 0, \
                        end_Condition=lambda player, mapInfo, worldStatus: player.get_thirst() > 0, start_level = "high"),
            "poisoning": Buff("poisoning", exe_function= self.__buffEffect.poisoning, \
                exe_args= list(), timeLimit= 5, end_Function= self.__buffEffect.emptyFunc, \
                    end_args=list())
        }
        
        self.__eventCommandMap = {
            "increase action point": ("increase action point", (None, "<random>")),
            "decrease action point": ("decrease action point", (None, "<random>")),
            "increase maximum action point": ("increase maximum action point", (None, "<random>")),
            "decrease maximum action point": ("decrease maximum action point", (None, "<random>")),
            "add thirsty status(low)": ("add buff", (self.__def_buff["thirsty"], "low")),
            "add thirsty status(median)": ("add buff", (self.__def_buff["thirsty"], "median")),
            "add thirsty status(high)": ("add buff", (self.__def_buff["thirsty"], "high")),
            "upgrade thirsty status": ("upgrade buff" , ("thirsty", )), 
            "remove thirsty status": ("remove buff", ("thirsty",)),
            "add potential poisoning status": ("add buff", (self.__def_buff["poisoning"], "potential")),
            "add poisoning status(low)": ("add buff", (self.__def_buff["poisoning"], "low")),
            "add poisoning status(median)": ("add buff", (self.__def_buff["poisoning"], "median")),
            "add poisoning status(high)": ("add buff", (self.__def_buff["poisoning"], "high")),
            "upgrade poisoning status": ("upgrade buff" , ("poisoning", )), 
            "remove poisoning status": ("remove buff", ("poisoning",)),
        }
        
        self.__commandTranslate = {
            "increase action point": preDefinedCommands.increase_action_point,
            "decrease action point": preDefinedCommands.decrease_action_point,
            "increase maximum action point": preDefinedCommands.increase_maximum_action_point,
            "decrease maximum action point": preDefinedCommands.decrease_maximum_action_point,
            "add buff": self.__buffEffect.add_buff,
            "remove buff": self.__buffEffect.remove_buff,
            "upgrade buff": self.__buffEffect.upgrade_buff,
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
            definitely_Object = self.__terrain_type[terrain].definitely_Object
            possible_Object = self.__terrain_type[terrain].possible_Object
            weight = self.__terrain_type[terrain].possible_Object_Weight
            for item in self.__def_items:
                if item.possibleWeight[terrain] >= 20:
                    definitely_Object = np.append(definitely_Object, item)
                    # print(definitely_Object[-1].item_name)
                    # self.__terrain_type[terrain].definitely_Object.append(item)
                elif item.possibleWeight[terrain] > 0:
                    possible_Object = np.append(possible_Object, item)
                    weight = np.append(weight, item.possibleWeight[terrain])
            
            self.__terrain_type[terrain].definitely_Object = definitely_Object
            self.__terrain_type[terrain].possible_Object = possible_Object
            self.__terrain_type[terrain].possible_Object_Weight = weight
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
    
    def get_buff(self) -> dict[str, Buff]:
        return self.__def_buff
    
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
