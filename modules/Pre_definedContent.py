from status_record import *
import random



class Commands():
    def __init__(self, player: Player_status, map: Map_information) -> None:
        """
        This class is pre-defined commands in methods form
        """
        self.__player = player
        self.__map = map
        # self.__executionTranslator
        
    def move(self, target) -> None:
        """
        Move to specific direction or target place
        """
        action_point_changed = 0
        if self.__map.get_current_area_type() == 1:
            action_point_changed = -5
        elif self.__map.get_current_area_type() == 0:
            if False:
                pass
            else:
                action_point_changed = -20
        if target == "North":
            x, y = self.__player.get_currentLocation()
            self.__player.set_currentLocation(x, y+1)
        elif target == "South":
            x, y = self.__player.get_currentLocation()
            self.__player.set_currentLocation(x, y-1)
        elif target == "East":
            x, y = self.__player.get_currentLocation()
            self.__player.set_currentLocation(x+1, y)
        elif target == "West":
            x, y = self.__player.get_currentLocation()
            self.__player.set_currentLocation(x-1, y)
        else:
            self.__player.set_currentLocation(*target)
        self.__player.set_action_point(self.__player.get_action_point() +\
            action_point_changed)
        
    def action_point_adjust(self, value: int) -> None:
        """
        Recovery or consume action point
        """
        self.__player.set_action_point(self.__player.get_action_point() + value)
        
    def hp_adjust(self, value: int) -> None:
        """
        Recovery or reduce health point
        """
        self.__player.set_hp(self.__player.get_hp() + value)
        
    def add_items(self, items: list[Items]) -> None:
        """
        Add one or more items to player's package
        """
        self.__player.set_items(self.__player.get_items() + items)
        
    def remove_items(self, items: list[Items]) -> None:
        """
        Remove one or more items to player's package
        """
        
        self.__player.set_items(self.__player.get_items() + items)
        
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
    
class character_effectSys():
    def __init__(self, player: Player_status, preDefinedCommands: Commands) -> None:
        """
        This class is pre-defined buff function in methods form
        """
        self.__player = player
        self.__preDefinedCommands = preDefinedCommands
        
    def hp_recovery(self, amount):
        self.__preDefinedCommands.hp_adjust(amount)
        
    def more_hp(self, amount):
        self.__player.set_maximum_hp(self.__player.get_maximum_hp() + amount)
        
    def action_point_recovery(self, amount):
        self.__preDefinedCommands.action_point_adjust(amount)
        
    def more_ap(self, amount):
        self.__player.set_maximum_action_point(self.__player.get_maximum_action_point() + amount)

class DefininedSys(): # 
    def __init__(self, preDefinedCommands: Commands) -> None:
        """
        All the defined content stored here\n\n
        `__def_items:` All the objects with same or differnt type here\n
        `__def_actions:` Defined player action, contains the name of action and the command will be executed in method form,
        usage example>>> <method stored in Actions>(*<arguments of method>), this would call the method\n
        """
        self.__def_items = [
            # Items("Campfire", 20, "Items"),
            Items("Stream", 10, "Landscape Features"),
            # Items("Shelter", 30, "Items"),
            Items("Bread", 15, "Items"),
            Items("Traps", 10, "Items"),
            Items("First Aid Kit", 25, "Items"),
            # Items("Toolkits", 15),
            # Items("Maps", 5),
            Items("Edible Plants", 10, "Items"),
            # Items("Animal Tracks", 5),
            Items("Firewood", 0, "Items"),
            Items("Rocks", 0, "Landscape Features"),
            # Items("Wildlife", 20),
            # Items("Weather Conditions", 0),
            # Items("Hidden Stashes", 15),
            # Items("Footprints", 0),
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
            "Move West": Actions("Move West", [(preDefinedCommands.move, ("West",))])
        }
        
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
        
