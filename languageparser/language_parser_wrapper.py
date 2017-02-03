# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair
#
# language_parser_wrapper.py
# Description: Wraps the return values from LanguageParser
# Created by Shawn to interface between parser and GameClient; maintained by Shawn and Niza
#
# CITATIONS
# CITE:



# DEV NOTES: Here's how this would be used in LanguageParser:
#
# results = LanguageParserWrapper
# results.set_verb(STEAL)
# results.set_target("graphics card", OBJECT_TYPE)    # Need to define OBJECT_TYPE in the 'verbs.py' file
#
# You could also add subjects. Let's say you had 3 subjects, you could do a loop:
# for subject in subjects:
#     results.append_subject(subject.name, subject.type)

class LanguageParserWrapper:
    def __init__(self):
        self.verb = ""
        self.target = {}
        self.subjects = []
        self.preposition = ""

    def set_verb(self, verb_string):
        self.verb = verb_string

    def set_target(self, target_name_string, target_type_string):
        self.target['name'] = target_name_string
        self.target['type'] = target_type_string

    def add_subject(self, subject_name_string, subject_type_string):
        new_subject = {
            'name' : subject_name_string,
            'type' : subject_type_string
        }

        self.subjects.append(new_subject)

    def set_preposition(self, preposition_string):
        self.preposition = preposition_string

    def get_verb(self):
        return self.verb

    def get_target(self):
        return self.target

    def get_subjects(self):
        return self.subjects