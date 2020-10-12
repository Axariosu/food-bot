import random

class Board:
    def __init__(self):
        self.rows, self.cols = (6, 7)
        self.board = [[None for x in range(self.cols)] for y in range(self.rows)]
        self.turn = 1
        self.gameEnd = False
        self.player1 = None
        self.player2 = None
        self.timer = 0
    
    def placePiece(self, c, p):
        # temporary check
        if 0 <= c <= 6 and not self.gameEnd:
            if self.turn == 1 and self.player1 == p:
                # for col in range(len(self.board[0])):
                # for row in range(len(self.board)):
                # for col in range(len(self.board[0])):
                check = 0
                while self.board[len(self.board) - 1 - check][c] != None and check < len(self.board):
                    check += 1
                if check == len(self.board):
                    return False
                else:
                    self.board[len(self.board) - 1 - check][c] = 1
                    self.turn = 2
                    return True
            if self.turn == 2 and self.player2 == p: 
                # for row in range(len(self.board)):
                check = 0
                while self.board[len(self.board) - 1 - check][c] != None and check < len(self.board):
                    check += 1
                if check > len(self.board) - 1:
                    return False
                else: 
                    self.board[len(self.board) - 1 - check][c] = 2
                    self.turn = 1
                    return True

    def generateRandomBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col] = random.choice([1, 2])

    def getBoard(self):
        res = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == None:
                    res += '⚫'
                if self.board[row][col] == 1:
                    res += '🔴' 
                if self.board[row][col] == 2:
                    res += '🟡'
                # res += str(self.board[row][col])
            res += "\n"
        res += '1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣'
        return res

    def initBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col] = None
    
    def checkWin(self):
        winFlag = (False, False)
        # counta = 0
        # countb = 0
        # print(len(self.board), len(self.board[0]))
        # [
        # [@ @ @ @ @ @ @]
        # [@ @ @ @ @ @ @]
        # [@ @ @ @ @ @ @]
        # [@ @ @ @ @ @ @]
        # [@ @ @ @ @ @ @]
        # [@ @ @ @ @ @ @]
        #               ]
        for row in range(len(self.board)): # 0-5
            for col in range(len(self.board[row])): # 0-6
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
                if row < self.rows - 3 and col < self.cols - 3:
                    if (self.board[row][col], self.board[row+1][col+1], self.board[row+2][col+2], self.board[row+3][col+3]) == (1, 1, 1, 1):
                        winFlag = (True, False)
                        # counta += 1
                    if (self.board[row][col], self.board[row+1][col+1], self.board[row+2][col+2], self.board[row+3][col+3]) == (2, 2, 2, 2):
                        winFlag = (False, True)
                        # countb += 1
                # diagonally up
                if row >= 3 and col < self.cols - 3:
                    if (self.board[row][col], self.board[row-1][col+1], self.board[row-2][col+2], self.board[row-3][col+3]) == (1, 1, 1, 1):
                        winFlag = (True, False)
                        # counta += 1
                    if (self.board[row][col], self.board[row-1][col+1], self.board[row-2][col+2], self.board[row-3][col+3]) == (2, 2, 2, 2):
                        winFlag = (False, True)
                        # countb += 1
        # print(counta, countb)
        if winFlag != (False, False):
            self.gameEnd = True
        return winFlag



# def sampleWin():
#     b = Board()
#     b.initBoard()
#     # b.generateRandomBoard()
#     b.placePiece(2)
#     b.placePiece(2)
#     b.placePiece(1)
#     b.placePiece(2)
#     b.placePiece(3)
#     b.placePiece(2)
#     b.placePiece(4)
#     b.printBoard()
#     print(b.checkWin())

# a()

# print(board)