from cardlib import *
import pytest


def test_deck():
    # Check that there's 13 cards of each suit
    deck = StandardDeck()

    # run the test twice to check that new deck is created
    for _ in range(2):
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

        deck.new_deck()


def test_hand():
    deck = StandardDeck()
    deck.shuffle()
    hand = Hand()
    for i in range(6):
        hand.add_card(deck.draw())
    hand.sort_cards()

    # Check that the order is from low to high
    for i in range(1, len(hand.cards)-1):
        assert hand.cards[i].value >= hand.cards[i-1].value

    # check indices of hand.drop_cards
    h = Hand([NumberedCard(3, Suit.Spades), KingCard(Suit.Diamonds), NumberedCard(6, Suit.Spades),
              AceCard(Suit.Hearts), NumberedCard(2, Suit.Spades)])
    removed_cards = h.drop_cards([1, 3])
    assert removed_cards[0] == KingCard(Suit.Diamonds)
    assert removed_cards[1] == AceCard(Suit.Hearts)
    assert len(h.cards) == 3

    rc = h.drop_cards(0)
    assert rc == NumberedCard(3, Suit.Spades)


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
    assert check_hand.hand_type.name == 'STRAIGHT_FLUSH'
    print('Test Straight flush : ====================================================')
    print('Straight-flush gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

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
    assert check_hand.hand_type.name == 'ONE_PAIR'
    print('Test One Pair : ====================================================')
    print('Pair gives:', check_hand.hand_type.value, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

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


def test_two_pairs():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[27])
    hand.add_card(deck.cards[16])
    # hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 3
    assert check_hand.hand_type.name == 'TWO_PAIR'
    print('Test two pairs : ====================================================')
    print('Two pair gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

def test_three():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[26])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    # hand.show_hand()
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
    #hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 7
    assert check_hand.hand_type.name == 'FULL_HOUSE'
    print('Test full house : ====================================================')
    print('Full house gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')

def test_four():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[13])
    hand.add_card(deck.cards[26])
    hand.add_card(deck.cards[39])
    hand.add_card(deck.cards[16])
    # hand.show_hand()
    check_hand = PokerHand(hand.cards)
    # print(check_hand.best_cards)
    assert check_hand.hand_type.value == 8
    assert check_hand.hand_type.name == 'FOUR_OF_A_KIND'
    print('Test four of a kind : ====================================================')
    print('Four of a kind gives:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')


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

def test_straight():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[5])
    hand.add_card(deck.cards[14])
    hand.add_card(deck.cards[15])
    hand.add_card(deck.cards[16])
    hand.add_card(deck.cards[17])
    # hand.show_hand()
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


def test_flush():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.cards[0])
    hand.add_card(deck.cards[2])
    hand.add_card(deck.cards[3])
    hand.add_card(deck.cards[5])
    hand.add_card(deck.cards[12])
    # hand.show_hand()
    check_hand = PokerHand(hand.cards)
    assert check_hand.hand_type.value == 6
    assert check_hand.hand_type.name == 'FLUSH'
    print('Test flush : ====================================================')
    print('Flush:', check_hand.points, 'points with hand:', end=' [')
    for i in check_hand.best_cards:
        print(i, end=' ')
    print(']\n')


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
