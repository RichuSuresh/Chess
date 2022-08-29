import random
scoreDict = {"K":0, "Q":100, "R":50, "B":30, "N":30, "p":10}

kingPositions = [[-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-2, -3, -3, -4, -4, -3, -3, -2],
                [-1, -2, -2, -2, -2, -2, -2, -1],
                [2, 2, 0, 0, 0, 0, 2, 2],
                [2, 3, 1, 0, 0, 1, 3, 2]]

queenPositions = [[-2,-1, -1, -0.5, -0.5, -1, -1, -2],
                  [-1, 0, 0, 0, 0, 0, 0, -1],
                  [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
                  [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
                  [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
                  [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
                  [-1, 0, 0.5, 0, 0, 0, 0, -1],
                  [-2, -1, -1, -0.5, -0.5, -1, -1, -2]]

rookPositions = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                 [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                 [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                 [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                 [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                 [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                 [0, 0, 0, 0, 0, 0, 0, 0]]

bishopPositions = [[-2, -1, -1, -1, -1, -1, -1, -2],
                   [-1, 0, 0, 0, 0, 0, 0, -1],
                   [-1,  0, 0.5, 1, 1, 0.5, 0, -1],
                   [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
                   [-1, 0, 1, 1, 1, 1, 0, -1],
                   [-1, 1, 1, 1, 1, 1, 1, -1],
                   [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
                   [-2, -1, -1, -1, -1, -1, -1, -2]]

knightPositions = [[-5, -4, -3, -3, -3, -3, -4, -5],
                   [-4, -2, 0, 0, 0, 0, -3, -4],
                   [-3, 0, 1, 1.5, 1.5, 1, 0,  -3],
                   [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
                   [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
                   [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
                   [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
                   [-5, -4, -3, -3, -3, -3, -4, -5]]

pawnPositions = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [5, 5, 5, 5, 5, 5, 5, 5],
                 [1, 1, 2, 3, 3, 2, 1, 1],
                 [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
                 [0, 0, 0, 2, 2, 0, 0, 0],
                 [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
                 [0.5, 1, 1, -2, -2, 1, 1, 0.5],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

piecePosDict = {"K":kingPositions, "Q":queenPositions, "R":rookPositions, "B":bishopPositions, "N":knightPositions, "p":pawnPositions}
checkmate = 1000
stalemate = 0

maxDepth = 2


                 

                  

def movefinder(gameState, moves):
    global bestMove
    random.shuffle(moves)
    bestMove = moves[0]
    minmax(gameState, moves, gameState.whiteTurn, maxDepth, -1000, 1000)
    return (bestMove)

def minmax(gameState, moves, whiteTurn, depth, alpha, beta):
    global bestMove
    if depth == 0:
        return totalScore(gameState)
            
    if whiteTurn:
        maxScore = -checkmate
 
        for move in moves:
            gameState.move(move)
            nextMoves = gameState.validMoves()
            score = minmax(gameState, nextMoves, False, depth - 1, alpha, beta)
            if score > maxScore:
                maxScore = score
                if depth == maxDepth:
                    bestMove = move
            gameState.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore
    else:
        minScore = checkmate
        for move in moves:
            gameState.move(move)
            nextMoves = gameState.validMoves()
            score = minmax(gameState, nextMoves, True, depth - 1, alpha, beta)
            if score < minScore:
                minScore = score
                if depth == maxDepth:
                    bestMove = move
            gameState.undoMove()
            if minScore < beta:
                beta = minScore
            if alpha >= beta:
                break
        return minScore
        

def totalScore(gameState):
    score = 0
    if gameState.checkmate:
        if gameState.whiteTurn:
            return -checkmate
        else:
            return checkmate
    elif gameState.stalemate:
        return stalemate
    
    for i in range(8):
        for j in range(8):
            square = gameState.board[i][j]
            if square != "--":
                positions = piecePosDict[square[1]]
                score += positions[i][j]
            if square[0] == "w":
                score += scoreDict[square[1]]
            if square[0] == "b":
                score -= scoreDict[square[1]]
    return score
