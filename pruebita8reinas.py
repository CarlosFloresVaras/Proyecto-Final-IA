import heapq
import time
from colorama import Fore, Back, Style, init

# Función que dibuja el tablero de ajedrez con las reinas en sus posiciones
def drawBoard(chessboard):
    for i in range(8):
        for j in range(8):
            if chessboard[i][j] == 1:
                print("Q ", end="")
            else:
                if (i + j) % 2 == 0:
                    print("□ ", end="")
                else:
                    print("■ ", end="")
        print()
    print()

# Función heurística para el problema de las 8 reinas (número de conflictos)
def heuristic(board):
    conflicts = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                # Verificar conflictos en la misma fila y columna
                for k in range(8):
                    if k != j and board[i][k] == 1:
                        conflicts += 1
                    if k != i and board[k][j] == 1:
                        conflicts += 1
                # Verificar conflictos en las diagonales
                for k in range(1, 8):
                    if i + k < 8 and j + k < 8 and board[i + k][j + k] == 1:
                        conflicts += 1
                    if i + k < 8 and j - k >= 0 and board[i + k][j - k] == 1:
                        conflicts += 1
                    if i - k >= 0 and j + k < 8 and board[i - k][j + k] == 1:
                        conflicts += 1
                    if i - k >= 0 and j - k >= 0 and board[i - k][j - k] == 1:
                        conflicts += 1
    return conflicts

# Función para verificar si es seguro colocar una reina en una posición dada
def isSafe(board, row, col):
    for x in range(col):
        if board[row][x] == 1:
            return False
    for x, y in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[x][y] == 1:
            return False
    for x, y in zip(range(row, 8, 1), range(col, -1, -1)):
        if board[x][y] == 1:
            return False
    return True

# Algoritmo A* para resolver el problema de las 8 reinas
def solveNQueensAStar():
    # Inicializar el tablero vacío
    initial_board = [[0] * 8 for _ in range(8)]
    open_list = []
    heapq.heappush(open_list, (0, 0, initial_board))  # (f_score, number_of_queens_placed, board)
    
    closed_list = set()
    
    while open_list:
        f, g, board = heapq.heappop(open_list)
        board_tuple = tuple(tuple(row) for row in board)
        
        if board_tuple in closed_list:
            continue
        
        closed_list.add(board_tuple)
        
        if g == 8:  # Si se han colocado 8 reinas, se ha encontrado una solución
            return board
        
        for row in range(8):
            if board[row][g] == 0 and isSafe(board, row, g):
                new_board = [r[:] for r in board]
                new_board[row][g] = 1
                new_g = g + 1
                new_h = heuristic(new_board)
                heapq.heappush(open_list, (new_g + new_h, new_g, new_board))
    
    return None  # No se encontró solución

# MM Algorithm

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

# Ejemplo de uso del algoritmo A*
initial_chessboard = [[0] * 8 for _ in range(8)]
print("Tablero Inicial")
drawBoard(initial_chessboard)

print("---- A* Algorithm ---- ")
solution = solveNQueensAStar()
if solution:
    drawBoard(solution)
else:
    print("No se encontró una solución.")

print("---- MM Algorithm ---- ")
solution = mmSolver(initial_chessboard)
if solution:
    drawBoard(solution)
else:
    print("No se encontró una solución.")
