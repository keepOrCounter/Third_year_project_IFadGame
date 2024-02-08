import numpy as np
import cellpylib as cpl
from status_record import *
from Pre_definedContent import *
from interactionSys import OutputGenerator
import cv2
import random
import copy
import math

class MapGenerator():
    def __init__(self, player : Player_status, map_info: Map_information, defininedContent: DefininedSys) -> None:
        """
        Generate game map, just call `map_info_update()` to update any new information and \
            call `game_map_generation()` method to Generate a map, the map will be automaticly \
                record into `map_info` object
        """
        # self.textual_map = {}  # {x_coordinate : [Location_names(whose indices are y cordinate)]}
        # self.current_coord = {"x" : player.get_currentLocation()[0], "y" : player.get_currentLocation()[1]} # a copy of coord
        # self.current_main_terrain = 0 # land pattern, main terrain would be land mass
        self.__terrain_type = np.array(defininedContent.get_terrain_type())
        self.__player = player
        self.__map_info = map_info
        self.__generated_map = dict()
        self.__defininedContent = defininedContent
        
        init_start_point = np.random.randint(0,2**31) # generate init place
        init_start_point -= init_start_point % 100
        self.__random_seeds: np.ndarray = np.arange(init_start_point, init_start_point + 100)
        self.__used_seed = {init_start_point}
        
        self.player_surrounding = ["Front", "Left hand side", "Current location", "Right hand side", "Back"]
        

    def generate_random_map(self, rows: int, cols: int, land_prob: float=0.65, \
        area: tuple[int]= (0, 0))-> np.ndarray: # rows, cols = y, x
        if area not in self.__generated_map.keys():
            if self.__random_seeds.shape[0] == 0:
                init_start_point = None
                while init_start_point == None or init_start_point in self.__used_seed:
                    init_start_point = np.random.randint(0,2**31) # generate init place
                    init_start_point -= init_start_point % 100
                self.__random_seeds: np.ndarray = np.arange(init_start_point, init_start_point + 100)
                self.__used_seed.add(init_start_point)

            index_random = np.random.randint(0, self.__random_seeds.shape[0])
            map_seed = self.__random_seeds[index_random]
            self.__generated_map[self.__map_info.get_current_map_coordinate()] = map_seed
            self.__random_seeds = np.delete(self.__random_seeds, index_random)
        else:
            map_seed = self.__generated_map[self.__map_info.get_current_map_coordinate()]
        
        np.random.seed(map_seed) # use seed to get the same map for visited place
        return np.random.choice([0, 1], size=(rows, cols), p=[1-land_prob, land_prob])


    def random_map_update_8n_rule(self, cell_grid: np.ndarray, threshold: int):
        rows, cols = cell_grid.shape
        cell = cell_grid[int(rows/2), int(cols/2)]
        oneD = cell_grid.copy().flatten()
        number_of_1 = np.where(oneD == 1)[0].shape[0]
        number_of_0 = oneD.shape[0] - number_of_1

        if cell == 1:
            number_of_1 -= 1
        else:
            number_of_0 -= 1
        # print(cell_grid)
        # print(number_of_1)
        # print(number_of_0)
        # print(cell)
        # print("-------------------")
        if number_of_1 > threshold:
            cell = 1
        elif number_of_1 < threshold:
            cell = 0

        return cell
    
    def rule(self, grid, cell, time_step, mode="8_neighbours", threshold = 4):
        # print(grid, c, t)
        if mode == "8_neighbours":
            return self.random_map_update_8n_rule(grid, threshold)
        
    def game_map_generation(self, cellular_timesteps: int, convert_threshold: int, \
        mode="8_neighbours", area: tuple[int]= (0, 0)): # rows, cols = y, x

        # self.map_info_update()
        rows, cols = self.__map_info.get_map_size()
        if self.__map_info.get_current_area_type() == 1:
            random_map = self.generate_random_map(rows, cols, land_prob=0.65, area=area)
            random_map[0, :] = np.zeros((cols,))
            random_map[rows - 1, :] = np.zeros((cols,))
            
            random_map[:, 0] = np.zeros((rows,))
            random_map[:, cols - 1] = np.zeros((rows,))
            
        else:
            random_map = self.generate_random_map(rows, cols, land_prob=0.35)
            
        cellular_automaton = cpl.init_simple2d(rows, cols)
        cellular_automaton[0] = random_map
        # print(cellular_automaton)
        # print(np.where(np.array([0, 0, 1, 0, 1, 0, 0, 1, 1, 1]) == 1)[0].shape[0])

        # The rule function must return a scalar for each cell
        

        # print(cpl.nks_rule(np.array([[0, 0, 0],[0, 1, 0],[0, 0, 0]]), 30))
        updated_map = cpl.evolve2d(cellular_automaton, timesteps=cellular_timesteps, \
            apply_rule=lambda grid, cell, time_step: \
                self.rule(grid, cell, time_step, mode, convert_threshold))

        # print(updated_map)
        # print(random_map)
        # print(updated_map[-1])

        
        return random_map, updated_map[-1] # for debug use
        # return updated_map[-1]
        
        
    def visualized(self, random_map, updated_map, mode="8_neighbours"): # rows, cols = y, x

        # random_map, updated_map = self.game_map_generation(cellular_timesteps, \
        #     convert_threshold, mode)

        # print(updated_map)
        print(random_map)
        print(updated_map)
        print(self.__terrain_type[updated_map].tolist())

        array = random_map

        # Convert the array to a grayscale image
        # image = np.uint8(array * 255)
        colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
        colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
        colored_image[array == 1] = [0, 255, 0]  # Green for 1s

        # Optionally, scale the image to make it visually better
        scale_factor = 5
        scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

        # Display the image
        cv2.imshow('Visualized Image', scaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        array = updated_map

        # Convert the array to a grayscale image
        # image = np.uint8(array * 255)
        colored_image = np.zeros((array.shape[0], array.shape[1], 3), dtype=np.uint8)
        colored_image[array == 0] = [255, 0, 0]  # Blue for 0s
        colored_image[array == 1] = [0, 255, 0]  # Green for 1s

        # Optionally, scale the image to make it visually better
        scale_factor = 5
        scaled_image = cv2.resize(colored_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_NEAREST)

        # Display the image
        cv2.imshow('Visualized Image', scaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def mapArea_And_RelativeCoordinate(self, coord: tuple[int]= (0, 0)):
        """Used to calculate what area the location is at(in coordinate of the left coner of current map), 
        and the relative coordinate(index) of this location in current map
        Args:
            `coord` (tuple[int]): coordinate in form (x, y). 
            Defaults to (0, 0).
        
        Returns:
        Two coordinates in form (x, y): map coordinate(Area), and relative coordinate of this location in that map
        """
        init_area = self.__map_info.get_init_map_coordinate()
        map_size = self.__map_info.get_map_size()
        
        # normalized_coord = (int((coord[0] - abs(init_area[0]))/map_size[1]) - int((coord[0] - abs(init_area[0]))/map_size[1]<0), 
        #     int((coord[1] + abs(init_area[1]))/map_size[0]) + 1 - int((coord[1] + abs(init_area[1]))/map_size[0]<0))
        normalized_coord = (math.floor((coord[0] - abs(init_area[0]))/map_size[1]), 
            math.ceil((coord[1] + abs(init_area[1]))/map_size[0]))
        # transform player coordinate into the number of area, (-1, 1) \
            # means the number 1 in both x,y coordinates, (0, 1) means the number 2 in x coord and 1 in y coord
        
        new_area_coord = (normalized_coord[0]*map_size[1] + abs(init_area[0]), \
            normalized_coord[1]*map_size[0] - abs(init_area[1]))
        
        relative_coord = (abs(coord[0] - new_area_coord[0]), \
                            abs(coord[1] - new_area_coord[1]))
        return new_area_coord, relative_coord
        
        
    def map_info_update(self, firstGenerate = False) -> None:
        """This method would update any changes on map system, i.e. generates new map when player
        entering a new area
        
        `This method should be called each move`
        
        args:
            `firstGenerate`: whether you are calling the method first time in the game
        """
        map_size = self.__map_info.get_map_size()
        playerCoord = self.__player.get_currentLocation()
        current_area = self.__map_info.get_current_map_coordinate()
        if len(self.__defininedContent.get_terrain_type()) > np.shape(self.__terrain_type)[0]:
            self.__terrain_type = np.array(self.__defininedContent.get_terrain_type())
            
        if firstGenerate or not (current_area[0] <= playerCoord[0] < current_area[0]+map_size[0] \
            and current_area[1] >= playerCoord[1] > current_area[1]-map_size[1]):
            # enetering into a new area
            new_area_coord, _ = self.mapArea_And_RelativeCoordinate(playerCoord)
            self.__map_info.set_current_map_coordinate(new_area_coord)
            # update current map coordination
            
            # self.__mapPCG.game_map_generation(5, 4) 

            
            # x, y = self.__player.get_currentLocation()
            # rows, cols = self.__map_info.get_map_size() # row, cols = y, x

            # x_areaType = (x + int(cols/2)) /cols
            # y_areaType = (y + int(rows/2)) /rows
            
            if new_area_coord[0] % 2 != 0 and new_area_coord[1] % 2 != 0:
                self.__map_info.set_current_area_type(1)
            else:
                self.__map_info.set_current_area_type(0)
            
            _, updated_map = self.game_map_generation(5, 4, area=new_area_coord) # generate map for new area
            # TODO edit arguments to get potential better map
            
            self.__map_info.set_currentMap(self.__terrain_type[updated_map])
            
    def surroundingLocation(self, playerCoord: tuple[int]) -> dict[str, Location]:
        surrounding = copy.copy(self.player_surrounding)
        player_surrounding = dict()
        current_area = self.__map_info.get_current_map_coordinate()
        # print("player's location",(playerCoord[0], playerCoord[1]))
        # print(current_area)
        
        for y in range(1, -2, -1):
            for x in range(-1, 2):
                if x == 0 or y == 0:
                    placement_coord = (playerCoord[0] + x, playerCoord[1] + y)
                    # if placement_coord in visted_place.keys():
                    #     current_location = visted_place[placement_coord]
                    # else:
                    mapArea, relaCoord = self.mapArea_And_RelativeCoordinate(placement_coord)
                    print(relaCoord)
                    print(type(relaCoord[0]))
                    if current_area == mapArea:
                        # print(self.__map_info.get_currentMap())
                        # print(type(self.__map_info.get_currentMap()))
                        current_location_name = self.__map_info.get_currentMap()\
                            [relaCoord[0], relaCoord[1]]
                    else:
                        _, updated_map = self.game_map_generation(5, 4, area=mapArea)
                        # generate map for new area
                        current_location_name = self.__terrain_type[updated_map]\
                            [relaCoord[0], relaCoord[1]]
                    
                    # objects_in_current_location = self.__objectsPCG.objectGeneration(1, 3) # TODO edit to change object amount
                    current_location = Location(current_location_name, \
                        placement_coord[0], placement_coord[1])

                    
                    player_surrounding[surrounding[0]] = current_location
                    # print("relative coord:", abs(placement_coord[0] - current_area[0]), \
                    #     abs(placement_coord[1] - current_area[1]))
                    # print(arounding[0])
                    surrounding.pop(0)
                    # if x == 0 and y == 0:
                    #     visted_place[placement_coord] = current_location
                    #     # print("player's relative coord:", abs(placement_coord[0] - current_area[0]), \
                    #     #     abs(placement_coord[1] - current_area[1]))
                    #     self.__map_info.currentLocation = current_location
                        
        return player_surrounding


class objectsGenerator():
    def __init__(self, defininedContent: DefininedSys) -> None:
        self.__defininedContent = defininedContent
        
    def objectGeneration(self, lowest_amount: int, highest_amount: int) -> list[Items]:
        """
        Args:
            `lowest_amount` (int): lower bound of number of objects generated (includ end point)\n
            `highest_amount` (int): upper bound of number of objects generated (includ end point)\n
        """
        objectList = self.__defininedContent.get_items()
        generateResult = random.choices(objectList, k=random.randint(lowest_amount, highest_amount))
        
        return generateResult


class eventGenerator():
    def __init__(self, defininedContent: DefininedSys, player : Player_status, \
        map_info: Map_information, currentEvents: EventsTriggered, \
            descriptionGenerator: OutputGenerator) -> None:
        self.__defininedContent = defininedContent
        self.__player = player
        self.__map_info = map_info
        self.__currentEvents = currentEvents
        self.__descriptionGenerator = descriptionGenerator
        
    def eventGeneration(self) -> list[Events]:
        eventList = self.__defininedContent.get_events()
        generateResult = random.choice(eventList)
        
        return generateResult
    
    def event_triger(self) -> Events:
        triggered_event: Events = None
        if self.__player.get_action_point() < 40 and self.__currentEvents.triggeredType["survival crisis"]["action point"]:
            self.__currentEvents.triggeredType["survival crisis"]["action point"] = False
            triggered_event = copy.deepcopy(self.__defininedContent.get_events_frameWork()["survival crisis"]["action point"])
            
            triggered_event.current_location = self.__map_info.currentLocation.location_name
            player_action = self.__player.get_currentAction()
            if player_action == None:
                triggered_event.currentAction = "None"
            else:
                triggered_event.currentAction = player_action.actionName
            
            state = self.__player.get_buffs()
            if len(state) == 0:
                state = "normal"
            triggered_event.play_current_status = state
            triggered_event.description = self.__map_info.currentLocation.description

        if self.__player.get_action_point() >= 40:
            self.__currentEvents.triggeredType["survival crisis"]["action point"] = True
            
        if triggered_event != None:
            self.__currentEvents.eventsTriggered.append(triggered_event)
        return triggered_event
    
    def event_handler(self):
        """
        Please call this every turn
        """
        self.__currentEvents.eventsTriggered
        x = 0
        while x < len(self.__currentEvents.eventsTriggered):
            self.__currentEvents.eventsTriggered[x].triggered_time += 1
            player_action = self.__player.get_currentAction()
            if player_action == None:
                self.__currentEvents.eventsTriggered[x].currentAction = "None"
            else:
                self.__currentEvents.eventsTriggered[x].currentAction = player_action.actionName
        
            result = self.__descriptionGenerator.eventDevelopment(self.__currentEvents.eventsTriggered[x])
            
            print(result["development description"])
                
            for y in range(len(result["reward"])):
                strCommand = self.__currentEvents.eventsTriggered[x].possible_reward[result["reward"][y]]
                
                func, arg = self.__defininedContent.get_eventCommandMap()[strCommand]
                self.__defininedContent.get_commandTranslate()[func](arg)
                
            for y in range(len(result["penalty"])):
                strCommand = self.__currentEvents.eventsTriggered[x].possible_penalty[result["penalty"][y]]
                
                func, arg = self.__defininedContent.get_eventCommandMap()[strCommand]
                self.__defininedContent.get_commandTranslate()[func](arg)
            
            if result["fail"] == True or result["successful"] == True:
                self.__currentEvents.eventsTriggered.pop(x)
                x -= 1
                
            x += 1


class PCGController():
    def __init__(self, defininedContent: DefininedSys, player : Player_status, \
        map_info: Map_information, descriptionGenerator: OutputGenerator, \
            eventController: EventsTriggered) -> None:
        self.__mapPCG = MapGenerator(player, map_info, defininedContent)
        self.__objectsPCG = objectsGenerator(defininedContent)
        self.__eventPCG = eventGenerator(defininedContent, player, map_info, eventController, \
            descriptionGenerator)
        self.__player = player
        self.__map_info = map_info
        self.__descriptionGenerator = descriptionGenerator
        self.__eventController = eventController
        
        self.__first_turn = True
        
    def locationPCG_each_turn(self) -> dict[str, Location]:
        """
        Should be called each turn to generat objects and other things in current location
        """
        playerCoord = self.__player.get_currentLocation()
        
        

        self.__mapPCG.map_info_update(self.__first_turn)
        self.__first_turn = False
        current_area = self.__map_info.get_current_map_coordinate()
        visted_place = self.__map_info.get_visitedPlace()
        self.__eventPCG.event_handler() # determine the effects caused by any events
        
        player_surrounding = self.__mapPCG.surroundingLocation(playerCoord)
        if playerCoord in visted_place.keys():
            current_location = visted_place[playerCoord]
            player_surrounding["Current location"] = current_location
            self.__map_info.currentLocation = current_location
            
            triggered_event = self.__eventPCG.event_triger()
            if triggered_event != None:
                # TODO change the eventDescription to make it description all current events
                self.__descriptionGenerator.eventDescription(triggered_event)
                output = triggered_event.description
                # self.__eventController.add_new_event(triggered_event)
            elif self.__player.get_lastLocation() != playerCoord:
                output = self.__map_info.currentLocation.description
        else:
            objects_in_current_location = self.__objectsPCG.objectGeneration(1, 3) # TODO edit to change object amount

            player_surrounding["Current location"].objects = objects_in_current_location
            visted_place[playerCoord] = player_surrounding["Current location"]
            self.__map_info.currentLocation = player_surrounding["Current location"]
            
            
            # print("\n{}\n\n{}\n\n{}\n\n{}".format(output["location name"], \
            #     output["Description of current and surrounding locations"], output["Landscape Features description"], \
            #         output["Items description"]))
        
            triggered_event = self.__eventPCG.event_triger()
            if triggered_event != None:
                # TODO change the eventDescription to make it description all current events
                self.__descriptionGenerator.locationDescription(player_surrounding)
                self.__descriptionGenerator.eventDescription(triggered_event)
                output = triggered_event.description
                # self.__eventController.add_new_event(triggered_event)
            elif self.__player.get_lastLocation() != playerCoord:
                output = self.__map_info.currentLocation.description

        self.__map_info.set_visitedPlace(visted_place)
        # player_arounding = {"Current location": current_location, \
        #     "Front": Location("<Do not know>", 0, 0), "Back": Location("<Do not know>", 0, 0), \
        #         "Right hand side": Location("<Do not know>", 0, 0), "Left hand side": Location("<Do not know>", 0, 0)}
        # if playerCoord in visted_place.keys():
            

        # elif self.__player.get_lastLocation() != playerCoord:
        
        self.__player.set_lastLocation(*playerCoord)
        print(output)
    


if __name__ == "__main__":
    # test = MapGenerator(Player_status(), Map_information(1))
    # test.debug(5, 4)
    # test = objectsGenerator(DefininedSys())
    # test.objectGeneration(1, 6)
    player_info = Player_status()
    map_record = Map_information(current_area_type = 1, map_size=(20, 20)) # land type
    worldStatus = globalInfo()
    
    defined_command = Commands(player_info, map_record, worldStatus)
    game_content = DefininedSys(defined_command)
    test = MapGenerator(player_info, map_record, game_content)
    test.map_info_update(True)
    print(test.mapArea_And_RelativeCoordinate((0, -10)))
    print(test.surroundingLocation((0, -10)))
    
    test.visualized(*test.game_map_generation(5, 4))