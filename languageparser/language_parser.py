from stringresources.verbs import *

from debug.debug import *
logger = logging.getLogger(__name__)



class LanguageParser:
    '''
    TODO: Implement
    '''
    def __init__(self):
        logger.debug("Language Parser initialized")


    def parse_command(self, command):
        '''
        Presently returning a constant defined in a stringresources/verbs.py file so that the
        return values from parser can just be set. Thi is Shawn's temporary solution. Later on
        we will need to send more than just the verb back (the subject etc. also needed)
        '''

        # Parse any command to all lowercase to reduce complexity of our parser.
        # TODO: Might also want to strip trailing / leading whitespace (but not inner whitespace)
        # l.strip() strips the left-side whitespace, not sure on right side whitespace
        command = command.lower().lstrip()

        if command in QUIT_ALIASES:
            return QUIT
        elif command in NEW_GAME_ALIASES:
            return NEW_GAME
        elif command in LOAD_GAME_ALIASES:
            return LOAD_GAME
        elif command in HELP_ALIASES:
            return HELP
        else:
            return INVALID_INPUT