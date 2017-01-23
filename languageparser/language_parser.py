# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem:, Shawn Hillyer, Niza Volair
#
# language_parser.py
# Description: Class used to parse the language and return relevant components
# Principal Author of this file per Project plan: Niza Volair
#
# CITATIONS
# CITE:
#
# #########################################################################################################
# DEV NOTES:
# 1/22/17:
# The language parser will have to return more than the verb. It will also need to identify the
# subject (feature or object) and appropriate prepositions and such. At a minimum I'd expect the LP to
# return a python dictionary of a verb that's being called and one or more subjects that are trying to
# be interacted. For example "use broom on dusty floor" might return:
#
# {
#     'verb' : 'use',
#     'subject' : 'broom',
#     'objects' : [
#         'dusty floor'
#     ]
# }
#
# (SSH)
#
# #########################################################################################################


from stringresources.verbs import *

from debug.debug import *
logger = logging.getLogger(__name__)



class LanguageParser:
    '''
        TODO:

    '''
    def __init__(self):
        logger.debug("Language Parser initialized")


    def parse_command(self, command):
        '''
        Presently returning a constant defined in a stringresources/verbs.py file so that the
        return values from parser can just be set. Thi is Shawn's temporary solution. Later on
        we will need to send more than just the verb back (the subject etc. also needed). See Dev note near file head
        '''


        # Parse any command to all lowercase to reduce complexity of our parser.
        # TODO: Might also want to strip trailing / leading whitespace (but not inner whitespace)
        # l.strip() strips the left-side whitespace, not sure on right side whitespace
        command = command.lower().lstrip()



        # This simple code just checks if the string entered by user us in one of several Lists defined in the resource
        # file stringresources/verbs.py. Each list is a set of aliases for each verb and it returns a simple string that
        # the gameclient is able to examine.
        # Once this is re-implemented in a stable way, gameclient will need to be reconfigured to properly parse whatever
        # ends up being returned by the parser. -- (SSH)

        if command in QUIT_ALIASES:
            return QUIT
        elif command in NEW_GAME_ALIASES:
            return NEW_GAME
        elif command in LOAD_GAME_ALIASES:
            return LOAD_GAME
        elif command in HELP_ALIASES:
            return HELP
        elif command in LOOK_ALIASES:
            return LOOK
        else:
            return INVALID_INPUT