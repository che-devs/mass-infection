from threading import Thread
from modules import ClapDetector, NumPad, Player, Printer, Translations, Logger
from time import sleep
from random import randint
from datetime import datetime


class Taskmanager:
    """
    Taskmanager controls the game logic, player state, and hardware interaction.
    Handles barcode input, clap detection, player registration, scoring, and printing results.
    """
    def __init__(self, numpad, clap_detector) -> None:
        """Initialize Taskmanager with NumPad and ClapDetector."""
        self.numpad = numpad
        self.clap_detector = clap_detector
        self.players = []
        try:
            self.printer = Printer()
        except:
            print("Printer is not connected.")
            self.printer = None

        self.translations = Translations()
        self.logger = Logger('info.log')

        self.state = 'idle'
        self.state_save = ''
        self.run = True
        self.registration_queu = []

    def start(self):
        """Main loop for handling game states and player actions."""
        while self.run:
            # State machine for game logic
            match self.state:
                case 'idle':
                    # Wait for new barcode scan
                    if self.numpad.new_barcode():
                        self.state = 'do_the_task'

                case 'do_the_task':
                    # Handle player registration and game actions
                    if len(self.registration_queu):  # If registration queue is not empty
                        id = self.registration_queu.pop(0)
                    else:
                        id = self.numpad.get_barcode()
                    # Check if player already exists
                    match = False
                    for i, player in enumerate(self.players):
                        if id == player.get_id():
                            match = True
                            break
                    if not match:  # Player was not found
                        self.players.append(Player(id))
                        i = len(self.players) - 1
                        self.logger.info('A new player has entered the game.')
                    # Log player info
                    self.logger.info('ID: {} Score: {} Level: {}'.format(
                        id,
                        self.players[i].get_score(),
                        self.players[i].get_level()
                    ))

                    evaluation = 'fail'

                    # ---- GameOver Check ----
                    # Check if player has lost
                    if self.players[i].get_gameover():
                        self.logger.info('GAME OVER')
                        evaluation = 'end'
                    else:
                        # ---- LEVELS ----
                        # Handle game levels and actions
                        match self.players[i].get_level():
                            case 0:
                                self.logger.info('level 0')  # Registration
                                evaluation = 'new'
                                self.players[i].level_up()

                            case 1:
                                self.logger.info('level 1')  # First clap
                                # Check for correct number of claps
                                claps = self.clap_detector.get_claps()
                                if claps >= 2 and claps <= 4:
                                    evaluation = 'success'
                                    self.players[i].add_score(2)
                                    self.players[i].level_up()
                                else:
                                    self.logger.warning('Incorrect number of claps')
                                    self.players[i].add_score(-1)

                            case 2:
                                self.logger.info('level 2')  # Pat on the back
                                evaluation = 'success'
                                self.players[i].add_score(1)
                                self.players[i].level_up()

                            case 3:
                                self.logger.info('level 3')  # Trash can
                                # Check for correct number of claps
                                claps = self.clap_detector.get_claps()
                                if claps >= 4 and claps <= 6:
                                    evaluation = 'success'
                                    self.players[i].add_score(3)
                                    self.players[i].level_up()
                                else:
                                    self.logger.warning('Incorrect number of claps')
                                    self.players[i].add_score(-1)
                            
                            case 4:
                                self.logger.info('level 4')  # Another person
                                timeout = 500  # 5s
                                # Wait for a new barcode, check if player is already registered or scanned
                                while timeout > 0:
                                    if self.numpad.new_barcode():
                                        new_id = self.numpad.get_barcode()
                                        break_for = False
                                        for player in self.players:
                                            if new_id == player.get_id():
                                                self.logger.warning('Player already registered')
                                                self.players[i].add_score(-1)
                                                break_for = True
                                                break
                                        if break_for:
                                            break
                                        break_for = False
                                        for in_queu in self.registration_queu:
                                            if new_id == in_queu:
                                                self.logger.warning('This player already scanned')
                                                self.players[i].add_score(-1)
                                                break_for = True
                                                break
                                        if break_for:
                                            break
                                        self.registration_queu.append(new_id)
                                        evaluation = 'success'
                                        self.players[i].add_score(3)
                                        self.players[i].level_up()
                                        break
                                    else:
                                        timeout -= 1
                                    sleep(0.01)
                            
                            case 5:
                                self.logger.info('level 5')  # Windy Picture
                                evaluation = 'success'
                                self.players[i].add_score(3)
                                self.players[i].level_up()

                            case 6:
                                self.logger.info('level 6')  # 2 new persons
                                timeout = 1000  # 10s
                                new_players = 0
                                # Wait for two new barcodes, check if already registered or scanned
                                while timeout > 0:
                                    if self.numpad.new_barcode():
                                        new_id = self.numpad.get_barcode()
                                        break_for = False
                                        for player in self.players:
                                            if new_id == player.get_id():
                                                self.logger.warning('Player already registered')
                                                self.players[i].add_score(-1)
                                                break_for = True
                                                break
                                        if break_for:
                                            break
                                        break_for = False
                                        for in_queu in self.registration_queu:
                                            if new_id == in_queu:
                                                self.logger.warning('This player already scanned')
                                                self.players[i].add_score(-1)
                                                break_for = True
                                                break
                                        if break_for:
                                            break
                                        new_players += 1
                                        self.registration_queu.append(new_id)
                                        if new_players == 2:
                                            evaluation = 'success'
                                            self.players[i].add_score(10)
                                            self.players[i].level_up()
                                            break
                                    else:
                                        timeout -= 1
                                    sleep(0.01)

                            case 7:
                                self.logger.info('level 7')  # Flashmob
                                now = datetime.now()
                                # Win if after 12:45
                                if now.hour * 60 + now.minute >= 765:  # 12h*60 + 45min = 765min
                                    evaluation = 'won'
                                    self.players[i].add_score(15)
                                    self.players[i].level_up()
                                else:
                                    self.players[i].add_score(-5)
                            
                            case 8:
                                self.logger.info('bonus level')
                                self.players[i].level_up()
                                evaluation = 'bonus'

                            case _:
                                self.logger.info('no more tasks')
                                evaluation = 'end'
                            
                        # Check for game over after level
                        if self.players[i].get_gameover():
                            evaluation = 'game_over'

        
                    # ---- EVALUATION ----
                    # Prepare printout and logging based on evaluation
                    match evaluation:
                        case 'new':  # New players
                            text = '\n{}\nNr: {}\n\n{}\n'.format(
                                self.translations.get_general(0),  # Welcome
                                id,
                                self.translations.get_task(self.players[i].get_level() - 1)
                            )
                        
                        case 'success':
                            text = '\n{}\nNr: {}\n{}: {}\n\n{}\n'.format(
                                self.translations.get_nice(randint(0, 5)),
                                id,
                                self.translations.get_general(1),  # Your new score is
                                self.players[i].get_score(),
                                self.translations.get_task(self.players[i].get_level() - 1)
                            )

                        case 'fail':
                            text = '\n{}\nNr: {}\n{}: {}\n\n{}\n{} {}\n'.format(
                                self.translations.get_bad(randint(0, 5)),
                                id,
                                self.translations.get_general(1),  # Your new score is
                                self.players[i].get_score(),
                                self.translations.get_task(self.players[i].get_level() - 1),
                                self.translations.get_general(5),  # Remaining attempts
                                self.players[i].get_attempts()
                            )

                        case 'won':
                            text = '\n{} {}'.format(
                                    self.translations.get_general(3),
                                    self.players[i].get_score()
                            )

                        case 'bonus':
                            text = '\n{}'.format(
                                        self.translations.get_general(4),
                            )

                        case 'end':
                            text = ''

                        case 'game_over':
                            text = '\n{}\n'.format(
                                self.translations.get_general(6),  # Game lost
                            )

                        case _:
                            text = ''
                            

                    if text != '':
                        # Print result and log
                        self.printer.print_text(text)
                        self.printer.cut()
                        self.logger.debug(text)

                    # Set next state
                    if len(self.registration_queu):
                        self.state = 'do_the_task'
                    else:
                        self.state = 'idle'

            # End match
            # Log state changes
            if self.state_save != self.state:
                self.state_save = self.state
                self.logger.info(f'Current state: {self.state}')

            sleep(0.01)

    def stop(self):
        """Stop the main loop."""
        self.run = False



if __name__ == "__main__":
    # Initialize hardware modules
    numpad = NumPad()

    clap_detector = ClapDetector()
    # Start clap detection in a separate thread
    clap_thread = Thread(target=clap_detector.start)
    clap_thread.daemon = True
    clap_thread.start()

    # Start main game logic in a separate thread
    taskmanager = Taskmanager(numpad, clap_detector)
    taskmanager_thread = Thread(target=taskmanager.start)
    taskmanager_thread.daemon = True
    taskmanager_thread.start()

    # Run numpad input loop (main thread)
    numpad.run()