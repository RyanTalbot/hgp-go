import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    changePlayerTurnSignal = pyqtSignal(int)  # signal sent when swap player is updated.

    boardWidth = 6  # board is 6 squares wide
    boardHeight = 6  # board is 6 squares tall
    timerSpeed = 1000  # the timer updates ever 1 second
    counter = 300  # the number the counter will count down from 300
    playerTurn = Piece.Black  # starting player is always black

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        """initiates board"""
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        # use INT type for now in array
        # TODO - create a 2d int/Piece array to store the state of the game
        self.boardArray = [[0 for i in range(7)] for j in range(7)]
        self.printBoardArray()

    def printBoardArray(self):
        """prints the boardArray in an attractive way"""
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        """convert the mouse click event to a row and column"""
        # Save the x,y position of each click
        x_pos = event.x()
        y_pos = event.y()

        x_coord = round(x_pos / self.squareWidth() - 1)
        y_coord = round(y_pos / self.squareHeight() - 1)

        print(x_coord, y_coord)

        # Adding a check system to ensure no invalid moves
        if self.boardArray[y_coord][x_coord] == 0:
            self.boardArray[y_coord][x_coord] = self.playerTurn
            self.changePlayerTurn()
        else:
            self.showNotification("Invalid Move!")
            
        self.printBoardArray()
        self.update()

    def squareWidth(self):
        """returns the width of one square in the board"""
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        """returns the height of one square of the board"""
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        """starts game"""
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        """this event is automatically called when the timer is updated. based on the timerSpeed variable """
        # TODO adapter this code to handle your timers

        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter == 0:
                self.showNotification("Time's Up, Game Over!")
                # update when game logic is finished top show winner
                # if black wins print  self.show_notification("Black WINS")
                # if white wins print  self.show_notification("White WINS")
                self.timer.stop()
                self.close()
                self.resetGame()
            else:
                self.counter -= 1
            # print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling other wise pass it to the super class for handling

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        clickLoc = "click location [" + str(event.x()) + "," + str(
            event.y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)
        self.mousePosToColRow(event)

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game
        self.boardArray = [[0 for i in range(7)] for j in range(7)]
        # set game pieces back to zero in game logic

    def tryMove(self, newX, newY):
        """tries to move a piece"""

    # WORKED NEEDED
    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor.fromRgb(217, 179, 255))  # test color
        painter.setBrush(brush)

        for row in range(0, Board.boardHeight):

            if brush.color() == (QColor.fromRgb(217, 179, 255)):  # to ensure alternate colors on new rows
                brush.setColor(QColor.fromRgb(0, 153, 153))
            else:
                brush.setColor(QColor.fromRgb(217, 179, 255))

            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(row, col, self.squareWidth(), self.squareHeight(), brush)
                painter.restore()

                if brush.color() == (QColor.fromRgb(217, 179, 255)):  # to ensure alternate colors on new columns
                    brush.setColor(QColor.fromRgb(0, 153, 153))
                else:
                    brush.setColor(QColor.fromRgb(217, 179, 255))

    # WORK NEEDED
    def drawPieces(self, painter):
        """draw the prices on the board"""
        color = Qt.transparent  # empty square could be modeled with transparent pieces
        for row in range(-1, len(self.boardArray)):

            for col in range(-1, len(self.boardArray)):

                painter.save()
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() / 2,
                                  (self.squareHeight()) * col + self.squareHeight() / 2)

                # currently based on the array using INT variables
                # will change to game pieces next

                if self.boardArray[col][row] == 0:
                    color = QColor(Qt.transparent)
                elif self.boardArray[col][row] == 1:
                    color = QColor(Qt.white)
                elif self.boardArray[col][row] == 2:
                    color = QColor(Qt.black)

                painter.setPen(color)
                painter.setBrush(color)

                radius = (self.squareWidth() - 2) / 2
                radius2 = (self.squareHeight() - 2) / 2

                center = QPoint(radius, radius2)
                painter.drawEllipse(center, radius - 15, radius2 - 15)
                painter.restore()

    def showNotification(self, message):
        QMessageBox.about(self, "!", message)

    # Can be moved to game logic if needed
    def changePlayerTurn(self):
        # function to swap turns
        self.counter = 300  # reset timer every turn
        print(" -- Next Players Turn -- ")
        if self.playerTurn == Piece.Black:
            self.playerTurn = Piece.White
        else:
            self.playerTurn = Piece.Black

        self.changePlayerTurnSignal.emit(self.playerTurn)  # signal sent to display Current PLayer Turn message
