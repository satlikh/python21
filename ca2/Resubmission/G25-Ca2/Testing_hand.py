from cardlib import *
import pytest


def test_cards():
    """
    The test checks that the get_values function returns the correct value of the cards, that only integers between 2-10
    can be entered for the numbered cards and that only correct suits can be entered at Suit.
    """
    card_list_spades = [AceCard(Suit.Spades, first=True)] + [NumberedCard(x, Suit.Spades) for x in range(2, 11)] +\
        [JackCard(Suit.Spades), QueenCard(Suit.Spades), KingCard(Suit.Spades), AceCard(Suit.Spades)]
    card_list_hearts = [AceCard(Suit.Hearts, first=True)] + [NumberedCard(x, Suit.Hearts) for x in range(2, 11)] + \
                       [JackCard(Suit.Hearts), QueenCard(Suit.Hearts), KingCard(Suit.Hearts), AceCard(Suit.Hearts)]
    value = 0
    for card in range(len(card_list_spades)):
        value += 1
        assert card_list_spades[card].get_value() == value
        # control that it's the value of the card that determines equality and not suit
        assert card_list_hearts[card] == card_list_spades[card]
        if card > 0:
            assert card_list_spades[card-1] < card_list_spades[card]

    # check the value entering of NumberedCard
    val = [-2, 12, 2.7, 'two', 2]
    for value in val:
        try:
            h2 = NumberedCard(value, Suit.Hearts)
            assert value == 2  # it should be the only value that works
        except Exception as e:
            assert isinstance(e, ValueError)

    # test the suit entering
    correct_suits = [Suit.Hearts, Suit.Spades, Suit.Clubs, Suit.Diamonds]
    st = ['Hearts', 1, 1.5, -2] + correct_suits
    # For JackCard
    for suit in st:
        try:
            jh = JackCard(suit)
            assert jh.suit in correct_suits  # Only suits that should work
        except Exception as e:
            assert isinstance(e, ValueError)


def test_deck():
    """
    The test checks that the correct amount and correct types of cards are created with StandardDeck. It checks that the
    top card is removed and that the shuffle function results in a shuffled deck.
    """

    deck = StandardDeck()

    # Run the test twice to check that new deck is created
    # Check that there's 13 cards of each suit
    for _ in range(2):
        assert len(deck.cards) == 52
        cards = {'Clubs': [], 'Diamonds': [], 'Hearts': [], 'Spades': []}
        for i, suit_type in enumerate(cards):
            for card_type in range(13):
                new_card = deck.draw()
                assert new_card  # check that we pick up a card
                cards[suit_type].append(new_card)
                assert new_card.suit.name == suit_type

        # testing that the cards are removed
        assert len(deck.cards) == 0

        un = np.unique(cards)
        for i, suit_type in enumerate(cards):
            assert len(un[0][suit_type]) == 13  # checks uniqueness in suits

        deck.new_deck()

    d_unshuffled = StandardDeck()
    d_shuffled = StandardDeck()
    d_shuffled.shuffle()
    same_place_cards = 0
    for c_unshuffled, c_shuffled in zip(d_unshuffled.cards, d_shuffled.cards):
        if c_unshuffled == c_shuffled:
            same_place_cards += 1
    # all the cards should not be in the "same place"
    assert same_place_cards != 52
    # it good if half the cards are not in the "same place"
    assert same_place_cards < 25


def test_hand():
    """
    The test checks that cards are added when using the add_card function, also checks that the cards are sorted with
    both random cards (using a shuffled deck) and controlled with determined cards. Also checks that the correct cards
    are dropped when using drop_cards
    """
    deck = StandardDeck()
    deck.shuffle()

    # Check that 6 cards are added and that sort leaves the order from low to high
    hand = Hand()
    for i in range(6):
        hand.add_card(deck.draw())
    assert len(hand.cards) == 6
    hand.sort_cards()
    for i in range(1, len(hand.cards)-1):
        assert hand.cards[i].value >= hand.cards[i-1].value

    # test that the cards are sorted correctly for both with and without pairs
    h1 = Hand([NumberedCard(3, Suit.Spades), KingCard(Suit.Diamonds), NumberedCard(6, Suit.Spades),
               AceCard(Suit.Hearts), NumberedCard(2, Suit.Spades)])
    h1_sorted = Hand([NumberedCard(2, Suit.Spades), NumberedCard(3, Suit.Spades), NumberedCard(6, Suit.Spades),
                      KingCard(Suit.Diamonds), AceCard(Suit.Hearts)])
    h1.sort()
    for c, c_sorted in zip(h1.cards, h1_sorted.cards):
        assert c == c_sorted

    h2 = Hand([QueenCard(Suit.Hearts), NumberedCard(2, Suit.Spades), NumberedCard(2, Suit.Hearts),
               QueenCard(Suit.Diamonds), NumberedCard(5, Suit.Hearts)])
    h2_sorted = [NumberedCard(2, Suit.Spades), NumberedCard(2, Suit.Hearts), NumberedCard(5, Suit.Hearts),
                 QueenCard(Suit.Hearts), QueenCard(Suit.Diamonds)]
    h2.sort()
    assert h2.cards == h2_sorted

    # check indices of hand.drop_cards
    h = Hand([NumberedCard(3, Suit.Spades), KingCard(Suit.Diamonds), NumberedCard(6, Suit.Spades),
              AceCard(Suit.Hearts), NumberedCard(2, Suit.Spades)])
    removed_cards = h.drop_cards([1, 3])
    assert removed_cards[0] == KingCard(Suit.Diamonds)
    assert removed_cards[1] == AceCard(Suit.Hearts)
    assert len(h.cards) == 3

    # also works for a single index
    rc = h.drop_cards(0)
    assert rc == NumberedCard(3, Suit.Spades)


def test_straight_flush():
    """
    The test checks that a straight-flush is created instead of straight for pokerhand.
    :return: a PokerHand of type STRAIGHT-FLUSH
    """
    hand = Hand()
    hand.add_card(AceCard(Suit.Spades))
    hand.add_card(NumberedCard(2, Suit.Hearts))
    hand.add_card(NumberedCard(3, Suit.Hearts))
    hand.add_card(NumberedCard(4, Suit.Hearts))
    hand.add_card(NumberedCard(5, Suit.Hearts))
    hand.add_card(AceCard(Suit.Hearts))
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 9
    assert check_hand.hand_type.name == 'STRAIGHT_FLUSH'
    print('Test Straight flush : ====================================================')
    print('Straight-flush gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    return check_hand

def test_pair():
    """
    The test checks that one pair is created instead of high card and that higher pair bets lower pair. Also checks that
    pairs are created for all values.
    :return: a PokerHand of type ONE_PAIR
    """
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 2
    assert check_hand.hand_type.name == 'ONE_PAIR'
    print('Test One Pair : ====================================================')
    print('Pair gives:', check_hand.hand_type.value, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    # testing same pair but higher kicker-card
    h1 = Hand([NumberedCard(3, Suit.Spades), AceCard(Suit.Spades)])
    h2 = Hand([NumberedCard(3, Suit.Hearts), JackCard(Suit.Spades)])
    h3 = Hand([NumberedCard(8, Suit.Hearts), JackCard(Suit.Hearts)])
    pc = [NumberedCard(3, Suit.Clubs), NumberedCard(5, Suit.Diamonds), NumberedCard(6, Suit.Clubs),
          NumberedCard(10, Suit.Diamonds), NumberedCard(8, Suit.Clubs)]


    ph1 = h1.best_poker_hand(pc)
    ph2 = h2.best_poker_hand(pc)
    ph3 = h3.best_poker_hand(pc)
    # Ace bets Jack
    assert ph1 > ph2
    # pairs in 8 bets pair in 3
    assert ph2 < ph3

    # test pairs in all values
    j = 4
    k = 3
    for i in range(2, 11):
        hc = Hand([NumberedCard(i, Suit.Spades), AceCard(Suit.Hearts)])
        if k == i:
            k = 2
        elif j == i:
            j = 3
        tc = [NumberedCard(i, Suit.Hearts), KingCard(Suit.Diamonds), JackCard(Suit.Clubs),
              NumberedCard(j, Suit.Hearts), NumberedCard(k, Suit.Spades)]
        ph = hc.best_poker_hand(tc)
        assert ph.hand_type.value == 2
        assert ph.hand_type.name == 'ONE_PAIR'

    cards_list = [KingCard(Suit.Clubs), JackCard(Suit.Diamonds), AceCard(Suit.Diamonds)]
    for card in cards_list:
        hc = Hand([card, AceCard(Suit.Hearts)])
        ph = hc.best_poker_hand(tc)
        assert ph.hand_type.value == 2
        assert ph.hand_type.name == 'ONE_PAIR'

    hc = Hand([QueenCard(Suit.Spades), QueenCard(Suit.Hearts)])
    ph = hc.best_poker_hand(tc)
    assert ph.hand_type.value == 2
    assert ph.hand_type.name == 'ONE_PAIR'

    return check_hand


def test_two_pairs():
    """
    The test checks that one pair is created instead of high card and that higher pair bets lower pair. Also checks that
    pairs are created for all values.
    :return: a PokerHand of type TWO_PAIRS
    """
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[27])
    hand.add_card(deck.cards[16])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 3
    assert check_hand.hand_type.name == 'TWO_PAIR'
    print('Test two pairs : ====================================================')
    print('Two pair gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    # testing same value pairs but higher kicker
    h1 = Hand([NumberedCard(3, Suit.Spades), AceCard(Suit.Spades)])
    h2 = Hand([NumberedCard(3, Suit.Hearts), JackCard(Suit.Spades)])
    h3 = Hand([NumberedCard(3, Suit.Diamonds), NumberedCard(8, Suit.Spades)])
    pc = [NumberedCard(3, Suit.Clubs), NumberedCard(5, Suit.Diamonds), NumberedCard(5, Suit.Clubs),
          NumberedCard(10, Suit.Diamonds), NumberedCard(8, Suit.Clubs)]

    ph1 = h1.best_poker_hand(pc)
    ph2 = h2.best_poker_hand(pc)
    ph3 = h3.best_poker_hand(pc)
    # Ace bets Jack
    assert ph1 > ph2
    # Better pairs
    assert ph3 > ph1

    return check_hand


def test_three():
    """
    The test checks that three of a kind is created and can be for all values. Also checks that higher three of a kind
    bets lower.
    :return: a PokerHand of type THREE_OF_A_KIND
    """
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[26])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 4
    assert check_hand.hand_type.name == 'THREE_OF_A_KIND'
    print('Test three of a kind : ====================================================')
    print('Three of a kind gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    k = 3
    for i in range(2, 11):
        hc = Hand([NumberedCard(i, Suit.Spades), AceCard(Suit.Hearts)])
        if k == i:
            k = 2
        tc = [NumberedCard(i, Suit.Hearts), KingCard(Suit.Diamonds), JackCard(Suit.Clubs),
              NumberedCard(i, Suit.Clubs), NumberedCard(k, Suit.Spades)]
        ph = hc.best_poker_hand(tc)
        assert ph.hand_type.value == 4
        assert ph.hand_type.name == 'THREE_OF_A_KIND'
        assert ph.best_cards == [NumberedCard(i, Suit.Hearts), NumberedCard(i, Suit.Clubs),
                                 NumberedCard(i, Suit.Spades), AceCard(Suit.Hearts), KingCard(Suit.Diamonds)]

    cards_list_king = [KingCard(Suit.Diamonds), KingCard(Suit.Clubs)]
    cards_list_jack = [JackCard(Suit.Diamonds), JackCard(Suit.Clubs)]
    cards_list_ace = [AceCard(Suit.Diamonds), AceCard(Suit.Clubs)]

    for c1, c2 in cards_list_king, cards_list_jack, cards_list_ace:
        tc = [c1, KingCard(Suit.Spades), JackCard(Suit.Clubs),
              NumberedCard(3, Suit.Clubs), NumberedCard(5, Suit.Spades)]
        hc = Hand([c2, AceCard(Suit.Hearts)])
        ph = hc.best_poker_hand(tc)
        assert ph.hand_type.value == 4
        assert ph.hand_type.name == 'THREE_OF_A_KIND'

    tc[0] = QueenCard(Suit.Diamonds)
    hc = Hand([QueenCard(Suit.Spades), QueenCard(Suit.Hearts)])
    ph = hc.best_poker_hand(tc)
    assert ph.hand_type.value == 4
    assert ph.hand_type.name == 'THREE_OF_A_KIND'

    # testing that three of 4s are better than three of 3s
    h1 = Hand([NumberedCard(4, Suit.Spades), NumberedCard(4, Suit.Diamonds)])
    h2 = Hand([NumberedCard(3, Suit.Hearts), NumberedCard(3, Suit.Diamonds)])
    pc = [NumberedCard(3, Suit.Clubs), JackCard(Suit.Spades), NumberedCard(4, Suit.Clubs),
          AceCard(Suit.Spades), NumberedCard(10, Suit.Clubs)]
    ph1 = h1.best_poker_hand(pc)
    ph2 = h2.best_poker_hand(pc)
    assert ph1 > ph2

    return check_hand

def test_full_house():
    """
    The test checks that a full house can be created and a type with a higher three of a kind bets a type with lower
    three of a kind but with higher pair.
    :return: a PokerHand of type FULL_HOUSE
    """
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[2])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[27])
    hand.add_card(deck.cards[40])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 7
    assert check_hand.hand_type.name == 'FULL_HOUSE'
    print('Test full house : ====================================================')
    print('Full house gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    # three of 4s should be better than three of 3s
    h1 = Hand([NumberedCard(4, Suit.Spades), AceCard(Suit.Spades)])
    h2 = Hand([NumberedCard(3, Suit.Hearts), JackCard(Suit.Spades)])
    pc = [NumberedCard(3, Suit.Clubs), NumberedCard(3, Suit.Diamonds), NumberedCard(4, Suit.Clubs),
          NumberedCard(4, Suit.Diamonds), NumberedCard(10, Suit.Clubs)]

    ph1 = h1.best_poker_hand(pc)
    ph2 = h2.best_poker_hand(pc)
    assert ph1 > ph2

    return check_hand

def test_four():
    """
    The test checks that four of a kind is created and can be for all values. Also checks that higher four of a kind
    bets lower.
    :return: a PokerHand of type FOUR_OF_A_KIND
    """
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[26])
    hand.add_card(deck.cards[39])
    hand.add_card(deck.cards[16])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 8
    assert check_hand.hand_type.name == 'FOUR_OF_A_KIND'
    print('Test four of a kind : ====================================================')
    print('Four of a kind gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    # testing that the four of a kind are possible for all cards
    for i in range(2, 11):
        hc = Hand([NumberedCard(i, Suit.Spades), AceCard(Suit.Hearts)])
        tc = [NumberedCard(i, Suit.Hearts), KingCard(Suit.Diamonds), JackCard(Suit.Clubs),
              NumberedCard(i, Suit.Diamonds), NumberedCard(i, Suit.Clubs)]
        ph = hc.best_poker_hand(tc)
        assert ph.hand_type.value == 8
        assert ph.hand_type.name == 'FOUR_OF_A_KIND'
        assert ph.best_cards == [NumberedCard(i, Suit.Hearts), NumberedCard(i, Suit.Diamonds),
                                 NumberedCard(i, Suit.Clubs), NumberedCard(i, Suit.Spades), AceCard(Suit.Hearts)]

    cards_list_king = [KingCard(Suit.Clubs), KingCard(Suit.Hearts), KingCard(Suit.Spades)]
    cards_list_jack = [JackCard(Suit.Diamonds), JackCard(Suit.Hearts), JackCard(Suit.Spades)]
    cards_list_ace = [AceCard(Suit.Diamonds), AceCard(Suit.Hearts), AceCard(Suit.Spades)]

    for c1, c2, c3 in cards_list_king, cards_list_jack, cards_list_ace:
        tc = [c2, KingCard(Suit.Diamonds), JackCard(Suit.Clubs),
              NumberedCard(6, Suit.Clubs), c3]
        hc = Hand([c1, AceCard(Suit.Hearts)])
        ph = hc.best_poker_hand(tc)
        assert ph.hand_type.value == 8
        assert ph.hand_type.name == 'FOUR_OF_A_KIND'

    tc[0:2] = [QueenCard(Suit.Diamonds), QueenCard(Suit.Clubs)]

    hc = Hand([QueenCard(Suit.Spades), QueenCard(Suit.Hearts)])
    ph = hc.best_poker_hand(tc)
    assert ph.hand_type.value == 8
    assert ph.hand_type.name == 'FOUR_OF_A_KIND'

    # four of 4s should be better than four of 3s
    h1 = Hand([NumberedCard(4, Suit.Spades), NumberedCard(4, Suit.Diamonds)])
    h2 = Hand([NumberedCard(3, Suit.Hearts), NumberedCard(3, Suit.Diamonds)])
    pc = [NumberedCard(3, Suit.Clubs), NumberedCard(3, Suit.Spades), NumberedCard(4, Suit.Clubs),
          NumberedCard(4, Suit.Hearts), NumberedCard(10, Suit.Clubs)]

    ph1 = h1.best_poker_hand(pc)
    ph2 = h2.best_poker_hand(pc)
    assert ph1 > ph2

    return check_hand


def test_straight():
    """
    The test checks that a straight can be created with all values between 1-14 (low ace to high ace). It also checks
    that straight is created instead of two pairs and that higher straight bets lower straight.
    :return: a PokerHand of type STRAIGHT
    """
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[5])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    hand.add_card(deck.cards[17])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 5
    assert check_hand.hand_type.name == 'STRAIGHT'
    print('Test straight : ====================================================')
    print('Straight gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

    # Check that straight works for all the cards values
    suit_list = [suit for suit in Suit] * 2 + [Suit.Spades, Suit.Hearts]
    card_list = [AceCard(Suit.Clubs, first=True)] + [NumberedCard(x, suit) for x, suit in zip(range(2,11), suit_list)]\
        + [JackCard(Suit.Hearts), QueenCard(Suit.Diamonds), KingCard(Suit.Clubs), AceCard(Suit.Spades)]

    hc = Hand([NumberedCard(3, Suit.Clubs), NumberedCard(5, Suit.Hearts)])
    for i in range(9):
        pc = card_list[i:i+5]
        ph = hc.best_poker_hand(pc)
        assert ph.hand_type.value == 5
        assert ph.hand_type.name == 'STRAIGHT'
        assert ph.best_cards == pc

    assert check_hand < ph

    return check_hand


def test_flush():
    """
    The test checks that flush is created and can be created for all suit types.
    :return: a PokerHand of type FLUSH
    """
    # test for all suits
    for suit in Suit:
        hand = Hand([NumberedCard(2, suit), NumberedCard(5, suit)])
        pc = [NumberedCard(6, suit), AceCard(suit), JackCard(suit), NumberedCard(8, suit),
              NumberedCard(3, Suit.Hearts)]
        ph = hand.best_poker_hand(pc)
        assert ph.hand_type.value == 6
        assert ph.hand_type.name == 'FLUSH'

    print('Test flush : ====================================================')
    print('Flush:', ph.points, 'points with hand:', end=' [')
    for i in ph.best_cards:
        print(i, end=' ')
    print(']\n')

    return ph


def test_PokerHand_order():
    """
    The test runs previous test and retrieves the previous poker hand types. It checks that the type cards in the poker
    hand (pairs in this case) is first used to determine winner and then the kicker (high card). If hand type cards and
    kickers are the same (but different suits) the poker hand are equal. It also checks the ranking orders of the
    hand types.
    """
    hand1 = Hand([NumberedCard(3, Suit.Spades),
                  NumberedCard(3, Suit.Hearts),
                  NumberedCard(5, Suit.Diamonds),
                  NumberedCard(5, Suit.Clubs),
                  NumberedCard(10, Suit.Spades)])

    hand2 = Hand([NumberedCard(4, Suit.Diamonds),
                  NumberedCard(4, Suit.Hearts),
                  NumberedCard(5, Suit.Spades),
                  NumberedCard(5, Suit.Hearts),
                  NumberedCard(9, Suit.Hearts)])

    hand3 = Hand([NumberedCard(4, Suit.Diamonds),
                  NumberedCard(4, Suit.Hearts),
                  NumberedCard(5, Suit.Spades),
                  NumberedCard(5, Suit.Hearts),
                  NumberedCard(10, Suit.Hearts)])

    hand4 = Hand([NumberedCard(4, Suit.Clubs),
                  NumberedCard(4, Suit.Spades),
                  NumberedCard(5, Suit.Clubs),
                  NumberedCard(5, Suit.Diamonds),
                  NumberedCard(10, Suit.Diamonds)])

    ph1 = PokerHand(hand1.cards)
    ph2 = PokerHand(hand2.cards)
    ph3 = PokerHand(hand3.cards)
    ph4 = PokerHand(hand4.cards)

    assert ph1 < ph2
    assert ph2 < ph3
    assert ph3 == ph4

    # test the order of all poker hand types
    ph_pair = test_pair()
    ph_two_pair = test_two_pairs()
    ph_three = test_three()
    ph_full_house = test_full_house()
    ph_flush = test_flush()
    ph_straight = test_straight()
    ph_four = test_four()
    ph_straight_flush = test_straight_flush()

    assert ph_pair < ph_two_pair < ph_three < ph_straight < ph_flush < ph_full_house < ph_four < ph_straight_flush


# Print the deck:
deck = StandardDeck()
print('===============')
print('Deck of cards:')
print('===============')
for i, j in enumerate(deck.cards):
    print(f'{j}', end=' ')
    if i==12 or i==25 or i==38 or i==51:
        print('')
print('')


test_cards()
test_deck()
test_PokerHand_order()
test_hand()
