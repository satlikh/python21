from cardlib import *

deck = StandardDeck()
deck.shuffle()
deck.shuffle()
deck.shuffle()
deck.shuffle()
deck.shuffle()
hand = Hand()
hand.add_card(deck.draw())
hand.add_card(deck.draw())
hand.add_card(deck.draw())
hand.add_card(deck.draw())
hand.add_card(deck.draw())
hand.add_card(deck.draw())
# hand.show_hand()

def test_straight_flush():
    deck1 = StandardDeck()
    hand1 = Hand()
    hand1.add_card(deck1.draw())
    hand1.add_card(deck1.draw())
    hand1.add_card(deck1.draw())
    hand1.add_card(deck1.draw())
    hand1.add_card(deck1.draw())
    hand1.add_card(deck1.draw())
    check_hand = PokerHand(hand1.cards)
    assert check_hand.points == 9
    print('Straight-flush gives:', check_hand.points,'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')


def test_pair():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    check_hand = PokerHand(hand.cards)
    assert check_hand.points == 2
    print('Pair gives:', check_hand.points,'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')


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
    assert check_hand.points == 3
    print('Two pair gives:', check_hand.points,'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')


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
    assert check_hand.points == 4
    print('Three of a kind gives:', check_hand.points, 'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')

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
    assert check_hand.points == 7
    print('Full house gives:', check_hand.points, 'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')

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
    assert check_hand.points == 8
    print('Four of a kind gives:', check_hand.points, 'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')


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
    assert check_hand.points == 5
    print('Straight gives:', check_hand.points, 'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')


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
    assert check_hand.points == 6
    print('Flush:', check_hand.points, 'points with hand:')
    for i in check_hand.cards:
        print(i, end=',')


print('\n------one pair-----')
test_pair()
print('\n------Two pairs-----')
test_two_pairs()
print('\n------Three of a kind-----')
test_three()
print('\n------Full house-----')
test_full_house()
print('\n------Flush-----')
test_flush()
print('\n------Straight-----')
test_straight()
print('\n------Four of a kind-----')
test_four()
print('\n------Straight flush-----')
test_straight_flush()
