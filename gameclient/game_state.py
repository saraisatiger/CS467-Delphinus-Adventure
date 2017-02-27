# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair

# game_state.py
# Description: GameState class that encapsulates all things that can be changed in the game world
# Principal Author of this file per Project plan: Shawn Hillyer

from constants.gameplay_settings import STARTING_TIME
from constants.gameover_status_codes import *
from fileio.room import *
from fileio.object import *
from gameclient.user_interface import *

from debug.debug import *
logger = logging.getLogger(__name__)

class GameState:
    '''
    Holds all of the variables that maintain the game's state
    '''
    def __init__(self):
        self.ob = ObjectBuilder()
        self.rb = RoomBuilder()
        self.initialize_gamestate()
        self.game_file = ""

    def set_current_room(self, room):
        '''
        Update the location the player is in
        :param room: The room the player is in (actual room)
        :return: N/A
        '''
        try:
            self.prior_room = self.current_room
        except:
            self.prior_room = room
        self.current_room = room

    def get_room_by_name(self, room_name):
        for room in self.rooms:
            if room.name.lower() == room_name.lower():
                return room
        return None

    def get_object_by_name(self, object_name):
        for room_object in self.objects:
            if room_object.get_name().lower() == object_name.lower():
                return room_object
        return None

    def initialize_gamestate(self):
        self.current_room = None
        self.prior_room = None
        self.rooms = []
        self.objects = []
        self.player = Player()
        self.time_left = STARTING_TIME
        self.is_trash_can_looted = False
        self.spraypaint_data = {}

    def load_rooms_and_objects_from_file(self):
        # Initialize the rooms and objects to their defaults
        self.rooms = self.rb.load_room_data_from_file()
        self.objects = self.ob.load_object_data_from_file()  # Being done in the initialize_gamestate()

    def initialize_new_game(self):
        self.initialize_gamestate()
        self.load_rooms_and_objects_from_file()

        # Still need to set the default room and put the objects in the rooms
        self.set_default_room_by_name(DEFAULT_ROOM)
        self.place_objects_in_rooms(self.objects)

        # Set the spraypainted status for each room to be blank
        self.initialize_spraypaint_data()

    def initialize_load_game(self, filename):
        self.game_file = filename.replace('.json', '')

        # Clear all of the variables by calling what is essentially the constructor
        self.initialize_gamestate()
        self.load_rooms_and_objects_from_file()

        save_data = SaveGame(None)
        save_data.load_from_file(filename)

        # Room information
        current_room_name = save_data.get_current_room()
        self.current_room = self.get_room_by_name(current_room_name)
        visited_rooms_names = save_data.get_visited_rooms_list()
        for room_name in visited_rooms_names:
            room = self.get_room_by_name(room_name)
            room.set_is_visited(True)
        prior_room_name = save_data.get_prior_room()
        try:
            self.prior_room = self.get_room_by_name(prior_room_name)
        except:
            self.prior_room = None

        # Hacked features
        hacked_feature_mapping = save_data.get_hacked_feature_mapping()
        for room_name in hacked_feature_mapping:
            for feature_name in hacked_feature_mapping[room_name]:
                room = self.get_room_by_name(room_name)
                feature = room.get_feature_by_name(feature_name)
                feature.set_is_hacked(True)

        # Special booleans
        self.is_trash_can_looted = save_data.get_is_trash_can_looted()

        # Objects in rooms and inventory
        objects_room_mapping = save_data.get_objects_room_mapping()
        for room_name in objects_room_mapping:
            for object_name in objects_room_mapping[room_name]:
                obj = self.get_object_by_name(object_name)
                room = self.get_room_by_name(room_name)
                room.add_object_to_room(obj)
                # logger.debug("Adding object " + obj.get_name() + " to room " + room.get_name() + ".")
        #
        player_inventory_list = save_data.get_player_inventory()
        for object_name in player_inventory_list:
            obj = self.get_object_by_name(object_name)
            self.player.add_object_to_inventory(obj)
            # logger.debug("Adding object " + obj.get_name() + " to player's bag.")

        # Objects owned by player
        player_owned = save_data.get_owned()
        for object_name in player_owned:
            # obj = self.get_object_by_name(object_name)
            # copy_of_object = copy.copy(object)
            self.player.owned.append(object_name)
            # logger.debug("Adding object " + object_name + " to player's 'owned' list.")

        # Player variables
        # logger.debug("self.player_cash = save_data.get_player_cash() = " + str(save_data.get_player_cash()))
        self.player.cash = save_data.get_player_cash()
        self.player.coolness = save_data.get_player_coolness()
        self.player.speed = save_data.get_player_speed()
        self.player.set_has_hack_skill(save_data.get_player_has_hack_skill())
        self.player.set_has_skate_skill(save_data.get_player_has_skate_skill())
        self.player.set_has_spraypaint_skill(save_data.get_player_has_spraypaint_skill())

        # Other variables stored in GameState
        self.time_left = save_data.get_time_left()

        # TODO: Read SaveGame data once it's implemented isntead of the below re-initialization
        # self.spraypaint_data = save_data.get_spraypaint_data()
        self.initialize_spraypaint_data()  # TODO: Delete this once we can get the data from save_data (SaveGame obj.)

    def game_status(self):
        # TODO: Implement this properly. Status codes in constants\gameover_status_codes.py  ((SSH))
        # This function should/will check if player has won or lost(died/whatever)
        if self.time_left is 0:
            return GAMEOVER_LOSE
        return GAME_CONTINUE

    def get_header_info(self):
        header_info = {
            'speed' : self.player.speed,
            'coolness' : self.player.coolness,
            'current_room' : self.current_room.get_name(),
            'time_left' : self.time_left,
            'cash' : self.player.get_cash(),
            'hack_skill': self.player.can_hack(),
            'skate_skill': self.player.can_skateboard(),
            'spraypaint_skill' : self.player.can_spraypaint()
        }
        return header_info

    def set_object_vars_to_default(self):
        '''
        Sets ownership on all objects to be False, called during new game init.
        '''
        for obj in self.objects:
            obj.set_is_owned_by_player(False)

    def set_default_room_by_name(self, room_name):
        '''
        Sets the default room to the room_name passed in. Called during game initialization
        :param room_name:
        '''
        default_room = self.get_room_by_name(room_name)
        self.set_current_room(default_room)

    def initialize_spraypaint_data(self):
        '''
        Creates a dictionary of spraypaint data for every non-virtual room in the game and sets is_spraypainted false,
        message is None
        '''
        self.spraypaint_data.clear()
        for room in self.rooms:
            if room.is_virtual_space() is False:
                room_name = room.get_name()
                is_spraypainted = False
                entry = {
                         'is_spraypainted': is_spraypainted,
                         'spraypaint_message': None
                }
                self.spraypaint_data[room_name] = entry
        # logger.debug(str(self.spraypaint_data)) # TODO: Comment this out later

    def is_room_spray_painted_by_name(self, room_name):
        '''
        Check if a room is spraypainted by looking it up by name. Returns True or False
        :param room_name: String, the name of the room as found in its JSON file.
        :return: True if room is spraypainted, false otherwise
        '''
        is_painted = None
        try:
            entry = self.spraypaint_data[room_name]
            if entry is not None:
                is_painted = entry['is_spraypainted']
        except:
            logger.debug("There was a problem finding the room '" + str(room_name) + "' + in the self.spraypaint_data dictionary")
        # logger.debug("is_room_spray_painted_by_name(" + room_name + ") returns " + str(is_painted))
        return is_painted

    def set_room_spray_painted_by_name(self, room_name, painted=True):
        '''
        Updates the self.spraypaint_data dictionary to show that the room is painted
        :param room_name: String. Name of the room to set the value for, as found in its JSON file.
        :param painted:  Boolean. True if room is painted (default), False if it's not.
        '''
        try:
            entry = self.spraypaint_data[room_name]
            entry['is_spraypainted'] = painted
            # logger.debug(str(entry))
        except:
            logger.debug("Tried to set_room_spray_painted_by_name( +" + room_name + "," + str(painted) +  " ) but failed with exception.")

    def set_room_spray_painted_message(self, room_name, message):
        '''
        Set the message that is painted in the room
        :param room_name: String. Name of the room to paint as found in its JSON file.
        :param message:  String. The message to be printed in the room as graffiti/spraypaint.
        :return:
        '''
        try:
            entry = self.spraypaint_data[room_name]
            entry['spraypaint_message'] = str(message)
            # logger.debug("Setting the message... entry is now " + str(entry))
            # logger.debug(str(self.spraypaint_data))
        except:
            logger.debug("Error setting the message in this room")
            logger.debug(str(self.spraypaint_data))

    def get_room_spray_painted_message(self, room_name):
        '''
        Looks up the message stored in the self.spraypaint_data dictionary for the room_name passed in
        :param room_name:  String. Name of the room as found in its JSON file.
        :return:
        '''
        try:
            # logger.debug("Trying to get spray painted message from room " + room_name)
            entry = self.spraypaint_data[room_name]
            # logger.debug("self.spraypaint_data[" + room_name + "]" + str(entry))
            # logger.debug(entry['spraypaint_message'])
            return entry['spraypaint_message']
        except:
            # logger.debug("Couldn't find a message for the room " + room_name + ", this isn't necessarily a problem if in a virtual space")
            return None

    def place_objects_in_rooms(self, game_objects):
        '''
        Iterates through a list of game objects and places them in the inventory or room as appropriate
        :param game_objects:
        :return:
        '''
        for game_object in game_objects:
            # Cash wad is "hidden" in the trash can so you won't see it in the room in the normal fashion.
            object_location = game_object.get_default_location_name().lower()
            # logger.debug("object_location = " + object_location)
            try:
                if object_location == "inventory":
                    # logger.debug("Location is inventory, trying to add it...")
                    try:
                        # logger.debug("Added to inventory...")
                        self.player.add_object_to_inventory(game_object)
                    except:
                        logger.debug("place_objects_in_rooms() failed to place " + game_object.get_name() + " in inventory")
                else:
                    try:
                        room = self.get_room_by_name(object_location)
                        room.add_object_to_room(game_object)
                        # logger.debug("Success??")
                    except:
                        logger.debug("place_objects_in_rooms() failed to place " + game_object.get_name() + " because room_name " + object_location + " does not exist.")
            except:
                logger.debug("place_objects_in_rooms() failed for some unknown reason")

    def get_current_room(self):
        return self.current_room

    def get_prior_room(self):
        return self.prior_room

    def update_time_left(self, time_change):
        '''
        Update the amount of time_left left.
        :param time_change: Integer. Positive increases time_left, Negative decreases time_left
        :return: N/A
        '''
        # TODO: Game design decision. What exactly does speed do? This implementation just adds the speed to any negative
        # time effects unless it reduces the effect to cause a GAIN in time which makes no sense
        # We could also make speed some kind of multiplier or some other method
        if time_change < 0:
            time_change += self.player.speed
            # IF player is so fast that the action would cost no time, make sure we don't change time_left
            if time_change > 0:
                time_change = 0
        self.time_left += time_change

    def get_time_left(self):
        # if self.game_file == "":
        #     return self.time_left
        # else:
        #     self.time_left =
        return self.time_left
