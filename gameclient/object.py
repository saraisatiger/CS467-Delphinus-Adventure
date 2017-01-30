# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair

# object.py
# Description: Object and related classes
# Principal Author of this file per Project plan: Shawn Hillyer

# CITATIONS
# CITE:

from gameclient.room import *

from debug.debug import *
logger = logging.getLogger(__name__)

import json
import glob


class Object:
    '''
    An object. Can be in a Room or players inventory.
     Can be picked up from a room, dropped in a room, used, 'look at'ed, and possibly other actions
    '''
    def __init__(self, properties):
        if properties['name']:
            self.name = properties['name']
        if properties['long_description']:
            self.long_description = properties['long_description']
        if properties['short_description']:
            self.short_description = properties['short_description']
        if properties['default_location']:
            self.default_location = properties['default_location']
        if properties['cost']:
            self.cost = properties['cost']

    def get_long_description(self):
        return self.long_description

    def get_short_description(self):
        return self.short_description

    def get_name(self):
        return self.name

    def get_default_location_name(self):
        if self.default_location:
            return self.default_location
        return None

    def get_cost(self):
        return self.cost

    def get_environmental_description(self):
        # TODO: Refine the output of this function somewhat? Could give objects unique environmental descriptions but
        # TODO: 1depending on the room they are in it wouldn't make sense once dropped somewhere else(SSH)
        description = "You see a " + self.name + " in the area."
        return description

class ObjectBuilder:
    '''
    Generates objects and returns them to caller
    '''
    def __init__(self):
        pass

    def get_game_objects(self):
        all_objects = []

        skateboard = Object({
            'name' : 'Skateboard',
            'long_description' : 'A trendy skateboard with the text \'Z3R0 C007\' inked on its surface',
            'short_description' : 'Skateboard is good',
            'default_location' : 'Street'
        })


        all_objects.append(skateboard)

        return all_objects

    def load_object_data_from_file(self):
        '''
        Called by GameClient to instantiate all of the objects. This is called whether the game is new
        or loaded. Returns ALL objects as a list.
        '''
        object_list = []
        objects_dir = './gamedata/objects/*.json'
        objects_files =  glob.glob(objects_dir)

        # Load room content from directory
        # TODO: Determine logical order; for now, based on Project Plan (hashems)
        for object in objects_files:
            with open(object) as object:
                object_properties = json.load(object)
                new_object = Object(object_properties)
                object_list.append(new_object)

        # DEBUG
        # for i in rooms:
        #     print(i.name)

        return object_list