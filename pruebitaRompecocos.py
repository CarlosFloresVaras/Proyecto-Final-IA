import heapq
import time

# Obtener distancia Manhattan (heurística)
def heuristica(puzzleState):
    distanciaTotal = 0
    for i in range(3):  # Fila
        for j in range(3):  # Columna
            # Si la pieza no es hueco, calcular la fila y columna objetivo de cada número
            if puzzleState[i][j] != 0:
                filaObjetivo = (puzzleState[i][j] - 1) // 3
                columnaObjetivo = (puzzleState[i][j] - 1) % 3
                distanciaTotal += abs(i - filaObjetivo) + abs(j - columnaObjetivo)
    return distanciaTotal

# Obtener posición vacía del tablero
def obtenerHueco(puzzleState):
    for i in range(3):
        for j in range(3):
            # Si encuentra 0 (hueco), devolver posición del hueco
            if puzzleState[i][j] == 0:
                return i, j

# Obtener sucesores y verificar movimientos del hueco
def obtenerSucesores(puzzleState):
    sucesores = []
    filaV, columnaV = obtenerHueco(puzzleState)  # Fila vacía, columna vacía
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Derecha, izquierda, abajo, arriba
    
    for df, dc in movimientos:
        newFila, newColumna = filaV + df, columnaV + dc
        # Verificar que los movimientos no salgan del tablero y sean horizontales o verticales
        if 0 <= newFila < 3 and 0 <= newColumna < 3:
            newState = [fila[:] for fila in puzzleState]  # Copia del tablero actual
            newState[filaV][columnaV], newState[newFila][newColumna] = newState[newFila][newColumna], newState[filaV][columnaV]
            sucesores.append((newState, (newFila, newColumna)))
    
    return sucesores

def obtenerSucesoresMM(state):
    # Possible directions for moving the blank space
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # Initialize an empty list to store successors
    successors = []
    # Get the row and column indices of the blank space
    row, col = obtenerHueco(state)
    # Iterate over possible directions
    for dx, dy in directions:
        # Calculate new row and column indices
        newRow = row + dy
        newCol = col + dx
        # Check if the new indices are within the board bounds
        if 0 <= newRow < 3 and 0 <= newCol < 3:
            # Create a copy of the state to avoid modifying the original
            newState = [fila[:] for fila in state]
            # Swap the blank space with the element at the new indices
            newState[row][col], newState[newRow][newCol] = newState[newRow][newCol], newState[row][col]
            # Calculate the heuristic value for the new state
            heuristic_value = heuristica(newState)
            # Append the new state and its heuristic to the successors list
            successors.append((heuristic_value, newState))
    return successors

# Resolver Puzzle

## Algoritmo A*
def astarSolver(initialState):
    currentState = initialState
    priorityQueue = [(heuristica(initialState), initialState)]
    visited = set()
    visitedStates = []
    solution = None

    while priorityQueue:
        # Extraer estado del tablero con menor heurística
        h, currentState = heapq.heappop(priorityQueue)
        # Agregar estados a visited y visitedStates
        visited.add(tuple(map(tuple, currentState)))
        visitedStates.append([fila[:] for fila in currentState])

        # Si se encuentra la solución, actualizar solución
        if currentState == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            solution = currentState
            break
        successors = obtenerSucesores(currentState)
        for child, _ in successors:
            # Si no se ha explorado el estado actual, agregar a la cola de prioridad
            if tuple(map(tuple, child)) not in visited:
                heapq.heappush(priorityQueue, (heuristica(child), child))

    # Devolver todos los movimientos realizados y la solución
    return visitedStates, solution

## Algoritmo MM (Meet in the Middle)

def mmSolver(initialState):
    goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    priorityQueueF = [(heuristica(initialState), initialState, 0)]
    priorityQueueB = [(heuristica(goalState), goalState, 0)]
    visitedF = {}
    visitedB = {}
    visitedStatesF = []
    visitedStatesB = []
    solution = None
    U = float("inf")

    while priorityQueueF and priorityQueueB:
        # Extract state with lowest heuristic from forward queue
        if priorityQueueF:
            hF, currentStateF, gF = heapq.heappop(priorityQueueF)
            # Check if the state is already visited in backward direction
            if tuple(map(tuple, currentStateF)) in visitedB:
                solution = currentStateF
                break
            visitedF[tuple(map(tuple, currentStateF))] = gF
            visitedStatesF.append([fila[:] for fila in currentStateF])
            successorsF = obtenerSucesoresMM(currentStateF)
            for heuristic_value, child in successorsF:
                g = gF + 1
                if tuple(map(tuple, child)) not in visitedF or g < visitedF[tuple(map(tuple, child))]:
                    heapq.heappush(priorityQueueF, (heuristic_value + g, child, g))
                    visitedF[tuple(map(tuple, child))] = g

        # Extract state with lowest heuristic from backward queue
        if priorityQueueB:
            hB, currentStateB, gB = heapq.heappop(priorityQueueB)
            # Check if the state is already visited in forward direction
            if tuple(map(tuple, currentStateB)) in visitedF:
                solution = currentStateB
                break
            visitedB[tuple(map(tuple, currentStateB))] = gB
            visitedStatesB.append([fila[:] for fila in currentStateB])
            successorsB = obtenerSucesoresMM(currentStateB)
            for heuristic_value, child in successorsB:
                g = gB + 1
                if tuple(map(tuple, child)) not in visitedB or g < visitedB[tuple(map(tuple, child))]:
                    heapq.heappush(priorityQueueB, (heuristic_value + g, child, g))

    # Devolver todos los movimientos realizados y la solución
    return visitedStatesF + visitedStatesB, solution


def mostrarMovimientos(visitedStates):
    for movimiento, estado in enumerate(visitedStates, start=1):
        print(f"--- Movimiento {movimiento} ---")
        for fila in estado:
            print(" ".join(map(str, fila)))
        print()

tableroInicial = [
    [3, 1, 2],
    [4, 0, 5],
    [6, 7, 8]
]


print("---- A* Algorithm ---- ")
start_time = time.perf_counter_ns()      # Agregamos 'start_time' para medir el tiempo de ejecución por cada algoritmo, se repitira esta línea por cada algoritmo
movimientos, solucion = astarSolver(tableroInicial)
astarSolver_time = (time.perf_counter_ns() - start_time)*1e-9     # Current time - start time = tiempo de ejecución
mostrarMovimientos(movimientos)
print(f"Solución en {len(movimientos)} movimientos:         Tiempo de ejecución: {astarSolver_time} s")

for fila in solucion:
    print(" ".join(map(str, fila)))

print("\n---- MM Algorithm ---- ")
start_time = time.perf_counter_ns()
movimientos, solucion = mmSolver(tableroInicial)
mmSolver_time = (time.perf_counter_ns() - start_time)*1e-9
mostrarMovimientos(movimientos)
print(f"Solución en {len(movimientos)} movimientos:         Tiempo de ejecución: {mmSolver_time} s wiiiii")

