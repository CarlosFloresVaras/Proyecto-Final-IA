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
            sucesores.append(newState)
    
    return sucesores

# Resolver Puzzle

## Algoritmo A*
def astarSolver(initialState = [[3, 1, 2],[4, 0, 5],[6, 7, 8]]):
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
        for child in successors:
            # Si no se ha explorado el estado actual, agregar a la cola de prioridad
            if tuple(map(tuple, child)) not in visited:
                heapq.heappush(priorityQueue, (heuristica(child), child))

    # Devolver todos los movimientos realizados y la solución
    return visitedStates, solution

## Algoritmo MM (Meet in the Middle)
def mmSolver(initialState):
    goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    # Definir colas de prioridad y conjuntos de visitados para ambas direcciones
    forwardQueue = [(heuristica(initialState), initialState)]
    backwardQueue = [(heuristica(goalState), goalState)]
    
    # Diccionario de tableros visitados (key: tablero en forma de tupla de tuplas, value: None)
    forwardVisited = {tuple(map(tuple, initialState)): None}
    backwardVisited = {tuple(map(tuple, goalState)): None}
    
    # Listas para almacenar los estados de los tableros visitados
    forwardVisitedStates = []
    backwardVisitedStates = []

    # Variable para almacenar el punto de encuentro y los estados visitados
    meetingPoint = None

    while forwardQueue and backwardQueue:
        # Expandir el nodo con menor costo heurístico en la búsqueda hacia adelante
        _, forwardState = heapq.heappop(forwardQueue)
        forwardVisitedStates.append([fila[:] for fila in forwardState]) # Crear copia profunda de cada fila de forwardState
        
        # Si el estado extraído se encuentra en la búsqueda hacia atrás, actualizar meetingPoint
        if tuple(map(tuple, forwardState)) in backwardVisited:
            meetingPoint = forwardState
            break
        
        # Obtener sucesores del estado extraído
        for child in obtenerSucesores(forwardState):
            childTuple = tuple(map(tuple, child))
            # Si el sucesor no se ha visitado, agregar a visitados de forward y a forwardQueue
            if childTuple not in forwardVisited:
                forwardVisited[childTuple] = tuple(map(tuple, forwardState))
                heapq.heappush(forwardQueue, (heuristica(child), child))
        
        # ~~~~~~~~~~ BÚSQUEDA HACIA ATRÁS ~~~~~~~~~~~
        
        # Expandir el nodo con menor costo heurístico en la búsqueda hacia atrás
        _, backwardState = heapq.heappop(backwardQueue)
        backwardVisitedStates.append([fila[:] for fila in backwardState])
        
        # Si el estado extraído se encuentra en la búsqueda hacia adelante, actualizar meetingPoint
        if tuple(map(tuple, backwardState)) in forwardVisited:
            meetingPoint = backwardState
            break
        
        # Obtener sucesores del estado extraído
        for child in obtenerSucesores(backwardState):
            childTuple = tuple(map(tuple, child))
            # Si el sucesor no se ha visitado, agregar a visitados de backward y a backwardQueue
            if childTuple not in backwardVisited:
                backwardVisited[childTuple] = tuple(map(tuple, backwardState))
                heapq.heappush(backwardQueue, (heuristica(child), child))

    # Si se encuentra un meeting point, reconstruir camino desde el estado inicial hasta el final
    if meetingPoint:
        path = []
        state = tuple(map(tuple, meetingPoint)) # Convertir meetingPoint a una tupla de tuplas
        while state:
            path.append(state)
            state = forwardVisited[state] # Actualizar state al estado previo
        path.reverse()
        
        state = tuple(map(tuple, meetingPoint))
        state = backwardVisited[state] # Estado previo de backwardVisited
        while state:
            path.append(state)
            state = backwardVisited[state]
        
        # Devolver camino en forma de lista y el meetingPoint
        return [list(map(list, p)) for p in path], meetingPoint

    # Devolver todos los movimientos realizados y el punto de encuentro
    return forwardVisitedStates + backwardVisitedStates, meetingPoint

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

# tableroInicial = [3, 1, 2],[4, 0, 5],[6, 7, 8] # Tablero inicial 3, 1, 2, 4, 0, 5, 6, 7, 8

print("---- A* Algorithm ---- ")
start_time = time.perf_counter_ns()
movimientos, solucion = astarSolver(tableroInicial)
astarSolver_time = (time.perf_counter_ns() - start_time) * 1e-9
mostrarMovimientos(movimientos)
print(f"Solución en {len(movimientos)} movimientos: Tiempo de ejecución: {astarSolver_time} s")

if solucion:
    for fila in solucion:
        print(" ".join(map(str, fila)))
else:
    print("No se encontró solución con A*")

print("---- Meet in the Middle Algorithm ----")
start_time = time.perf_counter_ns()
movimientos_mm, meetingPoint = mmSolver(tableroInicial)
mmSolver_time = (time.perf_counter_ns() - start_time) * 1e-9
mostrarMovimientos(movimientos_mm)
print(f"Solución en {len(movimientos_mm)} movimientos: Tiempo de ejecución: {mmSolver_time} s")

if meetingPoint:
    print("Meeting-point")
    for fila in meetingPoint:
        print(" ".join(map(str, fila)))
else:
    print("No se encontró solución con MM")
