# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair
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
# subject (feature or verb_subject_name) and appropriate prepositions and such. At a minimum I'd expect the LP to
# return a python dictionary of a verb that's being called and one or more targets that are trying to
# be interacted. For example "use broom on dusty floor" might return:
#
# {
#     'verb' : 'use',
#     'verb_subject_name' : 'broom',
#     'targets' : [
#         'dusty floor'
#     ]
# }
#
# (SSH)
#
# #########################################################################################################


from constants.verbs import *
from languageparser.language_parser_wrapper import *
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
        Presently returning a constant defined in a constants/verbs.py file so that the
        return values from parser can just be set. Thi is Shawn's temporary solution. Later on
        we will need to send more than just the verb back (the subject etc. also needed). See Dev note near file head
        '''

        # Parse any command to all lowercase to reduce complexity of our parser.
        # TODO: Might also want to strip trailing whitespace (SSH)
        # l.strip() strips the left-side whitespace, not sure on right side whitespace (SSH)
        command = command.lower().lstrip()
        subject = None
        targets = None

        # Hacky way to parse a "look at" command to find the verb_subject_name/feature player wants to examine.
        # NOTE: Doesn't parse aliases
        if 'look at' in command:
            subject = command.replace("look at ", "", 1) # replace "look at " with empty string - rest is the verb_subject_name
            command = "look at"

        # hacky way to parse a 'take' command.
        # NOTE: Doesn't parse aliases
        elif 'take' in command:
            subject = command.replace("take ", "", 1) # replace at most one instance of "take " with empty str
            command = "take"

        # hacky way to parse a 'drop' command
        # NOTE: Doesn't parse aliases
        elif 'drop' in command:
            subject = command.replace("drop ", "", 1) # replace at most one instance of "drop " with empty str
            command = "drop"

        # Same thing for go
        elif 'go' in command:
            subject = command.replace("go ", "", 1)
            command = "go"

        elif 'buy' in command:
            subject = command.replace("buy ", "", 1)
            command = "buy"

        elif 'use' in command:
            subject = command.replace("use ", "", 1)
            command = "use"

        elif 'steal' in command:
            subject = command.replace("steal ", "", 1)
            command = "steal"

        # This simple code just checks if the string entered by user us in one of several Lists defined in the resource
        # file constants/verbs.py. Each list is a set of aliases for each verb and it returns a simple string that
        # the gameclient is able to examine.
        # Once this is re-implemented in a stable way, gameclient will need to be reconfigured to properly parse whatever
        # ends up being returned by the parser. -- (SSH)

        if command in QUIT_ALIASES:
            command = QUIT
        elif command in NEW_GAME_ALIASES:
            command = NEW_GAME
        elif command in LOAD_GAME_ALIASES:
            command = LOAD_GAME
        elif command in SAVE_GAME_ALIASES:
            command = SAVE_GAME
        elif command in HELP_ALIASES:
            command = HELP
        elif command in LOOK_ALIASES:
            command = LOOK
        elif command in LOOK_AT_ALIASES:
            command = LOOK_AT
        elif command in GO_ALIASES:
            command = GO
        elif command in TAKE_ALIASES:
            command = TAKE
        elif command in DROP_ALIASES:
            command = DROP
        elif command in INVENTORY_ALIASES:
            command = INVENTORY
        elif command in BUY_ALIASES:
            command = BUY
        elif command in USE_ALIASES:
            command = USE
        elif command in SPRAYPAINT_ALIASES:
            command = SPRAYPAINT
        elif command in STEAL_ALIASES:
            command = STEAL
        # cheat codes
        elif command == "mess with the best":
            command = CHEATCODE_LOSE
        elif command == "die like the rest":
            command = CHEATCODE_WIN

        else:
            command = INVALID_INPUT

        # return (command, subject, targets)

        results = LanguageParserWrapper()
        results.set_verb(str(command))
        results.set_noun(str(subject), str("object"))

        logger.debug("Returning: \n" + str(results))
        return results