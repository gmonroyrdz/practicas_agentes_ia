# 0 = limpia, 1 = sucia, 2 = obstaculo
MUNDO = [
    [1, 0, 1, 2, 0],
    [0, 2, 0, 0, 1],
    [1, 0, 2, 0, 0],
    [0, 0, 1, 2, 1],
    [2, 0, 0, 1, 0],
]

FILAS    = len(MUNDO)
COLUMNAS = len(MUNDO[0])

# Movimientos: arriba, abajo, izquierda, derecha
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def vecinos(mundo, fila, col):
    """Devuelve las celdas libres adyacentes a (fila, col)."""
    resultado = []
    for df, dc in MOVIMIENTOS:
        nf, nc = fila + df, col + dc
        if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
            if mundo[nf][nc] != 2:      # no es obstaculo
                resultado.append((nf, nc))
    return resultado

from collections import deque

def bfs(mundo, origen, meta):
    """Devuelve la lista de celdas del camino mas corto de origen a meta."""
    cola = deque([origen])
    visitados = {origen}
    padre = {origen: None}

    while cola:
        actual = cola.popleft()
        if actual == meta:
            return reconstruir_camino(padre, meta)

        for v in vecinos(mundo, *actual):
            if v not in visitados:
                visitados.add(v)
                padre[v] = actual
                cola.append(v)

    return []   # no hay camino

def reconstruir_camino(padre, meta):
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = padre[actual]
    camino.reverse()
    return camino

def celdas_sucias(mundo):
    """Devuelve todas las celdas con valor 1."""
    sucias = []
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if mundo[f][c] == 1:
                sucias.append((f, c))
    return sucias

def sucia_mas_cercana(mundo, posicion):
    """Ejecuta BFS hacia cada celda sucia y devuelve la de menor camino."""
    mejor_camino = None
    for sucia in celdas_sucias(mundo):
        camino = bfs(mundo, posicion, sucia)
        if camino and (mejor_camino is None or len(camino) < len(mejor_camino)):
            mejor_camino = camino
    return mejor_camino

def agente_aspiradora(mundo, inicio):
    """Simula el agente hasta que no queden celdas sucias."""
    posicion = inicio
    pasos = 0
    historial = [posicion]

    while celdas_sucias(mundo):
        camino = sucia_mas_cercana(mundo, posicion)
        if not camino:
            print("No hay camino a ninguna celda sucia.")
            break

        # Recorrer el camino hasta la celda sucia
        for celda in camino[1:]:
            posicion = celda
            pasos += 1
            historial.append(posicion)

        # Aspirar
        mundo[posicion[0]][posicion[1]] = 0
        print(f"Aspirado en {posicion}  (paso {pasos})")

    return historial, pasos

import random
def map_aleatorio(filas, columnas, prob_sucia=0.4, prob_obs=0.15):
    return [[2 if random.random() < prob_obs else (1 if random.random() < prob_sucia else 0)
    for _ in range(columnas)]
    for _ in range(filas)]

if __name__ == "__main__":
    #mundo = [fila[:] for fila in MUNDO]   # copia para no modificar el original
    inicio = (0, 0)

    mundo = map_aleatorio(10,10,0.2,0.15)

    print("Mapa inicial:")
    for fila in mundo:
        print(fila)

    historial, pasos = agente_aspiradora(mundo, inicio)

    print("\nMapa final:")
    for fila in mundo:
        print(fila)

    print(f"\nCeldas recorridas: {len(historial)}")
    print(f"Pasos totales:    {pasos}")
