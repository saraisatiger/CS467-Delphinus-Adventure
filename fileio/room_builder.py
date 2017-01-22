from gameclient.room import *

from debug.debug import *
logger = logging.getLogger(__name__)



class RoomBuilder:
    def __init__(self):
        logger.debug("RoomBuilder instantiated")

    def load_room_data_from_file(self):
        # rooms = []
        # room_properties = { 'to' : 'do '}
        # rooms.append(Room(room_properties))

        # return rooms

        return self.build_rooms_from_code()

    def build_rooms_from_code(self):
        '''
        Method for use in testing game engine and demonstrates how the features and rooms could be parsed
        from a file; would be useful if we were hard-coding the values. Could also convert to the real
        file loader by replacing static strings with information from various file-read operations
        :return:
        '''
        street_feature_1_properties = {
            'name' : '"No Skateboarding" sign',
            'description' : 'The sign states very clearing that skateboarding is prohibited in this area. Fine: $300',
            'known_to_player' : False
        }
        street_feature_2_properties = {
            'name' : 'Guardrails',
            'description' : 'These guard rails look perfect for grinding on with a skateboard!',
            'known_to_player' : False
        }

        street_connection_1_properties = {
                'label': 'Arcade',
                'cardinal_direction': 'North',
                'description': "an exciting sign for an arcade",
                'destination': 'Arcade'
        }


        street_feature_1 = RoomFeature(street_feature_1_properties)
        street_feature_2 = RoomFeature(street_feature_2_properties)
        street_connection_1 = RoomConnection(street_connection_1_properties)

        street_properties = {
            'room_features' : [street_feature_1, street_feature_2],
            'long_description' : 'Long description here... This is a really long description of the Street and would be read from a file in the event of a real program',
            'short_description' : "Short description here... You're standing on the street",
            'visited' : False,
            'room_connections' : [street_connection_1]
        }


        street = Room(street_properties)

        rooms =  [ street ]

        return rooms