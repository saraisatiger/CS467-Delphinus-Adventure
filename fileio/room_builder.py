from gameclient.room import *

from debug.debug import *
logger = logging.getLogger(__name__)

import json
from pprint import pprint


class RoomBuilder:
    def __init__(self):
        logger.debug("RoomBuilder instantiated")

    def load_room_data_from_file(self):
        rooms = []

        with open('./gamedata/rooms/sample_room.json') as sample_room:
            room_properties = json.load(sample_room)
            new_room = Room(room_properties)
            rooms.append(new_room)
        # pprint(rooms)

        return rooms
        # return self.build_rooms_from_code()

    def build_rooms_from_code(self):
        '''
        Method for use in testing game engine and demonstrates how the features and rooms could be parsed
        from a file; would be useful if we were hard-coding the values. Could also convert to the real
        file loader by replacing static strings with information from various file-read operations
        :return:
        '''

        '''
            TODO: Create loop (or massive switch statement) to determine which item to parse
        '''
        # Parse long descriptions from input file
        with open('long_descriptions.json') as long_descriptions:
            rooms = json.load(long_descriptions)
        # DEBUG
        pprint(rooms[0])

        # Parse feature descriptions from input file
        with open('features.json') as features:
            features = json.load(features)
        #DEBUG
        pprint(features[0])


        street_feature_1 = RoomFeature(features[0]["features"][0])
        street_feature_2 = RoomFeature(features[0]["features"][1])

        '''
            TODO: Add connection links to room_properties
        '''
        street_connection_1_properties = {
                'label': 'Arcade',
                'cardinal_direction': 'North',
                'description': "an exciting sign for an arcade",
                'destination': 'Arcade'
        }
        street_connection_1 = RoomConnection(street_connection_1_properties)

        '''
            TODO: Create room_properties as pre-built JSON
        '''
        street_properties = {
            'room_features' : [street_feature_1, street_feature_2],
            'long_description' : rooms[0]["description"],
            'short_description' : "Short description here... You're standing on the street",
            'visited' : False,
            'room_connections' : [street_connection_1]
        }

        street = Room(street_properties)
        rooms =  [ street ]
        return rooms

