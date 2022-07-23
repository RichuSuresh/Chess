import numpy as np

class Move():
    def __init__(self, pieceCaptured, startRow, startColumn, endRow, endColumn, isPromotion):
        self.pieceCaptured = pieceCaptured
        self.startRow = startRow
        self.startColumn = startColumn
        self.endRow = endRow
        self.endColumn = endColumn
        self.isPromotion = isPromotion
        
class gameState():
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])

        self.whiteTurn = True
        self.moveLog = []
        self.stalemate = False
        self.checkmate = False
        self.blackInCheck = False
        self.whiteInCheck = False

    def allMoves(self):
        moves = []
        self.blackInCheck = False
        self.whiteInCheck = False
        for i in range(8):
            for j in range(8):
                if (self.whiteTurn and self.board[i][j][0] == 'w') or (self.board[i][j][0] == 'b' and self.whiteTurn == False):
                    if self.board[i][j][1] == 'K':
                        self.kingMoves(i, j, moves)
                    if self.board[i][j][1] == 'p':
                        self.pawnMoves(i, j, moves)
                    if self.board[i][j][1] == 'N':
                        self.knightMoves(i, j, moves)
                    if self.board[i][j][1] == 'B':
                        self.bishopMoves(i, j, moves)
                    if self.board[i][j][1] == 'R':
                        self.rookMoves(i, j, moves)
                    if self.board[i][j][1] == 'Q':
                        self.queenMoves(i, j, moves)
        return(moves)

    def validMoves(self):
        moves = self.allMoves()
        if len(moves) == 0:
            if self.whiteInCheck or self.blackInCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        
        for i in range(len(moves)-1, -1, -1):
            move = moves[i]
            if self.isCheck(move):
                moves.remove(move)
        return(moves)
        
    
    def isCheck(self, move):
        self.move(move)
        self.allMoves()
        if (not self.whiteTurn and self.whiteInCheck) or (self.whiteTurn and self.blackInCheck):
            self.undoMove()
            return True
        self.undoMove()
        return False
        
        
    def undoMove(self):
        move = self.moveLog.pop()
        if move.isPromotion:
            if not self.whiteTurn:
                piece = "wp"
            elif self.whiteTurn:
                piece = "bp"
        else:
            piece = self.board[move.endRow][move.endColumn]
            
        self.board[move.startRow][move.startColumn] = piece
        self.board[move.endRow][move.endColumn] = move.pieceCaptured
        self.whiteTurn = not self.whiteTurn
        
    def move(self, move):
        if move.isPromotion:
            if self.whiteTurn:
                piece = "wQ"
            elif not self.whiteTurn:
                piece = "bQ"
        elif not move.isPromotion:
            piece = self.board[move.startRow][move.startColumn]
        self.moveLog.append(move)
        self.board[move.endRow][move.endColumn] = piece
        self.board[move.startRow][move.startColumn] = "--"      
        self.whiteTurn = not self.whiteTurn
        
    def pawnMoves(self, row, column, moves):
        promotion = False
        if self.whiteTurn:
            if row - 1 == 0:
                promotion = True
            if self.board[row-1][column] == "--":
                move = Move("--", row, column, row - 1, column, promotion)
                moves.append(move)
                if row == 6:
                    if self.board[row-2][column] == "--":
                        move = Move("--", row, column, row - 2, column, False)
                        moves.append(move)
            if column == 0:
                if (self.board[row-1][column+1][0] == 'b'):
                    if self.board[row-1][column+1] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row-1][column+1], row, column, row - 1, column + 1, promotion)
                    moves.append(move)
            if column == 7:
                if (self.board[row-1][column-1][0] == 'b'):
                    if self.board[row-1][column-1] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row-1][column-1], row, column, row - 1, column - 1, promotion)
                    moves.append(move)
            else:
                if (self.board[row-1][column-1][0] == 'b'):
                    if self.board[row-1][column-1] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row-1][column-1], row, column, row - 1, column - 1, promotion)
                    moves.append(move)
                if (self.board[row-1][column+1][0] == 'b'):
                    if self.board[row-1][column+1] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row-1][column+1], row, column, row - 1, column + 1, promotion)
                    moves.append(move)
                    
        if not self.whiteTurn:
            if row + 1 == 7:
                promotion = True
            if self.board[row+1][column] == "--":
                move = Move("--", row, column, row + 1, column, promotion)
                moves.append(move)
                if row == 1:
                    if self.board[row+2][column] == "--":
                        move = Move("--", row, column, row + 2, column, False)
                        moves.append(move)
            if column == 0:
                if (self.board[row+1][column+1][0] == 'w'):
                    if self.board[row+1][column+1] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row+1][column+1], row, column, row + 1, column+1, promotion)
                    moves.append(move)
            if column == 7:
                if (self.board[row+1][column-1][0] == 'w'):
                    if self.board[row+1][column-1] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row+1][column-1], row, column, row + 1, column-1, promotion)
                    moves.append(move)
            else:
                if (self.board[row+1][column-1][0] == 'w'):
                    if self.board[row+1][column-1] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row+1][column-1], row, column, row + 1, column-1, promotion)
                    moves.append(move)
                if (self.board[row+1][column+1][0] == 'w'):
                    if self.board[row+1][column+1] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row+1][column+1], row, column, row + 1, column+1, promotion)
                    moves.append(move)
                    
    def rookMoves(self, row, column, moves):  
        self.obstructedUp = False
        self.obstructedDown = False
        self.obstructedLeft = False
        self.obstructedRight = False
        self.counter = 1
        while self.obstructedUp == False or self.obstructedDown == False or self.obstructedLeft == False or self.obstructedRight == False:
            if row - self.counter < 0:
                self.obstructedUp = True
            if self.obstructedUp == False:
                if self.whiteTurn:
                    if self.board[row-self.counter][column][0] == 'w':
                        self.obstructedUp = True
                    elif self.board[row-self.counter][column][0] == 'b':
                        if self.board[row-self.counter][column] == 'bK':
                            self.blackInCheck = True
                        move = Move(self.board[row-self.counter][column], row, column, row-self.counter, column, False)
                        moves.append(move)
                        self.obstructedUp = True
                    else:
                        move = Move("--", row, column, row-self.counter, column, False)
                        moves.append(move)
                elif self.whiteTurn == False:
                    if self.board[row-self.counter][column][0] == 'b':
                        self.obstructedUp = True
                    elif self.board[row-self.counter][column][0] == 'w':
                        if self.board[row-self.counter][column] == 'wK':
                            self.whiteInCheck = True
                        move = Move(self.board[row-self.counter][column], row, column, row-self.counter, column, False)
                        moves.append(move)
                        self.obstructedUp = True
                    else:
                        move = Move(self.board[row-self.counter][column], row, column, row-self.counter, column, False)
                        moves.append(move)
                        
            if row + self.counter > 7:
                self.obstructedDown = True
            if self.obstructedDown == False:
                if self.whiteTurn:                 
                    if self.board[row+self.counter][column][0] == 'w':
                        self.obstructedDown = True
                    elif self.board[row+self.counter][column][0] == 'b':
                        if self.board[row+self.counter][column] == 'bK':
                            self.blackInCheck = True
                        move = Move(self.board[row+self.counter][column], row, column, row+self.counter, column, False)
                        moves.append(move)
                        self.obstructedDown = True
                    else:
                        move = Move("--", row, column, row+self.counter, column, False)
                        moves.append(move)
                if self.whiteTurn == False:
                    if self.board[row+self.counter][column][0] == 'b':
                        self.obstructedDown = True
                    elif self.board[row+self.counter][column][0] == 'w':
                        if self.board[row+self.counter][column] == 'wK':
                            self.whiteInCheck = True
                        move = Move(self.board[row+self.counter][column], row, column, row+self.counter, column, False)
                        moves.append(move)
                        self.obstructedDown = True
                    else:
                        move = Move("--", row, column, row+self.counter, column, False)
                        moves.append(move)
                        
            if column + self.counter > 7:
                self.obstructedRight = True
            if self.obstructedRight == False:
                if self.whiteTurn:
                    if self.board[row][column+self.counter][0] == 'w':
                        self.obstructedRight = True
                    elif self.board[row][column+self.counter][0] == 'b':
                        if self.board[row][column+self.counter] == 'bK':
                            self.blackInCheck = True
                        move = Move(self.board[row][column+self.counter], row, column, row, column+self.counter, False)
                        moves.append(move)
                        self.obstructedRight = True
                    else:
                        move = Move(self.board[row][column+self.counter], row, column, row, column+self.counter, False)
                        moves.append(move)
                elif self.whiteTurn == False:
                    if self.board[row][column+self.counter][0] == 'b':
                        self.obstructedRight = True
                    elif self.board[row][column+self.counter][0] == 'w':
                        if self.board[row][column+self.counter] == 'wK':
                            self.whiteInCheck = True
                        move = Move(self.board[row][column+self.counter], row, column, row, column+self.counter, False)
                        moves.append(move)
                        self.obstructedRight = True
                    else:
                        move = Move(self.board[row][column+self.counter], row, column, row, column+self.counter, False)
                        moves.append(move)
                        
            if column - self.counter < 0:
                self.obstructedLeft = True
            if self.obstructedLeft == False:
                if self.whiteTurn:
                    if self.board[row][column-self.counter][0] == 'w':
                        self.obstructedLeft = True
                    elif self.board[row][column-self.counter][0] == 'b':
                        if self.board[row][column-self.counter] == 'bK':
                            self.blackInCheck = True
                        move = Move(self.board[row][column-self.counter], row, column, row, column-self.counter, False)
                        moves.append(move)
                        self.obstructedLeft = True
                    else:
                        move = Move(self.board[row][column-self.counter], row, column, row, column-self.counter, False)
                        moves.append(move)
                elif self.whiteTurn == False:
                    if self.board[row][column-self.counter][0] == 'b':
                        self.obstructedLeft = True
                    elif self.board[row][column-self.counter][0] == 'w':
                        if self.board[row][column-self.counter] == 'wK':
                            self.whiteInCheck = True
                        move = Move(self.board[row][column-self.counter], row, column, row, column-self.counter, False)
                        moves.append(move)
                        self.obstructedLeft = True
                    else:
                        move = Move(self.board[row][column-self.counter], row, column, row, column-self.counter, False)
                        moves.append(move)

            self.counter += 1
                    
    def knightMoves(self, row, column, moves):
        if row + 2 <= 7:       
            if column - 1 >= 0:
                if self.whiteTurn:
                    if self.board[row+2][column-1] == "bK":
                        self.blackInCheck = True
                    if self.board[row+2][column-1][0] == "b" or self.board[row+2][column-1] == "--":
                        move = Move(self.board[row+2][column-1], row, column, row+2, column-1, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row+2][column-1] == "wK":
                        self.whiteInCheck = True
                    if self.board[row+2][column-1][0] == "w" or self.board[row+2][column-1] == "--":
                        move = Move(self.board[row+2][column-1], row, column, row+2, column-1, False)
                        moves.append(move)
            if column + 1 <= 7:
                if self.whiteTurn:
                    if self.board[row+2][column+1] == "bK":
                        self.blackInCheck = True
                    if self.board[row+2][column+1][0] == "b" or self.board[row+2][column+1] == "--":
                        move = Move(self.board[row+2][column+1], row, column, row+2, column+1, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row+2][column+1] == "wK":
                        self.whiteInCheck = True
                    if self.board[row+2][column+1][0] == "w" or self.board[row+2][column+1] == "--":
                        move = Move(self.board[row+2][column+1], row, column, row+2, column+1, False)
                        moves.append(move)
        if row + 1 <= 7:
            if column - 2 >= 0:
                if self.whiteTurn:
                    if self.board[row+1][column-2] == "bK":
                        self.blackInCheck = True
                    if self.board[row+1][column-2][0] == "b" or self.board[row+1][column-2] == "--":
                        move = Move(self.board[row+1][column-2], row, column, row+1, column-2, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row+1][column-2] == "wK":
                        self.whiteInCheck = True
                    if self.board[row+1][column-2][0] == "w" or self.board[row+1][column-2] == "--":
                        move = Move(self.board[row+1][column-2], row, column, row+1, column-2, False)
                        moves.append(move)        
            
            if column + 2 <= 7:
                if self.whiteTurn:
                    
                    if self.board[row+1][column+2] == "bK":
                        self.blackInCheck = True
                    if self.board[row+1][column+2][0] == "b" or self.board[row+1][column+2] == "--":
                        move = Move(self.board[row+1][column+2], row, column, row+1, column+2, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row+1][column+2] == "wK":
                        self.whiteInCheck = True
                    if self.board[row+1][column+2][0] == "w" or self.board[row+1][column+2] == "--":
                        move = Move(self.board[row+1][column+2], row, column, row+1, column+2, False)
                        moves.append(move)
        if row - 2 >= 0:       
            if column - 1 >= 0:
                if self.whiteTurn:
                    if self.board[row-2][column-1] == "bK":
                        self.blackInCheck = True
                    if self.board[row-2][column-1][0] == "b" or self.board[row-2][column-1] == "--":
                        move = Move(self.board[row-2][column-1], row, column, row-2, column-1, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row-2][column-1] == "wK":
                        self.whiteInCheck = True
                    if self.board[row-2][column-1][0] == "w" or self.board[row-2][column-1] == "--":
                        move = Move(self.board[row-2][column-1], row, column, row-2, column-1, False)
                        moves.append(move)
            if column + 1 <= 7:
                if self.whiteTurn:
                    if self.board[row-2][column+1] == "bK":
                        self.blackInCheck = True
                    if self.board[row-2][column+1][0] == "b" or self.board[row-2][column+1] == "--":
                        move = Move(self.board[row-2][column+1], row, column, row-2, column+1, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row-2][column+1] == "wK":
                        self.whiteInCheck = True
                    if self.board[row-2][column+1][0] == "w" or self.board[row-2][column+1] == "--":
                        move = Move(self.board[row-2][column+1], row, column, row-2, column+1, False)
                        moves.append(move)
        if row - 1 >= 0:
            if column - 2 >= 0:
                if self.whiteTurn:
                    if self.board[row-1][column-2] == "bK":
                        self.blackInCheck = True
                    if self.board[row-1][column-2][0] == "b" or self.board[row-1][column-2] == "--":
                        move = Move(self.board[row-1][column-2], row, column, row-1, column-2, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row-1][column-2] == "wK":
                        self.whiteInCheck = True
                    if self.board[row-1][column-2][0] == "w" or self.board[row-1][column-2] == "--":
                        move = Move(self.board[row-1][column-2], row, column, row-1, column-2, False)
                        moves.append(move)
            if column + 2 <= 7:
                if self.whiteTurn:
                    if self.board[row-1][column+2] == "bK":
                        self.blackInCheck = True
                    if self.board[row-1][column+2][0] == "b" or self.board[row-1][column+2] == "--":
                        move = Move(self.board[row-1][column+2], row, column, row-1, column+2, False)
                        moves.append(move)
                elif not self.whiteTurn:
                    if self.board[row-1][column+2] == "wK":
                        self.whiteInCheck = True
                    if self.board[row-1][column+2][0] == "w" or self.board[row-1][column+2] == "--":
                        move = Move(self.board[row-1][column+2], row, column, row-1, column+2, False) 
                        moves.append(move)

    def bishopMoves(self, row, column, moves):
        TRobst = False
        TLobst = False
        BRobst = False
        BLobst = False
        i = 1
        while not TRobst or not TLobst or not BRobst or not BLobst:
            if (row + i) > 7:
                BRobst = True
                BLobst = True
            if (row - i) < 0:
                TRobst = True
                TLobst = True
            if (column - i) < 0:
                BLobst = True
                TLobst = True
            if (column + i) > 7:
                TRobst = True
                BRobst = True
            if BRobst == False:
                if self.board[row + i][column + i] == "--":
                    move = Move("--", row, column, row+i, column+i, False)
                    moves.append(move)
                elif self.board[row + i][column + i][0] == "b" and self.whiteTurn:
                    if self.board[row+i][column+i] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row+i][column+i], row, column, row+i, column+i, False)
                    moves.append(move)
                    BRobst = True
                elif self.board[row + i][column + i][0] == "w" and not self.whiteTurn:
                    if self.board[row+i][column+i] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row + i][column + i], row, column, row+i, column+i, False)
                    moves.append(move)
                    BRobst = True
                else:
                    BRobst = True
            if BLobst == False:
                if self.board[row + i][column - i] == "--":
                    move = Move(self.board[row+i][column-i], row, column, row+i, column-i, False)
                    moves.append(move)
                elif self.board[row + i][column - i][0] == "b" and self.whiteTurn:
                    if self.board[row+i][column-i] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row+i][column-i], row, column, row+i, column-i, False)
                    moves.append(move)
                    BLobst = True
                elif self.board[row + i][column - i][0] == "w" and not self.whiteTurn:
                    if self.board[row+i][column-i] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row+i][column-i], row, column, row+i, column-i, False)
                    moves.append(move)
                    BLobst = True
                else:
                    BLobst = True
            if TRobst == False:
                if self.board[row - i][column + i] == "--":
                    move = Move(self.board[row-i][column+i], row, column, row-i, column+i, False)
                    moves.append(move)
                elif self.board[row - i][column + i][0] == "b" and self.whiteTurn:
                    if self.board[row-i][column+i] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row-i][column+i], row, column, row-i, column+i, False)
                    moves.append(move)
                    TRobst = True
                elif self.board[row - i][column + i][0] == "w" and not self.whiteTurn:
                    if self.board[row-i][column+i] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row-i][column+i], row, column, row-i, column+i, False)
                    moves.append(move)
                    TRobst = True
                else:
                    TRobst = True
            if TLobst == False:
                if self.board[row - i][column - i] == "--":
                    move = Move(self.board[row-i][column-i], row, column, row-i, column-i, False)
                    moves.append(move)
                elif self.board[row - i][column - i][0] == "b" and self.whiteTurn:
                    if self.board[row-i][column-i] == "bK":
                        self.blackInCheck = True
                    move = Move(self.board[row-i][column-i], row, column, row-i, column-i, False)
                    moves.append(move)
                    TLobst = True
                elif self.board[row - i][column - i][0] == "w" and not self.whiteTurn:
                    if self.board[row-i][column-i] == "wK":
                        self.whiteInCheck = True
                    move = Move(self.board[row-i][column-i], row, column, row-i, column-i, False)
                    moves.append(move)
                    TLobst = True
                else:
                    TLobst = True
            i += 1

    def queenMoves(self, row, column, moves):
        TRobst = False
        BRobst = False
        Robst = False
        TLobst = False
        BLobst = False
        Lobst = False
        Dobst = False
        Uobst = False
        i = 1
        while not TRobst or not TLobst or not BRobst or not BLobst or not Robst or not Lobst or not Dobst or not Uobst:
            if (row + i) > 7:
                BRobst = True
                BLobst = True
                Dobst = True
            if (row - i) < 0:
                TRobst = True
                TLobst = True
                Uobst = True
            if (column - i) < 0:
                BLobst = True
                TLobst = True
                Lobst = True
            if (column + i) > 7:
                TRobst = True
                BRobst = True
                Robst = True
            if BRobst == False:
                if self.board[row+i][column+i] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row+i][column+i] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row + i][column + i] == "--":
                    move = Move(self.board[row+i][column+i], row, column, row+i, column+i, False)
                    moves.append(move)
                elif self.board[row + i][column + i][0] == "b" and self.whiteTurn:
                    move = Move(self.board[row+i][column+i], row, column, row+i, column+i, False)
                    moves.append(move)
                    BRobst = True
                elif self.board[row + i][column + i][0] == "w" and not self.whiteTurn:
                    move = Move(self.board[row+i][column+i], row, column, row+i, column+i, False)
                    BRobst = True
                    moves.append(move)
                else:
                    BRobst = True
            if BLobst == False:
                if self.board[row+i][column-i] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row+i][column-i] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row + i][column - i] == "--":
                    move = Move(self.board[row+i][column-i], row, column, row+i, column-i, False)
                    moves.append(move)
                elif self.board[row + i][column - i][0] == "b" and self.whiteTurn:
                    BLobst = True
                    move = Move(self.board[row+i][column-i], row, column, row+i, column-i, False)
                    moves.append(move)
                elif self.board[row + i][column - i][0] == "w" and not self.whiteTurn:
                    BLobst = True
                    move = Move(self.board[row+i][column-i], row, column, row+i, column-i, False)
                    moves.append(move)
                else:
                    BLobst = True
            if TRobst == False:
                if self.board[row-i][column+i] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row-i][column+i] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row - i][column + i] == "--":
                    move = Move(self.board[row-i][column+i], row, column, row-i, column+i, False)
                    moves.append(move)
                elif self.board[row - i][column + i][0] == "b" and self.whiteTurn:
                    TRobst = True
                    move = Move(self.board[row-i][column+i], row, column, row-i, column+i, False)
                    moves.append(move)
                elif self.board[row - i][column + i][0] == "w" and not self.whiteTurn:
                    TRobst = True
                    move = Move(self.board[row-i][column+i], row, column, row-i, column+i, False)
                    moves.append(move)
                else:
                    TRobst = True
            if TLobst == False:
                if self.board[row-i][column-i] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row-i][column-i] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row - i][column - i] == "--":
                    move = Move(self.board[row-i][column-i], row, column, row-i, column-i, False)
                    moves.append(move)
                elif self.board[row - i][column - i][0] == "b" and self.whiteTurn:
                    TLobst = True
                    move = Move(self.board[row-i][column-i], row, column, row-i, column-i, False)
                    moves.append(move)
                elif self.board[row - i][column - i][0] == "w" and not self.whiteTurn:
                    TLobst = True
                    move = Move(self.board[row-i][column-i], row, column, row-i, column-i, False)
                    moves.append(move)
                else:
                    TLobst = True
            if Uobst == False:
                if self.board[row-i][column] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row-i][column] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row - i][column] == "--":
                    move = Move(self.board[row-i][column], row, column, row-i, column, False)
                    moves.append(move)
                elif self.board[row - i][column][0] == "b" and self.whiteTurn:
                    move = Move(self.board[row-i][column], row, column, row-i, column, False)
                    moves.append(move)
                    Uobst = True
                elif self.board[row - i][column][0] == "w" and not self.whiteTurn:
                    move = Move(self.board[row-i][column], row, column, row-i, column, False)
                    moves.append(move)
                    Uobst = True
                else:
                    Uobst = True
            if Dobst == False:
                if self.board[row+i][column] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row+i][column] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row + i][column] == "--":
                    move = Move(self.board[row+i][column], row, column, row+i, column, False)
                    moves.append(move)
                elif self.board[row + i][column][0] == "b" and self.whiteTurn:
                    move = Move(self.board[row+i][column], row, column, row+i, column, False)
                    moves.append(move)
                    Dobst = True
                elif self.board[row + i][column][0] == "w" and not self.whiteTurn:
                    move = Move(self.board[row+i][column], row, column, row+i, column, False)
                    moves.append(move)
                    Dobst = True 
                else:
                    Dobst = True
            if Lobst == False:
                if self.board[row][column-i] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row][column-i] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row][column - i] == "--":
                    move = Move(self.board[row][column-i], row, column, row, column-i, False)
                    moves.append(move)
                elif self.board[row][column - i][0] == "b" and self.whiteTurn:
                    move = Move(self.board[row][column-i], row, column, row, column-i, False)
                    moves.append(move)
                    Lobst = True
                elif self.board[row][column - i][0] == "w" and not self.whiteTurn:
                    move = Move(self.board[row][column-i], row, column, row, column-i, False)
                    moves.append(move)
                    Lobst = True
                else:
                    Lobst = True
            if Robst == False:
                if self.board[row][column+i] == "bK" and self.whiteTurn:
                    self.blackInCheck = True
                if self.board[row][column+i] == "wK" and not self.whiteTurn:
                    self.whiteInCheck = True
                if self.board[row][column + i] == "--": #or (self.board[row][column+i][0] == "b" and self.whiteTurn) or (self.board[row][column+i][0] == "w" and not self.whiteTurn):
                    move = Move(self.board[row][column+i], row, column, row, column+i, False)
                    moves.append(move)
                elif self.board[row][column + i][0] == "b" and self.whiteTurn:
                    move = Move(self.board[row][column+i], row, column, row, column+i, False)
                    moves.append(move)
                    Robst = True
                elif self.board[row][column + i][0] == "w" and not self.whiteTurn:
                    move = Move(self.board[row][column+i], row, column, row, column+i, False)
                    moves.append(move)
                    Robst = True
                else:
                    Robst = True
                        
            i += 1

    def kingMoves(self, row, column, moves):
        if (row + 1) <= 7:
            space = self.board[row+1][column]
            newRow = row + 1
            if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                if space == "bK":
                    self.blackInCheck = True
                elif space == "wK":
                    self.whiteInCheck = True
                move = Move(space, row, column, newRow, column, False)
                moves.append(move)
            if (column + 1) <= 7:
                space = self.board[row+1][column+1]
                newColumn = column + 1
                if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                    if space == "bK":
                        self.blackInCheck = True
                    elif space == "wK":
                        self.whiteInCheck = True
                    move = Move(space, row, column, newRow, newColumn, False)
                    moves.append(move)
            if (column - 1) >= 0:
                space = self.board[row+1][column-1]
                newColumn = column - 1
                if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                    if space == "bK":
                        self.blackInCheck = True
                    elif space == "wK":
                        self.whiteInCheck = True
                    move = Move(space, row, column, newRow, newColumn, False)
                    moves.append(move)
        if (row - 1) >= 0:
            space = self.board[row-1][column]
            newRow = row-1
            if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                if space == "bK":
                    self.blackInCheck = True
                elif space == "wK":
                    self.whiteInCheck = True
                move = Move(space, row, column, newRow, column, False)
                moves.append(move)
            if (column + 1) <= 7:
                space = self.board[row-1][column+1]
                newColumn = column + 1
                if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                    if space == "bK":
                        self.blackInCheck = True
                    elif space == "wK":
                        self.whiteInCheck = True
                    move = Move(space, row, column, newRow, newColumn, False)
                    moves.append(move)
            if (column - 1) >= 0:
                space = self.board[row-1][column-1]
                newColumn = column - 1
                if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                    if space == "bK":
                        self.blackInCheck = True
                    elif space == "wK":
                        self.whiteInCheck = True
                    move = Move(space, row, column, newRow, newColumn, False)
                    moves.append(move)
        if (column + 1) <= 7:
            space = self.board[row][column+1]
            newColumn = column + 1
            if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                if space == "bK":
                    self.blackInCheck = True
                elif space == "wK":
                    self.whiteInCheck = True
                move = Move(space, row, column, row, newColumn, False)
                moves.append(move)
        if (column - 1) >= 0:
            space = self.board[row][column-1]
            newColumn = column - 1
            if space == "--" or (space[0] == "b" and self.whiteTurn) or (space[0] == "w" and not self.whiteTurn):
                if space == "bK":
                    self.blackInCheck = True
                elif space == "wK":
                    self.whiteInCheck = True
                move = Move(space, row, column, row, newColumn, False)
                moves.append(move)
        

        
                    
            
            
            
            
    


        
