import heapq
import time

# Obtener distancia Manhattan (heurístca)

def heuristica(puzzleState):
    distanciaTotal = 0
    for i in range(3): # Fila
        for j in range(3): # Columna

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
    filaV, columnaV = obtenerHueco(puzzleState) #Fila vacía, columna vacía
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Derecha, izquierda, abajo, arriba
    
    for df, dc in movimientos:
        newFila, newColumna = filaV + df, columnaV + dc
        # Verificar que los movimientos no salgan del tablero y sean horizontales o verticales
        if 0 <= newFila < 3 and 0 <= newColumna < 3:
            newState = [fila[:] for fila in puzzleState] # Copia del tablero actual
            newState[filaV][columnaV], newState[newFila][newColumna] = newState[newFila][newColumna], newState[filaV][columnaV]
            sucesores.append((newState, (newFila, newColumna)))
    
    return sucesores

def obtenerSucesoresMM(state):
  # Possible directions for moving the blank space
  directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

  # Crear nueva lista de sublistas, para modificar newState sin alterar state
  newState = [fila[:] for fila in state]

  # Initialize an empty list to store successors
  successors = []

  # Get the row and column indices of the blank space
  row, col = obtenerHueco(newState)

  # Iterate over possible directions
  for dx, dy in directions:
    # Calculate new row and column indices
    newRow = row + dy
    newCol = col + dx

    # Check if the new indices are within the board bounds
    if 0 <= newRow < 3 and 0 <= newCol < 3:
      # Swap the blank space with the element at the new indices
      newState[row][col], newState[newRow][newCol] = newState[newRow][newCol], newState[row][col]

      # Calculate the heuristic value for the new state
      heuristic_value = heuristica(newState)

      # Agregar valor heurístico sin alterar el valor de state
      successors.append((heuristic_value, [fila[:] for fila in newState]))   # Return a tuple

      # Swap the elements back to their original positions (for the next iteration)
      newState[row][col], newState[newRow][newCol] = newState[newRow][newCol], newState[row][col]

  # Devolver lista de sucesores
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
                heapq.heappush(priorityQueue, (obtenerSucesores(child), child))

    # Devolver todos los movimientos realizados y la solución
    return visitedStates, solution

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

# Hacer la función del algoritmo MM (Meet in the Middle) para resolver el puzzle del 8

def mmSolver(initialState):
  goalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
  priorityQueueF = [(heuristica(initialState), initialState)]
  priorityQueueB = [(heuristica(initialState), goalState)]
  visitedF = set()
  visitedB = set()
  visitedStatesF = []
  visitedStatesB = []
  solution = None
  U = float("inf")

  while priorityQueueF and priorityQueueB:
    # Extract state with lowest heuristic
    hF, currentStateF = heapq.heappop(priorityQueueF)
    hB, currentStateB = heapq.heappop(priorityQueueB)
    # Add states to visited and visitedStates
    visitedF.add(tuple(map(tuple, currentStateF)))
    visitedB.add(tuple(map(tuple, currentStateB)))
    visitedStatesF.append([fila[:] for fila in currentStateF])
    visitedStatesB.append([fila[:] for fila in currentStateB])

    # Check if solution found
    if tuple(map(tuple, currentStateF)) in visitedB:
      solution = currentStateF
      break
    if tuple(map(tuple, currentStateB)) in visitedF:
      solution = currentStateB
      break

    successorsF = obtenerSucesoresMM(currentStateF)
    successorsB = obtenerSucesoresMM(currentStateB)

    for heuristic_value, child in successorsF:
      # Skip explored states and those exceeding minimum cost
      if tuple(map(tuple, child)) not in visitedF:
        heapq.heappush(priorityQueueF, (heuristic_value, child))
        visitedF.add(tuple(map(tuple, child)))
        visitedStatesF.append([fila[:] for fila in child])
        # Check for meeting point (solution)
        if tuple(map(tuple, child)) in visitedB:
          U = min(U, heuristic_value + hB)

    for heuristic_value, child in successorsB:
      # Skip explored states and those exceeding minimum cost
      if tuple(map(tuple, child)) not in visitedB:
        heapq.heappush(priorityQueueB, (heuristic_value, child))
        visitedB.add(tuple(map(tuple, child)))
        visitedStatesB.append([fila[:] for fila in child])
        # Check for meeting point (solution)
        if tuple(map(tuple, child)) in visitedF:
          U = min(U, heuristic_value + hF)

  return visitedStatesF + visitedStatesB, solution

# Imprimir cada movimiento

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
