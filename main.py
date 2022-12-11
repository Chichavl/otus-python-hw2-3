import logging
import argparse
import pprint
import random
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s [in %(funcName)s %(pathname)s:%(lineno)d]', level=logging.DEBUG)
logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=2)

class Player():
  
  def __init__(self, bag, name, isComputer = False) -> None:
    self.name = name + "_AI" if isComputer else name
    self.isComputer = isComputer
    self._player_loose = False
    self._player_win = False
    self.card = Card(bag)

  def make_move(self, barrel) -> None:
    if self.isComputer:
      self._make_ai_move(barrel)
    else:
      self._make_human_move(barrel)
    self.card.check_win(self)

  def _make_ai_move(self, barrel):
    if self.card.contains_barrel(barrel):
      self.card.strikethrough(barrel)
  
  def _make_human_move(self, barrel):
    answer = query_yes_no("Зачеркнуть цифру?", None)
    if answer:
      if self.card.contains_barrel(barrel):
        logger.debug(f"Card contains {barrel}")
        self.card.strikethrough(barrel)
      else:
        self._player_loose = True
    else:
      if self.card.contains_barrel(barrel):
        self._player_loose = True
  
  def check_loose(self):
    return self._player_loose

  def check_win(self):
    return self._player_win
  def __repr__(self) -> str:
    return f"Player {self.name}"

class Card():
  ROWS = 3
  COLUMNS = 9
  NUMBERS_IN_A_ROW = 5
  CELLS = ROWS * COLUMNS

  def __init__(self, bag):
    # https://stackoverflow.com/a/6142706
    self.state = [0] * self.CELLS
    for i in range(0, self.ROWS):
      _row_numbers = []
      for j in range(0, self.NUMBERS_IN_A_ROW):
        cur = bag.getRandomBarrel()
        _row_numbers.append(cur)
      _row_numbers.sort()
      _places = random.sample(range(self.COLUMNS), self.NUMBERS_IN_A_ROW)
      _places.sort()
      logger.debug(f"Row numbers: {_row_numbers}")
      logger.debug(f"Places: {_places}")
      for j in range(0, self.NUMBERS_IN_A_ROW):
        self.state[i*self.COLUMNS+_places[j]] = _row_numbers[j]
      logger.debug(f"State after insert: {self.state}")
      logger.debug(f"{self}")

  def contains_barrel(self, barrel):
    return barrel in self.state

  def strikethrough(self, barrel):
    logger.debug(f"Card before strikethrough: {self.state}")

    i = self.state.index(barrel)
    self.state[i] = -1
    logger.debug(f"Card after strikethrough: {self.state}")

  def check_win(self, player):
    for i in range(self.ROWS):
      strikethrough_count = 0
      for j in range(self.COLUMNS):
        # logger.debug(f"Checking {i*self.COLUMNS+j} position")
        if self.state[i*self.COLUMNS+j] == -1:
          strikethrough_count +=1
      logger.debug(f"Row {i} has {strikethrough_count} strikethrough count")
      if strikethrough_count == self.NUMBERS_IN_A_ROW:
        player._player_win = True

  def __repr__(self) -> str:
    _card = ""
    for i in range(self.CELLS):
      # empty cell
      if self.state[i] == 0:
        _card += "   "
      # strikethrough cell 
      elif self.state[i] == -1:
        _card += "-- "
      else:
        _card += f"{self.state[i]:02d} "
      if (i+1) % self.COLUMNS == 0:
        _card += '\n'
    spacer_length = self.COLUMNS*2+self.COLUMNS-1
    # https://stackoverflow.com/a/54950733
    return "-"*spacer_length  + '\n' + _card + "-"*spacer_length + '\n'
    

class Bag():
  BAG_CAPACITY = 90

  def __init__(self):
    self.state = []
    for i in range(1, self.BAG_CAPACITY+1):
      self.state.append(i)
  
  def isEmpty(self) -> bool:
    return len(self.state) <= 0
  
  def getRandomBarrel(self) -> int:
    barrel = random.choice(self.state)
    self.state.remove(barrel)
    return barrel
  
  def barrels_left(self) -> int:
    return len(self.state)

  def __repr__(self):
    return f"Bag has {len(self.state)} barrels left. {self.state}"


class Game():
  def __init__(self, players) -> None:
    self.bag = Bag()
    self.players = []
    for player_name, isComputer in players:
      self.players.append(Player(self.bag, player_name, isComputer))
    
  def start(self):
    # Reset bag, before game.
    self.bag = Bag()
    while not self.bag.isEmpty():
      barrel = self.bag.getRandomBarrel()
      print(f"Новый бочонок: {barrel} (осталось {self.bag.barrels_left()})")
      for player in self.players:
        print(f"Карточка игрока {player.name}")
        print(player.card)
        player.make_move(barrel)
        if player.check_loose():
          self._player_loose(player)
        if player.check_win():
          self._player_win(player)
  
  def _player_loose(self, player):
    print(f"Player {player.name} looses. Game over")
    exit(0)
  
  def _player_win(self, player):
    print(f"Player {player.name} wins. Congratilations!")
    exit(0)
      

# https://stackoverflow.com/a/3041990
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def get_parser():
  parser = argparse.ArgumentParser("Parser")
  parser.add_argument(
      "--verbose", "-v", action="store_true", help="Turn on debug mode"
  )
  parser.add_argument(
      "--player1", "-p1", action="store", default="Player 1", help="Provide first player name"
  )
  parser.add_argument(
      "--player2", "-p2", action="store", default="Player 2", help="Provide second player name"
  )
  parser.add_argument(
      "--player1ai", "-p1ai", action="store_true", help="Should player 1 use AI"
  )
  parser.add_argument(
      "--player2ai", "-p2ai", action="store_true", help="Should player 2 use AI"
  )
  return parser

if __name__ == "__main__":
  parser = get_parser()
  args = parser.parse_args()
  if args.verbose:
    logger.setLevel(logging.DEBUG)
  logger.debug(f"Provided args: {args}")
  game = Game([(args.player1, args.player1ai), (args.player2, args.player2ai)])
  game.start()