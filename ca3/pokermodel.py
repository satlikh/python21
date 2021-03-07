from PyQt5.QtCore import *
from cardlib import *
from abc import abstractmethod
import numpy as np


class GameModel(QObject):
    """ GameModel for a poker game in Texas Hold'em.
    :param players: A list with the name of the different players.
    :param starting_pot: An integer with the starting pot for the players, it's 50 if nothing is set.
    """
    button_clicked = pyqtSignal()
    data_changed = pyqtSignal()
    error_message = pyqtSignal((str,))
    end_game = pyqtSignal((str,))

    def __init__(self, players: list, starting_pot: int = 50):
        super().__init__()
        self.players_list = players
        self.starting_pot = starting_pot
        self.players = []
        self.player_turn = -1
        self.running = False
        self.betting_round = 0
        self.highest_bet = 0
        self.total_pot = 0
        self.zero_pot_players = []
        self.number_of_folded_players = 0

        self.active_players = []
        self.table_cards = TableCardsModel()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.current_poker_hand = PokerHandModel()

        for player in self.players_list:
            self.add_player(player)

    def __iter__(self):
        return iter(self.players)

    def start(self):
        if self.running:
            self.error_message.emit("A game is already running!")

        self.running = True
        self.new_hand()

    def add_player(self, player):
        self.players.append(PlayerModel(player, self))

    def remove_zero_pot_players(self):
        for i, player in enumerate(self.players):
            if player.pot == 0 and player.active_in_game:
                player.set_active_in_game(False)
                player.set_active(False)
                player.set_active_in_round(False)
                self.zero_pot_players.append(i)
        if len(self.players) == len(self.zero_pot_players) + 1:
            index = int(np.delete(range(len(self.players)), self.zero_pot_players))
            self.end_game.emit(f'{self.players[index]} won the game!')

    def set_active_player(self):
        """ Removes players which have folded during the round. """
        del self.active_players[:]
        self.number_of_folded_players = 0

        for player in self.players:
            if player.active_in_round:
                self.active_players.append(player)
        if len(self.active_players) == 1:
            self.check_winner()
        else:
            self.active_players[self.player_turn].set_active(True)

    def set_all_players_active(self):
        """ Add all the players still in the game to the round. """
        del self.active_players[:]

        for player in self.players:
            if player.active_in_game:
                player.set_active_in_round(True)
                self.active_players.append(player)

    def next_player(self):
        self.player_turn = (self.player_turn + 1) % len(self.active_players)

        # When everyone has had a turn we remove those who has folded.
        if self.player_turn == 0:
            self.set_active_player()

        self.active_players[self.player_turn-1].set_active(False)

        betting_done = self.check_current_betting()
        if self.player_turn == 0 and betting_done:
            self.new_betting_round()

        self.active_players[self.player_turn].set_active(True)
        self.data_changed.emit()

        # Skip players that can't bet
        if self.active_players[self.player_turn].pot == 0:
            self.next_player()

    def check_current_betting(self):
        """
        Checks if all the bets are the equal
        :return: bool
        """
        players_bet = []
        for player in self.active_players:
            if player.active_in_round:
                players_bet.append(player.bet)
        return len(players_bet) == players_bet.count(players_bet[0])

    def new_betting_round(self):
        """ Adds card(s) to the poker table and increases the betting round until four round are reached. """

        self.betting_round += 1
        if self.betting_round == 1:
            self.deck.draw()  # burned card
            self.table_cards.add_card(self.deck.draw())
            self.table_cards.add_card(self.deck.draw())
            self.table_cards.add_card(self.deck.draw())
        elif self.betting_round == 2:
            self.deck.draw()  # burned card
            self.table_cards.add_card(self.deck.draw())
        elif self.betting_round == 3:
            self.deck.draw()  # burned card
            self.table_cards.add_card(self.deck.draw())
        elif self.betting_round == 4:
            self.check_winner()
        elif self.betting_round > 4:
            self.error_message.emit('Something went wrong with the betting round! We must start a new round.')
            self.new_hand()

        self.data_changed.emit()

    def check_winner(self):
        """ Concludes the winner in the current round are adds the pot to the winner.
        If it's a tie, the pot is evenly divided between the winners. A new round is then conducted
         """
        if len(self.active_players) == 1:
            print(self.player_turn)
            self.active_players[0].won_round(self.total_pot)
        else:
            poker_hands = []
            for player in self.active_players:
                player.set_active(True)  # We have a showdown and player presents their cards
                poker_hands.append(player.hand.best_poker_hand(self.table_cards.cards))
            best_hand = max(poker_hands)
            winner_indices = [i for i, x in enumerate(poker_hands) if x == best_hand]
            number_of_winners = len(winner_indices)
            winner = 0
            for index in winner_indices:
                winner += 1
                self.active_players[index].won_round(round(self.total_pot/number_of_winners), winner=winner)

        self.new_hand()

    def new_hand(self):
        """ Starts a new round. The players without any money are removed and a new deck is used.
        The first player in the game always starts.
        """
        self.deck.new_deck()
        self.deck.shuffle()

        self.remove_zero_pot_players()

        for player in self.players:
            player.hand.clear()
            player.set_active(False)  # hides all the cards
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
        self.data_changed.emit()

    def restart_game(self):
        for player in self.players:
            player.reset_player()
        self.zero_pot_players.clear()
        self.running = False
        self.start()

    ##################################
    # Buttons
    ##################################

    def fold_button(self):
        self.active_players[self.player_turn].hand.clear()
        self.active_players[self.player_turn].set_active_in_round(False)

        self.number_of_folded_players += 1
        # If all the players but one have folded, we set the active players in the middle of the round.
        if self.number_of_folded_players == len(self.active_players) - 1:
            self.set_active_player()
        else:
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
        self.button_clicked.emit()

    def call_button(self):
        if self.highest_bet:
            bet = self.highest_bet - self.active_players[self.player_turn].bet
            self.active_players[self.player_turn].place_bet(bet, self.highest_bet)
        self.button_clicked.emit()

    def all_in_button(self):
        bet = self.active_players[self.player_turn].pot
        self.active_players[self.player_turn].place_bet(bet, self.highest_bet)
        self.button_clicked.emit()


class PlayerModel(QObject):
    """ The model for each players.
    :param name: String with the name of the player.
    :param game: The GameModel
    """

    data_changed = pyqtSignal()
    error_message = pyqtSignal((str,))
    winner_message = pyqtSignal((str,))

    def __init__(self, name: str, game: GameModel):
        super().__init__()
        self.name = name
        self.hand = HandModel()
        self.active = False
        self.active_in_game = True
        # self.hand.flip()
        self.bet = 0
        self.pot = game.starting_pot
        self.active_in_round = False
        self.game = game

    def __len__(self):
        return len([object])

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return "{}".format(self.name)

    def set_active(self, active):
        """ Sets the player active by showing the cards and updates the current poker hand."""
        self.active = active
        if active:
            if self.hand.flipped():
                self.hand.flip()
            self.game.current_poker_hand.update_model(self, self.game.table_cards.cards)
        else:
            if self.hand.flipped():
                pass
            else:
                self.hand.flip()
        self.data_changed.emit()

    def set_active_in_round(self, active_in_round):
        self.active_in_round = active_in_round
        self.data_changed.emit()

    def set_active_in_game(self, active_in_game):
        """ Set if the player can do anything in the game. It's set to false when the player has lost the game."""
        if active_in_game:
            self.active_in_game = active_in_game
        else:
            self.active_in_game = False
            self.set_pot(0)
            self.reset_bet()
            self.error_message.emit(f'{self.name} is no longer in the game!')

    def set_pot(self, pot):
        self.pot = pot
        self.data_changed.emit()

    def place_bet(self, bet, current_bet):
        if (self.bet + bet) < current_bet:
            self.error_message.emit("You have to bet more!")
        else:
            ok_bet = self.current_pot(bet)
            if ok_bet:
                self.game.highest_bet = self.bet
                self.game.total_pot += bet
                self.game.next_player()

    def reset_bet(self):
        self.bet = 0
        self.data_changed.emit()

    def reset_player(self):
        self.pot = self.game.starting_pot
        self.set_active_in_game(True)
        self.reset_bet()

    def current_pot(self, bet):
        """ Changes the pot of the player.
        :returns: bool if the attempted bet was possible or not.
        """
        if self.pot - bet < 0:
            self.error_message.emit("Bet too high!")
            return False
        else:
            self.bet += bet
            self.pot -= bet
            return True

    def won_round(self, won_pot, winner=1):

        self.set_active(True)
        if winner == 1:
            self.winner_message.emit(f"Yeah! {self.name} won!")
        else:
            self.winner_message.emit(f"Yeah! {self.name} also won!")
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

    def clear(self):
        # Removes the cards from the hand
        self.cards.clear()
        self.new_cards.emit()


class PokerHandModel(HandModel):
    """ The model is used to display the possible poker hand to the current player."""
    poker_hand_changed = pyqtSignal()

    def __init__(self, cards=[]):
        super().__init__()
        self.cards = cards
        self.hand_type = None
        self.name = 'None'

    def update_model(self, player: PlayerModel, table_cards):
        poker_hand = player.hand.best_poker_hand(table_cards)
        self.cards = poker_hand.best_cards
        self.cards.reverse()
        self.hand_type = poker_hand.hand_type
        self.name = poker_hand.hand_type.name
        if self.flipped():
            self.flip()
        self.new_cards.emit()
        self.poker_hand_changed.emit()


class TableCardsModel(HandModel):
    """ Model to display the cards on the table. """
    def __init__(self):
        HandModel.__init__(self)
        self.name = 'Table cards'

    def __iter__(self):
        return iter(self.cards)

    def flipped(self):
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()
