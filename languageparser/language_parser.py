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
# UPDATE: Old logic commented out and full dictionary returned with parsing results -NV
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


		# Parse any command to all lowercase to reduce complexity of our parser.
		# TODO: Might also want to strip trailing whitespace (SSH)
		# l.strip() strips the left-side whitespace, not sure on right side whitespace (SSH)
		command = command.lower().lstrip()
		object = None
		targets = None

		'''
		
		# New Logic -NV

		# Go through list of words and try to pull out each significant word in VERB-NOUN-PREPOSTION-TARGET order 
		# Note: we are using 'TARGET' to mean 'object of the preposition' to avoid confusion with objects
		# TODO: Deal with punctuation accounting for it in messages
		# STRETCH GOAL (finished): account for NEGATIONS
		# STRETCH GOAL (finished): account for other word sentence structure
		if command == '':
			error = INVALID_EMPTY
			
		command = command.lower().lstrip()

		verb = None
		verb_is_special = False
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
		
		# VERB check: must have a verb unless we have a destination
		if error == None:
			for idx, word in enumerate(words):
				for alias_array in VERB_ALIASES:
					for verb_alias in alias_array:
						num_words_in_alias = len(verb_alias.split())
						words_sublist = words[idx: (idx + num_words_in_alias)]
						words_sublist_string = ' '.join(words_sublist)
						if words_sublist_string == verb_alias:
							if verb == None:
								# the alias arrays always store the base word at index 0
								verb = str(alias_array[0])
								# index = next word in command we are parsing
								verb_idx = last_idx = idx + num_words_in_alias - 1
							elif idx > last_idx:
								if words_sublist_string == verb:
									error = INVALID_DOUBLE
								else:
									error = INVALID_EXTRA_VERBS
		
		# TODO: deal with room names
		# Get all of the rooms by name
		self.rooms = self.RoomBuilder.load_room_data_from_file("../gamedata/rooms/*.json")
		for room in self.rooms:
			DESTINATIONS.append(room.get_name())

		# DESTINATION check: the model is VERB(GO)-> DESTINATION or just a DESTINATION
		if error == None and (verb == None or verb == GO):
			for word in words:
				if word in DESTINATIONS:
					if noun == None:
						verb_is_special = True
						noun = word
						noun_is ='destination'
					else:
						error = INVALID_EXTRA_DESTINATIONS
		# ERROR check: no verb or destination issue
		if error == None and noun == None and (verb == None or verb == GO):
			if verb == GO:
				error = INVALID_GO_NO_DESTINATION
			else:
				error = INVALID_NO_VERB
	

		# SUBJECT or PREPOSTION check: the model is VERB-> (PREPOSITION ANY SUBSEQUENT LOCATION) + NOUN-> TARGET
		if error == None and verb != GO and noun_is != 'destination':

			# use new var to avoid incorrect list slicing 
			start_idx = last_idx + 1
			
			# for each word in the remaining string, check if noun (object or feature) or preposition
			for idx, word in enumerate(words[start_idx:]):
		
				#PREPOSITION check
				for prep_name in PREPOSITIONS:
					# check number of words in name so we can compare correct number of words from command
					num_words_in_name = len(prep_name.split())
					words_sublist = words[(start_idx + idx): (start_idx + idx + num_words_in_name)]
					words_sublist_string = ' '.join(words_sublist)
					if words_sublist_string == prep_name:
						if preposition == None:
							preposition = words_sublist_string
							prep_idx = last_idx = start_idx + idx + num_words_in_name - 1 
						# currently can only use one
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
							# only save  the first occurance of object or feature
							if noun == None:
								# the alias arrays always store the base word at index 0
								noun = str(obj_alias_array[0])
								noun_is = 'object'
								#last index is the last index of the last noun or target we found
								noun_idx = last_idx = start_idx + idx + num_words_in_alias - 1 
							# second occurance will be the target and cannot also be the noun
							elif target == None and noun != str(obj_alias_array[0]):
								target = str(obj_alias_array[0])
								target_is = 'object'
								targ_idx = last_idx = start_idx + idx + num_words_in_alias - 1 
							# current index must > last one we found a noun or target in
							elif start_idx + idx > last_idx:
								if str(obj_alias_array[0]) == noun or str(obj_alias_array[0]) == target:
									error = INVALID_DOUBLE
								else:
									error = INVALID_EXTRA_NOUNS
							# else it is just a double, such as 'floppy disk' which could be 'floppy' and 'disk'
								
				for feat_name_array in FEATURES:
					for feat_name in feat_name_array:
						num_words_in_name = len(feat_name.split())
						words_sublist = words[(start_idx + idx): (start_idx + idx + num_words_in_name)]
						words_sublist_string = ' '.join(words_sublist)
						if words_sublist_string == feat_name:
							if noun == None:
								noun = words_sublist_string
								noun_is = 'feature'
								noun_idx = last_idx = start_idx + idx + num_words_in_name - 1 
							elif target == None and noun != words_sublist_string:
								target = words_sublist_string
								target_is = 'feature'
								targ_idx = last_idx = start_idx + idx + num_words_in_name - 1 
							elif start_idx + idx > last_idx:
								if words_sublist_string == noun or words_sublist_string == target:
									error = INVALID_DOUBLE
								else:
									error = INVALID_EXTRA_NOUNS
		

		#TODO: possibly add TALK to special verbs
		
		#SPECIAL VERB check:
		if error == None:
			#***Valid Structures***
			#DESTINATION
			#VERB(GO)-DESTINATION

			#VERB-NOUN
			#VERB-PREP-NOUN
			
			#VERB-NOUN-TARGET
			#VERB-NOUN-PREP-TARGET
			#VERB-PREP-NOUN-TARGET
			#**********************
			
			#SPECIAL VERB check:
			#TARGET must be a message string
			if verb == SPRAYPAINT:
				#TO DO: Add additional special verb functionality
				verb_is_special = True
				#VERB(SPRAYPAINT)-TARGET 
				if noun == None:
					if verb_idx + 1 < len(words):
						start_idx = verb_idx + 1
						words_sublist = words[start_idx :]
						target = ' '.join(words_sublist)
						target_is = 'message'
					else:
						error = INVALID_SPRAYPAINT_NO_MESSAGE
				#VERB(SPRAYPAINT)-NOUN-TARGET
				#VERB(SPRAYPAINT)-PREP-NOUN-TARGET
				elif preposition == None or prep_idx < noun_idx:
					if noun_idx + 1 < len(words):
						start_idx = noun_idx + 1
						words_sublist = words[start_idx :]
						target = ' '.join(words_sublist)
						target_is = 'message'
					else:
						error = INVALID_SPRAYPAINT_NO_MESSAGE
			
		#INVALID SENTENCE STRUCTURE check: check for these if not handled by special verbs above:
		if error == None and verb_is_special == False:
			#INVALID: VERB NOUN PREP (no TARGET)
			if noun != None and preposition != None and target == None:
				if prep_idx > noun_idx:
					error = INVALID_SENTENCE_STRUCTURE
			#INVALID: VERB NOUN TARGET PREP
			elif noun != None and target != None and preposition != None:
				if prep_idx > target_idx:
					error = INVALID_SENTENCE_STRUCTURE
			#NEGATION Check: If we have a non special verb sentence, there shouldn't be any negations
			for word in words:
				if word in NEGATIONS:
					error = INVALID_NEGATION
		return R
		
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
		


		'''
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
		'''