from languageparser.language_parser import LanguageParser
from fileio.room_builder import RoomBuilder
from stringresources.strings import *
from stringresources.verbs import *

from debug.debug import *
logger = logging.getLogger(__name__)

class GameClient:
    '''
    Main controller for the game's flow and logic
    '''
    def __init__(self):
        self.gamestate = GameState()
        self.gamestate.load_rooms_from_files()
        self.ui = UserInterface()
        self.lp = LanguageParser()
        self.rb = RoomBuilder()
        self.user_input = ""
        self.command = INVALID_INPUT
        self.valid_main_menu_commands = { QUIT, LOAD_GAME, NEW_GAME , HELP }

        # Initiate game loop
        self.main_loop()

    def main_loop(self):
        '''
        Comments outline the flow of project and intended functions for now
        based on game engine workflow graph
        :return:
        '''

        # Load data from files (Specifically rooms, but can do other files as well)
        self.gamestate.rooms = self.rb.load_room_data_from_file()

        # Loop in main menu until a valid command is entered

        while self.command is not QUIT:
            self.main_menu_loop()

            if self.command is NEW_GAME:
                self.start_new_game()
            elif self.command is LOAD_GAME:
                self.load_game()
            elif self.command is QUIT:
                print(EXIT_MESSAGE)
                sys.exit()
            elif self.command is HELP:
                self.ui.print_help_menu()
            else:
                print(INVALID_MENU_COMMAND_MESSAGE)

            # Set these back to default values to ensure we don't enter endless loop
            self.command = INVALID_INPUT
            self.user_input = ""

    def main_menu_loop(self):
        '''
        Prints the main menu loop and sets self.command until command is set to a proper value
        :return:
        '''
        firstPass = True
        while not self.is_valid_menu_command(self. command):
            if firstPass:
                firstPass = False
            else:
                logger.debug(self.command + " : " + self.user_input)
            self.main_menu_prompt()
            self.command = self.lp.parse_command(self.user_input)



    def main_menu_prompt(self):
        '''
        Prints the main menu then prompts the user for input
        :return: none
        '''
        self.ui.print_main_menu()
        self.user_input = self.ui.user_prompt()

    def is_valid_menu_command(self, command):
        '''
        Checks the command returned from language parser against a list of valid menu commands defined on the
        GameClient class (which are in term constants defined in stringresources\verbs.py)
        :param command: A constant defined in stringresources\verbs.py
        :return: True or false depending on presence of the command in the list of valid commands
        '''
        if command in self.valid_main_menu_commands:
            return True
        else:
            return False

    def start_new_game(self):
        print(NEW_GAME_MESSAGE)

    def load_game(self):
        print(LOAD_GAME_MESSAGE)


class GameState:
    '''
    Holds all of the variables that maintain the game's state
    '''
    def __init__(self):
        self.rooms = []
        self.player = Player()

    def load_rooms_from_files(self):
        print("Loading rooms from files (This is a stub)")





class UserInterface:
    '''
    Primarily used to print information to the user's screen
    '''
    def __init__(self):
        self.prompt_text = ">> "

    def print_introduction(self):
        print(INTRO_STRING)

    def print_main_menu(self):
        for line in MAIN_MENU_LINES:
            print(line)

    def user_prompt(self):
        user_input = ""
        user_input = input(">> ")
        return user_input

    def print_help_menu(self):
        for line in HELP_MESSAGE:
            print(line)


class Player:
    '''
    Player stats and methods
    '''
    def __init__(self):
        self.cash = 0
        self.coolness = 0
        self.speed = 0
        self.inventory = Inventory()

class Inventory:
    '''
    Objects and methods related to adding and removing them from inventory
    '''
    def __init__(self):
        self.objects = []



class Object:

    def __init__(self, name, description):
        self.name = name
        self.description = description
