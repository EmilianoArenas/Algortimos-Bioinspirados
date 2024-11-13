import numpy as np
import random

nodos = 6
iteraciones = 50
alfa = 1.5
beta = 0.8
rho = 0.5
Q = 1

distancias = np.array([
    [0, 6, 9, 17, 13, 21],
    [6, 0, 19, 21, 12, 18],
    [9, 19, 0, 20, 23, 11],
    [17, 21, 20, 0, 15, 10],
    [13, 12, 23, 15, 0, 21],
    [21, 18, 11, 10, 21, 0]
])

feromonas = [[0.1 for _ in range(nodos)] for _ in range(nodos)]

#Selección de nodo
def seleccionarNodo(nodoActual, visitados):
    probabilidades = []
    for i in range(nodos):
        if i not in visitados:
            #calcular la visibilidad
            visibilidad = 1 / (distancias[nodoActual][i] + 1e-10)
            prob = (feromonas[nodoActual][i] ** alfa) * (visibilidad ** beta)
            probabilidades.append(prob)
        else:
            probabilidades.append(0)

    #selección por ruleta
    total = sum(probabilidades)
    seleccion = random.uniform(0, total)
    suma = 0
    for i in range(nodos):
        suma += probabilidades[i]
        if seleccion <= suma:
            return i
    return None

#algoritmo de colonia de hormigas
def algoritmo():
    mejorCosto = float('inf')
    mejorRuta = []

    for _ in range(iteraciones):
        rutas = []
        costos = []

        #recorrer para cada hormiga
        for hormiga in range(nodos):
            nodoActual = hormiga
            ruta = [nodoActual]
            visitados = set(ruta)

            while len(ruta) < nodos:
                siguienteNodo = seleccionarNodo(nodoActual, visitados)
                if siguienteNodo is not None:
                    ruta.append(siguienteNodo)
                    visitados.add(siguienteNodo)
                    nodoActual = siguienteNodo

            #regresar al nodo inicial
            ruta.append(ruta[0])
            rutas.append(ruta)

        #calculo del costo
        for ruta in rutas:
            costo = 0
            for i in range(len(ruta) - 1):
                costo += distancias[ruta[i]][ruta[i + 1]]
            costos.append(costo)
            if costo < mejorCosto:
                mejorCosto = costo
                mejorRuta = ruta[:]

        #actualizar feromonas
        for i in range(nodos):
            for j in range(nodos):
                feromonas[i][j] *= (1 - rho)
                for k, ruta in enumerate(rutas):
                    for l in range(len(ruta) - 1):
                        if (ruta[l] == i and ruta[l + 1] == j) or (ruta[l] == j and ruta[l + 1] == i):
                            feromonas[i][j] += Q / (costos[k] + 1)

    print("Mejor ruta encontrada:", mejorRuta)
    print("Costo total:", mejorCosto)
algoritmo()
