from enum import Enum
import numpy as np
import random


class Suit(Enum):
    Spades = 4  # Suit are not ranked, just for sorting purpose
    Hearts = 3
    Diamonds = 2
    Clubs = 1


class PlayingCard:
    """
    Playing cards for the deck.
    Ranked as NumberedCard: 2-10, JackCard: 11, QueenCard: 12, KingCard: 13 and AceCard: 14
    Suit is given as Suit.Spades, Suit.Hearts, Suit.Diamonds or Suit.Clubs
    """
    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return "[{}, {}]".format(self.suit.name, self.value)

    def __repr__(self):
        return "{}({})".format(self.suit.name, self.value)


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
    """
    Sets class of hand.

    :param cards: Set initial cards for pre-determined hand or create an empty hand.
    :return: Empty Hand class or with initially set cards

    add_card(self, new_card)
        Adds the "new_card" to the hand.

    sort_cards(self)
        sorts the cards by value

    sort_cards_by_suit(self)
        sorts the cards by both value and suit, (Clubs, Diamonds, Hearts and Spades)

    drop_cards(self, index)
        Drops the cards presented by index
        :param index: A list (or interger) of indices, with first position given as 0.
        :return: Card(s) given by index

    show_hand(self)
        Presents the cards in the hand.

    best_poker_hand(self, cards = [])
        Calculates the best poker hand of the hand, and the added cards
        :param cards: List of playing cards in addition to the hand cards.
        :return: PokerHand-class with best poker hand type and best cards.
    """
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    # add card to the hand with StandardDeck.take_card()
    def add_card(self, new_card):
        self.cards.append(new_card)

    def sort_cards(self):
        self.cards = sorted(self.cards, key=lambda x: getattr(x, 'value'))

    def sort_cards_by_suit(self):
        sorted_values = sorted(self.cards, key=lambda x: getattr(x, 'value'))
        sorting_suits = [[], [], [], []]
        for i in range(len(sorted_values)):
            sorting_suits[sorted_values[i].suit.value - 1].append(sorted_values[i])
        self.cards = [x for i in sorting_suits for x in i]
        self.cards = sorted(self.cards, key=lambda x: getattr(x, 'value'))

    def drop_cards(self, index=None):
        try:
            if type(index) is int:
                index = [index]
            # index is given as 0 at the first position
            dropped_cards = []
            for i in index:
                dropped_cards.append(self.cards[i])
            self.cards = np.delete(self.cards, index)
            return dropped_cards
        except TypeError:
            print('No index was given')
        except IndexError:
            print(f'IndexError: Given index is "{index}" while number of cards is {len(self.cards)}')

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
    """
    Add some comments here!!!

    """
    def __init__(self, cards):
        self.cards = cards
        hand_type = Enum('PokerHand', 'high_card one_pair two_pair three_of_a_kind '
                                      'straight flush full_house four_of_a_kind straight_flush', module=__name__)
        self.__hand_type(hand_type)

    def __lt__(self, other):
        if self.hand_type.value != other.hand_type.value:
            return self.hand_type.value < other.hand_type.value

        else:
            un_self, co_self = np.unique(self.best_cards, return_counts=True)
            un_other, co_other = np.unique(other.best_cards, return_counts=True)
            ind_self = np.array(range(len(un_self)))
            ind_other = np.array(range(len(un_other)))
            while any(co_self):
                next_best_ranked_card_self = max(un_self[co_self == max(co_self)])
                next_best_ranked_card_other = max(un_other[co_other == max(co_other)])
                if next_best_ranked_card_self != next_best_ranked_card_other:
                    return next_best_ranked_card_self < next_best_ranked_card_other
                else:
                    remove_index_self = ind_self[un_self == next_best_ranked_card_self]
                    remove_index_other = ind_other[un_other == next_best_ranked_card_other]
                    co_self[remove_index_self] = 0
                    co_other[remove_index_other] = 0

            return False

    def __eq__(self, other):
        if not (self < other) and not (self > other):
            return True
        else:
            return False

    # Checks the poker hand with the highest value (points) and sets as the hand type
    def __hand_type(self, hand_type):
        self.best_cards = []
        values = []
        for i in self.cards:
            values.append(i.value)
        self.__duplicate_values(hand_type)
        self._straight = self.__check_straight()
        self._straight_flush = False
        self.__check_flush()
        if self._straight_flush:
            self.__best_cards(self._straight_cards)
            self.points = 9
            self.hand_type = hand_type.straight_flush
        elif self.points < 7 and (self._flush or self._straight):
            if self._flush:
                self.__best_cards(self.flush_cards)
                self.points = 6
                self.hand_type = hand_type.flush
            else:
                self.points = 5
                self.hand_type = hand_type.straight
                self.__best_cards(self._straight_cards)
        else:
            self.__best_cards(self._duplicate_values)

    # Takes the 5 best cards i.e. the best poker hand (category_cards) + rest highest values)
    # and sets it as the best cards
    def __best_cards(self, category_cards=None):
        other_cards = self.cards.copy()
        indices = []
        if category_cards:
            for i, elem in enumerate(other_cards):
                for j in category_cards:
                    # checks which cards of the poker hand is the same as the ones in the initial hand to remove them
                    if (j == elem) and (j.suit.value == elem.suit.value):
                        indices.append(i)
        self.other_cards = list(np.delete(other_cards, indices))
        self.other_cards.sort(reverse=True)
        category_cards.extend(self.other_cards)
        self.best_cards = category_cards[:5].copy()

    # checks if there's any duplicate values, i.e. multiple of a kind
    def __duplicate_values(self, hand_type):
        unique, counts = np.unique(self.cards, return_counts=True)
        self._duplicate_values = []
        if any(counts == 2) & any(counts == 3):
            self.points = 7
            self.hand_type = hand_type.full_house
            full_house = [max(unique[counts == 2]), max(unique[counts == 3])]
            self._duplicate_values = self.__cards_in_category(full_house)
        elif any(counts == 2):
            if len(counts[counts == 2]) > 1:
                two_pair = unique[counts == 2]
                self._duplicate_values = self.__cards_in_category(two_pair)
                self.points = 3
                self.hand_type = hand_type.two_pair
            else:
                pair = unique[counts == 2]
                self._duplicate_values = self.__cards_in_category(pair)
                self.points = 2
                self.hand_type = hand_type.one_pair
        elif any(counts == 3):
            three_of_a_kind = unique[counts == 3]
            self._duplicate_values = self.__cards_in_category(three_of_a_kind)
            self.points = 4
            self.hand_type = hand_type.three_of_a_kind
        elif any(counts == 4):
            four_of_a_kind = unique[counts == 4]
            self._duplicate_values = self.__cards_in_category(four_of_a_kind)
            self.points = 8
            self.hand_type = hand_type.four_of_a_kind
        else:
            self.points = 1
            self.hand_type = hand_type.high_card

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
        # Change the value of the ace from 14 to 1 if there's a 2
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
        for i in range(len(cards) - 1):
            if cards[i].value + 1 == cards[i + 1].value:
                self._straight_cards.append(cards[i + 1])
            else:
                # in case we have 5 (straight) in row but 6th is not
                if len(self._straight_cards) >= 5:
                    straight = True
                    break
                self._straight_cards = []
                self._straight_cards.append(cards[i])
        if len(self._straight_cards) >= 5:
            straight = True
        return straight

    # Used for __duplicate_values to get the list of the multiple value
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
        self.cards = self.cards[:-1]
        return new_card
