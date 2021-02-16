from enum import Enum
import numpy as np
import random


class Suit(Enum):
    Spades = 4  # Suit are not ranked, just for sorting purpose
    Hearts = 3
    Diamonds = 2
    Clubs = 1


class PlayingCard:
    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return "[{}, {}]".format(self.suit.name, self.value)



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


class AceCard(PlayingCard):
    def __init__(self, suit: Suit, first=False):
        if first:
            self.value = 1
        else:
            self.value = 14
        self.suit = suit

    def get_value(self):
        print(self.value)
        return self.value


class Hand:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    # add card to the hand with StandardDeck.take_card()
    def add_card(self, new_card):
        self.cards.append(new_card)

    def sort_cards(self):
        # sorted_values = sorted(self.cards, key=lambda x: getattr(x, 'value'))
        # sorting_suits = [[], [], [], []]
        # for i in range(len(sorted_values)):
        #     sorting_suits[sorted_values[i].suit.value - 1].append(sorted_values[i])
        #
        # self.cards = [x for i in sorting_suits for x in i]
        # # above comments are for sorting by suit and value
        self.cards = sorted(self.cards, key=lambda x: getattr(x, 'value'))

    def drop_cards(self, index):
        # index is given as 0 at the first position
        dropped_cards = []
        for i in index:
            dropped_cards.append(self.cards[i])
        self.cards = np.delete(self.cards, index)
        return dropped_cards

    def show_hand(self):  # change ths to __repr__
        hand = []
        for i in range(len(self.cards)):
            hand.append([self.cards[i].value, self.cards[i].suit.name])
        print(hand)

    def best_poker_hand(self, cards=[]):
        poker_cards = self.cards.copy()
        if cards:
            if len(cards) > 1:
                poker_cards.extend(cards)
            else:
                poker_cards.append(cards)
        return PokerHand(poker_cards)


class PokerHand:
    def __init__(self, cards):
        self.cards = cards
        self.best_cards = []
        values = []
        for i in self.cards:
            print(i)
            values.append(i.value)
        self.__duplicate_values()
        self._straight = self.__check_straight()
        self._straight_flush = False
        self.__check_flush()
        if self._straight_flush:
            self.__best_cards(self._straight_cards)
            self.points = 9
        elif self.points < 7 and (self._flush or self._straight):
            if self._flush:
                self.__best_cards(self.flush_cards)
                self.points = 6
            else:
                self.points = 5
                self.__best_cards(self._straight_cards)
        else:
            self.__best_cards(self._duplicate_values)

    def __lt__(self, other):
        if self.points != other.points:
            return self.points < other.points
        elif max(self.other_cards) != max(other.other_cards):
            return max(self.other_cards) < max(other.other_cards)

    def __best_cards(self, category_cards=None):
        other_cards = self.cards.copy()
        indices = []
        if category_cards:
            for i, elem in enumerate(other_cards):
                for j in category_cards:
                    if (j == elem) and (j.suit.value == elem.suit.value):
                        indices.append(i)
        self.other_cards = list(np.delete(other_cards, indices))
        self.other_cards.sort(reverse=True)
        category_cards.extend(self.other_cards)
        self.best_cards = category_cards[:5].copy()

    def __duplicate_values(self):
        unique, counts = np.unique(self.cards, return_counts=True)
        self._duplicate_values = []
        if any(counts == 2) & any(counts == 3):
            self.points = 7
            full_house = [max(unique[counts == 2]), max(unique[counts == 3])]
            print(full_house)
            self._duplicate_values = self.__cards_in_category(full_house)
        elif any(counts == 2):
            if len(counts[counts == 2]) > 1:
                two_pair = unique[counts == 2]
                self._duplicate_values = self.__cards_in_category(two_pair)
                self.points = 3
            else:
                pair = unique[counts == 2]
                self._duplicate_values = self.__cards_in_category(pair)
                self.points = 2
        elif any(counts == 3):
            three_of_a_kind = unique[counts == 3]
            self._duplicate_values = self.__cards_in_category(three_of_a_kind)
            self.points = 4
        elif any(counts == 4):
            four_of_a_kind = unique[counts == 2]
            self._duplicate_values = self.__cards_in_category(four_of_a_kind)
            self.points = 8
        else:
            self.points = 1
        # duplicate_values = np.array(values)[values == unique[counts == max(counts)]]
        #duplicate_values = np.array(self.cards)[values == unique[counts == max(counts)]]
        #self._duplicate_values = list(duplicate_values)
        # self._duplicate_values = []
        # for elem in values:
        #     if values.count(elem) == 2:
        #         self._duplicate_values.append(2)
        #         print('pair')
        #     elif values.count(elem) == 3:
        #         self._duplicate_values.append(3)
        #         print('three of a kind')
        #     elif values.count(elem) == 4:
        #         self._duplicate_values.append(4)
        #         print('four of a kind')
        # if not self._duplicate_values:  # just to see if it's working
        #     print('No duplicates')
        # return self._duplicate_values

    def __check_flush(self, suit_cards=None):
        if not suit_cards:
            suit_cards = self.cards.copy()
        suits = []
        for i in suit_cards:
            suits.append(i.suit.value)
        self._flush = False
        un, co = np.unique(suits, return_counts=True)
        if any(co >= 5):
            self.flush_cards = []
            self._flush = True
            for i, color in enumerate(suits):
                if color == un[co >= 5]:
                    self.flush_cards.append(suit_cards[i])
            self._straight_flush = self.__check_straight(self.flush_cards)


    def __check_straight(self, straight_cards=None):
        if not straight_cards:
            straight_cards = self.cards.copy()
        cards = []

        if (AceCard(Suit) in straight_cards) and (NumberedCard(2, Suit) in straight_cards):
            suit_of_acecard = straight_cards[straight_cards.index(AceCard(Suit))].suit
            cards.append(AceCard(suit_of_acecard, first=True))
            straight_cards.sort()
            if KingCard(Suit) not in straight_cards:
                del (straight_cards[-1])  # removes AceCard with value 14
        cards.extend(straight_cards)
        cards.sort()
        self._straight_cards = []
        self._straight_cards.append(cards[0])
        straight = False
        # for i in range(len(values)-1):
        for i in range(len(cards) - 1):
            if cards[i].value + 1 == cards[i + 1].value:
                # if values[i] + 1 == values[i + 1]:
                #    straight += 1
                self._straight_cards.append(cards[i+1])
                # print(self._straight_cards,'----',len(self._straight_cards))
            else:
                #    straight = 0
                # in case we have 5 (straight) in row but 6th is not
                if len(self._straight_cards) >= 5:
                    straight = True
                    break
                self._straight_cards = []
                self._straight_cards.append(cards[i])
        if len(self._straight_cards) >= 5:
            straight = True
            #self._straight_flush = self.__check_suits(self._straight_cards)
        return straight

    def __cards_in_category(self, category_card):
        cards_list = []
        for j in range(len(category_card)):
            for i in self.cards:
                if i == category_card[j]:
                    cards_list.append(i)
        return cards_list


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

    def draw(self):
        new_card = self.cards[-1]
        # self.cards = np.delete(self.cards, -1)
        # self.cards.remove(self.cards[-1])
        self.cards = self.cards[:-1]
        return new_card
