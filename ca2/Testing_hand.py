from cardlib import *
import pytest


def test_deck():
    # Check that there's 13 cards of each suit
    deck = StandardDeck()
    assert len(deck.cards) == 52
    cards = {'Clubs': [], 'Diamonds': [], 'Hearts': [], 'Spades': []}
    for i, suit_type in enumerate(cards):
        for card_type in range(13):
            new_card = deck.draw()
            assert new_card  # check that we pick up a card
            cards[suit_type].append(new_card)
            assert new_card.suit.name == suit_type
    un = np.unique(cards)
    for i, suit_type in enumerate(cards):
        assert len(un[0][suit_type]) == 13  # checks uniqueness in suits


def test_hand():
    deck = StandardDeck()
    deck.shuffle()
    hand = Hand()
    hand2 = Hand()
    for i in range(6):
        hand.add_card(deck.draw())
    hand.sort_cards()

    # Check that the order is from low to high
    for i in range(1, len(hand.cards)-1):
        assert hand.cards[i].value >= hand.cards[i-1].value


def test_straight_flush():
    hand = Hand()
    hand.add_card(AceCard(Suit.Spades))
    hand.add_card(NumberedCard(2, Suit.Hearts))
    hand.add_card(NumberedCard(3, Suit.Hearts))
    hand.add_card(NumberedCard(4, Suit.Hearts))
    hand.add_card(NumberedCard(5, Suit.Hearts))
    # hand.add_card(NumberedCard(7, Suit.Spades))
    hand.add_card(AceCard(Suit.Hearts))
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 9
    assert check_hand.hand_type.name == 'straight_flush'
    # print('Straight-flush gives:', check_hand.points, 'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')

def test_pair():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 2
    assert check_hand.hand_type.name == 'one_pair'
    # print('Pair gives:', check_hand.points,'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')


def test_two_pairs():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[27])
    hand.add_card(deck.cards[16])
    hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 3
    assert check_hand.hand_type.name == 'two_pair'
    # print('Two pair gives:', check_hand.points,'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')

def test_three():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[26])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 4
    assert check_hand.hand_type.name == 'three_of_a_kind'
    # print('Three of a kind gives:', check_hand.points, 'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')

def test_full_house():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[2])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[27])
    hand.add_card(deck.cards[40])
    hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 7
    assert check_hand.hand_type.name == 'full_house'
    # print('Full house gives:', check_hand.points, 'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')

def test_four():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[26])
    hand.add_card(deck.cards[39])
    hand.add_card(deck.cards[16])
    hand.show_hand()
    check_hand = PokerHand(hand.cards)
    print(check_hand.best_cards)
    assert check_hand.hand_type.value == 8
    assert check_hand.hand_type.name == 'four_of_a_kind'
    # print('Four of a kind gives:', check_hand.points, 'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')

def test_straight():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[5])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    hand.add_card(deck.cards[17])
    hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 5
    assert check_hand.hand_type.name == 'straight'
    # print('Straight gives:', check_hand.points, 'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')

def test_flush():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[2])
    hand.add_card(deck.cards[3])
    hand.add_card(deck.cards[5])
    hand.add_card(deck.cards[12])
    hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 6
    assert check_hand.hand_type.name == 'flush'
    # print('Flush:', check_hand.points, 'points with hand:')
    # for i in check_hand.best_cards:
    #     print(i, end=',')
    # print('\n')


def test_PokerHand_order():
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



test_pair()
test_two_pairs()
test_three()
test_full_house()
test_flush()
test_straight()
test_four()
test_straight_flush()
test_deck()
test_PokerHand_order()
test_hand()
