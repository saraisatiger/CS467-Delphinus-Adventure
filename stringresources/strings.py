'''
These strings are used in the game_client.py to retreive strings from one central location
'''

# This string should introduce the game once at loadup. Could replace with ASCII art if desired
INTRO_STRING = "Welcome to Hacker: The Movie: The Adventure Game: The Sequel"
NO_INTERESTING_OBJECTS_MESSAGE = "You see nothing interesting laying around that you can pick up."

# main menu related strings
MAIN_MENU_1 = "MAIN MENU"
MAIN_MENU_2 = "newgame :: \tbegin a new game"
MAIN_MENU_3 = "loadgame:: \tload game from save"
MAIN_MENU_4 = "quit :: \texit game"
MAIN_MENU_5 = "help :: \tPrint instructions for the game"
MAIN_MENU_LINES = [
    MAIN_MENU_1,
    MAIN_MENU_2,
    MAIN_MENU_3,
    MAIN_MENU_4,
    MAIN_MENU_5,
]


NEW_GAME_MESSAGE = "Starting a new game."
LOAD_GAME_MESSAGE = "Let's load saved game."



# Prints when a user uses the 'help' verb
HELP_MESSAGE_1 = "Here's the information on how to play the game..."
HELP_MESSAGE_2 = "Type in a command. Valid commands are: "
VALID_VERB_LIST = "[[TODO: Fill in this list in strings.py]]: newgame, loadgame, quit, help, look, look at <object>, inventory, etc"
HELP_MESSAGE = [
    HELP_MESSAGE_1,
    HELP_MESSAGE_2,
    VALID_VERB_LIST
]


INVALID_MENU_COMMAND_MESSAGE = "That is not a valid command at the main menu"

EXIT_MESSAGE = "Exiting the game, bye."