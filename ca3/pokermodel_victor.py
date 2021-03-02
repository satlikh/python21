from PyQt5.QtCore import *
from cardlib import *
from abc import abstractmethod
import sys


class GameModel(QObject):
    button_clicked = pyqtSignal()
    data_changed = pyqtSignal()
    game_message = pyqtSignal((str,))

    def __init__(self):
        super().__init__()
        self.players = []
        self.player_turn = -1
        self.running = False
        self.turn = 0

    def add_player(self, player, starting_pot):
        self.players.append(PlayerModel(player, starting_pot))

    def start(self):
        add_player_signal = pyqtSignal()
        if self.running:
            self.game_message.emit("A game is already running!")
        adding_players = True
        self.running = True
        while adding_players:

            add_player_signal.emit(print('player added'))
        self.player_turn = 0

    def next_player(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)
        if self.player_turn == len(self.players) - 1:
            self.turn += 1
        self.data_changed.emit()

    def new_card(self):
        self.hand.add_card()
        self.data_changed.emit()

    #def new_round(self):
    #    if self.turn == 1:
    #        self.





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

    def set_active(self, active):
        self.active = active
        self.hand.flip()
        self.data_changed.emit()

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

# class BettingModel(QObject):
#     betting = pyqtSignal()
#
#     def __init__(self, player: PlayerModel):
#         super().__init__()
#         self.model = player


class ButtonModel(GameModel):
    buttons = pyqtSignal()
    error_message = pyqtSignal()

    def __init__(self, player: PlayerModel, current_bet):
        super().__init__()
        self.model = player
        self.current_bet = current_bet

    def fold_button(self):
        self.model.hand.clear()
        self.next_player()
        self.buttons.emit()

    def check_button(self):
        if self.model.bet < self.current_bet:
            self.error_message.emit("You can't check!")
        else:
            self.next_player()
        self.buttons.emit()

    def bet_button(self, bet):
        self.model.place_bet(bet)
        self.buttons.emit()

    def call_button(self):
        bet = self.current_bet - self.model.bet
        self.model.place_bet(bet)
        self.buttons.emit()

class TableCardsModel(HandModel):
    def __init__(self):
        HandModel.__init__(self)

    def __iter__(self):
        return iter(self.cards)

    def flipped(self):
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()


