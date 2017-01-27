# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair
#
# strings.py
# Description:  Used by game engine
# Principal Author of this file per Project plan: Shawn Hillyer
#
# CITATIONS
# CITE: Used a similar concept as seen in Android app development. Android uses an XML format; I just am localizing all
# of the strings here to one file so we can easily modify things without having to dig through code to find strings (SSH)
# CITE: Also this is similar to how our assembly programs stored strings in one spot and just referenced by name later


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
LOAD_GAME_MESSAGE = "Let's load saved game..."
QUIT_CONFIRM_PROMPT = "Are you sure you wish to quit this game and go to the main menu? (Y)es or (N)o"
YES_ALIASES = {'yes', 'y'}


# Prints when a user uses the 'help' verb
HELP_MESSAGE_1 = "Here's the information on how to play the game..."
HELP_MESSAGE_2 = "Type in a command. Valid commands are: "
VALID_VERB_LIST = "newgame, loadgame, quit, help, look, look at <object>, go <direction or description>, take <object>, \ndrop <object>, inventory, hack, steal <object>, buy <object>, spraypaint, use <object or feature>\n"
HELP_MESSAGE = [
    HELP_MESSAGE_1,
    HELP_MESSAGE_2,
    VALID_VERB_LIST
]

# Message used when player tries to look at something that isn't in current room/inventory
LOOK_AT_NOT_SEEN = "You do not see that here."

# Inventory-related strings
PICKUP_SUCCESS_PREFIX = "You pick up the "
PICKUP_SUCCESS_SUFFIX = " and put it in your backpack."

PICKUP_FAILURE_PREFIX = "You grasp for the non-existent "
PICKUP_FAILURE_SUFFIX = " and unsurprisingly fail!"

DROP_SUCCESS_PREFIX = "You drop the "
DROP_SUCCESS_SUFFIX = " on the ground."
DROP_FAILURE_PREFIX = "Your attempt to drop a "
DROP_FAILURE_SUFFIX = " fails because, alas, you do not have one."

INVENTORY_LIST_HEADER = "Your backpack contains: "
INVENTORY_EMPTY = "Absolutely nothing (say it again!)"


# Movement related
GO_SUCCESS_PREFIX = "You head off towards the "
GO_SUCCESS_SUFFIX = " without a problem."
GO_FAILURE_PREFIX = "You try to go to the "
GO_FAILURE_SUFFIX = " but just can't find a way."



INVALID_MENU_COMMAND_MESSAGE = "That is not a valid command at the main menu"
COMMAND_NOT_IMPLEMENTED_YET = "Either that verb isn't implemented yet, or you typed gibberish!"

# Gameover messages
GAMEOVER_CHEAT_WIN_MESSAGE = "Too cool for this game, eh? Well, you win!"
GAMEOVER_CHEAT_LOSE_MESSAGE = "Game too hard for you, script kiddie? L2Play, noob!"

EXIT_MESSAGE = "Exiting the game, bye."