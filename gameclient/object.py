# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair

# object.py
# Description: Object and related classes
# Principal Author of this file per Project plan: Shawn Hillyer

# CITATIONS
# CITE:

class Object:
    '''
    An object. Can be in a Room or players inventory.
     Can be picked up from a room, dropped in a room, used, 'look at'ed, and possibly other actions
    '''
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_environmental_description(self):
        # TODO: Refine the output of this function somewhat? Could give objects unique environmental descriptions but
        # TODO: 1depending on the room they are in it wouldn't make sense once dropped somewhere else(SSH)
        description = "You see a " + self.name + " laying around."
        return description