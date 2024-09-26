import random

#datos
productos = [
    {"item": "Detonadores de señuelo", "peso": 4, "precio": 10},
    {"item": "Caramelos de fiebre", "peso": 2, "precio": 3},
    {"item": "Poción de amor", "peso": 2, "precio": 8},
    {"item": "Pastillas vomitivas", "peso": 1.5, "precio": 2},
    {"item": "Orejas extensibles", "peso": 5, "precio": 12},
    {"item": "Turrón sangrante", "peso": 1, "precio": 2},
    {"item": "Caja de bromas", "peso": 5, "precio": 6}
]

#restricciones
capacidadMochila = 30
pocionesAmor = 3
cajaBromas = 2

#parametros
tamañoPoblacion = 10
generaciones = 50
probCruce = 0.85
probMutacion = 0.1

#sumar el peso total
def calcularPeso(cromo):
    pesoTotal = 0
    for i in range(len(cromo)):
        pesoTotal += cromo[i] * productos[i]["peso"]
    return pesoTotal

#crear un cromsoma que cumpla las restricciones
def crearCromosoma():
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
    return cromosoma

# calcular valor total
def aptitud(cromosoma):
    pesoTotalal = calcularPeso(cromosoma)
    valorTotal = sum(cromosoma[i] * productos[i]["precio"] for i in range(len(cromosoma)))
    if pesoTotalal > capacidadMochila:
        return 0  
    if cromosoma[2] < pocionesAmor or cromosoma[6] < cajaBromas:
        return 0 
    return valorTotal

def seleccion(poblacion):
    poblacionOrdenada = sorted(poblacion, key=aptitud, reverse=True)
    return poblacionOrdenada[0], poblacionOrdenada[1]

#cruce entre dos padres
def cruce(p1, p2):
    punto = len(p1) // 2
    h1 = p1[:punto] + p2[punto:]
    h2 = p2[:punto] + p1[punto:]
    h1[2] = max(h1[2], pocionesAmor)
    h1[6] = max(h1[6], cajaBromas)
    h2[2] = max(h2[2], pocionesAmor)
    h2[6] = max(h2[6], cajaBromas)
    return h1, h2

#para no exceder capacidad
def mutar(cromo):
    if random.random() < probMutacion: 
        pesoActual = calcularPeso(cromo)
        for i in range(len(cromo)):
            if pesoActual >= capacidadMochila:
                break
            if i % 2 == 0:
                cromo[i] = max(0, cromo[i] - 1)  
            else:
                cromo[i] = min(10, cromo[i] + 1) 
        cromo[2] = max(cromo[2], pocionesAmor)  
        cromo[6] = max(cromo[6], cajaBromas)  
    return cromo

# algoritmo
def algoritmo():
    poblacion = [crearCromosoma() for _ in range(tamañoPoblacion)]
    for _ in range(generaciones):
        nuevaPoblacion = []
        for _ in range(tamañoPoblacion // 2):
            p1, p2 = seleccion(poblacion)
            if probCruce > 0.5:
                h1, h2 = cruce(p1, p2)
            else:
                h1, h2 = p1, p2
            nuevaPoblacion.append(mutar(h1))
            nuevaPoblacion.append(mutar(h2))
        poblacion = nuevaPoblacion
    mejor = max(poblacion, key=aptitud)
    return mejor, aptitud(mejor)
mejorSol, mejorVal = algoritmo()

print("Mejor solución:", mejorSol)
print("Valor total:", mejorVal)

#calculos
def calculos(cromosoma):
    print("\nDetalles de la solución ")
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