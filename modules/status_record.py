import numpy as np
# from typing import Callable
# from interactionSys import OutputGenerator


class Items():
    def __init__(self, item_name: str, possibleWeight = {}, weight = 1, commandSuitable = "use"):
        """
            `item_name (str)`: name for player or gpt to recognized
            `possibleWeight (dict)`: possibility of showing up in different location, \
                from 0 to 20
            `weight (int)`: the weight of this item, from 1 to infinite, initial player \
                could carry 20 weight of items
        """
        self.item_name = item_name
        self.codeName = item_name
        self.category = "item"
        
        self.possibleWeight = possibleWeight
        self.weight = weight
        
        self.commandSuitable = commandSuitable
        
class Food(Items):
    def __init__(self, item_name: str, possibleWeight: dict[str, int], weight : int, \
        AP_recovery: int, eatable = True, freshness = -1, thirst_satisfied = 0, commandSuitable = "eat"):
        """
            `AP_recovery (int)`: the amount of action point player can recovery when \
                making consume this food
            `eatable (bool)`: Whether this food is safe for eat
        """
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.AP_recovery = AP_recovery
        self.eatable = eatable
        # self.state = state
        self.freshness = freshness
        self.thirst_satisfied = thirst_satisfied
        
        self.commandSuitable = commandSuitable
        
        self.category = "food"
        
class Tool(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=1, \
        durability = 1, commandSuitable = "use"):
        """
            `durability (int)`: the turns number this tool can be used
        """
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.durability = durability
        
        self.category = "tool"
        
class LandscapeFeature(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=2**10, \
        AP_recovery = 0, eatable=False, freshness = -1, commandSuitable = "break"):
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.AP_recovery = AP_recovery
        self.eatable = eatable
        self.freshness = freshness
        
        self.category = "landscape feature"
        
class EnvironmentElement(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=2**10, \
        AP_recovery = 0, eatable=False, commandSuitable = "collect"):
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.AP_recovery = AP_recovery
        self.eatable = eatable
        
        self.category = "environment element"
        
class Transportation(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=2**10, \
        suitablePlace = set(), APReduce = 1, commandSuitable = "by"):
        """
            `suitablePlace (set)`: the place this transportation can be rod
            `APReduce (int)`: to what precentage of action point would be reduce \
                when moving on a place, from 0 to 1
        """
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.suitablePlace = suitablePlace
        self.APReduce = APReduce
        
        self.category = "transportation"
        
class Weapon(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=1, \
        attack = 0, durability = 1, commandSuitable = "with"):
        """
            `durability (int)`: the turns number this tool can be used
            `attack (int)`: the hp value would reduce on target when player use this weapon
        """
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.durability = durability
        self.attack = attack
        
        self.category = "weapon"
        

class Container(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=1, \
        capacity = 1, commandSuitable = "fill"):
        """
            `capacity (int)`: the turn number the liquide inside can be used
        """
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.capacity = capacity
        self.currentCapacity = 0
        
        self.oldName = item_name
        
        self.category = "container"
        
class Liquid(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), weight=1, \
        eatable=False, commandSuitable = "fill", thirst_satisfied = 0):
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        
        self.eatable = eatable
        self.thirst_satisfied = thirst_satisfied
        
        self.category = "liquid"
        

class Suit(Items):
    def __init__(self, item_name: str, possibleWeight={}, weight=1, commandSuitable="use", durability = 1):
        super().__init__(item_name, possibleWeight, weight, commandSuitable)
        self.durability = durability
        
        self.category = "Suit"
        

class Events():
    # TODO Change event description format
    def __init__(self, eventName: str, eventType: str, time_limit: int, \
        description: str) -> None:
        
        self.eventName = eventName
        self.eventType = eventType
        # self.succeedCondition = succeedCondition
        self.time_limit = time_limit
        
        self.description = description
        
        self.currentAction = ""
        self.current_location = ""
        self.moving_tool = []
        self.play_current_status = ""
        
        self.triggered_time = 0
        
        # self.triggered = False
        # self.gpt_required = gpt_required
        
class PassivityEvents(Events):
    def __init__(self, eventName: str, eventType: str, triggered_reason, \
        possible_reward: list, possible_penalty: list, time_limit: int, description: str, \
            triggered_condition) -> None:
        """
        `triggered_condition`: a function that receive player, map information \
            as argument and return boolen based on these information
        """
        super().__init__(eventName, eventType, time_limit, description)
        self.triggered_reason = triggered_reason
        self.possible_reward = possible_reward
        self.possible_penalty = possible_penalty
        
        self.triggered_condition = triggered_condition
        
class DisasterEvents(Events):
    def __init__(self, eventName: str, eventType: str, triggered_reason, \
        possible_penalty: list, time_limit: int, description: str, \
            triggered_condition, end_condition) -> None:
        """
        `triggered_condition`: a function that receive player, map information \
            as argument and return boolen based on these information
        """
        super().__init__(eventName, eventType, time_limit, description)
        self.triggered_reason = triggered_reason
        # self.possible_reward = possible_reward
        self.possible_penalty = possible_penalty
        
        self.triggered_condition = triggered_condition
        self.end_condition = end_condition

class Actions():
    def __init__(self, actionName: str, command_executed: list, command_args: list[list], \
        actionPointCost: int, thirstCost: int, tag: list[str]) -> None:
        """
            `actionName (str)`: related to player input
            `command_executed (list[tuple])`: a list of method and its arguments would be called when player make this action
            `actionPointCost (int)`: basic action Point Cost on player
            `thirstCost (int)`: basic reduce on player's thirst level
        """
        self.actionName = actionName
        self.command_executed = command_executed
        
        self.actionPointCost = actionPointCost
        self.thirstCost = thirstCost

        self.tag = tag
        
        self.command_args = []
        for x in command_args:
            self.command_args.append([self] + x)
        
        
class Buff():
    def __init__(self, buff_name: str, exe_function, exe_args: list, timeLimit: int, \
        end_Function, end_args: list, trigerred_Condition = False, end_Condition = False, start_level = "potential") -> None:
        
        self.buff_name = buff_name
        self.exe_function = exe_function
        
        self.end_Function = end_Function
        
        self.timeLimit = timeLimit
        self.startedTime = 0
        
        self.trigerred_Condition = trigerred_Condition
        self.end_Condition = end_Condition
        
        self.level = 0
        self.start_level = start_level
        
        self.exe_args = tuple([self] + exe_args)
        self.end_args = tuple([self] + end_args)
        
        # a = lambda: (10>np.random.randint(0,20) and 5< np.random.randint(0,20))
        
        # dynamic_args = lambda self: (self.buff_name, self.timeLimit, self.startedTime)

        
        
class NPCs():
    def __init__(self, NPC_name: str, hp: int, maximum_hp: int, action_point: int, \
        maximum_action_point: int, thirst_satisfied: int, maximum_thirst_satisfied: int, \
            relationship_with_player: int, equipments: Items):
        self.NPC_name = NPC_name
        self.category = "NPCs"
        
        self.codeName = NPC_name
        
        self.__hp = hp
        self.__maximum_hp = maximum_hp
        self.__action_point = action_point
        self.__maximum_action_point = maximum_action_point
        self.__currentAction: str = None
        self.__buff: dict[str, Buff] = dict()

        self.__action_dLevel: float = 1
        self.__thirst_satisfied = thirst_satisfied
        self.__maximum_thirst_satisfied = maximum_thirst_satisfied
        
        self.relationship_with_player = relationship_with_player
        
        self.__equipment = equipments
        
        
    def get_hp(self) -> int:
        return self.__hp
    
    def set_hp(self, hp: int) -> None:
        self.__hp = hp

    def get_action_point(self) -> int:
        return self.__action_point
    
    def set_action_point(self, action_point: int) -> None:
        self.__action_point = action_point

    def get_maximum_hp(self) -> int:
        return self.__maximum_hp
    
    def set_maximum_hp(self, new_hp_limit: int) -> None:
        self.__maximum_hp = new_hp_limit

    def get_maximum_action_point(self) -> int:
        return self.__maximum_action_point
    
    def set_maximum_action_point(self, new_action_point_limit: int) -> None:
        self.__maximum_action_point = new_action_point_limit
        
    def get_thirst(self) -> int:
        return self.__thirst_satisfied
    
    def set_thirst(self, thirst_satisfied: int) -> None:
        self.__thirst_satisfied = thirst_satisfied
        
    def get_maximum_thirst(self) -> int:
        return self.__maximum_thirst_satisfied
    
    def set_maximum_thirst(self, maximum_thirst_satisfied: int) -> None:
        self.__maximum_thirst_satisfied= maximum_thirst_satisfied
        
    def get_equipment(self) -> Items:
        return self.__equipment
    
    # def set_equipment(self, equipment: Items) -> None:
    #     self.__equipment = equipment
    
    def get_action_dLevel(self) -> float:
        return self.__action_dLevel
    
    def set_action_dLevel(self, action_dLevel: float) -> None:
        self.__action_dLevel = action_dLevel
        
    def get_buffs(self) -> dict[str, Buff]:
        return self.__buff
    
    def set_buffs(self, newBuffs: dict[str, Buff]) -> None:
        self.__buff = newBuffs
        
    def get_currentAction(self) -> Actions:
        return self.__currentAction
    
    def set_currentAction(self, newAction: Actions) -> None:
        self.__currentAction = newAction



class humanNPC(NPCs):
    def __init__(self, NPC_name: str, hp: int, maximum_hp: int, action_point: int, \
        maximum_action_point: int, thirst_satisfied: int, maximum_thirst_satisfied: int, relationship_with_player: int, \
            equipments: Items, age: int, character: str, gender: str, commandSuitable = "talk", \
                items:dict[str, list[Items]] = dict(), cash: int = 0):
        super().__init__(NPC_name, hp, maximum_hp, action_point, maximum_action_point, thirst_satisfied, \
            maximum_thirst_satisfied, relationship_with_player, equipments)

        self.age = age
        self.character = character
        self.gender = gender

        self.commandSuitable = commandSuitable
        
        self.category = "human"
        self.items = items
        self.__cash = cash
        
    def get_cash(self) -> int:
        return self.__cash
    
    def set_cash(self, newAmount: int) -> None:
        self.__cash = newAmount
        
        
        
class Location():
    def __init__(self, location_name:str, x:int, y:int, objects:list[Items] = [], \
        npcs:list[NPCs] = [],description: str= "") -> None:
        """`location_name:` name of current terrain\n
            `objects:` items at current place\n
            `description:` description generated by GPT, only for visited places, in this format: \n
{
	"location name": <location name>,
	"Description of current and surrounding locations": <What is surrounding and where player at>,
	"Landscape Features description": <Any specific Landscape>, 
	"Items description": <Any items>
}\n
            `x\y: ` locations' coordinate
        """
        self.location_name = location_name
        self.objects = objects
        self.npcs = npcs
        self.description = description
        self.x = x
        self.y = y
        
        self.north: str = "<unknown>"
        self.south: str = "<unknown>"
        self.east: str = "<unknown>"
        self.west: str = "<unknown>"



class Terrain_type():
    def __init__(self, terrain_name: str, terrain_ID: int, possibilityOfGenerate: float, \
        move_dLevel: int, rules, extraArgs, allowedAppearUpon: int, visualizedColor: list[int] = [0, 0, 0]) -> None:
        
        self.terrain_name = terrain_name
        self.possibilityOfGenerate = possibilityOfGenerate
        self.rules = rules
        self.move_dLevel = move_dLevel
        self.extraArgs = extraArgs
        self.terrain_ID = terrain_ID
        self.allowedAppearUpon = allowedAppearUpon
        self.visualizedColor = visualizedColor
        
        self.definitely_Object: np.ndarray[Items] = np.array([])
        self.possible_Object: np.ndarray[Items] = np.array([])
        self.possible_Object_Weight: np.ndarray[int] = np.array([]).astype(int)


class Player_status():
    def __init__(self, currentLocation:list[int,int] = [0,0], items:dict[str, list[Items]] = dict(), \
        hp: int = 100, maximum_hp: int = 100, maximum_action_point: int = 100, \
            action_point: int = 100, currentAction: Actions = None, cash:int = 0, \
                buff:dict[str, Buff] = dict(), thirst_satisfied:int = 100, maximum_thirst_satisfied:int = 100) -> None:
        """ `__currentLocation:` player coordinate [x,y]\n
            `items:` items in bag\n
            `action_point:` energy bar of player
        """
        self.__currentLocation = currentLocation
        self.__lastLocation:list[int] = [None, None]
        self.__items = items
        self.__hp = hp
        self.__maximum_hp = maximum_hp
        self.__action_point = action_point
        self.__maximum_action_point = maximum_action_point
        self.__currentAction = currentAction
        self.__cash = cash
        self.__buff = buff
        self.__APrecovery = 10
        self.__thirst_satisfied = thirst_satisfied
        self.__maximum_thirst_satisfied = maximum_thirst_satisfied
        
        self.__transportation_used: Items = None
        self.__suit: Items = Suit("old shirt", {"sea": 0, "land": 0, "forest": 0, "beach": 0, "river": 0, \
            "desert": 0, "mountain": 0, "highland snowfield": 0, "town": 0, "grassland": 0}, 2)
        self.__equipment: Items = None
        
        self.__action_dLevel: float = 1
        # self.action_dLevel: float = 1
    
    def get_currentLocation(self) -> tuple[int]:
        return (self.__currentLocation[0], self.__currentLocation[1])
    
    def set_currentLocation(self, x:int, y:int) -> None:
        self.__currentLocation[0] = x
        self.__currentLocation[1] = y
        
    def get_lastLocation(self) -> tuple[int]:
        return (self.__lastLocation[0], self.__lastLocation[1])
    
    def set_lastLocation(self, x:int, y:int) -> None:
        self.__lastLocation[0] = x
        self.__lastLocation[1] = y

    def get_items(self) -> dict[str, list[Items]]:
        return self.__items
    
    def set_items(self, items: dict[str, list[Items]]) -> None:
        self.__items = items

    def get_hp(self) -> int:
        return self.__hp
    
    def set_hp(self, hp: int) -> None:
        self.__hp = hp

    def get_action_point(self) -> int:
        return self.__action_point
    
    def set_action_point(self, action_point: int) -> None:
        self.__action_point = action_point

    def get_maximum_hp(self) -> int:
        return self.__maximum_hp
    
    def set_maximum_hp(self, new_hp_limit: int) -> None:
        self.__maximum_hp = new_hp_limit

    def get_maximum_action_point(self) -> int:
        return self.__maximum_action_point
    
    def set_maximum_action_point(self, new_action_point_limit: int) -> None:
        self.__maximum_action_point = new_action_point_limit

    def get_currentAction(self) -> Actions:
        return self.__currentAction
    
    def set_currentAction(self, newAction: Actions) -> None:
        self.__currentAction = newAction

    def get_cash(self) -> int:
        return self.__cash
    
    def set_cash(self, newAmount: int) -> None:
        self.__cash = newAmount
        
    def get_buffs(self) -> dict[str, Buff]:
        return self.__buff
    
    def set_buffs(self, newBuffs: dict[str, Buff]) -> None:
        self.__buff = newBuffs
        
    def get_APrecovery(self) -> int:
        return self.__APrecovery
    
    def set_APrecovery(self, newAPrecovery: int) -> None:
        self.__APrecovery = newAPrecovery
        
    def get_thirst(self) -> int:
        return self.__thirst_satisfied
    
    def set_thirst(self, thirst_satisfied: int) -> None:
        self.__thirst_satisfied = thirst_satisfied
        
    def get_maximum_thirst(self) -> int:
        return self.__maximum_thirst_satisfied
    
    def set_maximum_thirst(self, maximum_thirst_satisfied: int) -> None:
        self.__maximum_thirst_satisfied= maximum_thirst_satisfied

    def get_action_dLevel(self) -> float:
        return self.__action_dLevel
    
    def set_action_dLevel(self, action_dLevel: float) -> None:
        self.__action_dLevel = action_dLevel
        
    def get_transportation(self) -> Items:
        return self.__transportation_used
    
    def set_transportation(self, transportation: Items) -> None:
        self.__transportation_used = transportation
        
    def get_suit(self) -> Items:
        return self.__suit
    
    def set_suit(self, suit: Items) -> None:
        self.__suit = suit
        
    def get_equipment(self) -> Items:
        return self.__equipment
    
    def set_equipment(self, equipment: Items) -> None:
        self.__equipment = equipment
        
class Map_information():
    def __init__(self, current_area_type: int = 0, currentMap: np.ndarray[str] = [], \
        map_size: tuple[int] = (20, 20)) -> None:
        """`current_area_type:` used for generate map, 0 for sea area, 1 for land \
            area, affect the probability of different terrain\n
            `visitedPlace:` Place has visited in this form: {(x, y): "Location_object"}\n
            `IMPORTANT!!! map_size: `opposite with coordinate system \
                tuple in `(row, cols)`, height and width of map, `(y, x)`
        """
        self.__visitedPlace = {} # {(x, y): "Location_object"}, update every turn
        self.__current_area_type = current_area_type # update when entering new area
        self.__currentMap = currentMap # update when entering new area
        self.__map_size = map_size # rows, cols = y, x, never update!!!
        self.__init_map_coordinate = (0 - int(map_size[1]/2), 0 + int(map_size[0]/2)) # never update!!!
        self.__current_map_coordinate = (0 - int(map_size[1]/2), 0 + int(map_size[0]/2)) # update when entering new area
        self.__current_map_coordinate_Normalised = (0, 0)
        self.currentLocation: Location = None

    def get_current_area_type(self) -> int:
        return self.__current_area_type

    def set_current_area_type(self, current_area_type: int):
        self.__current_area_type = current_area_type

    def get_currentMap(self) -> np.ndarray[str]:
        return self.__currentMap

    def set_currentMap(self, currentMap: np.ndarray[str]):
        self.__currentMap = currentMap

    def get_visitedPlace(self) -> dict[tuple, Location]:
        return self.__visitedPlace

    def set_visitedPlace(self, visitedPlace: dict[tuple, Location]):
        self.__visitedPlace = visitedPlace

    def get_map_size(self) -> tuple[int]:
        return self.__map_size

    def get_init_map_coordinate(self) ->tuple[int]:
        return self.__init_map_coordinate
    
    def get_current_map_coordinate(self) ->tuple[int]:
        return self.__current_map_coordinate
    
    def set_current_map_coordinate(self, map_ccord: tuple[int]):
        self.__current_map_coordinate = map_ccord
        
    def get_current_map_coordinate_Normalised(self) ->tuple[int]:
        return self.__current_map_coordinate_Normalised
    
    def set_current_map_coordinate_Normalised(self, map_ccord_Normalised: tuple[int]):
        self.__current_map_coordinate_Normalised = map_ccord_Normalised

class EventsTriggered():
    def __init__(self) -> None:
        """
        This class is used to record and process the effects caused by events
        
        Attribute:
        `eventsHappening`: list of events are happening
        `eventsTriggered`: waiting list of events just occured, events in this list \
            would be push back to UnTriggered event list when their trigerred \
                conditions are no longer met
        `UnTriggered_passivity_events`: UnTriggered `PassivityEvents` list
        """
        self.eventsHappening: list[Events]= []
        
        self.eventsTriggered: list[Events]= [] # event happened once
        self.UnTriggered_passivity_events : list[PassivityEvents]= []
        # self.triggeredType = {
        #     "survival crisis": {"action point": True, "health point": True}
        # }
        # self.__descriptionGenerator = descriptionGenerator
        
    # def get_current_events(self) -> list[Events]:
    #     return self.__eventsTriggered
    
    # def add_new_event(self, newEvent: Events) -> None:
    #     self.__eventsTriggered.append(newEvent)
        


class globalInfo():
    def __init__(self) -> None:
        """determine any global dynamic variable
        
        `move_APCost`: Action point cost of every move
        `directionKnown`: Whether player know about direction
        `move_dLevel`: Difficulty of player move
        `restPlace`: Whether player can have a rest currently
        """
        # self.move_APCost = 5
        self.directionKnown = False
        self.move_dLevel: float = 1
        
        self.restPlace = True
        self.lastPlace: str = None
        
        self.player_dangerAction = dict()
        self.NPC_action_toPlayer = dict()
        
        self.freshNessChangedItems: list[Items] = list()
        
        self.current_description: dict[str, str] = dict()
        
        self.naturalAP_reduce: int = 2
        self.naturalThirst_reduce: int = 4
        
        self.skipTurn = False