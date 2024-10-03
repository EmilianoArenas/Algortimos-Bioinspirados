import random

# datos
productos = [
    {"item": "Detonadores de señuelo", "peso": 4, "precio": 10},
    {"item": "Caramelos de fiebre", "peso": 2, "precio": 3},
    {"item": "Poción de amor", "peso": 2, "precio": 8},
    {"item": "Pastillas vomitivas", "peso": 1.5, "precio": 2},
    {"item": "Orejas extensibles", "peso": 5, "precio": 12},
    {"item": "Turrón sangrante", "peso": 1, "precio": 2},
    {"item": "Caja de bromas", "peso": 5, "precio": 6}
]

# restricciones
capacidadMochila = 30
pocionesAmor = 3
cajaBromas = 2

# parámetros
tamañoPoblacion = 10
generaciones = 50
probCruce = 0.85
probMutacion = 0.1

# sumar el peso total
def calcularPeso(cromo):
    pesoTotal = 0
    for i in range(len(cromo)):
        pesoTotal += cromo[i] * productos[i]["peso"]
    return pesoTotal

# crear un cromosoma que cumpla las restricciones
def crearCromosoma():
    while True:  
        cromosoma = [0] * len(productos)
        cromosoma[2] = pocionesAmor
        cromosoma[6] = cajaBromas
        pesoActual = calcularPeso(cromosoma)
        for i in range(len(cromosoma)):
            if i != 2 and i != 6:
                while pesoActual < capacidadMochila:
                    incremento = random.randint(0, 1)
                    nuevoPeso = pesoActual + (incremento * productos[i]["peso"])
                    if nuevoPeso <= capacidadMochila:
                        cromosoma[i] += incremento
                        pesoActual = nuevoPeso
                    else:
                        break        
        if calcularPeso(cromosoma) <= capacidadMochila and cromosoma[2] >= pocionesAmor and cromosoma[6] >= cajaBromas:
            return cromosoma

# calcular valor total
def aptitud(cromosoma):
    return sum(cromosoma[i] * productos[i]["precio"] for i in range(len(cromosoma)))

# ruleta
def ruleta(poblacion):
    sumaAptitudes = sum(aptitud(cromo) for cromo in poblacion)
    seleccionados = []
    for _ in range(2):  
        pick = random.uniform(0, sumaAptitudes)
        actual = 0
        for cromo in poblacion:
            actual += aptitud(cromo)
            if actual >= pick:
                seleccionados.append(cromo)
                break
    return seleccionados[0], seleccionados[1]

# cruce
def cruce(p1, p2):
    h1 = []
    h2 = []
    for i in range(len(p1)):  
        if random.random() < 0.5:
            h1.append(p1[i])  
            h2.append(p2[i])  
        else:
            h1.append(p2[i])  
            h2.append(p1[i])  
    
    # Verificar restricciones 
    if h1[2] < pocionesAmor:
        h1[2] = pocionesAmor
    if h1[6] < cajaBromas:
        h1[6] = cajaBromas

    if h2[2] < pocionesAmor:
        h2[2] = pocionesAmor
    if h2[6] < cajaBromas:
        h2[6] = cajaBromas
    
    return h1, h2

# mutación
def mutar(cromo):
    if random.random() < probMutacion: 
        pesoActual = calcularPeso(cromo)
        for i in range(len(cromo)):
            if pesoActual >= capacidadMochila:
                break
            if i % 2 == 0:
                cromo[i] = max(0, cromo[i] - 1)  
                cromo[i] = min(10, cromo[i] + 1)  
        if cromo[2] < pocionesAmor:
            cromo[2] = pocionesAmor
        if cromo[6] < cajaBromas:
            cromo[6] = cajaBromas
    return cromo

# algoritmo
def algoritmo():
    poblacion = []    
    while len(poblacion) < tamañoPoblacion:
        cromosoma = crearCromosoma()
        poblacion.append(cromosoma)
    for _ in range(generaciones):
        nuevaPoblacion = []
        for _ in range(tamañoPoblacion // 2):
            p1, p2 = ruleta(poblacion)            
            if random.random() < probCruce:
                h1, h2 = cruce(p1, p2)
            else:
                h1, h2 = p1, p2            
            h1 = mutar(h1)
            h2 = mutar(h2)
            if calcularPeso(h1) <= capacidadMochila and h1[2] >= pocionesAmor and h1[6] >= cajaBromas:
                nuevaPoblacion.append(h1)
            if calcularPeso(h2) <= capacidadMochila and h2[2] >= pocionesAmor and h2[6] >= cajaBromas:
                nuevaPoblacion.append(h2)
        while len(nuevaPoblacion) < tamañoPoblacion:
            cromosoma = crearCromosoma()
            nuevaPoblacion.append(cromosoma)
        poblacion = nuevaPoblacion    
    mejor = max(poblacion, key=aptitud)
    return mejor, aptitud(mejor)

mejorSol, mejorVal = algoritmo()

print("Mejor solución:", mejorSol)
print("Valor total:", mejorVal)

# cálculos
def calculos(cromosoma):
    print("\nDetalles de la solución")
    pesoTotalal = 0
    valorTotal = 0
    print(f"{'Producto':<20} {'Cantidad':<10} {'Peso unitario':<15} {'Peso total':<15} {'Valor total':<15}")
    for i in range(len(productos)):
        cantidad = cromosoma[i]
        pesoUni = productos[i]["peso"]
        valorUni = productos[i]["precio"]
        pesoProd = cantidad * pesoUni
        valorProd = cantidad * valorUni
        pesoTotalal += pesoProd
        valorTotal += valorProd
        print(f"{productos[i]['item']:<20} {cantidad:<10} {pesoUni:<15} {pesoProd:<15} {valorProd:<15}")
    print(f"\nPeso total de la mochila: {pesoTotalal} libras")
    print(f"Valor total de la mochila: {valorTotal} galeones")
    return pesoTotalal, valorTotal

calculos(mejorSol)
