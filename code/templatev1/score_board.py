from PyQt5.QtWidgets import QAction, QDockWidget, QFrame, QGridLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, \
    QWidget
from PyQt5.QtCore import *
from board import Board
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from functools import partial


class ScoreBoard(QDockWidget):
    """base the score_board on a QDockWidget"""

    def __init__(self):
        super().__init__()
        self.board = Board(self)
        self.initUI()

    def initUI(self):
        """initiates ScoreBoard UI"""
        self.resize(200, 200)
        self.setFixedWidth(200)
        self.center()
        self.setWindowTitle('ScoreBoard')

        # test color for docked widget
        color = QColor(QColor.fromRgb(230, 255, 230))
        self.setStyleSheet("QWidget { background-color: %s }" % color.name())

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Button options for Start/Reset/Skip
        self.btn_startGame = QPushButton("Start")
        self.btn_startGame.setFixedWidth(185)
        self.btn_startGame.setFixedHeight(50)
        self.btn_startGame.setStyleSheet("QPushButton { background-color: rgb(255,255,255) }")
        self.btn_startGame.setFont(QFont("Helvetica", 14))
        self.btn_startGame.clicked.connect(partial(self.click_btn, self.btn_startGame))

        self.btn_resetGame = QPushButton("Reset")
        self.btn_resetGame.setFixedWidth(185)
        self.btn_resetGame.setFixedHeight(50)
        self.btn_resetGame.setStyleSheet("QPushButton { background-color: rgb(255,255,255) }")
        self.btn_resetGame.setFont(QFont("Helvetica", 14))
        self.btn_resetGame.clicked.connect(partial(self.click_btn,self.btn_resetGame))

        self.btn_skipTurn = QPushButton("Skip Turn")
        self.btn_skipTurn.setFixedWidth(185)
        self.btn_skipTurn.setFixedHeight(50)
        self.btn_skipTurn.setStyleSheet("QPushButton { background-color: rgb(255,255,255) }")
        self.btn_skipTurn.setFont(QFont("Helvetica", 14))
        # self.btn_skipTurn.clicked.connect(self.on_click)

        # create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        # More labels to show different information to the user throughout the game
        self.label_playersTurn = QLabel("Black Goes First >")
        self.label_PrisonersTakenBlack = QLabel("Prisoners Taken by Black: ")
        self.label_PrisonersTakenWhite = QLabel("Prisoners Taken by White: ")

        # Add new labels to docked widget
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.btn_startGame)
        self.mainLayout.addWidget(self.label_playersTurn)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.btn_skipTurn)
        self.mainLayout.addWidget(self.label_PrisonersTakenBlack)
        self.mainLayout.addWidget(self.label_PrisonersTakenWhite)
        self.mainLayout.addWidget(self.btn_resetGame)
        self.setWidget(self.mainWidget)
        self.show()

    def center(self):
        """centers the window on the screen, you do not need to implement this method"""

    def make_connection(self, board):
        """this handles a signal sent from the board class"""
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.changePlayerTurnSignal.connect(self.updatePlayerTurn)
        # board.skipPlayerTurnSignal.connect(self.skipPlayerTurn)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        """updates the label to show the click location"""
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        """updates the time remaining label to show the time remaining"""
        update = "Time Remaining:" + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + update)
        # self.redraw()

    def updatePlayerTurn(self, Piece):
        if Piece == 1:
            self.label_playersTurn.setText("White's Turn To Move")
        elif Piece == 2:
            self.label_playersTurn.setText("Black's Turn To Move")

    # Allows player to skip their turn
    # Doesn't work
    def skipPlayerTurn(self, Piece):
        if Piece == 1:
            self.label_playersTurn.setText("Black has skipped, White's Turn To Move")
            self.board.playerTurn = Piece.White
        elif Piece == 2:
            self.label_playersTurn.setText("White has skipped, Black's Turn To Move")
            self.board.playerTurn = Piece.Black

    # Method for resetting the game
    def click_btn(self, btn):
        if btn == self.btn_resetGame:
            # Giving the user an option to ensure it wasn't clicked by mistake
            option = QMessageBox.question(
                self, 'Reset Game', 'Resetting The Game Means You Will Lose All Current Progress!',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if option == QMessageBox.Yes:
                print("GAME RESET")
            else:
                pass
