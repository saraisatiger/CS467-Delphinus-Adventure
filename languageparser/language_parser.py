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
#	 'verb' : 'use',
#	 'verb_subject_name' : 'broom',
#	 'targets' : [
#		 'dusty floor'
#	 ]
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
		
		# New Logic -NV///////////////////////////////////////////////////
		# parse command into words
		words = command.split()
		
		# Go through list of words and try to pull out each significant word in VERB-NOUN-PREPOSTION-TARGET order 
		# Note: we are using 'TARGET' to mean 'object of the preposition' to avoid confusion with objects
		# STRETCH GOAL: account for NEGATIONS
		# STRETCH GOAL: account for other word sentence structure
		verb = None
		noun = None
		noun_is = None
		preposition = None
		target = None
		target_is = None
		cur_idx = 0
		error = None
		prep_idx = -1
		noun_idx = -1
		targ_idx = -1

		# First significant word must be the VERB
		for idx, word in enumerate(words):
			for alias_array in VERB_ALIASES:
				for verb_alias in alias_array:
					if word == verb_alias:
						if verb == None:
							# the alias arrays always store the base word at index 0
							verb = str(alias_array[0])
							# index = next word in command we are parsing
							cur_index = idx + 1
						else:
							error = INVALID_MULTIPLE_VERBS
		
		if verb == None:
			error = INVALID_NO_VERB

		# Second word can be a SUBJECT or PREPOSTION  
		if error == None:
		
			# use new var to avoid incorrect list slicing 
			i = cur_index
			
			# for each word in the remaining string, check if noun (object or feature) or preposition
			for idx, word in enumerate(words[i:]):
			
			#VERB-PREP-NOUN
			#VERB-NOUN-PREP-TARGET
			
				#PREPOSITION check
				if word in PREPOSITIONS:
					#currently can only use one
					if preposition == None:
						preposition = word
						prep_idx = idx
					else:
						error = INVALID_EXTRA_PREPOSITIONS
				#NOUN and TARGET checks
				for obj_alias_array in OBJECT_ALIASES:
					for obj_alias in obj_alias_array:
						if word == obj_alias:
							# only save  the first occurance of object or feature
							if noun == None:
								# the alias arrays always store the base word at index 0
								noun = str(obj_alias_array[0])
								noun_is = 'object'
								noun_idx = idx
							# second occurance will be the target
							elif target == None:
								target = str(obj_alias_array[0])
								target_is = 'object'
								targ_idx = idx
							else:
								error = INVALID_EXTRA_NOUNS
								
				for feat_alias_array in FEATURES:
					for feat_alias in feat_alias_array:
						if word == feat_alias:
							if noun == None:
								noun = word
								noun_is = 'feature'
								noun_idx = idx
							elif target == None:
								target = word
								target_is = 'feature'
								targ_idx = idx
							else:
								error = INVALID_EXTRA_NOUNS
		
		R = LanguageParserWrapper()
		if error != None:
			R.set_error_message(str(error))
			
		if verb != None:
			R.set_verb(str(verb))
		else:
			R.set_verb("")
			
		if noun != None:
			R.set_noun(str(noun), str(noun_is))
		else:
			R.set_noun("", "")
			
		if preposition != None:
			R.set_preposition(str(preposition))
			
		if target != None:
			R.set_extra(str(target), str(target_is))
			
		logger.debug("Returning New Logic: \n" + str(R))

		

		#END New logic/////////////////////////////////////////////////
		

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

		results = LanguageParserWrapper()
		results.set_verb(str(command))
		results.set_noun(str(object), str("object"))

		#logger.debug("Returning: \n" + str(results))
		return results