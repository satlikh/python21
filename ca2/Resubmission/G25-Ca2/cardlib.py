from enum import Enum
from enum import IntEnum
import numpy as np
import random
from abc import ABC, abstractmethod
import abc


class Suit(Enum):
    """
    This is an enumerated class for four different playing card suits. Suits are not ranked and any given numbers
    are for sorting purposes only. Here, the unicode characters to symbolise the playing cards have been used.

    :param Spades: Representing spades.
    :type Spades: enum 'Suit'

    :param Hearts: Representing hearts.
    :type Hearts: enum 'Suit'

    :param Diamonds: Representing diamonds.
    :type Diamonds: enum 'Suit'

    :param Clubs: Representing clubs.
    :type Clubs: enum 'Suit'
    """
    Spades = '\U00002660'  # unicode character for representing playing card symbols
    Hearts = '\U00002665'
    Diamonds = '\U00002666'
    Clubs = '\U00002663'


class PlayingCard(metaclass=abc.ABCMeta):
    """
    Abstract class for playing cards for the deck.
    Ranked as NumberedCard: 2-10, JackCard: 11, QueenCard: 12, KingCard: 13 and AceCard: 14
    Suits are given as Suit.Spades, Suit.Hearts, Suit.Diamonds or Suit.Clubs according the Suit class.

    This abstract class enforces its child classes to overload two operators and one method:
    1. Operator <
    2. Operator ==
    3. Method get_value()
    """

    def __init__(self, suit: Suit):
        """
        Returns an object of the abstract class `PlayingCard`
        :param suit:
        """
        if isinstance(suit, Suit):
            self.suit = suit
        else:
            raise ValueError('The suit must be an instance of Suit class!')

    def __lt__(self, other):
        """
        Checks if the rank of the playing card is less than the rank of the other playing card.

        :param other: Other playing card.
        :type other: class PlayingCard

        :return: True if the rank of current playing card is less than the other one, otherwise it
        returns False.
        :rtype: Boolean
        """
        return self.get_value() < other.get_value()

    def __eq__(self, other):
        """
        Checks if the rank of the playing card is equal the rank of the other playing card.

        :param other: Other playing card.
        :type other: class PlayingCard

        :return: True if the rank of current playing card is equal the other one, otherwise it
        returns False.
        :rtype: Boolean
        """
        return self.get_value() == other.get_value()

    @abstractmethod
    def get_value(self):
        """
        Returns the value of a `PlayingCard` object which is an `int` in range [2,14].
        :return:
        """
        pass

    @abstractmethod
    def __str__(self):
        pass


class NumberedCard(PlayingCard):
    """
    This class is representing the numered cards in the Poker game. `NumberedCard` is a child of `PlayingCard`
    abstract class.
    """

    def __init__(self, value: int, suit: Suit):
        super().__init__(suit)
        """
        Returns a `NumberedCard` object.

        :param value: The value or the number on the playing card.
        :type value: int [2,10]

        :param suit: The suit type of the numbred card.
        :type suit: Suit

        :returns: A `NumberedCard` object.
        :rtype: NumberedCard
        """
        if value in range(2, 11) and isinstance(value, int):
            self.value = value
        else:
            raise ValueError(f'Oops, the value shall be an integer in range [2,10] for numbered cards! '
                             f'You entered {value}')

    def get_value(self):
        """
        Returns the value of a NumberedCard.

        :returns: value of a numbered card.
        :rtype: int
        """
        return self.value

    def __str__(self):
        """
        Returns the symbolic representation of a plying card using playing card unicode character.
        """
        return "{}{}".format(self.get_value(), self.suit.value)

    def __repr__(self):
        """
        Returns the name and value of the playing card.

        Note: This method is to generate an output for developers in codes.
        """
        return "[{}, {}]".format(self.get_value(), self.suit.name)


class JackCard(PlayingCard):
    """
    This class is representing the Jack cards in the Poker game. JackCard is a child of `PlayingCard`
    abstract class.
    """
    def __init__(self,  suit: Suit):
        super().__init__(suit)
        """
        Returns a `JackCard` object.

        :param suit: The suit type of the Jack card.
        :type suit: Suit

        :returns: A `JackCard` object.
        :rtype: JackCard
        """

        self.value = 11

    def get_value(self):
        """
        Returns the value of a JackCard.

        :returns: value of a Jack card which is 11 by default.
        :rtype: int
        """
        return self.value

    def __str__(self):
        """
        Returns the symbolic representation of a plying card using playing card unicode character.
        """
        return "{}{}".format('J', self.suit.value)

    def __repr__(self):
        """
        Returns the name and value of the playing card.

        Note: This method is to generate an output for developers in codes.
        """
        return "[{}, {}]".format('Jack', self.suit.name)


class QueenCard(PlayingCard):
    """
    This class is representing the Queen cards in the Poker game. QueenCard is a child of `PlayingCard`
    abstract class.
    """
    def __init__(self, suit: Suit):
        super().__init__(suit)
        """
        Returns a `QueenCard` object.

        :param suit: The suit type of the Queen card.
        :type suit: Suit

        :returns: A `QueenCard` object.
        :rtype: QueenCard
        """

        self.value = 12

    def get_value(self):
        """
        Returns the value of a QueenCard.

        :returns: value of a queen card which is 12 by default.
        :rtype: int
        """
        return self.value

    def __str__(self):
        """
        Returns the symbolic representation of a plying card using playing card unicode character.
        """
        return "{}{}".format('Q', self.suit.value)

    def __repr__(self):
        """
        Returns the name and value of the playing card.

        Note: This method is to generate an output for developers in codes.
        """
        return "[{}, {}]".format('Queen', self.suit.name)


class KingCard(PlayingCard):
    """
    This class is representing the King cards in the Poker game. KingCard is a child of `PlayingCard`
    abstract class.
    """
    def __init__(self, suit: Suit):
        super().__init__(suit)
        """
        Returns a `KingCard` object.

        :param suit: The suit type of the King card.
        :type suit: Suit

        :returns: A `KingCard` object.
        :rtype: KingCard
        """

        self.value = 13

    def get_value(self):
        """
        Returns the value of a KingCard.

        :returns: value of a king card which is 13 by default.
        :rtype: int
        """
        return self.value

    def __str__(self):
        """
        Returns the symbolic representation of a plying card using playing card unicode character.
        """
        return "{}{}".format('K', self.suit.value)

    def __repr__(self):
        """
        Returns the name and value of the playing card.

        Note: This method is to generate an output for developers in codes.
        """
        return "[{}, {}]".format('King', self.suit.name)


class AceCard(PlayingCard):
    """
    This class is representing the Ace cards in the Poker game. AceCard is a child of `PlayingCard`
    abstract class.
    """
    def __init__(self,  suit: Suit, first=False):
        super().__init__(suit)
        """
        Returns a `AceCard` object.

        :param suit: The suit type of the Ace card.
        :type suit: Suit

        :returns: A `AceCard` object.
        :rtype: AceCard
        """
        if first:
            self.value = 1
        else:
            self.value = 14

    def get_value(self):
        """
        Returns the value of a AceCard.

        :returns: value of a ace card which is 14 by default.
        :rtype: int
        """
        return self.value

    def __str__(self):
        """
        Returns the symbolic representation of a plying card using playing card unicode character.
        """
        return "{}{}".format('A', self.suit.value)

    def __repr__(self):
        """
        Returns the name and value of the playing card.

        Note: This method is to generate an output for developers in codes.
        """
        return "[{}, {}]".format('Ace', self.suit.name)


class Hand:
    """
    Sets a class of hand. The card attribute is a list of `PlayingCard` objects.
    """

    def __init__(self, cards=None):
        """
        Returns an object of the `Hand` class.

        :param cards: Set initial cards for pre-determined hand or create an empty hand.
        :type cards: list of PlayingCards

        :return: Empty Hand class or with initially set cards of class Hand
        :rtype: class Hand
        """
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    # add card to the hand with StandardDeck.draw()
    def add_card(self, new_card):
        """Adds the "new_card" to the hand.

        :param new_card: A `PlayingCard` object to be added to `Hand`.
        :type new_card: a `PlayingCard` object
        """
        self.cards.append(new_card)

    def sort(self):
        """ Sorts the cards by value and returns a sorted cards in a hand."""
        n = len(self.cards)
        if n > 0:
            for i in range(n-1):
                for j in range(0, n-i-1):
                    if self.cards[j+1] < self.cards[j]:
                        self.cards[j], self.cards[j+1] = self.cards[j+1], self.cards[j]
                    # For stable sorting:
                    if (self.cards[j] == self.cards[j+1]) and (self.cards[j+2].suit == self.cards[j].suit):
                        self.cards[j], self.cards[j + 1] = self.cards[j + 1], self.cards[j]

    def sort_cards(self):
        """ Sorts the cards by value"""
        self.cards = sorted(self.cards, key=lambda x: getattr(x, 'value'))

    def sort_cards_by_suit(self):
        """ Sorts the cards by both value and suit, (Clubs, Diamonds, Hearts and Spades)"""
        sorted_values = sorted(self.cards, key=lambda x: getattr(x, 'value'))
        sorting_suits = [[], [], [], []]
        for i in range(len(sorted_values)):
            sorting_suits[sorted_values[i].suit.value - 1].append(sorted_values[i])
        self.cards = [x for i in sorting_suits for x in i]
        self.cards = sorted(self.cards, key=lambda x: getattr(x, 'value'))

    def drop_cards(self, index=None):
        """
        Drops the cards presented by index.

        :param index: A list (or integer) of indices, with first position given as 0.
        :type index: list

        :return: Card(s) given by index
        :rtype: PlayinCard
        """
        try:
            if type(index) is int:
                index = [index]
            # index is given as 0 at the first position
            dropped_cards = []
            for i in index:
                dropped_cards.append(self.cards[i])
            self.cards = np.delete(self.cards, index)
            if len(dropped_cards) == 1:
                return dropped_cards[0]
            else:
                return dropped_cards
        except TypeError:
            print('No index was given')
        except IndexError:
            print(f'IndexError: Given index is "{index}" while number of cards is {len(self.cards)}')

    def show_hand(self):
        """ Presents the cards in the hand."""
        hand = []
        for i in range(len(self.cards)):
            hand.append([self.cards[i].value, self.cards[i].suit.name])
        print(hand)

    def best_poker_hand(self, cards=None):
        """ Calculates the best poker hand of the hand, and the added cards

        :param cards: List of playing cards in addition to the hand cards.
        :type cards: PlayinCard

        :return: PokerHand-class with best poker hand type and best cards.
        :rtype: Hand
        """
        if cards is None:
            cards = []
        poker_cards = self.cards.copy()
        if cards:
            if len(cards) > 1:
                poker_cards.extend(cards)
            else:
                poker_cards.append(cards)
        return PokerHand(poker_cards)


class PokerHandType(IntEnum):
    """ This is an enumerate class for the different poker hand type with their corresponding rank/value. Highest value
    i.e. STRAIGHT_FLUSH with value 9 is the best."""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class PokerHand:
    """
    Calculates the best poker hand of the given cards.

    Example:
    >>> h1 = Hand([NumberedCard(2,Suit.Hearts),
                   NumberedCard(2,Suit.Spades),
                   NumberedCard(5,Suit.Spades),
                   NumberedCard(5,Suit.Hearts),
                   NumberedCard(10,Suit.Clubs)])
    >>> ph1 = PokerHand(h1.cards)
    >>> ph1.hand_type
    <PokerHandType.TWO_PAIR: 3>
    """

    def __init__(self, cards):
        """
        Returns a `PokerHand` object.

        :param cards: List of playing cards
        :type cards: list

        :return: PokerHand class with the hand type of the best poker hand and the best cards.
        :rtype: PokerHand
        """
        self.cards = cards
        self.__hand_type()

    def __lt__(self, other):
        """
        Checks if the current poker hand is weaker than the other poker hand, including comparing the high-cards.

        :param other: Other poker hand.
        :type other: class PokerHand

        :return: True if the current poker hand is weaker than the other one, otherwise it
        returns False.
        :rtype: Boolean
        """
        if self.hand_type != other.hand_type:  # compares the rank of the poker hand type
            return self.hand_type < other.hand_type
        else:
            un_self, co_self = np.unique(self.best_cards, return_counts=True)
            un_other, co_other = np.unique(other.best_cards, return_counts=True)
            ind_self = np.array(range(len(un_self)))
            ind_other = np.array(range(len(un_other)))
            while any(co_self):
                # compares the value between highest ranking cards, e.g. triplets then pair for full house
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
        """
        Checks if the current poker hand is equal the other poker hand.

        :param other: Other poker hand.
        :type other: class PokerHand

        :return: True if the current poker hand is equal the other one, otherwise it
        returns False.
        :rtype: Boolean
        """
        if not (self < other) and not (self > other):
            return True
        else:
            return False

    # Checks the poker hand with the highest value (points) and sets as the hand type
    def __hand_type(self):
        """
        Determines the hand type of the poker hand. The hand type would be one of the following types:
        0-'high_card'
        1-'one_pair''
        2-'two_pair'
        3-'three_of_a_kind'
        4-'straight'
        5-'flush'
        6-'full_house'
        7-'four_of_a_kind'
        8-'straight_flush'

        """
        self.best_cards = []
        values = []
        for i in self.cards:
            values.append(i.value)
        self.__duplicate_values()
        self._straight = self.__check_straight()
        self._straight_flush = False
        self.__check_flush()
        if self._straight_flush:
            self.__best_cards(self._straight_cards)
            self.points = 9
            self.hand_type = PokerHandType(9)
        elif self.points < 7 and (self._flush or self._straight):

            if self._flush:
                self.__best_cards(self.flush_cards)
                self.points = 6
                self.hand_type = PokerHandType(6)
            else:
                self.points = 5
                self.hand_type = PokerHandType(5)
                self.__best_cards(self._straight_cards)
        else:
            self.__best_cards(self._duplicate_values)

    # Takes the 5 best cards i.e. the best poker hand (category_cards) + rest highest values)
    # and sets it as the best cards
    def __best_cards(self, category_cards=None):
        """
        Takes the 5 best cards between the poker hand type cards and the other cards. These other cards would be
        used for comparison with other poker hands.
        :param category_cards: Card list with the cards of the poker hand type, e.g. the cards of a pair,
        four of a kind etc.
        """
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

    def __duplicate_values(self):
        """
        Checks if there's any duplicate values, i.e. multiple of a kind.
        """
        unique, counts = np.unique(self.cards, return_counts=True)
        self._duplicate_values = []
        if any(counts == 4):
            four_of_a_kind = unique[counts == 4]
            self._duplicate_values = self.__cards_in_category(four_of_a_kind)
            self.points = 8
            self.hand_type = PokerHandType(8)
        elif any(counts == 2) & any(counts == 3):
            self.points = 7
            self.hand_type = PokerHandType(7)
            full_house = [max(unique[counts == 2]), max(unique[counts == 3])]
            self._duplicate_values = self.__cards_in_category(full_house)
        elif any(counts == 3):
            three_of_a_kind = unique[counts == 3]
            self._duplicate_values = self.__cards_in_category(three_of_a_kind)
            self.points = 4
            self.hand_type = PokerHandType(4)
        elif any(counts == 2):
            if len(counts[counts == 2]) > 1:
                two_pair = unique[counts == 2][-2:]
                self._duplicate_values = self.__cards_in_category(two_pair)
                self.points = 3
                self.hand_type = PokerHandType(3)
            else:
                pair = unique[counts == 2]
                self._duplicate_values = self.__cards_in_category(pair)
                self.points = 2
                self.hand_type = PokerHandType(2)
        else:
            self.points = 1
            self.hand_type = PokerHandType(1)

    def __check_flush(self, suit_cards=None):
        """
        Checks if the poker hand is a flush.
        """
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

    # straight_cards is to check if a given card series is straight. Used for flush to see if straight flush
    def __check_straight(self, straight_cards=None):
        """
        Checks if the poker hand is a straight.
        :param straight_cards: A list of cards which are to be determined if they are straight or not,
        used in __check_flush to check straight flush.
        """
        if not straight_cards:
            straight_cards = self.cards.copy()
        cards = []
        # Change the value of the ace from 14 to 1 if there's a 2 for low straight
        if (AceCard(Suit.Spades) in straight_cards) and (NumberedCard(2, Suit.Spades) in straight_cards):
            suit_of_acecard = straight_cards[straight_cards.index(AceCard(Suit.Spades))].suit
            cards.append(AceCard(suit_of_acecard, first=True))
            straight_cards.sort()
            if KingCard(Suit.Spades) not in straight_cards:
                del (straight_cards[-1])  # removes AceCard with value 14
        cards.extend(straight_cards)
        # cards.sort()
        cards = list(np.unique(cards))
        self._straight_cards = []
        self._straight_cards.append(cards[0])
        straight = False
        for i in range(1, len(cards)):
            if cards[i-1].value + 1 == cards[i].value:
                self._straight_cards.append(cards[i])
            else:
                if len(self._straight_cards) >= 5:  # in case we have 5 (straight) in row but 6th is not
                    straight = True
                    break
                self._straight_cards.clear()  # restart our check for straight
                self._straight_cards.append(cards[i])
        if len(self._straight_cards) >= 5:
            self._straight_cards = self._straight_cards[-5:]  # takes the five highest of the straight cards
            straight = True
        return straight

    def __cards_in_category(self, category_card):
        """
        Used for __duplicate_values to get the list of the multiple value
        """
        cards_list = []
        for j in range(len(category_card)):
            for i in self.cards:
                if i == category_card[j]:
                    cards_list.append(i)
        return cards_list

    def __str__(self):
        return "Poker Hand {} with {}".format(self.best_cards, self.hand_type.name)

    def __repr__(self):
        return "Poker Hand {} with {}".format(self.best_cards, self.hand_type)


class StandardDeck:
    """
    Creates a standard deck of 52 playing cards.
    """

    def __init__(self):
        """
        Returns an object of `StandardDeck` class of 52 playing cards.

        :return: Main class StandardDeck. StandardDeck.cards is a list of 52 playing cards in value order Ace-King
        and suit-order: Spades, Hearts, Diamonds, Clubs
        :rtype: StandardDeck
        """
        self.cards = []
        self.new_deck()

    def new_deck(self):
        """
        Creates a new list of 52 playing cards in StandardDeck.cards
        """
        self.cards.clear()
        for suit in Suit:
            for i in range(2, 15):
                if i == 11:
                    self.cards.append(JackCard(suit))
                elif i == 12:
                    self.cards.append(QueenCard(suit))
                elif i == 13:
                    self.cards.append(KingCard(suit))
                elif i == 14:
                    self.cards.append(AceCard(suit))
                else:
                    self.cards.append(NumberedCard(i, suit))

    def shuffle(self):
        """
        Reorders the list of cards into a random order.
        """
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    def draw(self):
        """
        Draws (removes) the top (last) card from the card-list

        :returns: A playing card.
        :rtype: PlayingCard
        """
        new_card = self.cards[-1]
        self.cards = self.cards[:-1]
        return new_card
