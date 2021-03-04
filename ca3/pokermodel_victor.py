from PyQt5.QtCore import *
from cardlib import *
from abc import abstractmethod
import sys


class GameModel(QObject):
    button_clicked = pyqtSignal()
    data_changed = pyqtSignal()
    game_message = pyqtSignal((str,))

    def __init__(self, players: list, starting_pot: int = 50):
        super().__init__()
        self.players = []
        self.player_turn = -1
        self.running = False
        self.betting_round = 0
        self.highest_bet = 0
        self.total_pot = 0
        self.active_players = []
        self.table_cards = TableCardsModel()
        self.deck = StandardDeck()
        self.deck.shuffle()
        # self.buttons = ButtonModel()

        for player in players:
            self.add_player(player, starting_pot)

    def __iter__(self):
        return iter(self.players)

    def add_player(self, player, starting_pot):
        self.players.append(PlayerModel(player, starting_pot))

    def start(self):
        if self.running:
            self.game_message.emit("A game is already running!")

        self.running = True
        self.new_hand()

    def set_active_player(self):
        del self.active_players[:]

        for player in self.players:
            if player.active_in_round:
                self.active_players.append(player)
        if len(self.active_players) == 1:
            self.check_winner()

    def set_all_players_active(self):
        del self.active_players[:]

        for player in self.players:
            player.set_active_in_round(True)
            self.active_players.append(player)

    def next_player(self):
        self.player_turn = (self.player_turn + 1) % len(self.active_players)
        self.active_players[self.player_turn-1].set_active(False)
        self.active_players[self.player_turn].set_active(True)
        betting_done = self.check_current_betting()
        if self.player_turn == 0 and betting_done:
            self.new_betting_round()
        # else:
        #    ButtonModel(self.active_players[self.player_turn], self.highest_bet)
        self.data_changed.emit()

    def check_current_betting(self):
        players_bet = []
        for player in self.active_players:
            if player.active_in_round:
                players_bet.append(player.bet)
        # check if all the bets are the same
        return len(players_bet) == players_bet.count(players_bet[0])

    def new_betting_round(self):
        self.betting_round += 1
        print(self.betting_round)
        self.set_active_player()
        if self.betting_round == 1:
            # burning a card
            self.deck.draw()
            self.table_cards.add_card(self.deck.draw())
            self.table_cards.add_card(self.deck.draw())
            self.table_cards.add_card(self.deck.draw())
        elif self.betting_round == 2:
            self.deck.draw()
            self.table_cards.add_card(self.deck.draw())
        elif self.betting_round == 3:
            self.deck.draw()
            self.table_cards.add_card(self.deck.draw())
        elif self.betting_round == 4:
            self.check_winner()
        # remove all players with active_in_round = False from active_players
        self.data_changed.emit()

    def check_winner(self):
        if len(self.active_players) == 1:
            self.active_players[0].won_round(self.total_pot)
        else:
            poker_hands = []
            for player in self.active_players:
                poker_hands.append(player.hand.best_poker_hand(self.table_cards.cards))
            index_best_poker_hand = poker_hands.index(max(poker_hands))
            self.active_players[index_best_poker_hand].won_round(self.total_pot)

        self.new_hand()

    def new_hand(self):
        self.deck = StandardDeck()  # create .new_deck in class
        self.deck.shuffle()
        for player in self.players:
            player.hand.clear()
        self.set_all_players_active()
        for _ in range(2):
            for player in self.active_players:
                player.hand.add_card(self.deck.draw())
                player.reset_bet()

        self.betting_round = 0
        self.total_pot = 0
        self.highest_bet = 0

        self.table_cards.clear()
        self.player_turn = 0
        self.active_players[self.player_turn].set_active(True)
        # self.buttons(self.active_players[self.player_turn], self.highest_bet)
        self.data_changed.emit()

##################################
# Buttons
##################################
    def fold_button(self):
        self.active_players[self.player_turn].hand.clear()
        self.active_players[self.player_turn].set_active_in_round(False)
        # self.active_player
        self.next_player()
        self.button_clicked.emit()

    def check_button(self):
        if self.active_players[self.player_turn].bet < self.highest_bet:
            self.error_message.emit("You can't check!")
        else:
            self.next_player()
        self.button_clicked.emit()

    def bet_button(self, bet):
        self.active_players[self.player_turn].place_bet(bet, self.highest_bet)
        self.next_player()
        self.button_clicked.emit()

    def call_button(self):
        bet = self.current_bet - self.model.bet
        self.active_players[self.player_turn].place_bet(bet, self.highest_bet)
        self.next_player()
        self.button_clicked.emit()

    def all_in_button(self):
        bet = self.player.pot
        self.active_players[self.player_turn].place_bet(bet, self.highest_bet)
        self.next_player()
        self.button_clicked.emit()



class PlayerModel(QObject):

    data_changed = pyqtSignal()
    error_message = pyqtSignal()

    def __init__(self, name, pot):
        super().__init__()
        self.name = name
        self.hand = HandModel()
        self.active = False
        # self.hand.flip()
        self.bet = 0
        self.pot = pot
        self.active_in_round = False
        self.poker_hand = PokerHandModel([AceCard(Suit.Spades), AceCard(Suit.Hearts)])

    def __len__(self):
        return len([object])

    def __eq__(self, other):
        return self.name == other.name

    def set_active(self, active):
        self.active = active
        if active:
            if self.hand.flipped():
                self.hand.flip()
        else:
            if self.hand.flipped():
                pass
            else:
                self.hand.flip()
        self.data_changed.emit()

    def set_active_in_round(self, active_in_round):
        self.active_in_round = active_in_round

    def set_pot(self, pot):
        self.pot = pot
        self.data_changed.emit()

    def place_bet(self, bet, current_bet):
        if (self.bet + bet) < current_bet:
            self.error_message.emit("You have to bet more!")
        else:
            self.current_pot(bet)
            self.bet += bet
        self.data_changed.emit()

    def reset_bet(self):
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
        # self.poker_hand = NumberedCard
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

    # def best_poker_hand(self, cards=None):
    #     self.poker_hand = super().best_poker_hand(cards)
    #     # print(self.poker_hand)
    #     self.poker_hand.best_cards.reverse()
    #     self.poker_hand.model = HandModel(cards=self.poker_hand.best_cards)  # for printing
    #     # self.poker_hand.type = poker_hand.hand_type
    #     self.new_cards.emit()

    def clear(self):
        del self.cards[:]
        self.new_cards.emit()


class PokerHandModel(Hand):
    # new_cards = pyqtSignal()

    def __init__(self, cards=None):
        Hand.__init__(self)
        # HandModel.__init__(self)
        poker_hand = super().best_poker_hand(cards)
        poker_hand.best_cards.reverse()
        self.model = HandModel(cards=poker_hand.best_cards)  # for printing
        self.type = poker_hand.hand_type
        # self.new_cards.emit()


# class BettingModel(QObject):
#     betting = pyqtSignal()
#
#     def __init__(self, player: PlayerModel):
#         super().__init__()
#         self.model = player

# class ButtonModel(QObject):
#     buttons = pyqtSignal()
#     error_message = pyqtSignal()
#
#     def __init__(self, player: PlayerModel, current_bet):
#         super().__init__()
#         self.player = player
#         self.current_bet = current_bet
#
#     def fold_button(self):
#         self.player.hand.clear()
#         self.player.set_active_in_round(False)
#         # self.active_player
#         self.next_player()
#         self.buttons.emit()
#
#     def check_button(self):
#         if self.player.bet < self.current_bet:
#             self.error_message.emit("You can't check!")
#         else:
#             self.next_player()
#         self.buttons.emit()
#
#     def bet_button(self, bet):
#         self.player.place_bet(bet)
#         self.next_player()
#         self.buttons.emit()
#
#     def call_button(self):
#         bet = self.current_bet - self.model.bet
#         self.player.place_bet(bet)
#         self.next_player()
#         self.buttons.emit()
#
#     def all_in_button(self):
#         bet = self.player.pot
#         self.self.player.place_bet(bet)
#         self.next_player()
#         self.buttons.emit()



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

#########
# testing
#########

p1 = PlayerModel('victor', 50)
p2 = PlayerModel('amanda', 50)
test = [p1, p2]
deck = StandardDeck()
p1.hand.add_card(deck.draw())
p1.hand.add_card(deck.draw())


p2.hand.add_card(deck.draw())
p2.hand.add_card(deck.draw())


tc = TableCardsModel()
tc.add_card(deck.draw())
tc.add_card(deck.draw())
tc.add_card(deck.draw())

p1.hand.best_poker_hand()
p2.hand.best_poker_hand()
