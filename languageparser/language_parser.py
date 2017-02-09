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
<<<<<<< HEAD
#	 'verb' : 'use',
#	 'verb_object' : 'broom',
#	 'targets' : [
#		 'dusty floor'
#	 ]
=======
#     'verb' : 'use',
#     'verb_subject_name' : 'broom',
#     'targets' : [
#         'dusty floor'
#     ]
>>>>>>> c338678f07a38725a40e624e09a727d9158c1cca
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
<<<<<<< HEAD
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
		object = None
		targets = None
		
		# New Logic -NV
		# parse command into words
		words = command.split()
		
		# Go through list of words and try to pull out each significant word in VERB-SUBJECT-PREPOSTION-TARGET order 
		# Note: we are using 'TARGET' to mean 'object of the preposition' to avoid confusion with objects
		# STRETCH GOAL: account for NEGATIONS
		# STRETCH GOAL: account for other word sentence structure
		# STRETCH GOAL: improve logic of for loops if possible to reduce time
		verb = None
		subject = None
		subject_is = None
		preposition = None
		target = None
		target_is = None
		cur_index = 0
		save_cur_index = 0

		# Add Aliases logic .eval()?
		
		# First significant word should be the VERB
		i = 0
		while i < len(words):
			if words[i] in VERBS:
				cur_index = i + 1
				verb = words[i]
				break
			i += 1
						
		# Second significant word should be the SUBJECT (optional) either a FEATURE or OBJECT
		i = cur_index
		save_cur_index = cur_index
		while i < len(words):
			if words[i] in FEATURES:
				cur_index = i + 1
				subject = words[i]
				subject_is = 'FEATURE'
				break
			i += 1
						
		if subject_is != 'FEATURE':
			i = save_cur_index
			while i < len(words):
				if words[i] in OBJECTS:
					cur_index = i + 1
					subject = words[i]
					subject_is = 'OBJECT'
					break
				i += 1
							
		# If there is no VERB, command is invalid
		if verb == None:
			verb = INVALID_INPUT
			
		# Third significant word should be the PREPOSITION (optional)
		# If there is no SUBJECT, skip the check for PREPOSTION
		if subject != None:
			i = cur_index
			while i < len(words):
				if words[i] in PREPOSITIONS:
					cur_index = i + 1
					preposition = words[i]
					break
				i += 1
							
		# Fourth significatn word should be the TARGET (optional)either a FEATURE or OBJECT
		# If there is no PREPOSTION, skip the check for TARGET 
		save_cur_index = cur_index
		if subject != None and preposition != None:
			i = cur_index
			while i < len(words):
				if words[i] in FEATURES:
					cur_index = i + 1
					target = words[i]
					target_is = 'FEATURE'
					break
				i += 1
						
		if subject != None and preposition != None and target_is != 'FEATURE':
			#reset to same starting search index as before
			i = save_cur_index
			while i < len(words):
				if words[i] in OBJECTS:
					cur_index = i + 1
					target = words[i]
					target_is = 'OBJECT'
					break
							
		logger.debug("New Logic: " + str(verb) + ", " + str(subject) + ", " + str(preposition)+ ", " + str(target))
		# Put in JSON Object
		# Return 
		
		
		#END New logic
		

		# Hacky way to parse a "look at" command to find the verb_object/feature player wants to examine.
		# NOTE: Doesn't parse aliases
		if 'look at' in command:
			object = command.replace("look at ", "", 1) # replace "look at " with empty string - rest is the verb_object
			command = "look at"

		# hacky way to parse a 'take' command.
		# NOTE: Doesn't parse aliases
		elif 'take' in command:
			object = command.replace("take ", "", 1) # replace at most one instance of "take " with empty str
			command = "take"

		# hacky way to parse a 'drop' command
		# NOTE: Doesn't parse aliases
		elif 'drop' in command:
			object = command.replace("drop ", "", 1) # replace at most one instance of "drop " with empty str
			command = "drop"

		# Same thing for go
		elif 'go' in command:
			object = command.replace("go ", "", 1)
			command = "go"

		elif 'buy' in command:
			object = command.replace("buy ", "", 1)
			command = "buy"

		elif 'use' in command:
			object = command.replace("use ", "", 1)
			command = "use"


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
		# cheat codes
		elif command == "mess with the best":
			command = CHEATCODE_LOSE
		elif command == "die like the rest":
			command = CHEATCODE_WIN

		else:
			command = INVALID_INPUT

		logger.debug("Returning: " + str(command) + ", " + str(object) + ", " + str(targets))
		return (command, object, targets)
=======
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

        elif 'hack' in command:
            subject = command.replace("hack ", "", 1)
            command = "hack"
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
        elif command in HACK_ALIASES:
            command = HACK
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
>>>>>>> c338678f07a38725a40e624e09a727d9158c1cca
