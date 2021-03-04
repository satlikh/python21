from PyQt5.QtCore import *
from cardlib import *
from abc import abstractmethod

class PlayerModel(QObject):

    data_changed = pyqtSignal()
    error_message = pyqtSignal()

    def __init__(self, name, pot):
        super().__init__()
        self.name = name
        self.hand = HandModel()
        self.active = False
        self.hand.flip()
        self.bet = 0
        self.pot = pot
        self.active_in_round = False

    def __len__(self):
        return len([object])

    def __eq__(self, other):
        return self.name == other.name

    def set_active(self, active):
        self.active = active
        self.hand.flip()
        self.data_changed.emit()

    def set_active_in_round(self, active_in_round):
        self.active_in_round = active_in_round

    def set_pot(self, pot):
        self.pot = pot
        self.data_changed.emit()

    def place_bet(self, bet):
        if (self.model.bet + bet) < self.current_bet:
            self.error_message.emit("You have to bet more!")
        else:
            self.model.current_pot(bet)
            self.model.bet += bet
        self.data_changed.emit()

    def reset_bet(self, bet):
        self.bet = 0
        self.data_changed.emit()

    def current_pot(self, bet):
        if self.pot - bet < 0:
            self.error_message.emit("Bet too high!")
        else:
            self.pot -= bet
        self.data_changed.emit()

    def won_round(self, won_pot):
        self.pot += won_pot
        self.data_changed.emit()


class CardModel(QObject):
    """ Base class that described what is expected from the CardView widget """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


class HandModel(Hand, CardModel):
    def __init__(self, cards=None):
        Hand.__init__(self, cards)
        CardModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = True
        # self.player = player

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!

    def best_poker_hand(self, cards=None):
        poker_hand = super().best_poker_hand(cards)
        poker_hand.best_cards.reverse()
        self.poker_hand.model = HandModel(cards=poker_hand.best_cards)
        self.poker_hand.type = poker_hand.hand_type
        self.new_cards.emit()

    def clear(self):
        del self.cards[:]
        self.new_cards.emit()

p1 = PlayerModel('victor', 50)
p2 = PlayerModel('amanda', 50)
test = [p1, p2]
deck = StandardDeck()
p1.hand.add_card(deck.draw())
p1.hand.add_card(deck.draw())
p1.hand.add_card(deck.draw())

p2.hand.add_card(deck.draw())
p2.hand.add_card(deck.draw())
p2.hand.add_card(deck.draw())

