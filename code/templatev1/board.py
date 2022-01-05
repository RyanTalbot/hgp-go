import math

from PyQt5.QtWidgets import QFrame, QMessageBox
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QRectF
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    changePlayerTurnSignal = pyqtSignal(int)  # signal sent when swap player is updated.
    #skipPlayerTurnSignal = pyqtSignal()  # signal sent when player skips turn

    boardWidth = 7  # board is 6 squares wide
    boardHeight = 7  # board is 6 squares tall
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

        x_coord = int(x_pos / self.squareWidth())       # change to int for more accurate picks
        y_coord = int(y_pos / self.squareHeight())

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
        self.clickLocationSignal.emit(clickLoc)
        self.mousePosToColRow(event)

    def resetGame(self):
        """clears pieces from the board"""
        # resetting the 2d array
        self.boardArray = [[0 for i in range(7)] for j in range(7)]
        # using drawPieces method to change all pieces transparent
        painter = QPainter(self)
        self.drawPieces(painter)

    def tryMove(self, newX, newY):
        """tries to move a piece"""

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor.fromRgb(217, 179, 255))  # test color
        painter.setBrush(brush)

        for row in range(0, Board.boardHeight - 1):
            if brush.color() == (QColor.fromRgb(217, 179, 255)):  # to ensure alternate colors on new columns
                brush.setColor(QColor.fromRgb(0, 153, 153))
            else:
                brush.setColor(QColor.fromRgb(217, 179, 255))

            for col in range(0, Board.boardWidth-1):
                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(55, 55, self.squareWidth(), self.squareHeight(), brush)
                painter.restore()

                if brush.color() == (QColor.fromRgb(217, 179, 255)):  # to ensure alternate colors on new rows
                    brush.setColor(QColor.fromRgb(0, 153, 153))
                else:
                    brush.setColor(QColor.fromRgb(217, 179, 255))

    def drawPieces(self, painter):
        """draw the prices on the board"""
        for row in range(0, len(self.boardArray)):

            for col in range(0, len(self.boardArray[0])):

                if self.boardArray[row][col] == 1:
                    painter.setPen(QPen(Qt.transparent, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

                elif self.boardArray[row][col] == 2:
                    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                else:
                    painter.setPen(QPen(Qt.transparent, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))

                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)

                radius = (self.squareWidth() * 0.55) / 2
                center = QPoint(55, 55)
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    # Checks to see if the board is filled
#     def boardFilled(self):
#         for row in self.boardArray:
#             for i in row:
#                 if i == 0:
#                     return False
#         return True

    def showNotification(self, message):
        QMessageBox.about(self, "!", message)

    def changePlayerTurn(self):
        # function to swap turns
        self.counter = 300  # reset timer every turn

        print(" -- Next Players Turn -- ")
        if self.playerTurn == Piece.Black:
            self.playerTurn = Piece.White
        else:
            self.playerTurn = Piece.Black

        self.changePlayerTurnSignal.emit(self.playerTurn)  # signal sent to display Current PLayer Turn message
