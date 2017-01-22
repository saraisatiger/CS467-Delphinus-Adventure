from debug.debug import *
logger = logging.getLogger(__name__)



class Room:
    def __init__(self, properties):
        logger.debug("Room initialized")
        if properties:
            # self.name = properties['name']
            self.long_description = properties['long_description']
            # self.long_description = str(properties['long_description'])
            self.short_description = properties['short_description']
            self.visited = properties['visited']
            self.room_features = properties['room_features']
            self.room_connections = properties['room_connections']

    def get_long_description(self):
        full_description = self.long_description + "\n\n" + self.get_connection_string()
        return full_description

    def get_short_description(self):
        full_description = self.short_description + "\n\n" +  self.get_connection_string()
        return full_description

    def get_connection_string(self):
        connection_string = ""
        if self.room_connections:
            for connection in self.room_connections:
                connection_string = connection_string + connection.get_connection_description()
        return connection_string

    def set_visited(self):
        self.visited = True

class RoomFeature:
    '''
    A feature of a room. Each room has a minimum of two features that can be examined
    Examining a feature causes it to be known_to_player
    '''
    def __init__(self, properties):
        self.name = properties['name']
        self.description = properties['description']
        '''
            TODO: I think known_to_player should be tracked either by a game state or player state dictionary
        '''
        # self.known_to_player = properties['known_to_player']

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def is_known_to_player(self):
        return self.known_to_player

    def discover(self):
        self.known_to_player = True


class RoomConnection:
    def __init__(self, properties):
        self.label = properties['label']
        self.cardinal_direction = properties['cardinal_direction']
        self.description = properties['description']
        self.destination = properties['destination']

    def get_connection_description(self):
        description = "To the " + self.cardinal_direction + " you see " + self.description + "."
        return description