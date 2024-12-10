import numpy as np

productos = [
    {"name": "Decoy Detonators", "peso": 4, "precio": 10},
    {"name": "Love Potion", "peso": 2, "precio": 8},
    {"name": "Extendable Ears", "peso": 5, "precio": 12},
    {"name": "Skiving Snackbox", "peso": 5, "precio": 6},
    {"name": "Fever Fudge", "peso": 2, "precio": 3},
    {"name": "Puking Pastilles", "peso": 1.5, "precio": 2},
    {"name": "Nosebleed Nougat", "peso": 1, "precio": 2},
]

# Restricciones
capacidad = 15 
max_items = [10, 3, 10, 2, 10, 10, 10]  
min_items = [0, 3, 0, 2, 0, 0, 0]      
swarm_size = 40
worker_bees = 20
onlooker_bees = 20
limit = 5
iterations = 50

def evaluarSolucion(solucion):
    precioTotal = sum(solucion[i] * productos[i]["precio"] for i in range(len(productos)))
    pesoTotal = sum(solucion[i] * productos[i]["peso"] for i in range(len(productos)))
    return precioTotal, pesoTotal

def seleccionRuleta(solucions, profits):
    total_profit = sum(profits)
    if total_profit == 0:
        return solucions[0]  
    probabilidades = [p / total_profit for p in profits]
    cumulative_probs = np.cumsum(probabilidades)
    r = np.random.uniform(0, 1)  
    for i, cp in enumerate(cumulative_probs):
        if r <= cp:
            return solucions[i]

swarm = []
for _ in range(swarm_size):
    while True:
        solucion = [np.random.randint(min_items[i], max_items[i] + 1) for i in range(len(productos))]
        _, peso = evaluarSolucion(solucion)
        if peso <= capacidad: 
            swarm.append(solucion)
            break

best_solucion = None
best_profit = 0
for _ in range(iterations):
    for i in range(worker_bees):
        solucion = swarm[i]
        profit, peso = evaluarSolucion(solucion)

        if peso > capacidad:
            profit = 0

        if profit > best_profit:
            best_profit = profit
            best_solucion = solucion

    profits = [evaluarSolucion(sol)[0] for sol in swarm]
    for i in range(onlooker_bees):
        selected = seleccionRuleta(swarm, profits)
        new_solucion = selected.copy()

        idx = np.random.randint(0, len(productos))
        if min_items[idx] <= new_solucion[idx] < max_items[idx]:
            new_solucion[idx] += -1 if np.random.uniform(0, 1) < 0.5 else 1

        profit, peso = evaluarSolucion(new_solucion)
        if peso <= capacidad and profit > evaluarSolucion(selected)[0]:
            swarm.append(new_solucion)
    swarm = swarm[:swarm_size]

if best_solucion is not None:
    print("Mejor solución encontrada:")
    for i in range(len(productos)):
        print(f"{productos[i]['name']}: {best_solucion[i]}")
    print(f"Beneficio total: {best_profit} galleons")
else:
    print("No se encontró una solución válida.")
