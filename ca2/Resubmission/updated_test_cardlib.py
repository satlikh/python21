import pytest
from cardlib import *

# Most of the errors may come from data entry level of the program. So, some tests would be done to see if
# the program can handle them.
def test_handle_negative_value():
    """
    This test function checks if the cardlib library allows the wrong values to be entered.
    """
    print('Handle negative values for value')
    value = -2
    # Two of Hearts
    try:
        h2 = NumberedCard(value, Suit.Hearts)
    except Exception as e:
        assert isinstance(e, ValueError)
# ====================================================================================================
def test_handle_out_of_range_value():
    """
    This test function checks if the cardlib library allows the wrong values to be entered.
    """
    print('Handle out of range values for value')
    value = 12
    # Two of Hearts
    try:
        h2 = NumberedCard(value, Suit.Hearts)
    except Exception as e:
        assert isinstance(e, ValueError)
# ====================================================================================================
def test_handle_float_value():
    """
    This test function checks if the cardlib library allows the wrong values to be entered.
    """
    print('Handle float values for value')
    value = 2.1
    # Two of Hearts
    try:
        h2 = NumberedCard(value, Suit.Hearts)
    except Exception as e:
        assert isinstance(e, ValueError)
# ====================================================================================================
def test_handle_str_value():
    """
    This test function checks if the cardlib library allows the wrong values to be entered.
    """
    print('Handle string values for value')
    value = 'Two'
    # Two of Hearts
    try:
        h2 = NumberedCard(value, Suit.Hearts)
    except Exception as e:
        assert isinstance(e, ValueError)

# ====================================================================================================
def test_handle_wrong_value():
    """
    This test function checks if the cardlib library allowes the wrong values to be entered.
    """
    print('Handle wrong values for value')
    val = [-2, 12, 2.7, 'two']
    # Two of Hearts
    for value in val:
        try:
            h2 = NumberedCard(value, Suit.Hearts)
        except Exception as e:
            assert isinstance(e, ValueError)
# ====================================================================================================
def test_handle_correct_value():
    """
    This test function checks if the cardlib library allowes the wrong values to be entered.
    """
    print('Handle wrong values for value')
    value = 2
    # Two of Hearts
    try:
        h2 = NumberedCard(value, Suit.Hearts)
        print(h2)
    except Exception as e:
        assert isinstance(e, ValueError)
# ====================================================================================================
def test_wrong_suit():
    """
    This test function checks if the cardlib library allows entering wrong suit for playing cards.
    """
    print('Handle wrong suit for playing card')
    st = ['Hearts', 1, 1.5, -2]
    # For JackCard
    for suit in st:
        try:
            jh = JackCard(suit)
        except Exception as e:
            assert isinstance(e, ValueError)
# ====================================================================================================
def test_correct_suit():
    """
    This test function checks if the cardlib library allows entering wrong suit for playing cards.
    """
    print('Handle wrong suit for playing card')
    st = [Suit.Hearts, Suit.Spades, Suit.Clubs, Suit.Diamonds]
    # For JackCard
    for suit in st:
        try:
            j = JackCard(suit)
            print(j, end=' ')
        except Exception as e:
            assert isinstance(e, ValueError)
# ====================================================================================================
def test_dressed_cards_value_encapsulation():
    """
    This test function tests if the value of dressed cards can be manipulated.
    """
    jack_heart = JackCard(Suit.Hearts)
    try:
        jack_heart.value = 11
    except Exception as e:
        assert isinstance(e, AttributeError)
        print('The value of dresses card is not accessible, even for correct values!')
# ====================================================================================================
def test_hand_sort():
    """
    This test function tests if the sort method in Hand class works properly.
    """
    h = Hand([QueenCard(Suit.Hearts), NumberedCard(2, Suit.Spades), NumberedCard(2, Suit.Hearts),
              QueenCard(Suit.Diamonds), NumberedCard(5, Suit.Hearts)])
    h_sorted = [NumberedCard(2, Suit.Spades), NumberedCard(2, Suit.Hearts), NumberedCard(5, Suit.Hearts),
                QueenCard(Suit.Hearts), QueenCard(Suit.Diamonds)]
    print(f'Unsorted hand: {h}')
    h.sort()
    assert h.cards == h_sorted
    print(h.cards)
# ====================================================================================================
def test_hand_sort_stable():
    """
    This test function tests if the sort method in Hand class works properly.
    """
    h = Hand([QueenCard(Suit.Hearts), NumberedCard(2, Suit.Spades), NumberedCard(2, Suit.Hearts),
              QueenCard(Suit.Diamonds), NumberedCard(5, Suit.Hearts)])
    h_sorted_stable = [NumberedCard(2, Suit.Spades), NumberedCard(2, Suit.Hearts), NumberedCard(5, Suit.Hearts),
                QueenCard(Suit.Hearts), QueenCard(Suit.Diamonds)]
    print(f'Unsorted hand: {h}')
    h.sort()
    assert h.cards == h_sorted_stable
    print(h.cards)
# ====================================================================================================


test_handle_wrong_value()
test_handle_negative_value()
test_handle_out_of_range_value()
test_handle_float_value()
test_handle_str_value()
test_handle_correct_value()
test_wrong_suit()
test_correct_suit()
test_dressed_cards_value_encapsulation()
test_hand_sort()
test_hand_sort_stable()
