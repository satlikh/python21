from PyQt5.QtCore import *
from cardlib import *
from abc import abstractmethod
import sys


# class GameModel(QObject):
#     button_clicked = pyqtSignal()
#     data_changed = pyqtSignal()
#     game_message = pyqtSignal((str,))
#
#     def __init__(self, players):
#         super().__init__()
#         self.players = players
#         self.player_turn = -1
#         self.running = False
#         self.turn = 0
#
#     def start(self):
#         if self.running:
#             self.game_message.emit("A game is already running!")
#
#         self.running = True
#         self.player_turn = 0
#
#     def next_player(self):
#         self.player_turn = (self.player_turn + 1) % len(self.players)
#         self.players[self.player_turn].set_active(True)
#         if self.player_turn == len(self.players) - 1:
#             self.turn += 1
#         self.data_changed.emit()
#
#     def new_card(self):
#         self.hand.add_card()
#         self.data_changed.emit()
#
#     #def new_round(self):
#     #    if self.turn == 1:
#     #        self.
#
#
#
#
#
# class PlayerModel(QObject):
#
#     data_changed = pyqtSignal()
#
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#         self.hand = HandModel()
#         self.active = False
#         self.hand.flip()
#
#     def set_active(self, active):
#         self.active = active
#         self.hand.flip()
#         self.data_changed.emit()

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
        return super().best_poker_hand(cards)


class TableCardsModel(HandModel):
    def __init__(self):
        HandModel.__init__(self)

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()


class ButtonModel(QObject):
    buttons = pyqtSignal()

    def __init__(self):
        super().__init__()

    def fold_button(self):

        self.buttons.emit()

    def check_button(self):
        self.buttons.emit()

    def bet_button(self):
        self.buttons.emit()

    def call_button(self):
        self.buttons.emit()
