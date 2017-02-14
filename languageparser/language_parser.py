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
		if command == '':
			error = INVALID_EMPTY
			
		command = command.lower().lstrip()
		object = None
		targets = None
		
		# New Logic -NV///////////////////////////////////////////////////

		# Go through list of words and try to pull out each significant word in VERB-NOUN-PREPOSTION-TARGET order 
		# Note: we are using 'TARGET' to mean 'object of the preposition' to avoid confusion with objects
		# STRETCH GOAL: account for NEGATIONS
		# STRETCH GOAL: account for other word sentence structure
		verb = None
		special_verb = False
		noun = None
		noun_is = None
		preposition = None
		target = None
		target_is = None
		error = None
		verb_idx = -1
		prep_idx = -1
		noun_idx = -1
		targ_idx = -1
		last_idx = -1

		# Check for empty string
		if command == '':
			error = INVALID_EMPTY
			
		# parse command into words
		words = command.split()
		
		# VERB check: must have a verb unless we have a direction
		if error == None:
			for idx, word in enumerate(words):
				for alias_array in VERB_ALIASES:
					for verb_alias in alias_array:
						num_words_in_alias = len(verb_alias.split())
						words_sublist = words[idx: (idx + num_words_in_alias)]
						words_sublist_string = ' '.join(words_sublist)
						if words_sublist_string == verb_alias:
							logger.debug("v: " + words_sublist_string + " / " + verb_alias)
							if verb == None:
								# the alias arrays always store the base word at index 0
								verb = str(alias_array[0])
								# index = next word in command we are parsing
								verb_idx = idx 
								last_idx = idx + num_words_in_alias - 1
							elif idx > last_idx:
								if words_sublist_string == verb:
									error = INVALID_DOUBLE
								else:
									error = INVALID_EXTRA_VERBS
								
		# DIRECTION check: the model is VERB(GO)-> DIRECTION or just a DIRECTION
		if error == None and (verb == None or verb == GO):
			for word in words:
				if word in DIRECTIONS:
					if noun == None:
						noun = word
						noun_is ='direction'
					else:
						error = INVALID_EXTRA_DIRECTIONS
		# ERROR check: no verb or direction issue
		if error == None and noun == None and (verb == None or verb == GO):
			if verb == GO:
				error = INVALID_GO_NO_DIRECTION	
			else:
				error = INVALID_NO_VERB
	

		# SUBJECT or PREPOSTION check: the model is VERB-> (PREPOSITION ANY SUBSEQUENT LOCATION) + NOUN-> TARGET
		if error == None and verb != GO and noun_is != 'direction':

			# use new var to avoid incorrect list slicing 
			start_idx = verb_idx + 1
			
			# for each word in the remaining string, check if noun (object or feature) or preposition
			for idx, word in enumerate(words[start_idx:]):
		
				#PREPOSITION check
				if word in PREPOSITIONS:
					# currently can only use one
					if preposition == None:
						preposition = word
						prep_idx = start_idx + idx
					else:
						error = INVALID_EXTRA_PREPOSITIONS
				#NOUN and TARGET checks
				for obj_alias_array in OBJECT_ALIASES:
					for obj_alias in obj_alias_array:
						# check number of words in alias so we can compare correct number of words from command
						num_words_in_alias = len(obj_alias.split())
						words_sublist = words[(start_idx + idx): (start_idx + idx + num_words_in_alias)]
						words_sublist_string = ' '.join(words_sublist)
						if words_sublist_string == obj_alias:
							logger.debug("o: " + words_sublist_string + " / " + obj_alias)
							# only save  the first occurance of object or feature
							if noun == None:
								# the alias arrays always store the base word at index 0
								noun = str(obj_alias_array[0])
								noun_is = 'object'
								noun_idx = start_idx + idx
								#last index is the last index of the last noun or target we found
								last_idx = start_idx + idx + num_words_in_alias - 1 
							# second occurance will be the target and cannot also be the noun
							elif target == None and noun != str(obj_alias_array[0]):
								target = str(obj_alias_array[0])
								target_is = 'object'
								targ_idx = start_idx + idx
								last_idx = start_idx + idx + num_words_in_alias - 1 
							# current index must > last one we found a noun or target in
							elif start_idx + idx > last_idx:
								if str(obj_alias_array[0]) == noun or str(obj_alias_array[0]) == target:
									error = INVALID_DOUBLE
								else:
									error = INVALID_EXTRA_NOUNS
							# else it is just a double, such as 'floppy disk' which could be 'floppy' and 'disk'
								
				for feat_alias_array in FEATURES:
					for feat_alias in feat_alias_array:
						num_words_in_alias = len(feat_alias.split())
						words_sublist = words[(start_idx + idx): (start_idx + idx + num_words_in_alias)]
						words_sublist_string = ' '.join(words_sublist)
						if words_sublist_string == feat_alias:
							logger.debug("f: " + words_sublist_string + " / " + feat_alias)
							if noun == None:
								noun = words_sublist_string
								noun_is = 'feature'
								noun_idx = start_idx + idx
								last_idx = start_idx + idx + num_words_in_alias - 1 
							elif target == None and noun != words_sublist_string:
								target = words_sublist_string
								target_is = 'feature'
								targ_idx = start_idx + idx
								last_idx = start_idx + idx + num_words_in_alias - 1 
							elif start_idx + idx > last_idx:
								if words_sublist_string == noun or words_sublist_string == target:
									error = INVALID_DOUBLE
								else:
									error = INVALID_EXTRA_NOUNS
		
		'''
		#Still working on this logic
		
		#SENTENCE STRUCTURE & SPECIAL VERB check:
		if error = None:
			#***Valid Structures***
			#DIRECTION
			#VERB(GO)-DIRECTION

			#VERB-NOUN
			#VERB-PREP-NOUN
			
			#VERB-NOUN-TARGET
			#VERB-NOUN-PREP-TARGET
			#VERB-PREP-NOUN-TARGET
			#**********************
			
			#SPECIAL VERB check:
			

			if VERB == SPRAYPAINT
				special_verb = True
				#VERB(SPRAYPAINT)-PREP-NOUN-TARGET("MESSAGE STRING WHICH CAN BE ANYTHING SO TARGET DOESN'T MATTER")		
				#VERB(SPRAYPAINT)-NOUN-PREP-TARGET("MESSAGE STRING WHICH CAN BE ANYTHING SO TARGET DOESN'T MATTER")
				

			#INVALID SENTENCE STRUCTURE check: check for these if not handled by special verbs above:
			
			#INVALID: VERB NOUN PREP
			elif special_verb = False and verb != None and noun != None and preposition != None:
				if prep_idx > noun_idx:
					error = INVALID_SENTENCE_STRUCTURE
			#INVALID: VERB NOUN TARGET PREP
			elif special_verb = False and verb != None and noun != None and target != None and preposition != None:
				if prep_idx > target_idx:
					error = INVALID_SENTENCE_STRUCTURE
		'''
		
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