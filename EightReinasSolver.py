import heapq
import time

# Eight Queens Problem

# Funcion que dibuja el tablero de ajedrez con lineas de separación y color de las casillas y coloca las reinas en sus posiciones con un "♛	&#x265b;""

def drawBoard(chessboard):
    if chessboard is None:
        print("No solution")
        return
    else:
        for i in range(8):
            for j in range(8):
                # Si la casilla tiene un 1, colocar una reina
                if chessboard[i][j] == 1:
                        print(" ♛ ", end="") # \033[31m es el color rojo
                else:
                    # Si la suma de i y j es par, la casilla es blanca
                    if (i+j)%2 == 0:
                            print(" □ ", end="") # \033[47m es el color blanco
                    else:
                            print(" ■ ", end="")
            print()
    print()

# Resolver Puzzle Eight con A* y MM

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

def solveNQueens(board = [[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]], col = 0): # board es el tablero, col es la columna actual que se está evaluando en la recursión
    if col == 8:
        print(board)
        return board
    for i in range(8):  # Iterate over each row in the current column save the movements made movimientos.append(board)
        if isSafe(board, i, col):    # Check if the queen can be placed in the current row and column
            board[i][col] = 1
            if solveNQueens(board, col + 1):
                return board
            board[i][col] = 0
    return None

## Algoritmo MM (Meet in the Middle)

"""
Pseudocódigo:

1   gF (start) := gB(goal) := 0; OpenF := {start};
    OpenB := {goal}; U := ∞
2   while (OpenF != ∅) and (OpenB != ∅) do
3       C := min(prminF , prminB)
4       if U ≤ max(C, fminF , fminB, gminF + gminB + )
        then
5           return U
6       if C = prminF then
7           // Expand in the forward direction
8       choose n ∈ OpenF for which prF (n) = prminF
        and gF (n) is minimum
9       move n from OpenF to ClosedF
10      for each child c of n do
11          if c ∈ OpenF ∪ ClosedF and gF (c) ≤ gF (n) + cost(n, c) 
            then
12              continue
13          if c ∈ OpenF ∪ ClosedF then
14              remove c from OpenF ∪ ClosedF
15          gF (c) := gF (n) + cost(n, c)
16          add c to OpenF
17          if c ∈ OpenB then
18              U := min(U,gF (c) + gB(c))
19          else
20              // Expand in the backward direction, analogously
21return ∞

"""
# Completar función con el algoritmo MM

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
print("---- Tablero Inicial ----\n")
drawBoard(initialchessboard)

# Tablero con las reinas colocadas ejemplo de solución
solutionchessboard = [[0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0]]
print("---- Un Tablero Solución ----\n")
drawBoard(solutionchessboard)

# Ejemplo de tablero para resolver el problema de las 8 reinas
ejemplochessboard = [[0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0, 0, 0, 0]]

print("---- A* Algorithm ----\n")
drawBoard(ejemplochessboard)
solucion = solveNQueens(ejemplochessboard, 4)
print("---- Solución ----\n")
drawBoard(solucion)


print("---- MM Algorithm ----\n")
