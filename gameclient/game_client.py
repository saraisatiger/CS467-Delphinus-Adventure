# DELPHINUS - ADVENTURE APP
# CS 467 - Winter 2017
# Team Members: Sara Hashem, Shawn Hillyer, Niza Volair

# game_client.py
# Description: GameClient class and closely-related classes
# Principal Author of this file per Project plan: Shawn Hillyer

# CITATIONS
# CITE: http://stackoverflow.com/questions/4810537/how-to-clear-the-screen-in-python
# CITE: http://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
# CITE: https://docs.python.org/3.3/library/random.html

from constants.gameplay_settings import *
from constants.language_words import *
from gameclient.game_state import *
from gameclient.random_event_generator import *
from gameclient.user_interface import *
from gameclient.wprint import *
from languageparser.language_parser import LanguageParser

from debug.debug import *
logger = logging.getLogger(__name__)


class GameClient:
    '''
    Main controller for the game's flow and logic
    '''
    def __init__(self):
        self.gamestate = GameState()

        # Instantiate unenforced singleton-style instances of various components
        self.ui = UserInterface()
        self.lp = LanguageParser()
        self.rand_event = RandomEventGenerator()

        # Variables used to store GameClient state
        self.reset_input_and_command()
        self.valid_main_menu_commands = { QUIT, LOAD_GAME, NEW_GAME , HELP }

        # Clear old console text before beginning game
        self.ui.clear_screen()

    def main_loop(self):
        '''
        Main control loop for game
        '''

        # Outer loop makes game play until user decides to quit from the main menu
        while self.command is not QUIT:

            # Inner loop runs the main menu and prompts until a valid command is entered
            self.main_menu_loop()

            # Branch initializes a new game or ends up loading a game, quits, or just prints the help and loops
            if self.command is NEW_GAME:
                try:
                    self.gamestate.initialize_new_game()
                except:
                    logger.debug("initialize_gamestate() exception")
            elif self.command is LOAD_GAME:
                try:
                    self.load_game_menu()
                except:
                    logger.debug("load_game_menu() exception")
            # Or exit the game...
            elif self.command is QUIT:
                wprint(EXIT_MESSAGE)
                sys.exit()
            # Or print the help menu
            elif self.command is HELP:
                self.ui.print_help_message()
                self.reset_input_and_command()
                continue

            # This logic exits ONLY IF Player decided to play game. GameState initialized in the if/elif structure above
            if self.command is NEW_GAME or self.command is LOAD_GAME:
                # Actually playing the game will eventually terminate for one of the below reasons
                # We handle each case separately because if a player forfeits and does not save,
                # it can have different logic than if they quit and save, etc.
                # The constants are defined in constants/gameover_status_codes.py

                if self.command is NEW_GAME:
                    self.ui.print_splash_screen_new_game()
                elif self.command is LOAD_GAME:
                    self.ui.print_splash_screen_load_game()

                exit_code = self.play_game()
                if exit_code is GAMEOVER_FORFEIT:
                    wprint("Game over: Forfeit")
                elif exit_code is GAMEOVER_WIN:
                    wprint("Game over: Player won")
                elif exit_code is GAMEOVER_LOSE:
                    wprint("Game over: Player lost")
                elif exit_code is GAMEOVER_SAVE:
                    self.save_game_menu()
                    wprint("Game over: Player saved game")
                elif exit_code is GAMEOVER_LOAD:
                    wprint("Game over: Player loading game")
                    self.reset_input_and_command()
                    self.command = LOAD_GAME
                    continue
                elif exit_code is GAMEOVER_QUIT:
                    wprint("Game over: Player quit")
                    self.reset_input_and_command()
            self.ui.wait_for_enter()
            self.reset_input_and_command()

    def main_menu_loop(self):
        '''
        Prints the main menu and sets self.command until command is set to a proper value
        :return: indirectly - sets instance variable, self.command, to a valid command
        '''

        # first_pass logic is to ensure we don't print invalid command to the user unless it's their second attempt
        first_pass = True
        while not self.is_valid_menu_command(self.command):
            if first_pass:
                first_pass = False
            else:
                self.ui.clear_screen()
                wprint(self.user_input + INVALID_MENU_COMMAND_MESSAGE + "\n\n")
                self.ui.wait_for_enter()
            self.main_menu_prompt()

            self.send_command_to_parser()

    def main_menu_prompt(self):
        '''
        Prints the main menu then prompts the user for input one time_left
        :return: Indirectly - sets instance variable user_input to the string typed by user
        '''
        self.ui.print_main_menu()
        self.user_input = self.ui.user_prompt()

    def is_valid_menu_command(self, command):
        '''
        Checks the command returned from language parser against a list of valid menu commands defined on the
        GameClient class (which are in term constants defined in constants\verbs.py)
        :param command: A constant defined in constants\verbs.py
        :return: True or false depending on presence of the command in the list of valid commands
        '''
        if command in self.valid_main_menu_commands:
            return True
        else:
            return False

    def reset_input_and_command(self):
        # Reset the input and command/verb_noun_name/targets from parser
        self.user_input = None
        self.verb_noun_name = None
        self.verb_noun_type = None
        self.verb_targets = None
        self.verb_preposition = None
        self.command = INVALID_INPUT
        self.extras = None

    def play_game(self):
        '''
        Primary game loop that prints information to user, reads input, and reacts accordingly
        :return: a status code as defined in constants\status_codes.py, used by gameclient to determine how
        and/or why game ended.
        '''

        status = GAME_CONTINUE          # Force entry into main loop

        print_long_description = False  # Override if user just typed the 'look' command

        # Game will loop until a 'Gameover' condition is met
        while status is GAME_CONTINUE:
            # Check game status; if Gameover, leave game loop and return status code
            status = self.gamestate.game_status()

            if status in GAMEOVER_STATES:  # list as defined in constants\gameover_status_codes.py
                return status

            # Handling for 'use computer' hint for player
            self.game_hint_check()

            # Print the current room's appropriate long_description
            self.verb_look(print_long_description)
            print_long_description = False # Reset this to false after printing

            # Prompt user for input and parse the command
            self.user_input = self.ui.user_prompt()
            self.send_command_to_parser()


            # TODO: Refactor verb_*() methods to check the parser_error_message before proceeding
            # Conditionally handle each possible verb / command
            if self.command is LOOK:
                # The verb_look() method is called at the top of each loop, so not explicitly called here
                print_long_description = True
                self.gamestate.update_time_left(LOOK_COST)
                self.ui.clear_screen()
            # Verbs
            elif self.command is LOOK_AT:
                self.verb_look_at(self.verb_noun_name, self.verb_noun_type)
            elif self.command is INVENTORY:
                self.verb_inventory()
            elif self.command is TAKE:
                self.verb_take(self.verb_noun_name, self.verb_noun_type)
            elif self.command is DROP:
                self.verb_drop(self.verb_noun_name)
            elif self.command is GO:
                self.verb_go(self.verb_noun_name, self.parser_error_message)
            elif self.command is HACK:
                self.verb_hack(self.verb_noun_name, self.verb_noun_type)
            elif self.command is STEAL:
                self.verb_steal(self.verb_noun_name, self.verb_noun_type)
            elif self.command is BUY:
                self.verb_buy(self.verb_noun_name)
            elif self.command is SKATE:
                self.verb_skate()
            elif self.command is SPRAYPAINT:
                self.verb_spraypaint(self.extras)
            elif self.command is USE:
                self.verb_use(self.verb_noun_name, self.verb_noun_type)
            elif self.command is HELP:
                self.verb_help(self.verb_noun_name, self.verb_noun_type)
            elif self.command is LOAD_GAME:
                load_confirmed = self.verb_quit(LOAD_CONFIRM_PROMPT)
                if load_confirmed == True:
                    status = GAMEOVER_LOAD
            elif self.command is SAVE_GAME:
                self.save_game_menu()
            elif self.command is CHEATCODE_WIN:
                status = self.verb_cheat_win()
            elif self.command is CHEATCODE_LOSE:
                status = self.verb_cheat_lose()
            elif self.command is QUIT:
                quit_confirmed = self.verb_quit(QUIT_CONFIRM_PROMPT)
                if quit_confirmed is True:
                    save_game_prompt = self.verb_save(SAVE_GAME_PROMPT)
                    if save_game_prompt is True:
                        status = GAMEOVER_SAVE
                    else:
                        status = GAMEOVER_QUIT
            else:
                wprint(COMMAND_NOT_UNDERSTOOD)
                self.ui.wait_for_enter()

        return status

    def load_game_menu(self):
        '''
        Sets appropriate variables in the GameClient's gamestate instance
        :return:
        '''
        wprint(LOAD_GAME_MESSAGE)

        savegame_list = SaveGame.get_savegame_filenames()

        if savegame_list:
            input_is_valid = False
            option = -1

            while input_is_valid is False:
                input_is_valid = True # Turn this back to false if we get exception converting to an int
                counter = 1
                for savegame in savegame_list:
                    wprint(str(counter) + ": " + savegame)
                    counter += 1

                wprint(LOAD_FILENAME_PROMPT)
                user_choice = self.ui.user_prompt()

                # Cite: http://stackoverflow.com/questions/5424716/how-to-check-if-input-is-a-number
                try:
                    option = int(user_choice)
                except:
                    wprint(LOAD_NOT_INTEGER)
                    input_is_valid = False
                    continue

                option -= 1
                if option < 0 or option >= len(savegame_list):
                    wprint(LOAD_OUT_OF_RANGE_MESSAGE)
                    input_is_valid = False
                    continue

            # If here we have a valid option
            self.gamestate.initialize_load_game(savegame_list[option])
            return True

        else:
            wprint(LOAD_GAME_NO_SAVES)
            return False

    def save_game_menu(self):
        save_game = SaveGame(self.gamestate)
        game_file = self.gamestate.game_file
        file_name = ""
        valid_filename = False

        if game_file == "":
            while valid_filename is False or file_name == "":
                wprint(SAVE_GAME_FILE_PROMPT)
                file_name = self.ui.user_prompt()
                valid_filename = save_game.is_existing_saved_game(file_name)
                while valid_filename is False:
                    wprint(SAVE_GAME_INVALID_EXISTS)
                    wprint(SAVE_GAME_AGAIN)
                    file_name = self.ui.user_prompt()
                    valid_filename = save_game.is_existing_saved_game(file_name)
        elif game_file:
            wprint(SAVE_GAME_EXISTING + game_file + '.json')
            wprint(SAVE_GAME_EXISTING_PROMPT)
            confirm = self.ui.user_prompt()
            if confirm in YES_ALIASES:
                file_name = game_file
                save_game.write_to_file(file_name)
            else:
                wprint(SAVE_GAME_FILE_PROMPT)
                file_name = self.ui.user_prompt()
                valid_filename = save_game.is_existing_saved_game(file_name)
                while valid_filename is False:
                    wprint(SAVE_GAME_INVALID_EXISTS)
                    wprint(SAVE_GAME_AGAIN)
                    file_name = self.ui.user_prompt()
                    valid_filename = save_game.is_existing_saved_game(file_name)

        while save_game.write_to_file(file_name) is False:
            wprint(SAVE_GAME_INVALID_CHARACTERS)
            wprint(SAVE_GAME_FAILED + file_name + '.json')
            wprint(SAVE_GAME_AGAIN)
            file_name = self.ui.user_prompt()
            valid_filename = save_game.is_existing_saved_game(file_name)
            while valid_filename is False:
                wprint(SAVE_GAME_INVALID_EXISTS)
                wprint(SAVE_GAME_AGAIN)
                file_name = self.ui.user_prompt()
                valid_filename = save_game.is_existing_saved_game(file_name)

        wprint(SAVE_GAME_SUCCESS + file_name + '.json')
        self.ui.wait_for_enter()

    def go_to_jail(self):
        jail_name = R7[0]
        jail_room = self.gamestate.get_room_by_name(jail_name)
        self.gamestate.set_current_room(jail_room)
        wprint(JAIL_GO_TO_MESSAGE)
        self.gamestate.update_time_left(JAIL_COST)

    def verb_buy(self, noun_name):
        '''
        :param noun_name: string, name of the object desired
        :return: True if player bought object_name, false otherwise
        '''
        buy_succeeded = False

        room_feature = self.gamestate.get_current_room().get_feature_by_name(noun_name)
        if room_feature is not None:
            wprint(BUY_FEATURE_PREFIX + room_feature.get_name())
            buy_succeeded = False
        else:
            object = self.gamestate.get_current_room().get_object_by_name(noun_name)
            player_cash = self.gamestate.player.get_cash()

            if object is None:
                wprint(BUY_NOT_IN_ROOM)
            elif object.get_cost() is 0:
                wprint(BUY_FREE_ITEM)
            # elif object.is_owned_by_player() is True:
            #     wprint(BUY_FREE_ITEM)
            elif object.get_cost() > player_cash:
                wprint(BUY_INSUFFICIENT_CASH_PREFIX + str(object.get_cost()) + BUY_INSUFFICIENT_CASH_SUFFIX)
            else:
                self.gamestate.player.add_object_to_inventory(object)
                self.gamestate.get_current_room().remove_object_from_room(object)
                self.gamestate.player.update_cash(object.get_cost() * -1 ) # Send in cost as negative to reduce cash
                wprint(BUY_SUCCESS_PREFIX + object.get_name() + BUY_SUCCESS_SUFFIX)
                buy_succeeded = True

        if buy_succeeded:
            self.gamestate.update_time_left(BUY_COST)

        self.ui.wait_for_enter()
        return buy_succeeded

    def verb_cheat_win(self):
        self.ui.clear_screen()
        wprint(GAMEOVER_CHEAT_WIN_MESSAGE)
        return GAMEOVER_WIN

    def verb_cheat_lose(self):
        self.ui.clear_screen()
        wprint(GAMEOVER_CHEAT_LOSE_MESSAGE)
        return GAMEOVER_FORFEIT

    def verb_drop(self, object_name):
        drop_success = False

        room_feature = self.gamestate.get_current_room().get_feature_by_name(object_name)
        if room_feature is not None:
            wprint(DROP_INVALID_PREFIX + room_feature.get_name() + DROP_INVALID_SUFFIX)
            drop_success = False

        else:
            inventory_object = self.gamestate.player.inventory.get_object_by_name(object_name)

            if self.gamestate.get_current_room().is_virtual_space() is True:
                wprint(DROP_FAILURE_VIRTUALSPACE)
            elif inventory_object is not None:
                self.gamestate.player.inventory.remove_object(inventory_object)
                self.gamestate.get_current_room().add_object_to_room(inventory_object)
                wprint(DROP_SUCCESS_PREFIX + self.verb_noun_name + DROP_SUCCESS_SUFFIX)
                drop_success = True
            else:
                wprint(DROP_FAILURE_PREFIX + self.verb_noun_name + DROP_FAILURE_SUFFIX)

        if drop_success:
            self.gamestate.update_time_left(DROP_COST)

        self.ui.wait_for_enter()
        return drop_success

    def verb_go(self, destination, error_message):
        go_success = False

        destination = destination.lower()
        destination_room_name = None
        cur_room = self.gamestate.get_current_room()
        cur_room_name = cur_room.get_name().lower()

        if destination is None or destination.isspace():
           message = GO_FAILURE_DESTINATION_MISSING

        room_feature = self.gamestate.get_current_room().get_feature_by_name(destination)
        if room_feature is not None:
            message = GO_INVALID_PREFIX + room_feature.get_name() + GO_INVALID_SUFFIX

        else:
            # See if the destination is the cardinal direction OR the name of one of the room_connections
            for connection in cur_room.room_connections:
                if connection.label.lower() == destination or connection.cardinal_direction.lower() == destination:
                    destination_room_name = connection.destination.lower()

                    # Handle sub-way logic:
                    if cur_room_name == "subway":
                        # It's free to go back where you came from, so check that first
                        if destination_room_name.lower() == self.gamestate.get_prior_room().get_name().lower():
                            go_success = True
                            break
                        elif cur_room.get_feature_by_name("Turnstiles").is_hacked() is not True:
                            if self.gamestate.player.get_cash() < SUBWAY_GO_DOLLAR_COST:
                                message = GO_FAILURE_SUBWAY_CASH
                                go_success = False
                                break
                            else:
                                self.gamestate.player.update_cash(SUBWAY_GO_DOLLAR_COST * -1)
                                go_success = True
                                break
                        else:
                            go_success = True
                            break

                    elif cur_room_name == "your computer":
                        if self.gamestate.endgame_data['computer_room']['is_operable'] is True:
                            go_success = True
                            break
                        else:
                            message = GO_FAILURE_COMPUTER_INOPERABLE
                            go_success = False
                            break

                    elif cur_room_name == "inside the metaverse":
                        if destination_room_name == "data tower":
                            has_fireball = self.gamestate.player.has_object_by_name(FIREBALL)
                            has_bug_carcass = self.gamestate.player.has_object_by_name("bug carcass") # TODO: Replace string with constant from language_words.py once defined

                            if has_fireball is False or has_bug_carcass is False:
                                go_success = False
                                wprint("You need the fireball and bug carcass to proceed") # TODO: Make better message to user?
                                break
                            else:
                                go_success = True
                                break

                    # Any room without special-handling / restrictions on movement is authorized to move, handle here
                    else:
                        go_success = True
                        break
                else:
                    message = GO_FAILURE_PREFIX + self.verb_noun_name + GO_FAILURE_SUFFIX


        if go_success is True:
            new_room = self.gamestate.get_room_by_name(destination_room_name)
            if new_room:
                self.gamestate.set_current_room(new_room)
                message = GO_SUCCESS_PREFIX + new_room.get_name() + GO_SUCCESS_SUFFIX
                self.gamestate.update_time_left(GO_COST)
                go_success = True
            else:
                # If go failed to find the room / direction desired, print a failure message
                logger.debug("The 'go' command almost worked, but the destination room isn't in the GameState.rooms list")
                logger.debug(GO_FAILURE_PREFIX + self.verb_noun_name + GO_FAILURE_SUFFIX)
                message = GO_FAILURE_PREFIX + self.verb_noun_name + GO_FAILURE_SUFFIX



        wprint(message)
        self.ui.wait_for_enter()
        return go_success

    def verb_hack(self, noun_name, noun_type):
        hack_success = False
        hacking_detected_by_police = False
        message = "Somehow message didn't get assigned, yikes! Tell the developer what you were doing!"

        if self.gamestate.player.can_hack() is False:
            message = HACK_FAIL_NOSKILL
        else: # Player can hack, try it
            if noun_type == NOUN_TYPE_OBJECT:
                message = HACK_FAIL_INVALID_TARGET
                hack_success = False

            elif noun_type == NOUN_TYPE_FEATURE:
                cur_room = self.gamestate.get_current_room()

                try:
                    feature = cur_room.get_feature_by_name(noun_name)
                    feature_name = feature.get_name().lower()

                    if feature.is_hackable() is True:
                        if feature.is_hacked() is True:
                            message = HACK_FAIL_ALREADY_HACKED

                        else: # Not hacked yet, player will attempt the hack
                            # These logical branches we don't allow the player to go to jail (while in jail or in metaverse)
                            if feature_name == "unattended police desktop":
                                hacking_detected_by_police = False
                                if self.gamestate.jailroom_data['cell_unlocked'] is True:
                                    message = HACK_SUCCESS_JAIL_COMPUTER
                                    self.gamestate.set_current_room(self.gamestate.get_room_by_name("street"))
                                    self.gamestate.initialize_jailroom_data()
                                    hack_success = True
                                else:
                                    message = HACK_FAIL_IN_CELL

                            elif feature_name == "binary files":
                                hack_success = self.hack_binary_files()
                                if hack_success is True:
                                    message = HACK_SUCCESS_BINARY_FILES
                                else:
                                    message = HACK_FAIL_BINARY_FILES

                            elif feature_name == "corrupted files":
                                hack_success = self.hack_corrupted_files()
                                if hack_success is True:
                                    message = HACK_SUCCESS_CORRUPTED_FILES
                                else:
                                    message = HACK_FAIL_CORRUPTED_FILES

                            elif feature_name == "Cat Videos from the Internet".lower():
                                hack_success = self.hack_cat_videos()
                                if hack_success is True:
                                    message = HACK_SUCCESS_CAT_VIDEOS
                                else:
                                    message = HACK_FAIL_CAT_VIDEOS

                            elif feature_name == "Nuclear Launch Codes".lower():
                                hack_success = self.hack_launch_codes()
                                if hack_success is True:
                                    message = HACK_SUCCESS_LAUNCH_CODES
                                else:
                                    message = HACK_FAIL_LAUNCH_CODES

                            # Every other hack has a chance of sending to jail
                            else:
                                hacking_detected_by_police = not self.rand_event.attempt_hack()

                                if hacking_detected_by_police is True:
                                    message = HACK_FAIL_CAUGHT
                                elif hacking_detected_by_police is False:
                                    if feature_name == "traffic lights":
                                        message = HACK_SUCCESS_TRAFFIC_LIGHTS
                                        self.gamestate.player.update_speed(HACK_LIGHT_SPEED_CHANGE)
                                        hack_success = True

                                    elif feature_name == "atm":
                                        message = HACK_SUCCESS_ATM + " You get " + str(HACK_ATM_CASH_AMOUNT) + " bucks."
                                        self.gamestate.player.update_cash(HACK_ATM_CASH_AMOUNT)
                                        hack_success = True

                                    elif feature_name == "turnstiles":
                                        message = HACK_SUCCESS_TURNSTILE
                                        hack_success = True

                                    else:
                                        message = "You tried to hack something that is hackable and has not already " \
                                                  "been hacked, but the programmers forgot to program an effect. " \
                                                  "Email the authors! "

                    else: # Feature is not a hackable feature
                        message = HACK_FAIL_INVALID_TARGET

                except:
                    message = HACK_FAIL_FEATURE_NOT_PRESENT
            else: # Player tried to hack something that's not an object or feature so it's nonsense
                message = HACK_FAIL_NONSENSE

        if hack_success is True:
            try:
                feature.set_is_hacked(True)
            except:
                logger.debug("hack_success is True but failed to call feature.set_is_hacked(True)")

        wprint(message)
        if hacking_detected_by_police is True:
            self.go_to_jail()
        self.ui.wait_for_enter()
        return hack_success


    def verb_help(self, noun_name, noun_type):
        '''
        Print help. Gives a generic message if user tries to call help on a feature or object in the room/inventory,
        otherwise just prints the generic help message.
        :param noun_name: subject passed back by language parser
        :param noun_type: subject's type (object/feature) as passed back from language parser
        :return:
        '''
        if noun_type == NOUN_TYPE_FEATURE:
            # Only print a hep message if the feature is part of current room to avoid confusion and player trying to
            # call the 'look at' verb on features in other rooms that they are not presently in
            room_feature = self.gamestate.get_current_room().get_feature_by_name(noun_name)
            if room_feature is not None:
                wprint(room_feature.get_name() + HELP_FEATURE_GENERIC)
                self.ui.wait_for_enter()
                return

        elif noun_type == NOUN_TYPE_OBJECT:
            # Only display help on objects in the current room or player's inventory. Generic message but avoids people
            # mining for information by spamming 'help' I suppose
            obj = self.gamestate.get_current_room().get_object_by_name(noun_name)
            if obj is None:
                obj = self.gamestate.player.inventory.get_object_by_name(noun_name)
            if obj is not None:
                wprint(obj.get_name() + HELP_OBJECT_GENERIC)
                self.ui.wait_for_enter()
                return
            else:
                self.ui.print_help_message()
        else:
            self.ui.print_help_message()

    def verb_inventory(self):
        self.gamestate.update_time_left(INVENTORY_COST)
        inventory_description = self.gamestate.player.get_inventory_string()
        self.ui.print_inventory(inventory_description)
        self.ui.wait_for_enter()

    def verb_look(self, print_long_description):
        '''
        First clear the screen then determine correct version to print.
        :param print_long_description: If set to true, forces long_description to print even if user has been in room
        before. Used for 'look' command
        :return:
        '''
        self.ui.clear_screen()

        cur_room = self.gamestate.get_current_room()
        if cur_room.is_visited() is False or print_long_description is True:
            description = cur_room.get_long_description()
        else:
            description = cur_room.get_short_description()

        header_info = self.gamestate.get_header_info()
        self.ui.print_status_header(header_info)

        # Print any 'graffiti' (spray paint messages)
        spray_painted_message = self.gamestate.get_room_spray_painted_message(cur_room.get_name())
        if spray_painted_message is not None:
            self.ui.print_graffiti(spray_painted_message)

        self.ui.print_room_description(description)
        self.gamestate.get_current_room().set_visited()

    def verb_look_at(self, noun_name, noun_type):
        '''
        Attempts to look at the subject
        :param noun_name: Grammatical object at which player wishes to look.
                            Could be a feature or an object in environment or in their inventory
        :return: None
        '''
        room_feature = self.gamestate.get_current_room().get_feature_by_name(noun_name)
        room_object = self.gamestate.get_current_room().get_object_by_name(noun_name)
        player_object = self.gamestate.player.inventory.get_object_by_name(noun_name)



        looked_at_trash_can = False
        looked_at_panel = False
        looked_at_bug = False
        looked_at_firewall = False

        if room_feature is not None:
            try:
                description = room_feature.get_description()
                room_feature_name = room_feature.get_name().lower()
                # CHeck for special room feature logic
                if room_feature_name == "trash can":
                    looked_at_trash_can = True
                elif room_feature_name == "panel":
                    looked_at_panel = True
                elif room_feature_name == "bug":
                    looked_at_bug = True
                elif room_feature_name == "firewall":
                    looked_at_firewall = True

            except:
                logger.debug("verb_look_at(): room_feature.get_description() exception")
                description = "Uh oh, something has gone wrong. Contact the developer!"
        elif room_object is not None:
            try:
                description = room_object.get_long_description()
            except:
                logger.debug("verb_look_at(): room_object.get_description() exception")
                description = "Uh oh, something has gone wrong. Contact the developer!"
        elif player_object is not None:
            try:
                description = player_object.get_long_description()
            except:
                logger.debug("verb_look_at(): player_object.get_description() exception")
                description = "Uh oh, something has gone wrong. Contact the developer!"
        else:
            description = LOOK_AT_NOT_SEEN

        self.gamestate.update_time_left(LOOK_AT_COST)
        description = textwrap.fill(description, TEXT_WIDTH)
        # image = textwrap.fill(image, TEXT_WIDTH)
        print(description) # Don't use wprint() or it will remove linebreaks
        try:
            room_object_art = self.gamestate.get_object_art(noun_name)
            if room_object_art is not None:
                print(room_object_art)
        except:
            logger.debug("Error with room object art method?")

        self.ui.wait_for_enter()

        # Handle special look at 'minigame' logic
        if looked_at_trash_can is True:
            self.search_trash_can()
        elif looked_at_panel is True:
            self.install_pc_components()
        elif looked_at_bug is True:
            self.minigame_bug()
        elif looked_at_firewall is True:
            self.minigame_firewall()

    def verb_quit(self, message):
        '''
        Prints the message passed in then prompts user if they are sure they wish to quit
        :param message: string
        :return: message that should be printed
        '''
        self.ui.clear_screen()
        self.ui.print_quit_confirm(message)
        confirm = self.ui.user_prompt().lower()
        if confirm in YES_ALIASES:
            return True
        return False

    def verb_save(self, message):
        '''
        Prints the message passed in then prompts user if they are sure they wish to save
        :param message: string
        :return: message that should be printed
        '''
        self.ui.clear_screen()
        self.ui.print_quit_confirm(message)
        confirm = self.ui.user_prompt().lower()
        if confirm in YES_ALIASES:
            return True
        return False

    def verb_take(self, noun_name, noun_type):
        '''
        Evaluates a command to take object_name from the Room and if it exists (and is allowed by game rules) then
        object placed in inventory for the player
        :param noun_name: string input by player in their command
        :return: True (success), False ( fail, object_name not found in the room)
        '''
        take_success = False

        if noun_type == NOUN_TYPE_FEATURE:
            # logger.debug("verb_take() noun_type == 'feature'")
            room_feature = self.gamestate.get_current_room().get_feature_by_name(noun_name)
            if room_feature is None:
                message = ("You don't see a " + noun_name + " to try and take.")
            else:
                message = ("You cannot take the " + room_feature.get_name() + " - that's impractical.")

        elif noun_type == NOUN_TYPE_OBJECT:
            # logger.debug("verb_take() noun_type == 'object'")
            room_object = self.gamestate.get_current_room().get_object_by_name(noun_name)

            if room_object is not None:
                if room_object.get_cost() is 0 or room_object.get_name() in self.gamestate.player.owned:
                    self.gamestate.get_current_room().remove_object_from_room(room_object)
                    self.gamestate.player.add_object_to_inventory(room_object)
                    message = (PICKUP_SUCCESS_PREFIX + self.verb_noun_name + PICKUP_SUCCESS_SUFFIX)
                    take_success = True
                elif room_object.get_cost() > 0:
                    message = (PICKUP_NOT_FREE)
            # Otherwise failed:
            else:
                message = (PICKUP_FAILURE_PREFIX + self.verb_noun_name + PICKUP_FAILURE_SUFFIX)

        else:
            message = (PICKUP_FAILURE_PREFIX + self.verb_noun_name + PICKUP_FAILURE_SUFFIX)

        if take_success:
            self.gamestate.update_time_left(TAKE_COST)

        wprint(message)
        self.ui.wait_for_enter()
        return take_success

    def verb_use(self, noun_name, noun_type):
        use_success = True
        current_room_name = self.gamestate.get_current_room().get_name().lower()
        noun_name = noun_name.lower()
        message = "This should never print. Check verb_use() logic"

        # Special 'use' case, 'use computer'. It's not a literal object that can be used, just the verbiage we chose
        if noun_name == "computer":
            if self.gamestate.player.has_computer_parts() is True:
                self.gamestate.set_current_room(self.gamestate.get_room_by_name("your computer"))
                use_success = True

                # Conditionally remove the 'new laptop' object if that's the item they had and toggle on 'operable' var
                if self.gamestate.player.has_object_by_name(NEW_COMPUTER) is True:
                    new_pc_item = self.gamestate.player.inventory.get_object_by_name(NEW_COMPUTER)
                    self.gamestate.player.remove_object_from_inventory(new_pc_item)
                    self.gamestate.endgame_data['computer_room']['is_operable'] = True
                    message = "You boot up the new computer and jack into the nearest RJ-45 port you can find. Time to Hack!"
                else: # Player must have the rest of the parts they needed, instead
                    message = "You have what you need to repair your computer! Time to install the components... A [Floppy Disk], a [Graphics Card], and a [RAM Chip] are spread out upon your portable anti-static mat!"

            else:
                message = "You don't have everything you need to fix your computer. Your [Floppy Disk] is toast, your [Graphics Card] is burned up, and the [RAM Chip] is corrupted! Or, you could just go buy a [New Laptop]!"

        elif noun_type == NOUN_TYPE_FEATURE:
            message = "You cannot use that."
            use_success = False
        elif noun_type == NOUN_TYPE_OBJECT:
            used_object = self.gamestate.player.inventory.get_object_by_name(noun_name)

            if used_object is not None:
                obj_label = used_object.get_name().lower()

                if obj_label == CASH_CRISP.lower():
                    cash_gained = self.rand_event.get_random_cash_amount(CASH_CRISP_MIN, CASH_CRISP_MAX)
                    self.gamestate.player.update_cash(cash_gained)
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    message = (USE_CASH_SUCCESS_PREFIX + str(cash_gained) + USE_CASH_SUCCESS_SUFFIX)
                elif obj_label == CASH_WAD.lower():
                    cash_gained = self.rand_event.get_random_cash_amount(CASH_WAD_CASH_MIN, CASH_WAD_CASH_MAX)
                    self.gamestate.player.update_cash(cash_gained )
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    message = (USE_CASH_SUCCESS_PREFIX + str(cash_gained) + USE_CASH_SUCCESS_SUFFIX)
                elif obj_label in {ACMERAM.lower(), RAM.lower(), GRAPHICS_CARD.lower()}:
                    if current_room_name == "your computer":
                        message = "You should take a [look at the panel] on the back of [Your Computer] to install this."
                    else:
                        message = USE_FAIL_COMPONENT_INSTALL
                elif obj_label == FLOPPY_DISK.lower():
                    if current_room_name == "your computer":
                        message = self.install_floppy_disk()
                    else:
                        message = USE_FAIL_COMPONENT_INSTALL
                elif obj_label == HACKERSNACKS.lower():
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    self.gamestate.player.update_speed(SNACK_SPEED_INCREASE)
                    message = (USE_SNACKS_SUCCESS)
                elif obj_label == SKATEBOARD.lower():
                    self.gamestate.player.set_has_skate_skill(True)
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    self.gamestate.player.update_speed(SKATEBOARD_SPEED_INCREASE)
                    message = (USE_SKATEBOARD_SUCCESS)
                elif obj_label == SPRAY_PAINT.lower():
                    self.gamestate.player.set_has_spraypaint_skill(True)
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    message = (USE_SPRAYPAINT_SUCCESS)
                elif obj_label == HACKER_MANUAL.lower():
                    self.gamestate.player.set_has_hack_skill(True)
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    message = (USE_HACKERMANUAL_SUCCESS)
                elif obj_label == SURGE.lower():
                    self.gamestate.player.remove_object_from_inventory(used_object)
                    self.gamestate.player.update_speed(SNACK_SPEED_INCREASE)
                    message = (USE_SURGE_SUCCESS)

                # TODO: TEST LOGIC BETWEEN HERE AND TODO END COMMENT AFTER PARSER SUPPORTS
                elif obj_label == FIREBALL.lower():
                    pass
                    # TODO: Once language parser passes back the preposition and target, we can pass it to below
                    target_feature = ""
                    if target_feature == "binary files":
                        self.use_object_on_feature(obj_label, target_feature, self.use_fireball_on_binary_files)

                elif obj_label == "bug carcass".lower():
                    pass
                    # TODO: Once language parser passes back the preposition and target, we can pass it to below
                    target_feature = ""
                    if target_feature == "binary files":
                        self.use_object_on_feature(obj_label, target_feature, self.use_bug_carcass_on_binary_files)
                # TODO: TEST METHODS BETWEEN HERE AND TODO START COMMENT AFTER PARSER SUPPORTS

                else:
                    logger.debug("Not implemented: use " + used_object.get_name())
                    message = ("You used something that the game doesn't know what to do with, please tell your local dev!")
                    use_success = False
            else:
                wprint(USE_FAIL_UNUSABLE)
                use_success = False
        else:
            message = USE_FAIL_NONSENSE

        if use_success:
            self.gamestate.update_time_left(USE_COST)

        wprint(message)
        self.ui.wait_for_enter()
        return use_success

    def verb_skate(self):
        '''
        TODO: Finish implementing this function ((SSH))
        :return:
        '''
        skate_success = False

        if self.gamestate.player.can_skateboard() is True:
            message = SKATE_SUCCESS
        else:
            message = SKATE_FAILURE_NO_SKILL

        wprint(message)
        self.ui.wait_for_enter()
        return skate_success

    def verb_spraypaint(self, command_extras):
        '''
        Player is attempting to spraypaint the current room with a message
        :param command_extras: This property stores the string that the user wants to print.
        :return:
        '''

        # Read the string for the message out of the argument passed in
        try:
            command_extra_first = command_extras[0]
            spraypaint_message = command_extra_first['name']
        except:
            wprint("Hmm, the language parser didn't send back the string, maybe you're confusing the software.")
        # logger.debug("Message will be: '" + spraypaint_message + "'")

        spraypaint_success = False
        spraypaint_detected_by_police = False

        cur_room = self.gamestate.get_current_room()
        cur_room_name = cur_room.get_name()

        if self.gamestate.player.can_spraypaint():
            if cur_room.is_virtual_space() is False:
                # Check of room is already painted
                is_cur_room_painted = self.gamestate.is_room_spray_painted_by_name(cur_room_name)
                if is_cur_room_painted is False:
                    spraypaint_detected_by_police = not self.rand_event.attempt_spraypaint()
                    if spraypaint_detected_by_police is False:
                        interface_message = SPRAYPAINT_ROOM_SUCCESS
                        spraypaint_success = True
                    else:
                        interface_message = SPRAYPAINT_FAIL_CAUGHT
                else:
                    # Room is already painted, currently don't allow doing it again
                    interface_message = SPRAYPAINT_ROOM_FAIL_ALREADY_PAINTED
            else:
                interface_message = SPRAYPAINT_FAIL_VIRTUAL_SPACE
        else:
            interface_message = SPRAYPAINT_FAIL_NO_SKILL

        if spraypaint_success is True:
            self.gamestate.set_room_spray_painted_by_name(cur_room_name, True)
            self.gamestate.set_room_spray_painted_message(cur_room_name, spraypaint_message)
            self.gamestate.update_time_left(SPRAYPAINT_COST)
            self.gamestate.player.update_coolness(SPRAYPAINT_COOLNESS_INCREASE)

        wprint(interface_message)
        if spraypaint_detected_by_police is True:
            self.go_to_jail()
        self.ui.wait_for_enter()
        return spraypaint_success

    def verb_steal(self, noun_name, noun_type):
        steal_success = False
        steal_detected_by_police = False
        message = "Somehow message didn't get assigned, yikes! Tell the developer what you were doing!"
        current_room = self.gamestate.get_current_room()

        jail_room_name = R7[0] # R7[0] is the jail room
        if (noun_name.lower() == "key") and (current_room.get_name().lower() == jail_room_name):
            if self.gamestate.jailroom_data['cell_unlocked'] is False:
                message = "You steal the key off the wall, where it is hanging just within your reach off of a hook. You then let yourself out."
                self.gamestate.jailroom_data['cell_unlocked'] = True
            else:
                message = "You already used the key and let yourself out!"

        elif noun_type == NOUN_TYPE_FEATURE:
            message = STEAL_FAIL_FEATURE_INVALID
            steal_success = False

        elif noun_type == NOUN_TYPE_OBJECT:

            room_object = current_room.get_object_by_name(noun_name)

            if room_object is not None: # Object is in this room
                # Only steal objects that we have never owned or that are not free
                # if room_object.is_owned_by_player() is True:  # This was the original logic, was changed to below method that doesn't allow for duplicate object verification (if you own one floppy disk, you own them ALL)
                if room_object.get_name() in self.gamestate.player.owned:
                    message =  STEAL_FAIL_ALREADY_OWNED
                elif room_object.get_cost() is 0:
                    message = STEAL_FAIL_FREE_ITEM
                elif room_object.get_cost() > 0:
                    steal_detected_by_police = not self.rand_event.attempt_steal()
                    if steal_detected_by_police is False:
                        current_room.remove_object_from_room(room_object)
                        self.gamestate.player.add_object_to_inventory(room_object)
                        message = STEAL_SUCCESS_PREFIX + room_object.get_name() + STEAL_SUCCESS_SUFFIX
                        steal_success = True
                        self.gamestate.update_time_left(STEAL_COST)
                    else:
                        message = STEAL_FAIL_PRISON
                        self.gamestate.update_time_left(STEAL_COST) # Still took the time to try and steal it
            else: # room_object isn't present in this room
                message = STEAL_FAIL_NOT_HERE
        else: # Not an object or a noun
            message = STEAL_FAIL_NOT_HERE

        wprint(message)
        if steal_detected_by_police is True:
            self.go_to_jail()
        self.ui.wait_for_enter()
        return steal_success

    def send_command_to_parser(self):
        '''
        Sends the user input to the parser then stores all of the results into the gamestate's variables
        TODO Stretch goal: Refactor this method and just store the entire result on gamestate each round
        THis would require reading the appropriate information off of the self.results inside of every verb. For 0 gain,
        that's a lot of work to do. Lowest tier of priority item.
        :return:
        '''
        results = self.lp.parse_command(self.user_input)
        try:
            self.command = results.get_verb()
        except:
            self.command = INVALID_INPUT
        try:
            self.verb_noun_name = results.get_noun()['name']
        except:
            self.verb_noun_name = None
        try:
            self.verb_noun_type = results.get_noun()['type']
        except:
            self.verb_noun_type = None
        try:
            self.extras = results.get_extras()
        except:
            self.extras = None
        try:
            self.verb_preposition = results.get_preposition()
        except:
            self.verb_preposition = None
        try:
            self.parser_error_message = results.get_error_message()
        except:
            self.parser_error_message = None

    def search_trash_can(self):
        '''
        If the player decides to search trash can, this is the special logic that handles it.
        '''
        if self.gamestate.is_trash_can_looted is True:
            message = LOOK_AT_TRASH_CAN_ALREADY_LOOTED
        else:
            wprint(LOOK_AT_TRASH_CAN_PROMPT)
            confirm = self.ui.user_prompt().lower()
            if confirm in YES_ALIASES:
                message = LOOK_AT_TRASH_SEARCHED
                ram_chip = self.gamestate.get_object_by_name(RAM.lower())
                self.gamestate.player.add_object_to_inventory(ram_chip)
                self.gamestate.player.update_coolness(TRASH_CAN_SEARCH_COOLNESS_COST)
                self.gamestate.is_trash_can_looted = True
            else:
                message = LOOK_AT_TRASH_NOT_SEARCHED

        wprint(message)
        self.ui.wait_for_enter()

    def install_floppy_disk(self):
        if self.gamestate.endgame_data['computer_room']['is_floppy_installed'] is True:
            message = "You've already installed one of those."
        else:
            wprint("Would you like to insert your [Floppy Disk] into the disk drive [y/n]?")
            user_input = self.ui.user_prompt()

            if user_input in YES_ALIASES:
                self.gamestate.endgame_data['computer_room']['is_floppy_installed'] = True
                self.gamestate.player.update_speed(FLOPPY_DISK_SPEED_INCREASE)
                floppy_disk = self.gamestate.player.inventory.get_object_by_name(FLOPPY_DISK)
                self.gamestate.player.remove_object_from_inventory(floppy_disk)
                message = "You insert the [Floppy Disk] and can see a performance increase already!"
            else:
                message = "You have second thoughts for some reason. Maybe later..."
        self.update_is_operable()
        return message

    def install_pc_components(self):
        ram_installed = self.gamestate.endgame_data['computer_room']['is_ram_installed']
        graphics_installed = self.gamestate.endgame_data ['computer_room']['is_graphics_installed']

        if ram_installed is False:
            wprint("You see some wires, one tiny RAM card looking lonely next to an empty slot. Don't these things usually come in pairs?")
            wprint("Would you like to put in your RAM chip [y/n]?")
            user_input = self.ui.user_prompt().lower()

            if user_input in YES_ALIASES:
                ram_chip = None
                if self.gamestate.player.has_object_by_name(RAM) is True:
                    ram_chip = self.gamestate.player.inventory.get_object_by_name(RAM)
                elif self.gamestate.player.has_object_by_name(ACMERAM) is True:
                    ram_chip = self.gamestate.player.inventory.get_object_by_name(ACMERAM)
                else:
                    wprint("Uh oh, this is bad. Where's that RAM chip??") # Don't expect this to ever print...
                if ram_chip is not None:
                    self.gamestate.player.remove_object_from_inventory(ram_chip)
                    self.gamestate.endgame_data['computer_room']['is_ram_installed'] = True
                    self.gamestate.player.update_speed(RAM_SPEED_INCREASE)
        else:
            wprint("The new RAM was installed easily and is clamped onto the MOBO securely.")

        if graphics_installed is False:
            wprint("There's a graphics card with a photo of pong on it - it's definitely toasted.")
            wprint("Would you like to replace the graphics card [y/n]?")
            user_input = self.ui.user_prompt()

            if user_input in YES_ALIASES:
                graphics_card = None
                if self.gamestate.player.has_object_by_name(GRAPHICS_CARD) is True:
                    graphics_card = self.gamestate.player.inventory.get_object_by_name(GRAPHICS_CARD)
                else:
                    wprint("Uh oh, this is bad. Where's that graphics card??")  # Don't expect this to ever print...
                if graphics_card is not None:
                    self.gamestate.player.remove_object_from_inventory(graphics_card)
                    self.gamestate.endgame_data['computer_room']['is_graphics_installed'] = True
                    self.gamestate.player.update_coolness(GRAPHICS_COOLNESS_INCREASE)
        else:
            wprint("A new Graphics Card takes up the majority of the expansion bay. This one has Sw33t-3d-Gr4phX Technology")

        self.update_is_operable()


    def update_is_operable(self):
        ram_installed = self.gamestate.endgame_data['computer_room']['is_ram_installed']
        graphics_installed = self.gamestate.endgame_data['computer_room']['is_graphics_installed']
        floppy_installed = self.gamestate.endgame_data['computer_room']['is_floppy_installed']

        if ram_installed and graphics_installed and floppy_installed is True:
            self.gamestate.endgame_data['computer_room']['is_operable'] = True

    def game_hint_check(self):
        hints = []
        player = self.gamestate.player
        cur_room = self.gamestate.get_current_room()
        if cur_room is None:
            logger.debug("UH OH!")
            in_computer_room = False
        else:
            in_computer_room = cur_room.get_name() == "Your Computer"

        if in_computer_room is False:
            # Check for laptop; if in inventory, tell player what to do
            new_laptop_name = 'new laptop'
            player_has_new_pc = player.has_object_by_name(new_laptop_name)
            if player_has_new_pc is True:
                hints.append(HINT_NEW_PC)
            # If not, check if the have all the parts they need
            else:
                if self.gamestate.player.has_computer_parts() is True:
                    hints.append(HINT_ALL_PARTS)

        if len(hints) > 0:
            self.ui.print_hints(hints)

    def minigame_bug(self):
        '''
        Called when player looks at the 'bug' inside metaverse
        :return:
        '''
        # TODO: Pull these out to the strings.py file as constants if desired

        spider_defeated = self.gamestate.endgame_data['metaverse']['is_spider_defeated']

        if spider_defeated is  True:
            wprint("You've already squashed this bug.")
            self.ui.wait_for_enter()
            return

        wprint("The bug notices your interest and scuttles towards you at a terrifying speed! Before you can run, "
               "the bug begins to cocoon you in an infinite loop!! You see the following code flash before your eyes "
               "as you begin to lose conciousness:")
        print("If (you == best hacker ever):")
        print("    You = spider food\n")
        print("You grab the '==' operator and quickly change it to:\n")
        print("\tA: !=")
        print("\tB: +=")
        print("\tC: IDK fight the freaking spider!\n")
        print("Enter [a/b/c]:")

        user_response = self.ui.user_prompt().lower()

        while user_response not in ANSWER_A and user_response not in ANSWER_B and user_response not in ANSWER_C:
            wprint(INVALID_PROMPT_RESPONSE)
            user_response = self.ui.user_prompt().lower()

        if user_response in ANSWER_A:
            wprint("The spider rares back in fear- sensing your superiority. Fortunately, it trips over its own feet "
                   "and ends up a dead spiddy on the floor. [Spider carcass] is added to your inventory")
            spider_defeated = True
        elif user_response in ANSWER_B:
            wprint("The spider quits its cocooning and throws a compiler error straight at your face, woah that is "
                   "gonna leave a nasty scar- you must look like, Rambo cool right now! Luckily you are able to break "
                   "free of the webbing, but you feel pretty dazed.")
            self.gamestate.player.update_speed(BUG_SPEED_LOSS)
            self.gamestate.player.update_coolness(BUG_COOLNESS_LOSS)
            spider_defeated = False
        elif user_response in ANSWER_C:
            wprint("You punch the spider in one of its many eyes, splooting out a bunch of green gunk and eye juices "
                   "all over your sweet outfit- so uncool. Good news- it’s dead and you now have a gnarly [spider "
                   "carcass] in your inventory")
            spider_defeated = True

        if spider_defeated is True:
            self.gamestate.endgame_data['metaverse']['is_spider_defeated'] = True
            self.gamestate.player.update_coolness(BUG_COOLNESS_LOSS)
            try:
                spider_carcass = self.gamestate.get_object_by_name("spider carcass") # TODO: replace string literal with constant from language_words.py once implemented
                self.gamestate.player.add_object_to_inventory(spider_carcass)
            except:
                logger.debug("Unable to add 'spider carcass' to player inventory, maybe the object doesn't exist yet?")

        self.ui.wait_for_enter()

    def minigame_firewall(self):
        firewall_defeated = self.gamestate.endgame_data['metaverse']['is_firewall_defeated']

        if firewall_defeated is True:
            wprint("The wall of flames seems to have a convenient hole straight through the center, probably just "
                   "scared of another encounter with such an awesome hacker. Also you might have stole its baby ["
                   "fireball]. Are you guys like, related now? Not really sure how these things work.")
        else:
            wprint("You see a mass of flames blocking your way from the Data Towers, the fire twists and turns "
                   "spiraling up towards the sky. How are you ever gonna get around that thing?! Thinking hard you "
                   "come up with three possible solutions:")
            print("\tA: Attempt ot Skateboard through the inferno")
            print("\tB: THrow a can of Surge at it - the ultimate thirst quencher!")
            print("\tC: IDK fight the firewall!!!!!\n")
            print("Enter [a/b/c]:")

            user_response = self.ui.user_prompt()

            while user_response not in ANSWER_A and user_response not in ANSWER_B and user_response not in ANSWER_C:
                wprint(INVALID_PROMPT_RESPONSE)
                user_response = self.ui.user_prompt().lower()

            if user_response in ANSWER_A:
                if self.gamestate.player.can_skateboard() is True:
                    wprint("You  jump on your board and pick up speed as you make your way toward the inferno. You "
                           "can almost feel your eyebrows singe as you pass right through the blistering heat. You "
                           "reach out and grasp a cute little [fireball], stashing it in your backpack as you glide "
                           "out")
                    firewall_defeated = True
                else:
                    wprint("Do you even know how to skateboard? You certainly don’t own one and like, that is just "
                           "lame. Even you realise that what you have attempted is so uncool. You should probably "
                           "think more next time.")
                    self.gamestate.player.update_coolness(FIREWALL_COOLNESS_COST)
            elif user_response in ANSWER_B:
                if self.gamestate.player.has_object_by_name(SURGE):
                    wprint("You take a trusty can of surge from your backpack, crack open that tab, listen to the "
                           "sweet fizz, and hurle the can straight into the wall of fire! It blows a sticky sugar "
                           "syrup hole right through the middle and you quietly thank your surge for sacrificing "
                           "itself for the greater good. That soda will not be forgotten! What’s this now? You notice "
                           "an adorable little fireball flung from the flames. Why not take the little guy along you "
                           "think, stashing him in your backpack.")
                    firewall_defeated = True
                    surge = self.gamestate.player.inventory.get_object_by_name(SURGE)
                    self.gamestate.player.remove_object_from_inventory(surge)
                    try:
                        fireball = self.gamestate.get_object_by_name(FIREBALL)
                        self.gamestate.player.add_object_to_inventory(fireball)
                    except:
                        logger.debug("Couldn't add fireball to inventory, maybe it doesn't exist yet in gamedata files")
                else:
                    wprint("Oh snap! You musta drank all your [Surge]. Better try something else next time.")
                    firewall_defeated = False
            elif user_response in ANSWER_C:
                wprint("You rush at the firewall, a wiry teen with nothing to lose. Fists flailing you beat back the "
                       "monstrous flame making a tunnel right to the Data Tower. Berserkering with rage, "
                       "your brutality knows no mercy when you notice a real cute lil’ ball of fire cowering from "
                       "your wraith as your scorched body pummels through the flames- this is gonna leave some pretty "
                       "sick scars. What the heck you think, scooping the little [fireball] up and depositing him in "
                       "your backpack. Isn’t his fault his relatives are super bogus.")
                self.gamestate.player.update_coolness(FIREWALL_COOLNESS_COST)
                firewall_defeated = True

            if firewall_defeated is True:
                self.gamestate.endgame_data['metaverse']['is_firewall_defeated'] = True

                try:
                    spider_carcass = self.gamestate.get_object_by_name("spider carcass")  # TODO: replace string literal with constant from language_words.py once implemented
                    self.gamestate.player.add_object_to_inventory(spider_carcass)
                except:
                    logger.debug("Unable to add spider carcass to inventory")

        self.ui.wait_for_enter()

    def hack_binary_files(self):
        '''
        Logic specific to the user trying to hack the binary files
        :return: True if the hack succeeds, false otherwise.
        '''
        hack_success = False

        wprint("You look into the strings of 1s and 0s barely able to make out anything in this nasty mess of tangled "
               "code- then you notice somethings! A number any hacker would immediately recognize: 101. This clearly "
               "means:")
        print("\tA: lol- as in lolzcats!")
        print("\tB: 101- the class you are clearly missing")
        print("\tC: Love You Lots, aww grandma!")
        print("Enter [a/b/c]")

        user_response = self.ui.user_prompt()

        while user_response not in ANSWER_A and user_response not in ANSWER_B and user_response not in ANSWER_C:
            wprint(INVALID_PROMPT_RESPONSE)
            user_response = self.ui.user_prompt().lower()

        if user_response in ANSWER_A:
            wprint("You got it! Love those crazy catz. You grab the [binary code] giving it a quick read before "
            "shoving it in your backpack. It say:  ‘Dear diary, this is Mr. Robot. How are you? I am fine. I have a "
            "secret?! Wanna know??? Of course you do, you are my best friend. Well, as president of EvilCorp Bank I "
            "decided to blow up the world! How ‘bout dat? I have some nuclear launch codes I plan to use, oh idk maybe "
            "Sunday? Lol, yours truly, Mr. Robot")
            try:
                binary_files = self.gamestate.get_object_by_name("binary files")  # TODO: replace string literal with constant from language_words.py once implemented
                self.gamestate.player.add_object_to_inventory(binary_files)
            except:
                logger.debug("Unable to add binary files")
            hack_success = True
        elif user_response in ANSWER_B:
            wprint("Yeah no, how could you be thinking of school at a time when your brain needs to actually be working?! Majorly uncool.")
            self.gamestate.player.update_coolness(BINARY_FILES_COOLNESS_COST)
            hack_success = False
        elif user_response in ANSWER_C:
            # TODO: Find a way so that the player can't keep hacking and getting this answer to increase coolness forever
            wprint("Grandma does love you- cause like you are the coolest, but this isn’t the right answer")
            self.gamestate.player.update_coolness(BINARY_FILES_COOLNESS_INCREASE)
            hack_success = False

        self.ui.wait_for_enter()
        return hack_success

    def hack_corrupted_files(self):
        '''
                Logic specific to the user trying to hack the binary files
                :return: True if the hack succeeds, false otherwise.
                '''
        hack_success = False

        wprint("You turn your hacking expertise to the oozing pile of corrupted files, hacking here and there to try "
               "and make some sense of the mess- finally a user prompt: ‘WaN7 7o play gaM3 t1NY huuuuMan?’ [y/n]")

        user_response = self.ui.user_prompt().lower()

        while user_response not in YES_ALIASES and user_response not in NO_ALIASES:
            wprint(INVALID_PROMPT_RESPONSE)
            user_response = self.ui.user_prompt().lower()

        if user_response in YES_ALIASES:
            wprint("Before your eyes flashes up like, a really big Wheel of Fortune type deal, you take a spin "
                   "throwing turing it as fast as you can and you see it tik tik tik around and around… fingers "
                   "crossed!")
            player_wins_spin = self.rand_event.coin_flip()

            if player_wins_spin is True:
                wprint("The wheel starts to slow and almost lands on ‘LiFe7ime SuPPly o’ F1ShStickz’ but makes it one "
                "more tik and lands on ‘1 Fr33 [Surge].’ Eh, that works for you")
                try:
                    surge = self.gamestate.get_object_by_name(SURGE)
                    self.gamestate.player.add_object_to_inventory(surge)
                except:
                    logger.debug("Unable to add surge from hack_corrupted_files() method")

            elif player_wins_spin is False:
                wprint("The wheel gets off to a good start and then quickly loses speed, landing on ‘i StteAL ur "
                       "MoNey’ - oh no, better check your cash fund")
                old_cash = self.gamestate.player.get_cash()
                cash_loss = int(-1 * old_cash * CORRUPTED_FILE_CASH_PERCENT_LOSS)
                self.gamestate.player.update_cash(cash_loss)
                logger.debug("Player is losing " + str(cash_loss) + " cash out of their total of " + str(old_cash))

            else:
                logger.debug("player_wins_spin must have returned a non-T/F value, that's nuts") # This should never print!

            hack_success = True

        else: # Must have responded 'no'
            wprint("You play it safe and make it back out of that putrid mess… wonder what that game might have been though…")
            hack_success = False

        self.ui.wait_for_enter()
        return hack_success

    def hack_cat_videos(self):
        '''
                Logic specific to the user trying to hack the binary files
                :return: True if the hack succeeds, false otherwise.
                '''
        hack_success = True

        wprint("Your eyes glaze over with adorableness… so much fluff. You had something important to do, "
               "but you can’t quite remember what. Do you want to keep watching [y/n]") 

        user_response = self.ui.user_prompt().lower()

        while user_response not in YES_ALIASES and user_response not in NO_ALIASES:
            wprint(INVALID_PROMPT_RESPONSE)
            user_response = self.ui.user_prompt().lower()

        if user_response in YES_ALIASES:
            wprint("You stare into the video screen giggling intermittently. Time seems to stop and you drool a bit. "
                   "Eventually you pass out on the floor for awhile. When you wake up you are pretty certain you’ve "
                   "missed at least a week’s worth of classes.")
            self.gamestate.player.update_speed(CAT_VIDEO_SPEED_COST)
            hack_success = True # Redudant call, just in case want to change this to 'failing' the hack

        else:  # Must have responded 'no'
            wprint("This is the hardest thing you’ve ever done. You scrunch up your face and turn your back on the "
                   "plethora of precious moments. A single tear falls down your battle hardened cheek, but you know "
                   "this was the right choice.")
            hack_success = True # Redudant call, just in case want to change this to 'failing' the hack

        self.ui.wait_for_enter()
        return hack_success

    def hack_launch_codes(self):
        '''
        Logic specific to the user trying to hack the binary files
        :return: True if the hack succeeds, false otherwise.
        '''
        hack_success = False

        wprint("As you reach for the codes, your hand is zapped by some weird blue electricity barrier- ow! You see "
               "some code flash up creating a wall between you and the codes, just as you expected there is going to "
               "be some decrypting to do. The code reads:")
        print("Cr# 0v3 rRid 3")
        print("\tA: Easy peasy, that means ‘Crashtag Oven Thrashers’ they are like the best punk bank ever.")
        print("\tB: Well doh, that’s ‘Creators Riddance 3’ almost the coolest video game.")
        print("\tC: Woah, they must be trying to frame you- that spells ‘Crash Override’ your super cool hacker handle!!!")
        print("Enter [a/b/c]")

        user_response = self.ui.user_prompt()

        while user_response not in ANSWER_A and user_response not in ANSWER_B and user_response not in ANSWER_C:
            wprint(INVALID_PROMPT_RESPONSE)
            user_response = self.ui.user_prompt().lower()

        if user_response in ANSWER_A or user_response in ANSWER_B:
            wprint("You enter the code with confidence. Just as you enter the last character a shockwave hits you "
                   "like a nasty pop quiz. Guess that isn’t the right answer")
            hack_success = False
            self.gamestate.player.update_speed(HACK_LAUNCH_CODE_COST)
        elif user_response in ANSWER_C:
            wprint("You type in the code, and the blue electricity shield drops. You gingerly take the codes and put "
                   "them in your backpack… you are gonna need these and proof that you're not the mastermind behind "
                   "this heinous scheme if you wanna beat this punk CPU!")

            try:
                launch_codes = self.gamestate.get_object_by_name("launch codes") # TODO: Update to string-literal from language_words.py once implemented
                self.gamestate.player.add_object_to_inventory(launch_codes)
            except:
                logger.debug("Unable to add launch codes from hack_launch_codes() method")

            hack_success = True

        self.ui.wait_for_enter()
        return hack_success

    def use_fireball_on_binary_files(self, fireball_object, binary_files_feature):
        '''
        Untested method. Should be called by game client with language parser tells us that this is the response,
        but parser does noet yet support (3/4/17).

        Probably will be called in verb_use() after checking if there is a target for the fireball item to be used on

        :return:
        '''
        wprint("Why did that seem like a good idea? Those are gonna be really hard to hack now.")
        self.gamestate.player.remove_object_from_inventory(fireball_object)
        self.gamestate.player.update_speed(FIREBALL_ON_BINARY_SPEED_COST)

    def use_bug_carcass_on_binary_files(self, bug_carcass_object, binary_files_feature):
        wprint("Why did that seem like a good idea? Those are gonna be really hard to hack now.")
        self.gamestate.player.remove_object_from_inventory(bug_carcass_object)

    def use_object_on_feature(self, object_name, feature_name, success_function):
        '''
        Attempts to use the object designed by object_name on the feature designated by feature_name
        :param object_name:
        :param feature_name:
        :param success_function:
        :return:
        '''
        success = False
        target_feature = self.gamestate.get_current_room().get_feature_by_name(feature_name)
        object_used = self.gamestate.player.inventory.get_object_by_name(object_name)

        if object_used is None:
            wprint("You don't have a " + object_name + " that you can use.")

        elif target_feature is None:
            wprint("You see no ["+ feature_name + "] here to target with the [" + object_used.get_name() + "].")

        else:
            success_function(target_feature, object_used)
            success = True

        return success