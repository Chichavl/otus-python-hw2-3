import logging
from main import Card
from main import Bag
from pytest import fixture

@fixture
def card_instance() -> Card:
  return Card(Bag())

class TestCard:
  def test_generation(self, card_instance, caplog):
    caplog.set_level(logging.DEBUG)
    non_zero_fields = 0
    for i in range(card_instance.CELLS):
      if card_instance.state[i] != 0:
        non_zero_fields += 1
    assert card_instance.ROWS * card_instance.NUMBERS_IN_A_ROW == non_zero_fields

  # def test_repr(self, card_instance):
  #   print(card_instance)
  #   assert True == False