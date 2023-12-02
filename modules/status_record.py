class Player_status():
    def __init__(self, currentLocation:list[int,int] = [0,0], items:list[str] = []) -> None:
        self.__currentLocation = currentLocation
        self.items = items
    
    def x_coordinate(self) -> int:
        
        return self.__currentLocation[0]
    
    def y_coordinate(self) -> int:
        
        return self.__currentLocation[1]
    
    def location_adder(self, delta_x:int, delta_y:int) -> None:
        self.__currentLocation[0] += delta_x
        self.__currentLocation[1] += delta_y
        
class Location():
    def __init__(self, location_name:str, x:int, y:int, objects:list = [], \
        description: str = "") -> None:
        
        self.location_name = location_name
        self.objects = objects
        self.description = description
        self.x = x
        self.y = y