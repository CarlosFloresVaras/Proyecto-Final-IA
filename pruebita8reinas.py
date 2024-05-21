import heapq
import time
from colorama import Fore, Back, Style
from queue import PriorityQueue

# Eight Queens Problem

# Funcion que dibuja el tablero de ajedrez con lineas de separación y color de las casillas y coloca las reinas en sus posiciones con un "♛	&#x265b;""
def drawBoard(chessboard):
        for i in range(8):
                        for j in range(8):
                                # Si la casilla tiene un 1, colocar una reina
                                if chessboard[i][j] == 1:
                                        print("Q ", end="") # \033[31m es el color rojo
                                else:
                                        # Si la suma de i y j es par, la casilla es blanca
                                        if (i+j)%2 == 0:
                                                print("□ ", end="") # \033[47m es el color blanco
                                        else:
                                                print("■ ", end="")
                        print()
        print()

# Heurística para el problema de las 8 reinas
def isSafe(board, row, col):
    for x in range(col):        # Check the row on the left side
        if board[row][x] == 1:  # Check if there is a queen in the left side
            return False        # Return False if there is a queen
    for x, y in zip(range(row, -1, -1), range(col, -1, -1)):    # Check upper diagonal on left side
        if board[x][y] == 1:    # Check if there is a queen in the upper left diagonal
            return False        # Return False if there is a queen
    for x, y in zip(range(row, 8, 1), range(col, -1, -1)):      # Check lower diagonal on left side
        if board[x][y] == 1:    # Check if there is a queen in the lower left diagonal
            return False        # Return False if there is a queen
    return True

## Algoritmo A*

def solveNQueens(board, col, movimientos =  []): 
    movimientos.append(board)
    if col == 8:
        print(board)
        return movimientos, board
    for i in range(8):  # Iterate over each row in the current column save the movements made movimientos.append(board)
        if isSafe(board, i, col):    # Check if the queen can be placed in the current row and column
            board[i][col] = 1
            if solveNQueens(board, col + 1):
                return movimientos, board
            board[i][col] = 0
    return movimientos, "No se encontró una solución"

def solveNQueens(board, col):   # board es el tablero, col es la columna actual que se está evaluando en la recursión
    movimientos = []
    if col == 8:

        return movimientos, board
    for i in range(8):
        if isSafe(board, i, col):
            board[i][col] = 1
            movimientos.append(board)
            if solveNQueens(board, col + 1):
                return movimientos, board
            board[i][col] = 0

    return None


def getSuccessors(board):
    successors = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                for k in range(8):
                    if board[k][j] == 0:
                        new_board = [list(row) for row in board]
                        new_board[i][j] = 0
                        new_board[k][j] = 1
                        successors.append(new_board)
                    if board[i][k] == 0:
                        new_board = [list(row) for row in board]
                        new_board[i][j] = 0
                        new_board[i][k] = 1
                        successors.append(new_board)
                k, l = i - min(i, j), j - min(i, j)
                while k < 8 and l < 8:
                    if board[k][l] == 0:
                        new_board = [list(row) for row in board]
                        new_board[i][j] = 0
                        new_board[k][l] = 1
                        successors.append(new_board)
                    k += 1
                    l += 1
                k, l = i - min(i, 7 - j), j + min(i, 7 - j)
                while k < 8 and l >= 0:
                    if board[k][l] == 0:
                        new_board = [list(row) for row in board]
                        new_board[i][j] = 0
                        new_board[k][l] = 1
                        successors.append(new_board)
                    k += 1
                    l -= 1
    return successors

## Heurística para el algoritmo MM

def heuristic(board):
    conflicts = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                for k in range(8):
                    if k != j and board[i][k] == 1:
                        conflicts += 1
                for k in range(8):
                    if k != i and board[k][j] == 1:
                        conflicts += 1
                k, l = i - min(i, j), j - min(i, j)
                while k < 8 and l < 8:
                    if k != i and l != j and board[k][l] == 1:
                        conflicts += 1
                    k += 1
                    l += 1
                k, l = i - min(i, 7 - j), j + min(i, 7 - j)
                while k < 8 and l >= 0:
                    if k != i and l != j and board[k][l] == 1:
                        conflicts += 1
                    k += 1
                    l -= 1
    return conflicts

## Algoritmo MM
def mmSolver(initialState):
    goalState = [[0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0]]

    forwardQueue = [(heuristic(initialState), initialState)]
    backwardQueue = [(heuristic(goalState), goalState)]

    def list_to_tuple(lst):
        return tuple(tuple(sub) for sub in lst)

    initialStateTuple = list_to_tuple(initialState)
    goalStateTuple = list_to_tuple(goalState)
    
    forwardVisited = {initialStateTuple: None}
    backwardVisited = {goalStateTuple: None}

    forwardVisitedStates = []
    backwardVisitedStates = []

    meetingPoint = None

    while forwardQueue and backwardQueue:
        _, forwardState = heapq.heappop(forwardQueue)
        forwardVisitedStates.append(list(forwardState))

        if list_to_tuple(forwardState) in backwardVisited:
            meetingPoint = forwardState
            break

        for child in getSuccessors(forwardState):
            childTuple = list_to_tuple(child)
            if childTuple not in forwardVisited:
                forwardVisited[childTuple] = list_to_tuple(forwardState)
                heapq.heappush(forwardQueue, (heuristic(child), child))

        _, backwardState = heapq.heappop(backwardQueue)
        backwardVisitedStates.append(list(backwardState))

        if list_to_tuple(backwardState) in forwardVisited:
            meetingPoint = backwardState
            break

        for child in getSuccessors(backwardState):
            childTuple = list_to_tuple(child)
            if childTuple not in backwardVisited:
                backwardVisited[childTuple] = list_to_tuple(backwardState)
                heapq.heappush(backwardQueue, (heuristic(child), child))

    if meetingPoint:
        path = []
        state = list_to_tuple(meetingPoint)
        while state:
            path.append(state)
            state = forwardVisited[state]
        path.reverse()

        state = list_to_tuple(meetingPoint)
        state = backwardVisited[state]
        while state:
            path.append(state)
            state = backwardVisited[state]

        return [list(map(list, p)) for p in path], meetingPoint

    return forwardVisitedStates + backwardVisitedStates, meetingPoint

# Imprimir cada movimiento

# Resolver el problema de las 8 reinas con A* y MM

# Tablero inicial sin reinas
initialchessboard = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
print("Tablero Inicial")
drawBoard(initialchessboard)

# Tablero con las reinas colocadas ejemplo de solución
solutionchessboard = [[0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0]]
print("Tablero Solución")
drawBoard(solutionchessboard)

# Ejemplo de tablero para resolver el problema de las 8 reinas
ejemplochessboard = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

print("---- A* Algorithm ---- ")
drawBoard(ejemplochessboard)
movimientos, solution = solveNQueens(ejemplochessboard, 1)
drawBoard(solution)

print("---- MM Algorithm ----")
print("Initial board")
drawBoard(initialchessboard)

path, solution = mmSolver(initialchessboard)
if solution:
    print("Tablero Solución:")
    drawBoard(solution)
else:
    print("Solución no encontrada.")
    drawBoard(path[-1])