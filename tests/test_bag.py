from main import Bag
from main import Card
from pytest import fixture

@fixture
def bag_instance() -> Bag:
  return Bag()

class TestBag:
  def test_generation(self, bag_instance):
    assert bag_instance.state[0] == 1
    assert bag_instance.state[-1] == bag_instance.BAG_CAPACITY
    assert len(bag_instance.state) == bag_instance.BAG_CAPACITY

  def test_ammount_card_generation(self, bag_instance):
    card1 = Card(bag_instance)
    card2 = Card(bag_instance)
    assert len(bag_instance.state) == bag_instance.BAG_CAPACITY - card1.NUMBERS_IN_A_ROW * card1.ROWS - card2.NUMBERS_IN_A_ROW * card2.ROWS

  def test_repr(self, bag_instance):
    assert str.__contains__(bag_instance.__repr__(), f"Bag has {len(bag_instance.state)} barrels left.")
