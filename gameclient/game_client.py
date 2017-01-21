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
        self.valid_main_menu_commands = { QUIT, LOAD_GAME, NEW_GAME }

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
        self.main_menu_loop()

    def main_menu_loop(self):
        self.main_menu_prompt()
        self.command = self.lp.parse_command(self.user_input)
        while not self.is_valid_menu_command(self. command):
            logger.debug("Invalid command is: " + self.command)
            self.main_menu_loop()

        print("Command is: " + self.command)

    def main_menu_prompt(self):
        self.ui.print_main_menu()
        self.user_input = self.ui.user_prompt()

    def is_valid_menu_command(self, command):
        if command in self.valid_main_menu_commands:
            return True
        else:
            return False






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
