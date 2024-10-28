import numpy as np

def funcion(x, y):
    return x**2 + y**2 + 25 * (np.sin(x) + np.sin(y)) #funcion

#Parametros
numeroParticulas = 20
numeroIteraciones = 50
a = 0.8
b1 = 0.7 
b2 = 1.2  
limites = (-5, 5)

particulas = []
velocidades = []
for _ in range(numeroParticulas):
    x, y = np.random.uniform(limites[0], limites[1], 2)
    particulas.append([x, y])
    vx, vy = np.random.uniform(-1, 1, 2)
    velocidades.append([vx, vy])

pbest = particulas.copy()
pbest_valores = [funcion(x, y) for x, y in pbest]
indice_mejor = pbest_valores.index(min(pbest_valores))
gbest = pbest[indice_mejor].copy()
gbest_valor = pbest_valores[indice_mejor]

#PSO
for t in range(numeroIteraciones):
    print(f"\n--- Iteración {t+1} ---")
    for i in range(numeroParticulas):
        pos = particulas[i]
        vel = velocidades[i]

#Posicion y velocidad actual
        r1 = np.random.random()
        r2 = np.random.random()
        vel[0] = (a * vel[0] +
                  b1 * r1 * (pbest[i][0] - pos[0]) +
                  b2 * r2 * (gbest[0] - pos[0]))
        vel[1] = (a * vel[1] +
                  b1 * r1 * (pbest[i][1] - pos[1]) +
                  b2 * r2 * (gbest[1] - pos[1]))

        pos[0] += vel[0]
        pos[1] += vel[1]
        pos[0] = np.clip(pos[0], limites[0], limites[1])
        pos[1] = np.clip(pos[1], limites[0], limites[1])
        valor_actual = funcion(pos[0], pos[1])

        if valor_actual < pbest_valores[i]:
            pbest[i] = pos.copy()
            pbest_valores[i] = valor_actual

        if valor_actual < gbest_valor:
            gbest = pos.copy()
            gbest_valor = valor_actual

        print(f"Partícula {i+1}")
        print(f"  Posición: {pos}")
        print(f"  Velocidad: {vel}")
        print(f"  pbest: {pbest[i]}")
    print(f"Mejor valor global (gbest): {gbest_valor} en posición {gbest}\n")
