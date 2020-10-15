import random
import copy
import sys 

sys.setrecursionlimit(10**7) 

# https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0


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
        if self.gameEnd:
            return False
        if 0 <= c <= 6:
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

    def generateBoardFromString(self, inp):
        for col in inp:
            if self.turn == 1:
                self.placePiece(int(col), self.player1)
            else:
                self.placePiece(int(col), self.player2)

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
    
    def getBoardText(self):
        res = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == None:
                    res += '~'
                if self.board[row][col] == 1:
                    res += '1' 
                if self.board[row][col] == 2:
                    res += '2'
                res += " "
                # res += str(self.board[row][col])
            res += "\n"
        res += '0 1 2 3 4 5 6'
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

    # def compute_utility(self, board, move, turn):
    #     tempBoard = self.board.copy()

def get_possible_next_boards(boardObject):
    columnList = []
    board = copy.copy(boardObject)

    count = 0
    for col in range(len(board.board[0])):
        while board.board[len(board.board) - 1 - count][col] != None and count < len(board.board[0]): 
            count += 1
        if count == len(board.board[0]):
            columnList.append(False)
        else:
            columnList.append(True)
        count = 0
    res = []
    
    for i in range(len(columnList)):
        board = copy.deepcopy(boardObject)
        if columnList[i]:
            if board.turn == 1:
                board.placePiece(i, board.player1)
            elif board.turn == 2: 
                board.placePiece(i, board.player2)
            res.append(board)
    # returns a list of next possible board states given the player's turn
    return res

def get_possible_next_moves(boardObject):
    columnList = []
    board = copy.copy(boardObject)

    count = 0
    for col in range(len(board.board[0])):
        while board.board[len(board.board) - 1 - count][col] != None and count < len(board.board[0]): 
            count += 1
        if count < len(board.board[0]):
            columnList.append(col)
        count = 0

    return columnList

def compute_utility(boardObject):
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
    board = boardObject.board
    # print(board)
    # print(board[5][0])
    rows = boardObject.rows
    cols = boardObject.cols
    for row in range(rows): # 0-5
        for col in range(cols): # 0-6
            # horizontal
            if col < cols - 3:
                if (board[row][col], board[row][col+1], board[row][col+2], board[row][col+3]) == (1, 1, 1, 1):
                    winFlag = (True, False)
                    # counta += 1
                if (board[row][col], board[row][col+1], board[row][col+2], board[row][col+3]) == (2, 2, 2, 2):
                    winFlag = (False, True)
                    # countb += 1
            # vertical
            if row < rows - 3:
                if (board[row][col], board[row+1][col], board[row+2][col], board[row+3][col]) == (1, 1, 1, 1):
                    winFlag = (True, False)
                    # counta += 1
                if (board[row][col], board[row+1][col], board[row+2][col], board[row+3][col]) == (2, 2, 2, 2):
                    winFlag = (False, True)
                    # countb += 1
            # diagonally down
            if row < rows - 3 and col < cols - 3:
                if (board[row][col], board[row+1][col+1], board[row+2][col+2], board[row+3][col+3]) == (1, 1, 1, 1):
                    winFlag = (True, False)
                    # counta += 1
                if (board[row][col], board[row+1][col+1], board[row+2][col+2], board[row+3][col+3]) == (2, 2, 2, 2):
                    winFlag = (False, True)
                    # countb += 1
            # diagonally up
            if row >= 3 and col < cols - 3:
                if (board[row][col], board[row-1][col+1], board[row-2][col+2], board[row-3][col+3]) == (1, 1, 1, 1):
                    winFlag = (True, False)
                    # counta += 1
                if (board[row][col], board[row-1][col+1], board[row-2][col+2], board[row-3][col+3]) == (2, 2, 2, 2):
                    winFlag = (False, True)
                    # countb += 1
    # print(counta, countb)
    # if winFlag != (False, False):
    #     self.gameEnd = True
    p1win, p2win = winFlag
    if winFlag != (False, False):
        count = 0
        if p1win:
            # print("P1 WINS")
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 1:
                        count += 1
            return 22 - count
        elif p2win:
            # print("P2 WINS")
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 2:
                        count += 1
            return count - 22
    else:
        count = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != None:
                    count += 1
        if boardObject.turn == 1:
            return 22 - count
        else:
            return count - 22

def is_terminal(boardObject):
    if boardObject.gameEnd:
        return True
    if compute_utility(boardObject) == 0:
        # if any item in the board is None, means there are still valid moves.
        for row in range(boardObject.rows):
            for col in range(boardObject.cols):
                if boardObject.board[row][col] == None:
                    return False
        
        return True

def next_state(boardObject, col):
    b = copy.deepcopy(boardObject)
    # print(b.turn, "\n", b.getBoardText())
    if b.turn == 1:
        b.placePiece(col, b.player1)
    else:
        b.placePiece(col, b.player2)
    # print(type(b))
    return b


def alpha_beta_search(boardObject, maxDepth):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    # player = game.to_move(state)
    # Functions used by alpha_beta
    def max_value(boardObject, alpha, beta, depth):
        # print(boardObject.getBoardText(), depth)
        if is_terminal(boardObject) or depth > maxDepth:
            # print(boardObject.getBoardText(), depth)
            return compute_utility(boardObject)
        v = -1e10
        for a in get_possible_next_moves(boardObject):
            v = max(v, min_value(next_state(boardObject, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(boardObject, alpha, beta, depth):
        # print(boardObject.getBoardText(), depth)
        if is_terminal(boardObject) or depth > maxDepth:
            return compute_utility(boardObject)
        v = 1e10
        for a in get_possible_next_moves(boardObject):
            v = min(v, max_value(next_state(boardObject, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -1e10
    beta = 1e10
    best_action = None
    possibleNextActions = []
    for a in get_possible_next_moves(boardObject):
        v = min_value(next_state(boardObject, a), best_score, beta, 1)

        if v > best_score:
            best_score = v
            best_action = a
    print(best_score)
    return best_action


    # for a in get_possible_next_boards(boardObject):
    #     v = min_value(a, best_score, beta, 1)
        
    #     if v > best_score:
    #         best_score = v
    #         best_action = a
    #         possibleNextActions = [] # empty the list if we have a better action
    #     else:
    #         possibleNextActions.append(a)
    # # print(best_action)
    # return best_action if best_action != None else random.choice(possibleNextActions)

# class Player(object):
#     def __init__(self, name):
#         self.name = name
#         self.type = None

# maxPlayer = Player("max")
# minPlayer = Player("min")
# b = Board()
# # b.generateBoardFromString("334455")
# b.generateBoardFromString("33344443110")
# b.player1 = maxPlayer
# b.player2 = minPlayer

# print(b.getBoardText())
# print(is_terminal(b))
# print(compute_utility(b))
# b.placePiece(3, maxPlayer)
# for x in get_possible_next_boards(b):
    
#     print(x.getBoardText())
# print(alpha_beta_search(b, 5))

# print(get_possible_next_moves(b))
# print(None > 5)




# for board in get_possible_next_boards(b):
#     print(compute_utility(board))
#     print(board.getBoardText())
# print(get_possible_next_boards(b))

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