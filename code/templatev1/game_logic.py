# TODO - Implement winner detection

class GameLogic:
    print("Game Logic Object Created")

    # Logic for removal of a Black Piece
    def blackLogic(self):
        counter = 0
        # 2x2 space
        for x in range(2):
            for y in range(2):
                # Counts the number of opposing pieces surrounding it
                if self.boardArray[x][y] == 1:
                    counter += 1
                    print(counter)
                    if counter == 4:
                        self.showNotification("Piece Captured!")
                        # Remove piece if completely surrounded
                else:
                    break

    # Logic for removal of a Black Piece in a corner
    def blackCornerLogic(self):
        counter = 0
        # 1x1 space
        for x in range(1):
            for y in range(1):
                # Counts the number of opposing pieces surrounding it
                if self.boardArray[x][y] == 1:
                    counter += 1
                    print(counter)
                    if counter == 4:
                        self.showNotification("Piece Captured!")
                        # Remove piece if completely surrounded
                else:
                    break

    def whiteLogic(self):
        counter = 0
        for x in range(2):
            for y in range(2):
                # Counts the number of opposing pieces surrounding it
                if self.boardArray[x][y] == 2:
                    counter += 1
                    print(counter)
                    if counter == 2:
                        self.showNotification("Piece Captured!")
                        # Remove piece if completely surrounded
                else:
                    break

    def whiteCornerLogic(self):
        counter = 0
        for x in range(1):
            for y in range(1):
                # Counts the number of opposing pieces surrounding it
                if self.boardArray[x][y] == 2:
                    counter += 1
                    print(counter)
                    if counter == 2:
                        self.showNotification("Piece Captured!")
                        # Remove piece if completely surrounded
                else:
                    break
