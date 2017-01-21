from gameclient.room import Room

from debug.debug import *
logger = logging.getLogger(__name__)



class RoomBuilder:
    def __init__(self):
        logger.debug("RoomBuilder instantiated")

    def load_room_data_from_file(self):
        rooms = []

        rooms.append(Room())

        return rooms