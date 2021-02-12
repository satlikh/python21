from enum import Enum
import numpy as np
import random


class Suit(Enum):
    Spades = 4  # Suit are not ranked, just for sorting purpose
    Hearts = 3
    Diamonds = 2
    Clubs = 1


class PlayingCard:
    pass


class NumberedCard(PlayingCard):
    def __init__(self, value: int, suit: Suit):
        self.value = value
        self.suit = suit

    def get_value(self):
        print(self.value)
        return self.value


class JackCard(PlayingCard):
    def __init__(self, suit: Suit):
        self.suit = suit
        self.value = 11

    def get_value(self):
        print(self.value)
        return self.value


class QueenCard(PlayingCard):
    def __init__(self, suit: Suit):
        self.suit = suit
        self.value = 12

    def get_value(self):
        print(self.value)
        return self.value


class KingCard(PlayingCard):
    def __init__(self, suit: Suit):
        self.suit = suit
        self.value = 13

    def get_value(self):
        print(self.value)
        return self.value


class AceCard:
    def __init__(self, suit: Suit):
        self.suit = suit
        self.value = 14

    def get_value(self):
        print(self.value)
        return self.value


class Hand:
    def __init__(self, card=None):
        if card is None:
            self.card = []
        else:
            self.card = card

    # add card to the hand with StandardDeck.take_card()
    def new_card(self, new_card):
        self.card.append(new_card)

    def sort_cards(self):
        sorted_values = sorted(self.card, key=lambda x: getattr(x, 'value'))
        sorting_suits = [[], [], [], []]
        for i in range(len(sorted_values)):
            sorting_suits[sorted_values[i].suit.value - 1].append(sorted_values[i])

        self.card = [x for i in sorting_suits for x in i]

    def drop_cards(self, index):
        # index is given as 0 at the first position
        dropped_cards = []
        for i in index:
            dropped_cards.append(self.card[i])
        self.card = np.delete(self.card, index)
        return dropped_cards

    def show_hand(self):
        hand = []
        for i in range(len(self.card)):
            hand.append([self.card[i].value, self.card[i].suit.name])
        print(hand)

    # def best_poker_hand(self, cards=[]):
    #


class PokerHand:
    def __init__(self, cards):
        self.cards = cards
        values = []
        for i in self.cards:
            values.append(i.value)
        self.__duplicate_values__(values)

    def __duplicate_values__(self, values):
        unique, counts = np.unique(values, return_counts=True)
        self.duplicate_values = []
        if any(counts == 2) & any(counts == 3):
            self.points = 7
        elif any(counts == 2):
            if len(counts[counts == 2]) > 1:
                self.points = 3
            else:
                self.points = 2
        elif any(counts == 3):
            self.points = 4
        elif any(counts == 4):
            self.points = 8
        else:
            self.points = 1
        # duplicate_values = np.array(values)[values == unique[counts == max(counts)]]
        duplicate_values = np.array(self.cards)[values == unique[counts == max(counts)]]
        self.duplicate_values = list(duplicate_values)
        # self.duplicate_values = []
        # for elem in values:
        #     if values.count(elem) == 2:
        #         self.duplicate_values.append(2)
        #         print('pair')
        #     elif values.count(elem) == 3:
        #         self.duplicate_values.append(3)
        #         print('three of a kind')
        #     elif values.count(elem) == 4:
        #         self.duplicate_values.append(4)
        #         print('four of a kind')
        # if not self.duplicate_values:  # just to see if it's working
        #     print('No duplicates')
        # return self.duplicate_values

    def __check_suits__(self):
        suits = []
        for i in self.cards:
            suits.append(i.suit.name)
        self.flush = False
        for elem in self.cards:
            if suits.count(elem) == 5: # add points
                self.flush = True
        return self.flush

    def __check_straight__(self, values):
        values.sort()
        straight = 1
        self.straight = False
        for i in range(len(values)-1):
            if values[i] + 1 == values[i+1]:
                straight += 1
            else:
                straight = 1
        if straight == 5:
            self.straight = True
        return self.straight






class StandardDeck:
    def __init__(self):
        cards = []
        for suit in enumerate(Suit):
            deck = np.array([NumberedCard(value, suit[1]) for value in range(1, 14)])
            deck[0] = AceCard(suit[1])
            deck[10] = JackCard(suit[1])
            deck[11] = QueenCard(suit[1])
            deck[12] = KingCard(suit[1])
            cards.append(deck)
        self.cards = np.reshape([cards[0], cards[1], cards[2], cards[3]], 52)
        self.cards = list(self.cards[:])  # to make the list mutable for random.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    def take_card(self):
        new_card = self.cards[-1]
        # self.cards = np.delete(self.cards, -1)
        self.cards.remove(self.cards[-1])
        return new_card

