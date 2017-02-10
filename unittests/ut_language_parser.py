# Unit tests for project
# Created by Shawn

import unittest
from constants.verbs import *
from languageparser.language_parser import *


class TestLanguageParser(unittest.TestCase):

    def setUp(self):
        self.LP = LanguageParser()

    def test_lp_main_menu(self):
        # Test 'newgame' and aliases
        for str in NEW_GAME_ALIASES:
            result = self.lp.parse_command(str)
            self.assertEquals(result.get_verb(), NEW_GAME)
            self.assertEquals(result.get_noun(), None)
            self.assertEquals(result.get_extras(), None)
            self.assertEquals(result.get_preposition(), None)
            self.assertEquals(result.get_error_message(), None)

        self.LP.parse_command()


if __name__ == '__main__':
    unittest.main()