import random

class Board:
    def __init__(self):
        self.rows, self.cols = (6, 7)
        self.board = [[None for x in range(self.cols)] for y in range(self.rows)]
        self.players = []
        self.turn = 1
    
    def placePiece(self, c):
        # temporary check
        if 0 <= c <= 6:
            if self.turn == 1:
                # for col in range(len(self.board[0])):
                # for row in range(len(self.board)):
                # for col in range(len(self.board[0])):
                check = 1
                while self.board[len(self.board) - check][c] != None and check < len(self.board):
                    check += 1
                self.board[len(self.board)-check][c] = 1
                self.turn = 2
            else: 
                # for row in range(len(self.board)):
                check = 1
                while self.board[len(self.board) - check][c] != None and check < len(self.board):
                    check += 1
                self.board[len(self.board)-check][c] = 1
                self.turn = 1


    def generateRandomBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col] = random.choice([1, 2])

    def printBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print(self.board[row][col], end=" ")
            print()

    def initBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col] = None
    
    def checkWin(self):
        winFlag = (False, False)
        # counta = 0
        # countb = 0
        print(len(self.board), len(self.board[0]))
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # horizontal
                if col < self.cols - 3:
                    if (self.board[row][col], self.board[row][col+1], self.board[row][col+2], self.board[row][col+3]) == (1, 1, 1, 1):
                        winFlag = (True, False)
                        # counta += 1
                    if (self.board[row][col], self.board[row][col+1], self.board[row][col+2], self.board[row][col+3]) == (2, 2, 2, 2):
                        winFlag = (False, True)
                        # countb += 1
                # vertical
                if row < self.rows - 3:
                    if (self.board[row][col], self.board[row+1][col], self.board[row+2][col], self.board[row+3][col]) == (1, 1, 1, 1):
                        winFlag = (True, False)
                        # counta += 1
                    if (self.board[row][col], self.board[row+1][col], self.board[row+2][col], self.board[row+3][col]) == (2, 2, 2, 2):
                        winFlag = (False, True)
                        # countb += 1
                # diagonally down
                if col < self.cols - 3 and row < self.rows - 3:
                    if (self.board[row][col], self.board[row][col+1], self.board[row][col+2], self.board[row][col+3]) == (1, 1, 1, 1):
                        winFlag = (True, False)
                        # counta += 1
                    if (self.board[row][col], self.board[row][col+1], self.board[row][col+2], self.board[row][col+3]) == (2, 2, 2, 2):
                        winFlag = (False, True)
                        # countb += 1
                # diagonally up
                if col < self.cols - 3 and row < self.rows - 3:
                    if (self.board[row][col], self.board[row][col-1], self.board[row][col-2], self.board[row][col-3]) == (1, 1, 1, 1):
                        winFlag = (True, False)
                        # counta += 1
                    if (self.board[row][col], self.board[row][col-1], self.board[row][col-2], self.board[row][col-3]) == (2, 2, 2, 2):
                        winFlag = (False, True)
                        # countb += 1
        # print(counta, countb)
        return winFlag

b = Board()
b.initBoard()
# b.generateRandomBoard()
for i in random
b.placePiece(2)
b.printBoard()
print(b.checkWin())

# print(board)