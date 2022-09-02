import Engine_v2 as Engine
import pygame
import AI
import time

WIDTH = HEIGHT = 512
sqSize = 512 // 8 #size of indivividual squares on board
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")
clock = pygame.time.Clock()
images = {}

#loads images from images folder
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sqSize, sqSize))
        
#draws the checkered board onto the game window
def drawBoard(screen, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if ((r+c) %2) == 0:
                pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect(c*sqSize, r*sqSize, sqSize, sqSize))
            else:
                pygame.draw.rect(screen, pygame.Color("gray"), pygame.Rect(c*sqSize, r*sqSize, sqSize, sqSize))
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(c*sqSize, r*sqSize, sqSize, sqSize))
                



gameState = Engine.gameState()
loadImages()
moves = gameState.validMoves()
sqSelected = ()
clickQueue = []
running = True
AImode = True   #change this to False for PVP or True for Player vs Computer
moveMade = False
promotion = False
endGame = False

#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            mousePos = pygame.mouse.get_pos()
        
            col = mousePos[0] // sqSize
            row = mousePos[1] // sqSize
            if sqSelected == (row, col):
                sqSelected = ()
                clickQueue = []
            else:
                sqSelected = (row, col)
                clickQueue.append(sqSelected)
            #player needs to click a space with their space, then click the space they wish to move the piece into
            if len(clickQueue) == 2:
                piece = gameState.board[clickQueue[0][0]][clickQueue[0][1]]
                pieceCaptured = gameState.board[clickQueue[1][0]][clickQueue[1][1]]
                promotion = False
                #checks whether a move is a pawn promotion move
                if piece == "wp" and sqSelected[0] == 0:
                    promotion = True
                if piece == "bp" and sqSelected[0] == 7:
                    promotion = True
                move = Engine.Move(pieceCaptured, clickQueue[0][0], clickQueue[0][1], clickQueue[1][0], clickQueue[1][1], promotion) 
                moveID = (move.startRow, move.startColumn, move.endRow, move.endColumn) #generates a moveID used to check whether the move is a valid move
                moveFound = False
                i = 0
                #searches through the valid moves array to check whether the player has made a valid move
                while not moveFound and i != len(moves):
                    compMoveID = (moves[i].startRow, moves[i].startColumn, moves[i].endRow, moves[i].endColumn)
                    if compMoveID == moveID:
                        moveFound = True
                        gameState.move(move)
                        moves = gameState.validMoves()
                        #if there are no valid moves, then a checkmate or stalemate has occured
                        if len(moves) == 0:
                            if gameState.checkmate:
                                if gameState.whiteTurn:
                                    print("checkmate, black wins")
                                else:
                                    print("checkmate, white wins")
 
                            elif gameState.stalemate:
                                print("stalemate")
                            endGame = True
                        if AImode:
                            moveMade = True
                        promotion = False
                    else:
                        i += 1
                sqSelected = ()
                clickQueue = []
        #if the player presses the z key, the most recent move is undone
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                gameState.undoMove()
                moves = gameState.validMoves()
                moveMade = False
                
    #AI code
    if moveMade == True and endGame == False:
        bestMove = AI.movefinder(gameState, moves)
        gameState.move(bestMove)
        moveMade = False
        moves = gameState.validMoves()
        if len(moves) == 0:
            if gameState.checkmate:
                if gameState.whiteTurn:
                    print("checkmate, black wins")
                else:
                    print("checkmate, white wins")

            elif gameState.stalemate:
                print("stalemate")
            endGame = True
    

    drawBoard(screen, gameState.board)
    clock.tick(15)
    pygame.display.flip()


pygame.quit()
