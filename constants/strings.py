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

from constants.constants import *
import textwrap

# This string should introduce the game once at loadup. Could replace with ASCII art if desired
# TODO: Replace INTRO_STRING with the introduction information in the Descriptions google doc
# URL: https://docs.google.com/document/d/1a4FziaNjpQGlQbCSIGH4rYGFegqCmM1LuPL1RIgQCLg/edit
INTRO_STRING = "Welcome to Hacker: The Movie: The Adventure Game: The Sequel"
DEFAULT_ROOM = "Street"

INVALID_MENU_COMMAND_MESSAGE = " is not a valid command at the main menu"
COMMAND_NOT_UNDERSTOOD = "What?! How dare you say that to me!"

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

# General UI strings
PROMPT_TEXT = ">> "
PRESS_KEY_TO_CONTINUE_MSG = "\n" + " Press [Enter] to continue ".center(80, "-")

# Status header strings
STATUS_HEADER_BAR = "=" * TEXT_WIDTH
STATUS_HEADER_LOCATION_LABEL = "\t[LOCATION]\t"
STATUS_HEADER_SPEED_LABEL = "\t[SPEED]\t\t"
STATUS_HEADER_COOLNESS_LABEL = "\t[COOLNESS]\t"
STATUS_HEADER_TIME_LABEL = "\t\t[TIME]\t"
STATUS_HEADER_CASH_LABEL = "\t\t[CASH]\t"
STATUS_HEADER_SKILLS_LABEL = "\t[SKILLS]\t"
STATUS_NO_SKILLS = "Nothing marketable!"

DESCRIPTION_HEADER = "DESCRIPTION:"
DESCRIPTION_FOOTER = "\n"
EXITS_HEADER = "Always know your exits:"
FEATURES_HEADER = "This area has the following interesting features:"
FEATURES_LIST_PREFIX = " * "
OBJECTS_HEADER = "You look around for anything not strapped down and you see:"
OBJECTS_LIST_PREFIX = " * "
CONNECTION_LIST_PREFIX = "  * ["
CONNECTION_LIST_SEGWAY= "] is "

# Various messages to user related to new/save/load/quit commands
NEW_GAME_MESSAGE = "Starting a new game."
LOAD_GAME_MESSAGE = "Let's load your saved game..."
LOAD_FILENAME_PROMPT = "Enter the number of the filename you wish to load and press [Enter]"
LOAD_CONFIRM_PROMPT = "Loading a game will cause you to lose unsaved progress.\nDo you wish to continue? (Y)es or (N)o"
LOAD_GAME_NO_SAVES = "There are no saved games available to load."
LOAD_NOT_INTEGER = "That's not a valid integer. Enter the number and press enter."
LOAD_OUT_OF_RANGE_MESSAGE = "That's not a valid menu option. Please choose an integer from the list to load the game"

SAVE_GAME_PROMPT = "Name a file to save this game (no extension): "
SAVE_GAME_SUCCESS = "Saving game to filename: "
SAVE_GAME_FAILED = "There was an error saving the game to filename: "
SAVE_GAME_VALID_FILENAME_MESSAGE = "Something about the filename you provided was invalid."
# QUIT_CONFIRM_PROMPT = "Quitting the game will cause you to lose unsaved progress.\nDo you wish to continue? (Y)es or (N)o"
QUIT_CONFIRM_PROMPT = "Quitting the game...\nDo you wish to save this game? (Y)es or (N)o"
YES_ALIASES = {'yes', 'y'}




# 'buy' strings
BUY_NOT_IN_ROOM = "That doesn't seem to be something you can buy here."
BUY_FREE_ITEM = "You don't have to buy that. Just take it!"
BUY_INSUFFICIENT_CASH_PREFIX = "You lack the necessary funds to make that purchase. It would cost $"
BUY_INSUFFICIENT_CASH_SUFFIX = " to buy that."
BUY_SUCCESS_PREFIX = "You hand over the cash and purchase the "
BUY_SUCCESS_SUFFIX = ", then carefully place it in your bag."
BUY_FEATURE_PREFIX = "You can't buy the "

# 'drop' strings
DROP_SUCCESS_PREFIX = "You drop the "
DROP_SUCCESS_SUFFIX = " on the ground."
DROP_FAILURE_PREFIX = "Your attempt to drop a "
DROP_FAILURE_SUFFIX = " fails because, alas, you do not have one."
DROP_FAILURE_VIRTUALSPACE = "You can't drop things in the virtual space!"
DROP_INVALID_PREFIX = "You can't drop the "
DROP_INVALID_SUFFIX = " because you're not carrying it. Don't be silly!"

# 'go' strings
GO_SUCCESS_PREFIX = "You head off towards the "
GO_SUCCESS_SUFFIX = " without a problem."
GO_FAILURE_PREFIX = "You try to go to the "
GO_FAILURE_SUFFIX = " but just can't find a way."
GO_INVALID_PREFIX = "You can't go to the "
GO_INVALID_SUFFIX = " because you're basically there already!"

# 'hack' strings
HACK_FAIL_NOSKILL = "You just don't know how to do that yet"
HACK_FAIL_INVALID_OBJECT = "There's no way to hack that. Try hacking something useful!"
HACK_FAIL_FEATURE_NOT_PRESENT = "There isn't one of those here to hack."
HACK_SUCCESS_TRAFFIC_LIGHTS = "You hack the Traffic Lights. You can cross the street whenever you want. That should make things a lot faster for you."

# 'help' strings
HELP_HEADER_TEXT = "HELP"
HELP_HEADER_TEXT_WIDTH = int((TEXT_WIDTH-(len(HELP_HEADER_TEXT)))/2)
HELP_HEADER = "=" * HELP_HEADER_TEXT_WIDTH + HELP_HEADER_TEXT + "=" * HELP_HEADER_TEXT_WIDTH + "\n"
HELP_MESSAGE = [
    "Type in a command. Valid commands are:",
    "* newgame:  Starts a new game when at the main menu",
    "* loadgame:  Load a saved game",
    "* savegame:  Save a game in progress",
    "* quit:  Exit back to main menu or the program if already there",
    "* help:  Prints this help message. Some hints can be found using 'help <object or feature'",
    "* look:  Prints the long-form description of a room again after a room has been visited",
    "* look at <object or feature>:  Looks at an object or feature",
    "* go <direction or description>:  Go to the direction or room you type. Must be directly accessible from your current location.",
    "* take <object>:  Take an object in the current room.",
    "* drop <object>:  Drop an object in the current location. You can't drop items when you're inside the network.",
    "* buy <object>:  Some objects cost money and cannot be taken.",
    "* steal <object>  Sometimes you don't have enough money to buy an object.",
    "* inventory  Look at all of the items youv'e collected so far.",
    "* hack <feature>  Try and hack a feature in the room. Not everything can be hacked.",
    "* spraypaint <feature>  If you have the necessary tools, you can paint the town red.",
    "* use <object or feature>  Everything has a purpose. Well, not everything."
]




HELP_FEATURE_GENERIC = " is a feature of the room. 'Look at' it to learn more."
HELP_OBJECT_GENERIC = " is an object. You can 'look at' an object and you can 'use' an object if it's in your 'inventory'."

# 'Inventory' strings
INVENTORY_LIST_HEADER = STATUS_HEADER_BAR + "\nBackpack Contents\n" + STATUS_HEADER_BAR
INVENTORY_LIST_FOOTER = STATUS_HEADER_BAR
INVENTORY_EMPTY = "Empty... not even a floppy disk"

# 'jail' strings
JAIL_GO_TO_MESSAGE = "Your actions have landed you in jail, costing you valuable time!"

# 'look' strings
NO_INTERESTING_OBJECTS_MESSAGE = " ...Hmmm, nothing worth taking."
NO_INTERESTING_FEATURES_MESSAGE = "You see nothing else worth checking out."


# 'Look at' strings
LOOK_AT_NOT_SEEN = "You do not see that here."

# 'steal' strings
STEAL_FAIL_ALREADY_OWNED = "You already own that. You can just take it!"
STEAL_FAIL_FREE_ITEM = "That doesn't cost anything. You should just take it - nobody will care!"
STEAL_SUCCESS_PREFIX = "Your nimble hands are able to procure the "
STEAL_SUCCESS_SUFFIX = " without being caught."
STEAL_FAIL_PRISON = "You aren't able to steal that without being seen. You've been caught!"
STEAL_FAIL_NOT_HERE = "Thou shalt not steal that which is not present!"

# 'take' strings
PICKUP_SUCCESS_PREFIX = "You pick up the "
PICKUP_SUCCESS_SUFFIX = " and put it in your backpack."
PICKUP_FAILURE_PREFIX = "You grasp for the non-existent "
PICKUP_FAILURE_SUFFIX = " and unsurprisingly fail!"
PICKUP_NOT_FREE = "That's not free. Perhaps you have the cash to Buy it... or, just steal it!"

# ' use' strings
USE_FAIL = "You cannot use that unless it is in your bag!"
USE_CASH_SUCCESS_PREFIX = "You count the bills and put them in your wallet. You are "
USE_CASH_SUCCESS_SUFFIX = " dollars richer!"
USE_COMPUTER_PARTS_SUCCESS = "You have used the computer parts successfully. Obviously we need to implement something here?!"
USE_COMPUTER_PARTS_MISSING = "You are missing some parts to the computer. Maybe you should read 'The Hacker's Guide to Building Amazing Hacking Machines' to see what you need?"
USE_HACKERMANUAL_SUCCESS = "You peruse the pages of the hacker manual and feel confident you can hack just about anything. Just don't get caught!"
USE_SNACKS_SUCCESS = "Crunchy yet satisfying. You feel faster, do you Grok it?"
USE_SKATEBOARD_SUCCESS = "Stepping onto the Skateboard, you feel as though you can do anything faster. Maybe that's just the Surge you drank for breakfast surging through your veins, though?"
USE_SPRAYPAINT_SUCCESS = "You spend a few moments shaking the Spray Paint and test it out. You can now spraypaint the town red!"
USE_SURGE_SUCCESS = "You gulp down the Surge and let out a belch. You feel energized!"

# Gameover cheating messages
GAMEOVER_CHEAT_WIN_MESSAGE = "Too cool for this game, eh? Well, you win!"
GAMEOVER_CHEAT_LOSE_MESSAGE = "Game too hard for you, script kiddie? L2Play, noob!"

# 'exit' messages
EXIT_MESSAGE = "Exiting the game, bye."
