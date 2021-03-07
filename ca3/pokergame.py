import sys
from pokerview import *
from pokermodel import *
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

players = ["Victor", "Mohammad", "Thomas", "Mikael"]  # more can be added
model = GameModel(players)
view = GameView(model)
view.show()

app.exec_()
