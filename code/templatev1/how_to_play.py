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

        titleFont = QFont("Helvetica", 18, QFont.Bold)
        contentFont = QFont("Helvetica", 10)

        label1 = QLabel("How to play 'GO'")
        label1.setFont(titleFont)

        scroll.setWidget(scrollContent)
        self.show()
