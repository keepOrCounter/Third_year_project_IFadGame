from status_record import *

class DefininedSys(): # 
    def __init__(self) -> None:
        self.__def_items = [
            Items("Campfire", 20),
            Items("Water Source", 10),
            Items("Shelter", 30),
            Items("Food Storage", 15),
            Items("Traps", 10),
            Items("First Aid Kit", 25),
            Items("Toolkits", 15),
            Items("Maps", 5),
            Items("Edible Plants", 10),
            Items("Animal Tracks", 5),
            Items("Firewood", 10),
            Items("Rocks", 5),
            Items("Wildlife", 20),
            Items("Weather Conditions", 0),
            Items("Hidden Stashes", 15),
            Items("Footprints", 0),
            Items("Weapon Crafting Bench", 0)
        ]
        self.__def_events = []
        
        
    def get_items(self) -> list[Items]:
        return self.__def_items
    
    # Setter method for def_items
    def set_items(self, new_items: list[Items]):
        self.__def_items = new_items
