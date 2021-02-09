from enum import Enum
import numpy as np
import random


class Suit(Enum):
    Spades = 4  # Highest in rank/Best
    Hearts = 3
    Diamonds = 2
    Clubs = 1  # Lowest in rank/Worst


class NumberedCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_value(self):
        print(self.value)
        return self.value


class JackCard:
    def __init__(self, suit):
        self.suit = suit
        self.value = 11

    def get_value(self):
        print(self.value)
        return self.value


class QueenCard:
    def __init__(self, suit):
        self.suit = suit
        self.value = 12

    def get_value(self):
        print(self.value)
        return self.value


class KingCard:
    def __init__(self, suit):
        self.suit = suit
        self.value = 13

    def get_value(self):
        print(self.value)
        return self.value


class AceCard:
    def __init__(self, suit):
        self.suit = suit
        self.value = 1

    def get_value(self):
        print(self.value)
        return self.value


class Hand:
    def __init__(self):
        self.card = []

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

    def shuffle(self):
        random.shuffle(self.cards)

    def take_card(self):
        new_card = self.cards[-1]
        self.cards = np.delete(self.cards, -1)
        return new_card

