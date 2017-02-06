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
# results.set_subject("graphics card", OBJECT_TYPE)    # Need to define OBJECT_TYPE in the 'verbs.py' file
#
# You could also add targets. Let's say you had 3 targets, you could do a loop:
# for subject in targets:
#     results.append_target(subject.name, subject.type)

class LanguageParserWrapper:
    def __init__(self):
        self.verb = ""
        self.subject = {}
        self.targets = []
        self.preposition = ""

    def __str__(self):
        '''
        override str() method for debug purposes
        :return:
        '''
        str = "{\n\t'verb' : '" + self.verb + "'\n"
        str += "\t'subject['name']' : '" + self.subject['name'] + "'\n"
        str += "\t'subject['type']' : '" + self.subject['type'] + "'\n"
        str += "\t'targets' : "
        if self.targets:
            for target in self.targets:
                str += "\n\t{\n['name' : '" + target['name'] + "']\n"
                str += "\t['type' : '" + target['type'] + "']\n},"
        else:
            str+= "\t\tNone\n"

        str += "\t'preposition' : "
        try:
            str += "'" + self.preposition + "'\n"
        except:
            str += "None\n"

        str += "}"
        return str

    def set_verb(self, verb_string):
        self.verb = verb_string

    def set_subject(self, target_name_string, target_type_string):
        self.subject['name'] = target_name_string
        self.subject['type'] = target_type_string

    def append_target(self, subject_name_string, subject_type_string):
        new_target = {
            'name' : subject_name_string,
            'type' : subject_type_string
        }

        self.targets.append(new_target)

    def set_preposition(self, preposition_string):
        self.preposition = preposition_string

    def get_verb(self):
        return self.verb

    def get_subject(self):
        return self.subject

    def get_targets(self):
        return self.targets