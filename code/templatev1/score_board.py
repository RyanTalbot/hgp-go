from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ScoreBoard(QDockWidget):
    """base the score_board on a QDockWidget"""

    def __init__(self):
        super().__init__()
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

        # create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        # More labels to show different information to the user throughout the game
        self.label_playersTurn = QLabel("Black Goes First >")
        self.label_PrisonersTakenBlack = QLabel("Prisoners Taken by Black: ")
        self.label_PrisonersTakenWhite = QLabel("Prisoners Taken by White: ")

        # Button for passing a turn
        self.btn_skipTurn.clicked.connect(self.skipPlayerTurn())

        # Add new labels to docked widget
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_playersTurn)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_PrisonersTakenBlack)
        self.mainLayout.addWidget(self.label_PrisonersTakenWhite)
        self.mainLayout.addWidget(self.btn_skipTurn)
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

    # This will be updated when game logic is added to show who's piece went last
    # Needs to be connected to board with signal
    def updatePlayerTurn(self, Piece):
        if Piece == 1:
            self.label_playersTurn.setText("White's Turn To Move")
        elif Piece == 2:
            self.label_playersTurn.setText("Black's Turn To Move")

    # Allows player to skip their turn
    def skipPlayerTurn(self, playerTurn):
        if playerTurn == Piece.Black:
            self.label_playersTurn.setText("Black has skipped, White's Turn To Move")
        elif playerTurn == Piece.White:
            self.label_playersTurn.setText("White has skipped, Black's Turn To Move")