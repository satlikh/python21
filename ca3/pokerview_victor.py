from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from pokermodel_victor import *
from abc import abstractmethod


# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.view = QGraphicsView()
#         self.view.setStyleSheet("background-image: url(cards/table.png);")
#         self.setCentralWidget(self.view)
#         self.scene = QGraphicsScene()
#         self.view.setScene(self.scene)


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit_file, suit in zip('SHDC', Suit):  # Check the order of the suits here!!!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: CardModel, label, card_spacing: int = 50, padding: int = 10, font_size: int = 50,
                 card_scale: int = 1):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding
        self.font_size = font_size
        self.label = label

        self.model = card_model
        self.card_scale = card_scale
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        card_model.new_cards.connect(self.change_cards)
        # It is completely optional if you want to do it this way, or have some overreaching Player/GameState
        # call the "change_cards" method instead. z

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, self.font_size/2 + self.padding)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)
        font = QGraphicsTextItem(self.label)
        font_style = QFont('Courier', self.font_size)
        font_style.setBold(True)
        font.setFont(font_style)
        font.setDefaultTextColor(QColor(229, 0, 25))
        font.setPos(self.font_size/2, 0)
        self.scene.addItem(font)
        #self.scene.setSceneRect(300, 300, 300, 250)
        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-(2*self.padding + self.font_size))/(313*self.card_scale)
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


class PlayerView(QGraphicsView):
    def __init__(self, player_model: PlayerModel):
        super().__init__()
        self.model = player_model
        #self.scene = QGraphicsScene()
        self.card_view = CardView(self.model.hand, label=f'{self.model.name}')

        self._chips_and_betting = BettingBox(self.model, self.card_view)




#def view_table_cards(cards: PlayingCard):


class ButtonGrp(QGroupBox):
    # def __init__(self, button_model: ButtonModel):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # game.button_clicked.connect(self.update_view)
        player = game.active_players[game.player_turn]
        current_bet = game.highest_bet
        def bet_button_func():
            self.game.bet_button(5)
        self.setLayout(QVBoxLayout())
        bet_button = QPushButton('Bet')
        bet_button.clicked.connect(bet_button_func)
        ###### add a dialogbox or something here ofr betting!
        call_button = QPushButton('Call')
        call_button.clicked.connect(self.game.call_button)
        self.layout().addWidget(bet_button)
        self.layout().addWidget(call_button)
        self.setLayout(QVBoxLayout())
        fold_button = QPushButton('Fold')
        fold_button.clicked.connect(self.game.fold_button)
        check_button = QPushButton('Check')
        check_button.clicked.connect(self.game.check_button)
        self.layout().addWidget(fold_button)
        self.layout().addWidget(check_button)

        all_in_button = QPushButton('All in!')
        all_in_button.clicked.connect(self.game.all_in_button)
        self.layout().addWidget(all_in_button)
        # self.vbox.setGeometry(QRect(0,0,150,50))
        # self.setLayout(vbox)

class PossiblePokerHand(QWidget):
    def __init__(self, game: GameModel):
        super().__init__()
        self.game = game
        self.poker_view = None
        #game.poker_hand_changed.connect(self.update)

        self.update()

    def update(self):
        poker_hand = self.game.active_players[self.game.player_turn].poker_hand
        # poker_hand.best_cards.reverse()
        # card_list = HandModel(cards=poker_hand.best_cards)
        # # card_list.player = poker_hand.hand_type.name
        # self.poker_view = CardView(card_list, label=f'Current best: {poker_hand.hand_type.name}',
        #                            font_size=50)
        # # print(self.width())
        # # self.setGeometry(0, 0, 150, 50)
        # # print(self.width())
        # print(self.game.active_players[self.game.player_turn].p)
        if poker_hand.type:
            self.poker_view = CardView(poker_hand.model, label=f'Current best: {poker_hand.type.name}', font_size=50)
        else:
            self.poker_view = CardView(poker_hand.model, label='Current best: ', font_size=50)



    # poker_hand.new_cards.connect(self.update)



class TableCardsView(QGraphicsProxyWidget):
    def __init__(self, table_cards_model: TableCardsModel):
        super().__init__()
        self.model = table_cards_model
        # self.model.new_cards.connect()
        self.model.flip()
        # print(self.model.flipped())
        view_poker_cards = CardView(self.model, label='Poker Cards', card_spacing=250)
        view_poker_cards.setLayout(QHBoxLayout())
        view_poker_cards.layout().addWidget(view_poker_cards)
        self.setWidget(view_poker_cards)
        self.setGeometry(QRectF(0, 0, 1000, 250))

class BettingBox(QGraphicsView):
    def __init__(self, player, card_scene: CardView):
        super().__init__()
        self.setScene(card_scene.scene)
        scene = self.scene()

        # self.setFrameRect(QRect(0,0,30,30))
        #self.scene.addRect(0, 0, 30, 50, QColor(229, 0, 25))
        # self.scene.setBackgroundBrush(QColor(229, 0, 25))
        # QColor(255, 255, 229)
        #'background-color: white;'))
        def update_layout():
            print(player.name)
            box_position = QRectF(290, 30, 150, 160)
            font_style = QFont('Courier', 20)
            font_style.setBold(True)

            font_chips = QGraphicsTextItem(f'#Chips:  \n   {player.pot}')
            font_chips.setFont(font_style)
            font_chips.setPos(box_position.x(), box_position.y() + 20)
            font_bet = QGraphicsTextItem(f'Your bet: \n   {player.bet}')
            font_bet.setFont(font_style)
            font_bet.setPos(box_position.x(), box_position.y() + 90)
            # font_bet.setDefaultTextColor(QColor(229, 0, 25))
            scene.addRect(box_position, QColor(0, 0, 0)).setBrush(QColor(255, 255, 229))
            scene.addItem(font_chips)
            scene.addItem(font_bet)

        player.data_changed.connect(update_layout)
        update_layout()


#         player.data_changed.connect(self.update_betting_box())
#     def update_betting_box(self):

        # ButtonModel.buttons.connect()
        # self.scene.setGeometry(0, 0, 200, 200)

        # label_chips = QLabel(f'#Chips: {number_of_chips}')
        # label_bet = QLabel(f'Your bet: {current_betting}')
        # self.scene.add(QVBoxLayout())
        # self.scene.layout.addWidget(label_chips)
        # self.scene.layout.addWidget(label_bet)
        # self.scene.setGeometry(QRect(0, 0, 30, 50))

class GameView(QMainWindow):
        def __init__(self, game_model: GameModel):
            super().__init__()
            # set Window
            self.view = QGraphicsView()
            self.view.setStyleSheet("background-image: url(cards/table.png);")
            self.setCentralWidget(self.view)
            self.scene = QGraphicsScene()
            self.view.setScene(self.scene)
            self.game = game_model
            game_model.start()
            #self.game.start()
            ############
            # table cards
            ############
            # poker_table_cards = TableCardsModel()
            table_cards_layout = TableCardsView(game_model.table_cards)
            #table_cards_layout = TableCardsView(self.game.table_cards)

            ############
            # player cards
            ############

            number_of_players = len(game_model.players)
            players_card_view = QGraphicsView()
            players_card_view.setLayout(QHBoxLayout())
            for player in game_model.players:
                player_view = PlayerView(player)
                players_card_view.layout().addWidget(player_view.card_view)

            players_card_layout = QGraphicsProxyWidget()
            players_card_layout.setWidget(players_card_view)
            players_card_layout.setGeometry(QRectF(0, 0, 330 * number_of_players, 300))

            ############
            # player buttons
            ############
            # player_buttons = ButtonModel()

            button_widget = ButtonGrp(game_model)
            pA = QGraphicsProxyWidget()
            pA.setWidget(button_widget)

            ############
            # poker cards
            ############
            # print(game_model.active_players)
            # print(game_model.player_turn)
            ph_layout = PossiblePokerHand(game_model)
            poker_hand_view = QGraphicsView()
            poker_hand_view.setLayout(QHBoxLayout())
            poker_hand_view.layout().addWidget(ph_layout.poker_view)
            poker_hand_layout = QGraphicsProxyWidget()
            poker_hand_layout.setWidget(poker_hand_view)
            poker_hand_layout.setGeometry(QRectF(0, 0, 250, 250))

        ##########
        # add all layouts
        ##########
            table_cards_layout.setPos(0, 0)
            players_card_layout.setPos(0, 250)
            pA.setPos(1000, 0)
            poker_hand_layout.setPos(750, 0)

            self.scene.addItem(table_cards_layout)
            self.scene.addItem(players_card_layout)
            self.scene.addItem(pA)
            self.scene.addItem(poker_hand_layout)

#########################################
# Remove what's after this later as well?
#########################################


# Lets test it out

# window = Window()
# #table_view = QVBoxLayout()
#
# ############
# # table cards
# ############
# card_list = [NumberedCard(3, Suit.Spades), NumberedCard(5, Suit.Hearts), NumberedCard(6, Suit.Clubs)
#                , NumberedCard(10, Suit.Spades), NumberedCard(8, Suit.Diamonds)]
# poker_table_cards = TableCardsModel()
#
# #for i in card_list:
# #    print(i)
# #    poker_table_cards.add_card(i)
# table_cards_layout = TableCardsView(poker_table_cards)
#
#
# # table_view.addLayout(vbox, 0, 1)
# # table_view.addWidget(view_poker_cards)
# ############
# # player cards
# ############
#
# hand = HandModel()
# hand.add_card(AceCard(Suit.Spades))
# hand.add_card(KingCard(Suit.Spades))
# # hand.flip()
#
# hand1 = HandModel()
# hand1.add_card(AceCard(Suit.Hearts))
# hand1.add_card(KingCard(Suit.Hearts))
#
# hand2 = HandModel()
# hand2.add_card(AceCard(Suit.Clubs))
# hand2.add_card(KingCard(Suit.Clubs))
# hand_list = [hand, hand1, hand2]
#
# betting_list = [10, 5, 4]
# chips_list = [20, 30, 99]
#
# number_of_players = 3
# players_card_view = QGraphicsView()
# players_card_view.setLayout(QHBoxLayout())
# for i in range(3):
#     player_view = PlayerView(hand_list[i], chips_list[i], betting_list[i])
#     players_card_view.layout().addWidget(player_view.card_view)
#
# players_card_layout = QGraphicsProxyWidget()
# players_card_layout.setWidget(players_card_view)
# players_card_layout.setGeometry(QRectF(0, 0, 330*number_of_players, 300))
#
# ############
# # player buttons
# ############
# player_buttons = ButtonModel()
# button_widget = ButtonGrp(player_buttons)
# pA = QGraphicsProxyWidget()
# pA.setWidget(button_widget)
#
# ############
# # poker cards
# ############
# #phbox = QHBoxLayout()
# ph = hand.best_poker_hand(poker_table_cards.cards)
# ph_layout = PossiblePokerHand(ph)
# poker_hand_view = QGraphicsView()
# poker_hand_view.setLayout(QHBoxLayout())
# poker_hand_view.layout().addWidget(ph_layout.poker_view)
# poker_hand_layout = QGraphicsProxyWidget()
# poker_hand_layout.setWidget(poker_hand_view)
# poker_hand_layout.setGeometry(QRectF(0, 0, 250, 250))
#
#
# ##########
# # add all layouts
# ##########
# table_cards_layout.setPos(0, 0)
# players_card_layout.setPos(0, 250)
# pA.setPos(1000, 0)
# poker_hand_layout.setPos(750, 0)
#
# window.scene.addItem(table_cards_layout)
# window.scene.addItem(players_card_layout)
# window.scene.addItem(pA)
# window.scene.addItem(poker_hand_layout)
# window.show()

