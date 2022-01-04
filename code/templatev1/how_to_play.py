import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class HowTo(QWidget):
    def __init__(self):
        super(HowTo, self).__init__()
        self.setGeometry(350, 150, 400, 400)
        self.initHowTo()

    def initHowTo(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        scroll = QScrollArea(self)
        vbox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        titleFont = QFont("Helvetica", 22, QFont.Bold)
        contentFont = QFont("Helvetica", 14)

        titleText = QLabel("How to play 'GO'")
        titleText.setFont(titleFont)
        ruleOne = QLabel("1. Games start with an empty board.")
        ruleOne.setFont(contentFont)
        ruleTwo = QLabel("2. Black goes first.")
        ruleTwo.setFont(contentFont)
        ruleThree = QLabel("3. Stones are placed on the intersection of the squares on the board.")
        ruleThree.setFont(contentFont)
        ruleFour = QLabel("4. Players also have the ability to pass their turn.")
        ruleFour.setFont(contentFont)
        ruleFive = QLabel("5. Two successive passes by a player will bring the game to an end.")
        ruleFive.setFont(contentFont)
        ruleSix = QLabel("6. The player who occupies the most territory at the end of the game wins.")
        ruleSix.setFont(contentFont)

        scrollLayout.addWidget(titleText)
        scrollLayout.addWidget(ruleOne)
        scrollLayout.addWidget(ruleTwo)
        scrollLayout.addWidget(ruleThree)
        scrollLayout.addWidget(ruleFour)
        scrollLayout.addWidget(ruleFive)
        scrollLayout.addWidget(ruleSix)

        scroll.setWidget(scrollContent)
        self.show()
