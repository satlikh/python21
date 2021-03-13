from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from pokermodel import *


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
    for suit_file, suit in zip('SHDC', Suit):
        for value_file, value in zip(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
                                     range(1, 15)):
            file = value_file + suit_file
            key = (value, suit)
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: CardModel, label_model=None, card_spacing: int = 50, padding: int = 10,
                 font_size: int = 50):
        """
        Initializes the view to display the content of the given model
        :param card_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param label_model: The model to set the corresponding label over the cards by label_model.name.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding
        self.font_size = font_size
        self.label = label_model

        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        card_model.new_cards.connect(self.change_cards)
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
            self.scene.addItem(c)
        # Adding text over the cards: player name, poker hand type or table cards
        font = QGraphicsTextItem(self.label.name.replace('_', ' '))  # Used for PokerHand name
        font_style = QFont('Courier', self.font_size)
        font_style.setBold(True)
        font.setFont(font_style)
        font.setDefaultTextColor(QColor(229, 0, 25))
        font.setPos(self.font_size/2, 0)
        self.scene.addItem(font)
        self.scene.setSceneRect(300, 300, 300, 250)
        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-(self.padding + self.font_size))/313
        self.resetTransform()
        self.scale(scale, scale)
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        self.update_view()
        super().resizeEvent(painter)


class PlayerView(QWidget):
    """ A View widget that represents players view, with their cards and their pot and bet. """
    def __init__(self, player_model: PlayerModel):
        super().__init__()
        self.model = player_model
        self.card_view = CardView(self.model.hand, label_model=self.model)
        self._chips_and_betting = PlayerBettingBox(self.model, self.card_view)
        self.card_view.setStyleSheet("margin: 0px; padding: 0px; \
                                   border-style: solid; border-width: 10px; \
                                   border-color: rgba(200,200,200,255);")

        self.card_view.setMaximumHeight(300)

        # layout = QHBoxLayout()
        # layout.addWidget(self._chips_and_betting)
        # self.setLayout(layout)

        def alert_winner(text: str):
            msg = QMessageBox()
            msg.setWindowTitle("Yippiiii!")
            msg.setText(text)
            msg.exec()

        def alert_error(text: str):
            msg = QMessageBox()
            msg.setWindowTitle("Hey!")
            msg.setIcon(QMessageBox.Information)
            msg.setText(text)
            msg.exec()

        self.model.error_message.connect(alert_error)
        self.model.winner_message.connect(alert_winner)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)


class ButtonGrp(QFrame):
    """ A widget that represents buttons in the game.
    :param game: Game model."""
    def __init__(self, game: GameModel):
        super().__init__()
        self.game = game

        def bet_button_func():
            if self.bet_line.text().isdigit():
                bet = int(self.bet_line.text())
                self.bet_line.clear()
                self.game.bet_button(bet)
            else:
                self.bet_line.clear()
                msg = QMessageBox()
                msg.setText('There was no bet!')
                msg.exec()

        self.setLayout(QVBoxLayout())
        self.bet_line = QLineEdit()
        self.bet_line.setPlaceholderText('Enter bet')
        self.bet_line.resize(100, 5)
        bet_button = QPushButton('Bet')
        bet_button.clicked.connect(bet_button_func)
        self.layout().addWidget(self.bet_line)
        self.layout().addWidget(bet_button)

        call_button = QPushButton('Call')
        call_button.clicked.connect(self.game.call_button)
        self.layout().addWidget(call_button)

        fold_button = QPushButton('Fold')
        fold_button.clicked.connect(self.game.fold_button)
        self.layout().addWidget(fold_button)

        check_button = QPushButton('Check')
        check_button.clicked.connect(self.game.check_button)
        self.layout().addWidget(check_button)

        all_in_button = QPushButton('All in!')
        all_in_button.clicked.connect(self.game.all_in_button)
        self.layout().addWidget(all_in_button)

        self.setMaximumWidth(150)


class PossiblePokerHand(QWidget):
    """ A widget to display the current poker hand for the player who's turn it is.
        :param game: Game model."""
    def __init__(self, game: GameModel):
        super().__init__()
        self.game = game
        self.poker_view = CardView(self.game.current_poker_hand, label_model=self.game.current_poker_hand, font_size=50)
        layout = QHBoxLayout()
        layout.addWidget(self.poker_view)
        self.setLayout(layout)
        self.setStyleSheet("margin: 0px; padding: 0px; \
                                   border-style: solid; border-width: 10px; \
                                   border-color: rgba(200,200,200,255);")#\
                                   #border-color: rgba(170,170,170,255);\
        self.setMaximumHeight(300)
        self.setFixedWidth(250)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        self.setFixedWidth(self.height()*1.1)


class TableCardsView(QWidget):
    """ A widget presenting the common cards on the table."""
    def __init__(self, table_cards_model: TableCardsModel):
        super().__init__()
        self.model = table_cards_model
        self.model.flip()
        self.view_poker_cards = CardView(self.model, label_model=self.model, card_spacing=250)
        # view_poker_cards.setLayout(QHBoxLayout())
        # view_poker_cards.layout().addWidget(view_poker_cards)
        layout = QHBoxLayout()
        layout.addWidget(self.view_poker_cards)
        self.setLayout(layout)
        # self.layout().addWidget(view_poker_cards)
        # self.setLayout(layout)
        self.setStyleSheet("border:none")
        # print(view_poker_cards.width())
        self.setMinimumWidth(self.view_poker_cards.width())
        self.setMaximumHeight(300)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        # self.setFixedWidth(self.width())


class PlayerBettingBox(QGraphicsView):
    """ A view that is added to the PlayerView which represents the pot and bet for the players. The view is added to
    the CardView for the player.
    :param player: Model of the current player
    :param card_scene: CardView from the current player.
    """
    def __init__(self, player, card_scene: CardView):
        super().__init__()
        self.setScene(card_scene.scene)
        scene = self.scene()

        def update_layout():
            box_position = QRectF(290, 30, 150, 160)
            font_style = QFont('Courier', 20)
            font_style.setBold(True)

            font_chips = QGraphicsTextItem(f'#Chips:  \n   {player.pot}')
            font_chips.setFont(font_style)
            font_chips.setPos(box_position.x(), box_position.y() + 20)
            font_bet = QGraphicsTextItem(f'Your bet: \n   {player.bet}')
            font_bet.setFont(font_style)
            font_bet.setPos(box_position.x(), box_position.y() + 90)
            scene.addRect(box_position, QColor(0, 0, 0)).setBrush(QColor(255, 255, 229))
            scene.addItem(font_chips)
            scene.addItem(font_bet)

        player.data_changed.connect(update_layout)
        update_layout()


class TableBettingBox(QWidget):
    """ A widget that displays the current total pot of the round along with the current highest bet."""
    def __init__(self, game: GameModel):
        super().__init__()
        self.game = game
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 10, 10)
        self.setLayout(layout)
        self.setStyleSheet("margin: 0px; padding: 0px; \
        background-color: \
                           rgba(255, 255, 229, 255); \
                           color: rgba(0,0,0,255); \
                           border-style: solid; \
                           border-radius: 4px; border-width: 1px; \
                           border-color: rgba(0,0,0,255);")

        font_style = QFont('Courier', 10)
        font_style.setBold(True)
        self.font_chips = QLabel()
        self.font_chips.setFont(font_style)
        self.font_bet = QLabel()
        self.font_bet.setFont(font_style)

        self.layout().addWidget(self.font_chips)
        self.layout().addWidget(self.font_bet)
        game.data_changed.connect(self.update_layout)
        self.update_layout()

    def update_layout(self):
        self.font_chips.setText(f'Total pot:  \n   {self.game.total_pot}')
        self.font_bet.setText(f'Highest bet: \n   {self.game.highest_bet}')



class GameView(QMainWindow):
    """ A View widget for the entire game on which the other widgets are added."""
    def __init__(self, game_model: GameModel):
        super().__init__()
        self.view = QGraphicsView()
        # scene = QGraphicsScene()
        # image = QPixmap('cards/table.png')
        # scene.setBackgroundBrush(QBrush(image))
        # self.view.setStyleSheet("""background-image: url(cards/table.png);""")
        self.view.setScene(TableScene())
        self.setWindowTitle("A game of Texas Hold'em poker")
        # self.view.setAutoFillBackground(True)
        # self.setCentralWidget(self.view)
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()


        #self.view = QGraphicsView()
        # self.grid.setStyleSheet("background-image: url(cards/table.png);")
        # widget.setWindowTitle("A game of Texas Hold'em poker")
        # self.setCentralWidget(self.view)
        # self.scene = QGraphicsScene()
        # self.view.setScene(self.scene)

        self.game = game_model
        game_model.start()

        # grid = QGridLayout()
        # self.view.setLayout(grid)

        ############
        # Set up player cards
        ############
        # players_card_view = QGraphicsView()
        # players_card_view.setLayout(QHBoxLayout())
        pcview = QHBoxLayout()
        for player in game_model.players:
            player_view = PlayerView(player)
            # players_card_view.layout().addWidget(player_view.card_view)
            pcview.addWidget(player_view.card_view)

        # players_card_layout = QGraphicsProxyWidget()
        # players_card_layout.setWidget(players_card_view)
        # players_card_layout.setGeometry(QRectF(0, 0, 330 * len(game_model.players), 300))

        ############
        # Set up table cards
        ############
        table_cards_layout = TableCardsView(game_model.table_cards)
        top_layout.addWidget(table_cards_layout)

        ############
        # Set up poker cards
        ############
        ph_layout = PossiblePokerHand(game_model)
        # poker_view = CardView(self.game.current_poker_hand, label_model=self.game.current_poker_hand, font_size=50)
        # main_layout.addWidget(poker_view)
        top_layout.addWidget(ph_layout)
        #poker_hand_layout = QGraphicsProxyWidget()
        #poker_hand_layout.setWidget(ph_layout.poker_view)
        #poker_hand_layout.setGeometry(QRectF(0, 0, 260, 250))

        ############
        # Set up player buttons
        ############
        button_widget = ButtonGrp(game_model)
        # button_widget.setStyleSheet("border:0")
        top_layout.addWidget(button_widget)
        # self.layout().addWidget(button_widget)
        # button_layout = QGraphicsProxyWidget()
        # button_layout.setWidget(button_widget)
        # button_layout.setGeometry(QRectF())

        #############
        # Set up table betting and pot
        #############
        table_bet_and_pot_widget = TableBettingBox(self.game)
        top_layout.addWidget(table_bet_and_pot_widget)
        # self.layout().addWidget(table_bet_and_pot_widget)
        # table_bet_and_pot_layout = QGraphicsProxyWidget()
        # table_bet_and_pot_layout.setWidget(table_bet_and_pot_widget)
        # table_bet_and_pot_layout.setGeometry(QRectF(0, 0, 100, 50))

        main_layout.addLayout(top_layout)
        main_layout.addLayout(pcview)
        self.view.setLayout(main_layout)
        self.setCentralWidget(self.view)

        ##########
        # Set each position and add all layouts
        ##########
        # table_cards_layout.setPos(0, 0)
        # players_card_layout.setPos(0, 250)
        # button_layout.setPos(1010, 0)
        # poker_hand_layout.setPos(750, 0)
        # table_bet_and_pot_layout.setPos(1130, 0)
        # main_layout.addLayout(top_layput)
        # self.layout().addWidget(top_layput)
        # main_layout.addLayout(players_card_view)
        # self.layout.addLayout(top_layput)
        # self.layout().addLayout(players_card_view)
        # self.setLayout(main_layout)


        # self.scene.addItem(table_cards_layout)
        # self.scene.addItem(players_card_layout)
        # self.scene.addItem(button_layout)
        # self.scene.addItem(poker_hand_layout)
        # self.scene.addItem(table_bet_and_pot_layout)

        #grid.addWidget(table_bet_and_pot_widget)


        # Center the game window on the screen
        # screen_center = QDesktopWidget().availableGeometry().center()
        # self.setMinimumSize(self.scene.width() + 10, self.scene.height() + 10)
        self.setMinimumSize(1200, 500)
        # window_geometry = self.frameGeometry()
        # window_geometry.moveCenter(screen_center)

        game_model.error_message.connect(self.alert_player)
        game_model.end_game.connect(self.end_game)

    def alert_player(self, text: str):
        msg = QMessageBox()
        msg.setWindowTitle("Hey!")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec()

    def end_game(self, text: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Game over!")
        msg.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)

        return_value = msg.exec()
        if return_value == QMessageBox.Reset:
            self.game.restart_game()
        else:
            self.close()
