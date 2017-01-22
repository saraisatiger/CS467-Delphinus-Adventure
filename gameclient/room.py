from debug.debug import *
logger = logging.getLogger(__name__)



class Room:
    def __init__(self, properties):
        logger.debug("Room initialized")
        if properties:
            self.room_features = properties['room_features']
            self.long_description = properties['long_description']
            self.short_description = properties['short_description']
            self.visited = properties['visited']
            self.room_connections = properties['room_connections']

    def get_long_description(self):
        full_description = self.long_description
        if self.room_connections:
            for connection in self.room_connections:
                full_description = full_description + connection.get_connection_description()


class RoomFeature:
    '''
    A feature of a room. Each room has a minimum of two features that can be examined
    Examining a feature causes it to be known_to_player
    '''
    def __init__(self, properties):
        self.name = properties['name']
        self.description = properties['description']
        self.known_to_player = properties['known_to_player']

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