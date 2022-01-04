from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QAction, QMessageBox
from PyQt5.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from how_to_play import HowTo


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

      # Adding main menu for help option
        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu("Help")

        # Adding help option to menu
        rules = QAction("Rules", self)
        rules.setShortcut("Ctrl+R")
        rules.triggered.connect(self.rulesMsg)
        helpMenu.addAction(rules)

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def getHowTo(self):
        return self.how_to_play

    def initUI(self):
        """initiates application UI"""
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.howToPlay = HowTo()

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        """centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def rulesMsg(self):
        message = QMessageBox()
        # simple rules taken from wikipedia
        message.setText("The Rules \n\nThe board is empty at the onset of the game (unless players agree to place a handicap) \n\n Black makes the first move, after which White and Black alternate \n\nA move consists of placing one stone of one's own color on an empty intersection on the board \n\nA player may pass their turn at any time. \n\nA stone or solidly connected group of stones of one color is captured and removed from the board when all the intersections directly adjacent to it are occupied by the enemy. (Capture of the enemy takes precedence over self-capture.) \n\nNo stone may be played so as to recreate a former board position. \n\nTwo consecutive passes end the game. \n\nA player's area consists of all the points the player has either occupied or surrounded. \n\nThe player with more area wins.")
        message.setIcon(QMessageBox.Question)
        message.setWindowTitle("Rules")
        message.exec()