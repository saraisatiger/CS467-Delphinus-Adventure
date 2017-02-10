# Unit tests for language parser
# Created by Shawn

import unittest
from constants.verbs import *
from languageparser.language_parser import *
from fileio.object import *
from debug.debug import *

logger = logging.getLogger(__name__)


class TestLanguageParser(unittest.TestCase):
    def setUp(self):
        self.LP = LanguageParser()
        self.ObjectBuilder = ObjectBuilder()
        self.objects = self.ObjectBuilder.load_object_data_from_file("../gamedata/objects/*.json")
        self.object_names = []
        for obj in self.objects:
            self.object_names.append(obj.get_name())

    def test_lp_newgame_valid_strings(self):
        for test_string in NEW_GAME_ALIASES:
            result = self.LP.parse_command(test_string)
            expected_noun = {'name': None, 'type': None}
            self.assertEquals(NEW_GAME, result.get_verb(), NEW_GAME + " does not match " + str(result.get_verb()))
            self.assertEquals(expected_noun, result.get_noun())
            self.assertIsNone(result.get_extras())
            self.assertIsNone(result.get_preposition())
            self.assertIsNone(result.get_error_message())
            logger.debug("Checking if string returns verb NEW_GAME: '" + test_string + "'")
            logger.debug("Passed.")

    def test_lp_loadgame_valid_strings(self):
        for test_string in LOAD_GAME_ALIASES:
            result = self.LP.parse_command(test_string)
            expected_noun = {'name': None, 'type': None}
            self.assertEquals(LOAD_GAME, result.get_verb(), LOAD_GAME + " does not match " + str(result.get_verb()))
            self.assertEquals(expected_noun, result.get_noun())
            self.assertIsNone(result.get_extras())
            self.assertIsNone(result.get_preposition())
            self.assertIsNone(result.get_error_message())
            logger.debug("Checking if string returns verb LOAD_GAME: '" + test_string + "'")
            logger.debug("Passed.")

    def test_lp_help_valid_strings(self):
        for test_string in HELP_ALIASES:
            result = self.LP.parse_command(test_string)
            expected_noun = {'name': None, 'type': None}
            self.assertEquals(HELP, result.get_verb(), HELP + " does not match " + str(result.get_verb()))
            self.assertEquals(expected_noun, result.get_noun())
            self.assertIsNone(result.get_extras())
            self.assertIsNone(result.get_preposition())
            self.assertIsNone(result.get_error_message())
            logger.debug("Checking if string returns verb HELP: '" + test_string + "'")
            logger.debug("Passed.")

    def test_lp_quit_valid_strings(self):
        for test_string in QUIT_ALIASES:
            result = self.LP.parse_command(test_string)
            self.assertEquals(QUIT, result.get_verb(), QUIT + " does not match " + str(result.get_verb()))
            expected_noun = {'name': None, 'type': None}
            self.assertEquals(expected_noun, result.get_noun())
            self.assertIsNone(result.get_extras())
            self.assertIsNone(result.get_preposition())
            self.assertIsNone(result.get_error_message())
            logger.debug("Checking if string returns verb QUIT: '" + test_string + "'")
            logger.debug("Passed.")

    def test_lp_buy_valid_object_names(self):
        for obj_name in self.object_names:
            test_string = "buy " + str(obj_name)
            obj_name = obj_name.lower()
            expected_noun = {'name': obj_name, 'type': "object"}
            result = self.LP.parse_command(test_string)
            self.assertEquals(BUY, result.get_verb(), BUY + " does not match " + str(result.get_verb()))
            self.assertEquals(expected_noun, result.get_noun())
            self.assertIsNone(result.get_extras())
            self.assertIsNone(result.get_preposition())
            self.assertIsNone(result.get_error_message())
            logger.debug("Checking if string returns verb BUY: '" + test_string + "' and NOUN: '" + obj_name + "'")
            logger.debug("Passed.")

    def test_lop_by_invalid_object_names(self):
        invalid_object_names = [
            '', ' ', '\n', '\t', 'hi', '  hi', 'flippers', 'two words'
        ]

        for obj_name in invalid_object_names:
            test_string = "buy " + str(obj_name)
            obj_name = obj_name.lower()
            # TODO: Revise this unit test with revised language parser logic
            # I think the language parser actually sets expected_noun to None instead of dictionary of None values?
            expected_noun = {'name': '', 'type': 'object'}
            result = self.LP.parse_command(test_string)
            self.assertEquals(BUY, result.get_verb(), INVALID_INPUT + " does not match " + str(result.get_verb()))
            self.assertEquals(expected_noun, result.get_noun())
            self.assertEquals(None, result.get_extras())
            self.assertEquals(None, result.get_preposition())
            self.assertIsNone(result.get_extras())
            logger.debug("Checking if string returns verb BUY: '" + test_string + "' and NOUN: '" + obj_name + "'")
            logger.debug("Passed.")


if __name__ == '__main__':
    unittest.main()