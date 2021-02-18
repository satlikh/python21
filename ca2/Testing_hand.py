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
    # deck1 = StandardDeck()
    hand = Hand()
    hand.add_card(AceCard(Suit.Spades))
    hand.add_card(NumberedCard(2, Suit.Hearts))
    hand.add_card(NumberedCard(3, Suit.Hearts))
    hand.add_card(NumberedCard(4, Suit.Hearts))
    hand.add_card(NumberedCard(5, Suit.Hearts))
    # hand.add_card(NumberedCard(7, Suit.Spades))
    hand.add_card(AceCard(Suit.Hearts))
    check_hand = PokerHand(hand.cards)
    assert check_hand.points == 9
    print('Straight-flush gives:', check_hand.points,'points with hand:')
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')

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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')


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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')

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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')

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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')

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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')

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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')

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
    for i in check_hand.best_cards:
        print(i, end=',')
    print('\n')


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
    hand4 = Hand([NumberedCard(4, Suit.Diamonds),
                  NumberedCard(4, Suit.Hearts),
                  NumberedCard(5, Suit.Spades),
                  NumberedCard(5, Suit.Hearts),
                  NumberedCard(10, Suit.Hearts)])

    ph1 = PokerHand(hand1.cards)
    ph2 = PokerHand(hand2.cards)
    ph3 = PokerHand(hand3.cards)
    ph4 = PokerHand(hand4.cards)

    assert ph1 < ph2
    assert ph2 < ph3
    assert ph3 == ph4


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
print('\n')
