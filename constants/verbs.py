# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair
#
# verbs.py
# Description:  Used by language parser - possibly a temporary solution to parsing the commands.
# Principal Author of this file per Project plan: Shawn Hillyer (Shawn conceived this to help in developing the language
#  parser enough to implement the game engine)
#
# CITATIONS
# CITE: None
#Additions of subjects & prepositions add to language parser functionality, though they don't do much for the file name -NV
#subjects- objects and features
#objects and aliases
CASH_CRISP = 'crisp cash'
CASH_CRISP_ALIASES = {'crisp', 'crisp money'} 
CASH_WAD = 'cash wad'
CASH_WAD_ALIASES = {'wad of cash', 'wad of money', 'money wad'}
SKATEBOARD = 'skateboard'
SKATEBORD_ALIASES = {'board', 'plank'}
HACKERSNACKS = 'hackersnacks'
HACKERSNACKS_ALIASES = {'snacks', 'munchies'}
SURGE = 'surge'
SURGE_ALIASES = {'soda', 'drink', 'beverage'} 
SPRAY_PAINT = 'spray paint'
SPRAY_PAINT_ALIASES = {'paint'}
FLOPPY_DISK = 'floppy disk'
FLOPPY_DISK_ALIASES = {'floppy', 'disk'}
GRAPHICS_CARD = 'graphics card'
GRAPHICS_CARD_ALIASES = {'card', 'graphics'}
RAM = 'ram chip'
RAM_ALIASES = {'random access memory', 'memory', 'chip', 'ram'}

OBJECTS = [SKATEBOARD, HACKERSNACKS, SURGE, SPRAY_PAINT, FLOPPY_DISK, GRAPHICS_CARD, RAM]

OBJECTS_AND_ALIASES = [SKATEBOARD, SKATEBORD_ALIASES, HACKERSNACKS, HACKERSNACKS_ALIASES, SURGE, SURGE_ALIASES, SPRAY_PAINT, SPRAY_PAINT_ALIASES, FLOPPY_DISK, FLOPPY_DISK_ALIASES, GRAPHICS_CARD, GRAPHICS_CARD_ALIASES, RAM, RAM_ALIASES]

#features 
#TODO: add aliases, simple 'look at' features and descriptions to ROOMS, then add logic here
R1_F = {'no skateboarding sign', 'gaurdrails'}
R2_F = {'phone booth', 'trash can'}
R3_F = {'ramp', 'death to the patriarchy'}
R4_F = {'counter', 'shelves', 'store clerk'}
R5_F = {'atm', 'cash', 'guard'}
R6_F = {'your gear', 'unattended police computer', 'police officer', 'unoccupied desk', 'metal door'}
R7_F = {'locker', 'teacher', 'fire alarm'}
R8_F = {'school-wide intercom mic', 'office computer', 'acid burn', 'clock', 'poster'}
R9_F = {'door', 'ledge'}
R10_F = {'disk drive', 'panel', 'terminal'}
R11_F = {'bug', 'firewall'}
R12_F = {'emojis', 'creature', 'acid burn'}
R13_F = {'input / output port', 'sentient cpu'}
R14_F = {'cat videos from the internet', 'nuclear launch codes'}
R15_F = {'binary files', 'corrupted files'}
R16_F = {'acid burn', 'diving board', 'windows'}

FEATURES = [R1_F, R2_F, R3_F, R4_F, R5_F, R6_F, R7_F, R8_F, R9_F, R10_F, R11_F, R12_F, R13_F, R14_F, R15_F, R16_F]

#propositions
PREPOSITIONS = {'on', 'in', 'onto', 'into', 'below', 'behind', 'above', 'over', 'next to', 'in front of', 'about'}

#verbs
# In alphabetical order
BUY = 'buy'
BUY_ALIASES = {'buy', 'purchase', 'pay for'}
CHEATCODE_LOSE = 'cheatcode lose'
CHEATCODE_LOSE_ALIASES = {'mess with the best'}
CHEATCODE_WIN = 'cheatcode win'
CHEATCODE_WIN_ALIASES = {'die like the rest'}
DROP = 'drop'
DROP_ALIASES = {'drop', 'put down', 'let go', 'leave'}
GO = "go"
GO_ALIASES = {'go', 'move', 'walk', 'run'}
HACK = 'hack'
HACK_ALIASES = {'hack'}
HELP = 'help'
HELP_ALIASES = {'help', 'info', 'information', 'assist', 'assistance'}
LOAD_GAME = 'load game'
LOAD_GAME_ALIASES = {'loadgame', 'load game', 'load_game_menu', 'load my game', 'load saved game', 'load old game'}
LOOK = 'look'
LOOK_ALIASES = {'look'}
LOOK_AT = 'look at'
LOOK_AT_ALIASES = {'look at', 'examine'}
TAKE = 'take'
TAKE_ALIASES = {'take', 'pick up', 'grab', 'acquire'}
INVENTORY = 'inventory'
INVENTORY_ALIASES = {'inventory', 'backpack', 'bag'}
INVALID_INPUT = 'invalid command'
NEW_GAME = 'new game'
NEW_GAME_ALIASES = {'newgame', 'new game', "hacktheplanet"}
QUIT = 'quit'
QUIT_ALIASES = {'quit', 'exit', 'bye', 'goodbye', 'leave game'}
SAVE_GAME = 'save game'
SAVE_GAME_ALIASES = ['save', 'savegame', 'save game', 'save_game']
SPRAYPAINT = 'spraypaint'
SPRAYPAINT_ALIASES = {'spraypaint', 'tag', 'spray'}
STEAL = 'steal'
STEAL_ALIASES = {'steal'}
USE = 'use'
USE_ALIASES = {'use'}

VERBS = [BUY, CHEATCODE_LOSE, CHEATCODE_WIN, DROP, GO, HACK, HELP, LOAD_GAME, LOOK, LOOK_AT, TAKE, INVENTORY,  NEW_GAME, QUIT, SAVE_GAME, SPRAYPAINT, STEAL, USE]

VERB_AND_ALIASES = [BUY, BUY_ALIASES, CHEATCODE_LOSE, CHEATCODE_LOSE_ALIASES, CHEATCODE_WIN, CHEATCODE_WIN_ALIASES, DROP, DROP_ALIASES, GO, GO_ALIASES, HACK, HACK_ALIASES, HELP, HELP_ALIASES, LOAD_GAME, LOAD_GAME_ALIASES, LOOK, LOOK_ALIASES, LOOK_AT, LOOK_AT_ALIASES, TAKE, TAKE_ALIASES, INVENTORY, INVENTORY_ALIASES, NEW_GAME, NEW_GAME_ALIASES, QUIT, QUIT_ALIASES, SAVE_GAME, SAVE_GAME_ALIASES, SPRAYPAINT, SPRAYPAINT_ALIASES, STEAL, STEAL_ALIASES, USE, USE_ALIASES]
