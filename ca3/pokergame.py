import sys
from PyQt5.QtCore import *
from pokermodel_victor import *
from pokerview_victor import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

players = ["Victor", "Mohammad", "Thomas"]  # more can be added
model = GameModel(players)
view = GameView(model)
view.show()

app.exec_()
