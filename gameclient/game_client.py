from languageparser.language_parser import LanguageParser
from fileio.room_builder import RoomBuilder
from stringresources.strings import *
from stringresources.verbs import *
from stringresources.status_codes import *

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
                self.initialize_new_game()
            elif self.command is LOAD_GAME:
                self.load_game_menu()
            elif self.command is QUIT:
                print(EXIT_MESSAGE)
                sys.exit()
            elif self.command is HELP:
                self.ui.print_help_menu()
            else:
                print(INVALID_MENU_COMMAND_MESSAGE)

            # Player decided to play the game, gamestate has already been initialized in the if/else above
            if self.command is NEW_GAME or self.command is LOAD_GAME:
                '''
                Actually playing the game will eventually terminate for one of the below reasons
                We handle each case separately because if a player forfeits and does not save,
                it can have different logic than if they quit and save, etc.
                The constants are defined in stringresources\status_codes.py
                '''
                exit_code = self.play_game()
                if exit_code is GAMEOVER_FORFEIT:
                    print("Game over: Forfeit")
                elif exit_code is GAMEOVER_WIN:
                    print("Game over: Player won")
                elif exit_code is GAMEOVER_LOSE:
                    print("Game over: Player lost")
                elif exit_code is GAMEOVER_SAVE:
                    print("Game over: Player saved game")
                elif exit_code is GAMEOVER_LOAD:
                    print("Game over: Player loading game")
                    self.load_game_menu()


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



    def play_game(self):
        '''
        Primary game loop that prints information to user, reads input, and reacts accordingly
        :return:
        '''
        print(NEW_GAME_MESSAGE)

        status = GAME_CONTINUE

        print_long_description = False  # Override for if user just typed the 'look' command

        while status is GAME_CONTINUE:
            # Check game status; if gameover, leave game
            status = self.game_status()
            if status in GAMEOVER_STATES:
                return status

            # Print appropriate description
            if self.gamestate.current_location.visited is False or print_long_description is True:
                print(self.gamestate.current_location.get_long_description())
                self.gamestate.current_location.set_visited()
                print_long_description = False
            else:
                print(self.gamestate.current_location.get_short_description())

            # Prompt user for input
            self.user_input = self.ui.user_prompt()
            self.command = self.lp.parse_command(self.user_input)


            # Conditionally handle each possible verb
            if self.command is LOOK:
                print_long_description = True
            else:
                print("Either that isn't implemented yet, or you typed gibberish!")

            self.user_input = ""
            self.command = INVALID_INPUT






    def load_game_menu(self):
        print(LOAD_GAME_MESSAGE)

    def initialize_new_game(self):
        logger.debug("A new game would be initialized here")
        self.gamestate.set_current_location(self.gamestate.rooms[0])

    def game_status(self):
        # TODO: Implement this properly. Status codes in stringresources\status_codes.py
        # if self.gamestate.player.speed is 0:
        #     return GAMEOVER_LOSE
        #
        # else:
            return GAME_CONTINUE


class GameState:
    '''
    Holds all of the variables that maintain the game's state
    '''
    def __init__(self):
        self.rooms = []
        self.player = Player()

    def load_rooms_from_files(self):
        logger.debug("Loading rooms from files (This is a stub)")

    def set_current_location(self, room):
        self.current_location = room





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
