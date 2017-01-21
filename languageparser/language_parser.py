from debug.debug import *
logger = logging.getLogger(__name__)



class LanguageParser:
    '''
    TODO: Implement
    '''
    def __init__(self):
        logger.debug("Language Parser initialized")


    def parse_command(self, command):
        # Stub function
        if isinstance(command, str):
            return "Command is a string"
        else:
            return "Command is not a string"