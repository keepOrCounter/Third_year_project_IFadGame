import numpy as np
# from typing import Callable
# from interactionSys import OutputGenerator

class Items():
    def __init__(self, item_name: str, possibleWeight = {}, use=None, weight = 1):
        """
            `item_name (str)`: name for player or gpt to recognized
            `possibleWeight (dict)`: possibility of showing up in different location, \
                from 0 to 20
            `use (method)`: command should be called after use this item
            `weight (int)`: the weight of this item, from 1 to infinite, initial player \
                could carry 20 weight of items
        """
        self.item_name = item_name
        # self.category = category
        
        self.possibleWeight = possibleWeight
        self.use = use
        self.weight = weight
        
class Food(Items):
    def __init__(self, item_name: str, possibleWeight: dict[str, int], use, weight : int, \
        item_energy_recovery: int, state = 0, freshness = -1, thirst = 0):
        """
            `item_energy_recovery (int)`: the amount of action point player can recovery when \
                making consume this food
            `eatable (bool)`: Whether this food is safe for eat
        """
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.item_energy_recovery = item_energy_recovery
        # self.eatable = eatable
        self.state = state
        self.freshness = freshness
        self.thirst = thirst
        
class Tool(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), use=None, weight=1, \
        durability = 1):
        """
            `durability (int)`: the turns number this tool can be used
        """
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.durability = durability
        
class LandscapeFeature(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), use=None, weight=2**10, \
        item_energy_recovery = 0, eatable=False):
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.item_energy_recovery = item_energy_recovery
        self.eatable = eatable
        
class EnvironmentElement(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), use=None, weight=2**10, \
        item_energy_recovery = 0, eatable=False):
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.item_energy_recovery = item_energy_recovery
        self.eatable = eatable
        
class Transportation(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), use=None, weight=2**10, \
        suitablePlace = set(), APReduce = 1):
        """
            `suitablePlace (set)`: the place this transportation can be rod
            `APReduce (int)`: to what precentage of action point would be reduce \
                when moving on a place, from 0 to 1
        """
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.suitablePlace = suitablePlace
        self.APReduce = APReduce
        
class Weapon(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), use=None, weight=1, \
        attack = 0, durability = 1):
        """
            `durability (int)`: the turns number this tool can be used
            `attack (int)`: the hp value would reduce on target when player use this weapon
        """
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.durability = durability
        self.attack = attack
        

class Container(Items):
    def __init__(self, item_name: str, possibleWeight=dict(), use=None, weight=1, \
        capacity = 1):
        """
            `capacity (int)`: the turn number the liquide inside can be used
        """
        super().__init__(item_name, possibleWeight, use, weight)
        
        self.capacity = capacity


class Events():
    # TODO Change event description format
    def __init__(self, eventName: str, eventType: str, triggered_reason: str, \
        possible_reward: list, possible_penalty: list, time_limit: int, description: str) -> None:
        
        self.eventName = eventName
        self.eventType = eventType
        # self.succeedCondition = succeedCondition
        self.triggered_reason = triggered_reason
        self.possible_reward = possible_reward
        self.possible_penalty = possible_penalty
        self.time_limit = time_limit
        
        self.description = description
        
        self.currentAction = ""
        self.current_location = ""
        self.moving_tool = []
        self.play_current_status = ""
        
        self.triggered_time = 0
        # self.gpt_required = gpt_required
        

class Actions():
    def __init__(self, actionName: str, command_executed: list[tuple]) -> None:
        """
            `actionName (str)`: related to player input
            `command_executed (list[tuple])`: a list of method and its arguments would be called when player make this action
        """
        self.actionName = actionName
        self.command_executed = command_executed
        
class Location():
    def __init__(self, location_name:str, x:int, y:int, objects:list[Items] = [], \
        description: str= "") -> None:
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
        self.description = description
        self.x = x
        self.y = y


class Buff():
    def __init__(self, buff_name: str, exe_function, exe_args: tuple) -> None:
        self.buff_name = buff_name
        self.exe_function = exe_function
        self.exe_args = exe_args


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
        
        self.definitely_Object = list()
        self.possible_Object = list()
        self.possible_Object_Weight = list()


class Player_status():
    def __init__(self, currentLocation:list[int,int] = [0,0], items:dict[str, list[Items]] = dict(), \
        hp: int = 100, maximum_hp: int = 100, maximum_action_point: int = 100, \
            action_point: int = 100, currentAction: Actions = None, cash:int = 0, \
                buff:list[Buff] = []) -> None:
        """ `__currentLocation:` player coordinate [x,y]\n
            `items:` items in bag\n
            `action_point:` energy bar of player
        """
        self.__currentLocation = currentLocation
        self.__lastLocation = [None, None]
        self.__items = items
        self.__hp = hp
        self.__maximum_hp = maximum_hp
        self.__action_point = action_point
        self.__maximum_action_point = maximum_action_point
        self.__currentAction = currentAction
        self.__cash = cash
        self.__buff = buff
        self.__APrecovery = 10
    
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
        
    def get_buffs(self) -> list[Buff]:
        return self.__buff
    
    def set_buffs(self, newBuffs: list[Buff]) -> None:
        self.__buff = newBuffs
        
    def get_APrecovery(self) -> int:
        return self.__APrecovery
    
    def set_APrecovery(self, newAPrecovery: int) -> None:
        self.__APrecovery = newAPrecovery

        
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

    def get_visitedPlace(self) -> dict:
        return self.__visitedPlace

    def set_visitedPlace(self, visitedPlace: dict):
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
        """
        self.eventsTriggered: list[Events]= []
        self.triggeredType = {
            "survival crisis": {"action point": True}
        }
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
        self.move_APCost = 5
        self.directionKnown = False
        self.move_dLevel = 1
        self.restPlace = True