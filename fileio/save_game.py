# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair

# save_game.py
# Description: SaveGame class. Encapsulates all of the data needed from the GameState class or a file to save/load data
# Principal Author of this file per Project plan: Shawn Hillyer

# CITATIONS
# CITE: http://stackoverflow.com/questions/4810537/how-to-clear-the-screen-in-python
# CITE: http://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
# CITE: http://stackoverflow.com/questions/7935972/writing-to-a-new-directory-in-python-without-changing-directory
# CITE: http://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file-using-python
# CITE: http://stackoverflow.com/questions/30876497/open-a-file-from-user-input-in-python-2-7

from constants.action_costs import STARTING_TIME
import json
import glob

class SaveGame:
    def __init__(self, gamestate):
        '''
        Instantiate a SaveGame from the gamestate data passed in
        If None is passed in, this constructor does nothing. Instead, call load_from_file() to load up the SaveGame
        with data which can then be accessed by calling various methods
        :param gamestate:
        '''

        # These must be defined - the only reason I give them values here is so that I can test the loadgame/savegame
        # methods without having them actually read/write from/to real files
        self.current_room = "Street"
        self.visited_rooms = []
        self.objects_in_rooms = {}
        self.player_inventory = []
        self.time_left = STARTING_TIME

        # TODO: Write more UNIT TESTS for this code
        if gamestate:
            self.current_room = gamestate.get_current_room().get_name()
            self.time_left = gamestate.get_time_left()

            for room in gamestate.rooms:
                if room.is_visited():
                    self.visited_rooms.append(room.get_name())

                # Grab all the objects for *this specific room* and add to a list, then append that to dictionary
                room_objects = []
                for room_object in room.objects:
                    room_objects.append(room_object)
                self.objects_in_rooms[room.get_name()] = room_objects

            # Read the player's inventory
            for inventory_object in gamestate.player.get_inventory_objects():
                self.player_inventory.append(inventory_object)



    def write_to_file(self, filename):
        '''
        SAVING A SAVEGAME FROM GAMESTATE
            A SaveGame would be instantiated when a player chooses to 'save' their game. Pass in the gamestate object
            from the GameClient and then parse through the object looking for the relevant data to save to file.

            Once a SaveGame object is instantiated, you can call write_to_file() method to save the data.
        '''
        saved_dir = './gamedata/savedgames/'
        filename = filename + '.json'

        with open(os.path.join(saved_dir, filename), 'w') as saved_game_file:
            json.dump(self, saved_game_file)

        write_successful = True

        # if write failed
        #   write_successful = False

        return write_successful


    def load_from_file(self, filename):
        '''
        LOADING A SAVEGAME FROM FILE
            Instead, call the load_from_file() method. This will populate the SaveGame object with the necessary
            data. The GameState class will simply create a SaveGame object, call load_from_file(), then use the SaveGame
            to parse it for the data it wants and handle the logic of "repopulating" the GameState so that it matches
            the original savegame in a similar fashion as write_to_file
        '''
        # saved_dir = './gamedata/savedgames/'
        # saved_game_files =  glob.glob(saved_dir)
        # self.gamestate = json.load(saved_game_file)
        filename = './gamedata/savedgames/' + filename
        self.gamestate = {}
        with open(filename, 'r') as savedgame:
            self.gamestate = json.load(savedgame)

        # DEBUG
        print(json.dumps(self.gamestate))

        # Load saved game content from file
        # for room in rooms_files:
        #     with open(room) as room:
        #         room_properties = json.load(room)
        #         new_room = Room(room_properties)
        #         rooms.append(new_room)

        return self.gamestate
        # pass

    def get_visited_rooms_list(self):
        if self.visited_rooms is not None:
            return self.visited_rooms
        return None

    def get_objects_in_rooms(self):
        if self.objects_in_rooms is not None:
            return self.objects_in_rooms
        return None

    def get_player_inventory(self):
        if self.player_inventory is not None:
            return self.player_inventory
        return None

    def get_current_room(self):
        if self.current_room is not None:
            return self.current_room
        return None

    def get_time_left(self):
        if self.time_left is not None:
            return self.time_left
        return None

    def is_valid_filename(self, file_name):
        '''
        Pass in a string and validate if the filename is valid
        Invalid might be because string is an invalid filename in the op system or some other reason(s)
        :param file_name:
        :return: True if filename is valid, False if not valid
        '''
        # savedgames = []
        savedgames = self.get_savegame_filenames()

        for savedgame in savedgames:
            if str(savedgame) == str(file_name):
                return True

        return False

    @staticmethod
    def get_savegame_filenames():
        '''
        Returns a list of the filenames in the savegame folder
        :return: All files in the savedgame folder
        '''
        # TODO: Implement this
        savedgames = []
        savedgames_dir = './gamedata/savedgames/*.json'
        savedgames_files_path =  glob.glob(savedgames_dir)

        # Trim preceding path from filename strings
        savedgames_files = []
        for file in savedgames_files_path:
            file = file[22:]
            savedgames_files.append(file)

        # Load saved game content from directory
        for savedgame in savedgames_files_path:
            with open(savedgame) as savedgame:
                savedgames.append(savedgame)
                # DEBUG
                print(json.load(savedgame))

        return savedgames_files
