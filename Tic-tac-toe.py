# A simple Tic-Tac-Toe game and AI created
# Board Game Scholar Post!1
# Freddy Reiber

import random
import copy

# This global variable is used for determining who's turn it is!
playerTurn = 'X'
moveCounter = 0


def printGameBoard(gameBoard):
    print(gameBoard[0][0] + "|" + gameBoard[0][1] + "|" + gameBoard[0][2] + "\n-+-+-\n" + gameBoard[1][0] + "|" +
          gameBoard[1][1] + "|" + gameBoard[1][2] + "\n-+-+-\n" + gameBoard[2][0] + "|" + gameBoard[2][1] + "|" +
          gameBoard[2][2])


def checkForWin(gameBoard, player):
    global playerTurn

    # Checks for a win on horizontal axis
    if gameBoard[0][0] == gameBoard[0][1] and gameBoard[0][1] == gameBoard[0][2] and gameBoard[0][2] == player:
        return True
    if gameBoard[1][0] == gameBoard[1][1] and gameBoard[1][1] == gameBoard[1][2] and gameBoard[1][2] == player:
        return True
    if gameBoard[2][0] == gameBoard[2][1] and gameBoard[2][1] == gameBoard[2][2] and gameBoard[2][2] == player:
        return True

    # Checks for a win on vertical axis
    if gameBoard[0][0] == gameBoard[1][0] and gameBoard[1][0] == gameBoard[2][0] and gameBoard[2][0] == player:
        return True, gameBoard[0][0]
    if gameBoard[0][1] == gameBoard[1][1] and gameBoard[1][1] == gameBoard[2][1] and gameBoard[2][1] == player:
        return True, gameBoard[0][1]
    if gameBoard[0][2] == gameBoard[1][2] and gameBoard[1][2] == gameBoard[2][2] and gameBoard[2][2] == player:
        return True

    # Checks for a win on diagonals
    if gameBoard[0][0] == gameBoard[1][1] and gameBoard[1][1] == gameBoard[2][2] and gameBoard[2][2] == player:
        return True, gameBoard[1][1]
    if gameBoard[0][2] == gameBoard[1][1] and gameBoard[1][1] == gameBoard[2][0] and gameBoard[2][0] == player:
        return True

    return False


# Adds marks the passed space with the current players turn and changes player turn.
def markSpace(space: int, gameBoard):
    global playerTurn
    space -= 1
    x = int(space / 3)
    y = space % 3
    gameBoard[x][y] = playerTurn


def alreadyPlayed(space: int, gameBoard):
    space -= 1
    x = int(space / 3)
    y = space % 3
    if gameBoard[x][y] == ' ':
        return False
    return True


# Begin Tic-Tac-Toe AI
# Creates a list of all possible moves for a given player
def generateAllPossibleMoves(board, player):
    listOfBoards = []
    for i in range(3):
        for k in range(3):
            if board[i][k] == " ":
                newBoard = copy.deepcopy(board)
                newBoard[i][k] = player
                listOfBoards.append(newBoard)
    return listOfBoards


# Iterates through all possible moves and finds the best one
def findNextMove(board):
    bestMove = None
    bestVal = -1000
    possibleMoves = generateAllPossibleMoves(board, 'O')
    for move in possibleMoves:
        moveValue = minimax(move, 0, False)
        if moveValue > bestVal:
            bestMove = move
            bestVal = moveValue
    return bestMove


# Minimax function used to determine value of specific moves
def minimax(board, depth: int, isMax: bool):
    global moveCounter

    if isMax:
        player = 'O'
    else:
        player = 'X'

    if checkForWin(board, 'O'):
        return 10 - depth

    if checkForWin(board, 'X'):
        return -10 + depth

    possibleMoves = generateAllPossibleMoves(board, player)
    if not possibleMoves:
        return 0

    if isMax:
        bestValue = -1000
        for move in possibleMoves:
            value = minimax(move, depth + 1, False)
            bestValue = max(bestValue, value)
        return bestValue
    else:
        bestValue = 1000
        for move in possibleMoves:
            value = minimax(move, depth + 1, True)
            bestValue = min(bestValue, value)
        return bestValue


# Runs the Main Game Loop
def mainGameLoop(singleplayer: bool = True):
    global playerTurn
    global moveCounter

    # Sets up data to be used later
    playedSpaces = []
    gameBoard = [[" " for i in range(3)] for j in range(3)]
    firstPlayer = random.randrange(2)

    # If AI is randomly selected as the first player!
    if firstPlayer == 1:
        nextAIMove = findNextMove(gameBoard)
        gameBoard = nextAIMove
        print(nextAIMove)
        if checkForWin(gameBoard, 'O'):
            print("Sorry, the AI has won")
        moveCounter += 1

    # Main game loop!
    while moveCounter < 9:
        # Gives board status and places player
        printGameBoard(gameBoard)
        playerSpace = int(input("It's " + playerTurn + "'s turn! Where do you want to go?"))
        while alreadyPlayed(playerSpace, gameBoard):
            playerSpace = int(input("Sorry, that space has already been played. Please select another one."))

        playedSpaces.append(playerSpace)
        markSpace(int(playerSpace), gameBoard)
        moveCounter += 1

        # Checks for win
        if checkForWin(gameBoard, playerTurn):
            printGameBoard(gameBoard)
            print("Congratulations " + playerTurn + " you have won!")
            break

        # Due to having it possible for two moves to be made in one loop, a second check needs to be here. If I had
        # planned better, this could have been avoided.
        if moveCounter > 8:
            break
        # Checks which version of the game user selected.
        # Runs the AI
        if singleplayer:
            nextAIMove = findNextMove(gameBoard)
            gameBoard = nextAIMove
            moveCounter += 1
            if checkForWin(gameBoard, 'O'):
                printGameBoard(gameBoard)
                print("Sorry, the AI has won")
                break

        # Continues main game loop without AI
        else:
            if playerTurn == 'X':
                playerTurn = 'O'
            else:
                playerTurn = 'X'

    if moveCounter > 8:
        printGameBoard(gameBoard)
        print("The game is a draw!")


# Simple input for turning the AI off and on. Used for testing the AI
single = True
# Driver code
while True:
    val = input("Playing with a friend? y/n")
    if val == 'y':
        single = False
        break
    if val == 'n':
        single = True
        break
    print("Not a recognized answer")
mainGameLoop(single)
