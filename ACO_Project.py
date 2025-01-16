import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
import time
import random

@dataclass
class Ruta:
    camino: List[int]
    distancia: float
    costo: float
    score: float

def crear_matriz_adyacencia():
    #Crea una matriz de adyacencia que representa las conexiones reales por carretera entre estados.
    estados = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", 
        "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", 
        "Colima", "Durango", "Estado de México", "Guanajuato", 
        "Guerrero", "Hidalgo", "Jalisco", "Michoacán", 
        "Morelos", "Nayarit", "Nuevo León", "Oaxaca", 
        "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
        "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", 
        "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
    ]
    
    num_estados = len(estados)
    matriz = np.zeros((num_estados, num_estados), dtype=bool)
    
    conexiones = {
        "Aguascalientes": ["Zacatecas", "Jalisco", "San Luis Potosí"],
        "Baja California": ["Sonora"],
        "Baja California Sur": ["Baja California"],
        "Campeche": ["Yucatán", "Quintana Roo", "Tabasco"],
        "Chiapas": ["Oaxaca", "Veracruz", "Tabasco"],
        "Chihuahua": ["Sonora", "Sinaloa", "Durango", "Coahuila"],
        "Ciudad de México": ["Estado de México", "Morelos"],
        "Coahuila": ["Chihuahua", "Durango", "Nuevo León", "Zacatecas", "San Luis Potosí"],
        "Colima": ["Jalisco", "Michoacán"],
        "Durango": ["Chihuahua", "Sinaloa", "Nayarit", "Zacatecas", "Coahuila"],
        "Estado de México": ["Ciudad de México", "Morelos", "Guerrero", "Michoacán", 
                           "Querétaro", "Hidalgo", "Tlaxcala", "Puebla"],
        "Guanajuato": ["San Luis Potosí", "Querétaro", "Michoacán", "Jalisco"],
        "Guerrero": ["Estado de México", "Morelos", "Puebla", "Oaxaca", "Michoacán"],
        "Hidalgo": ["Estado de México", "San Luis Potosí", "Veracruz", "Puebla", 
                    "Tlaxcala", "Querétaro"],
        "Jalisco": ["Nayarit", "Zacatecas", "Aguascalientes", "Guanajuato", 
                    "Michoacán", "Colima"],
        "Michoacán": ["Colima", "Jalisco", "Guanajuato", "Querétaro", 
                      "Estado de México", "Guerrero"],
        "Morelos": ["Ciudad de México", "Estado de México", "Guerrero", "Puebla"],
        "Nayarit": ["Sinaloa", "Durango", "Zacatecas", "Jalisco"],
        "Nuevo León": ["Coahuila", "San Luis Potosí", "Tamaulipas"],
        "Oaxaca": ["Guerrero", "Puebla", "Veracruz", "Chiapas"],
        "Puebla": ["Tlaxcala", "Hidalgo", "Estado de México", "Morelos", 
                   "Guerrero", "Oaxaca", "Veracruz"],
        "Querétaro": ["Guanajuato", "San Luis Potosí", "Hidalgo", 
                      "Estado de México", "Michoacán"],
        "Quintana Roo": ["Yucatán", "Campeche"],
        "San Luis Potosí": ["Nuevo León", "Tamaulipas", "Veracruz", "Hidalgo", 
                           "Querétaro", "Guanajuato", "Zacatecas", "Coahuila"],
        "Sinaloa": ["Sonora", "Chihuahua", "Durango", "Nayarit"],
        "Sonora": ["Baja California", "Chihuahua", "Sinaloa"],
        "Tabasco": ["Veracruz", "Chiapas", "Campeche"],
        "Tamaulipas": ["Nuevo León", "San Luis Potosí", "Veracruz"],
        "Tlaxcala": ["Puebla", "Hidalgo", "Estado de México"],
        "Veracruz": ["Tamaulipas", "San Luis Potosí", "Hidalgo", "Puebla", 
                     "Oaxaca", "Chiapas", "Tabasco"],
        "Yucatán": ["Quintana Roo", "Campeche"],
        "Zacatecas": ["Durango", "Coahuila", "San Luis Potosí", "Aguascalientes", 
                      "Jalisco", "Nayarit"]
    }
    
    for estado, vecinos in conexiones.items():
        idx_estado = estados.index(estado)
        for vecino in vecinos:
            idx_vecino = estados.index(vecino)
            matriz[idx_estado][idx_vecino] = True
            matriz[idx_vecino][idx_estado] = True
            
    return matriz

class ACO:
    def __init__(self, 
                 distancias: np.ndarray, 
                 costos: np.ndarray,
                 matriz_adyacencia: np.ndarray,
                 num_hormigas: int = 30,
                 alfa: float = 1.0,
                 beta: float = 2.0,
                 rho: float = 0.1,
                 q: float = 1.0,
                 peso_distancia: float = 0.5):
        self.distancias = distancias
        self.costos = costos
        self.matriz_adyacencia = matriz_adyacencia
        self.num_ciudades = len(distancias)
        self.num_hormigas = num_hormigas
        self.alfa = alfa
        self.beta = beta
        self.rho = rho
        self.q = q
        self.peso_distancia = peso_distancia
        self.dist_max = np.max(distancias[distancias > 0])
        self.cost_max = np.max(costos[costos > 0])        
        self.distancias_norm = np.where(distancias > 0, distancias / self.dist_max, 1)
        self.costos_norm = np.where(costos > 0, costos / self.cost_max, 1)
        self.feromonas = np.ones((self.num_ciudades, self.num_ciudades)) * 0.1
        self.todas_rutas = []  

    def calcular_heuristica(self, ciudad_actual: int, ciudad_siguiente: int) -> float:
        dist_norm = self.distancias_norm[ciudad_actual][ciudad_siguiente]
        cost_norm = self.costos_norm[ciudad_actual][ciudad_siguiente]        
        if dist_norm == 0 or cost_norm == 0:
            return 0.0
        return 1.0 / (self.peso_distancia * dist_norm + (1 - self.peso_distancia) * cost_norm)
    
    def ruleta_probabilidad(self, probabilidades: np.ndarray, ciudades_adyacentes: Set[int]) -> int:
        prob_adyacentes = [probabilidades[ciudad] for ciudad in ciudades_adyacentes]
        suma_prob = sum(prob_adyacentes)
        if suma_prob == 0:
            return list(ciudades_adyacentes)[0]        
        prob_normalizadas = [prob / suma_prob for prob in prob_adyacentes]
        # Implementar ruleta
        punto_ruleta = np.random.random()
        suma_acumulada = 0
        for i, prob in enumerate(prob_normalizadas):
            suma_acumulada += prob
            if punto_ruleta <= suma_acumulada:
                return list(ciudades_adyacentes)[i]
        return list(ciudades_adyacentes)[-1]
        
    def seleccionar_siguiente_ciudad(self, ciudad_actual: int, ciudades_no_visitadas: Set[int]) -> int:
        ciudades_adyacentes = {
            ciudad for ciudad in ciudades_no_visitadas 
            if self.matriz_adyacencia[ciudad_actual][ciudad]
        }
        
        if not ciudades_adyacentes:
            return -1
            
        probabilidades = np.zeros(self.num_ciudades)
        
        for ciudad in ciudades_adyacentes:
            heuristica = self.calcular_heuristica(ciudad_actual, ciudad)
            probabilidades[ciudad] = (self.feromonas[ciudad_actual][ciudad] ** self.alfa) * \
                                   (heuristica ** self.beta)
        
        return self.ruleta_probabilidad(probabilidades, ciudades_adyacentes)
    
    def construir_ruta(self, ciudad_inicio: int, ciudad_destino: int) -> Ruta:
        ruta = [ciudad_inicio]
        ciudades_no_visitadas = set(range(self.num_ciudades)) - {ciudad_inicio}
        ciudad_actual = ciudad_inicio
        
        while ciudades_no_visitadas and ciudad_destino not in ruta:
            siguiente_ciudad = self.seleccionar_siguiente_ciudad(ciudad_actual, ciudades_no_visitadas)
            if siguiente_ciudad == -1:
                break
            ruta.append(siguiente_ciudad)
            ciudades_no_visitadas.remove(siguiente_ciudad)
            ciudad_actual = siguiente_ciudad
            
            if siguiente_ciudad == ciudad_destino:
                break
        
        if ciudad_destino in ruta:
            idx_destino = ruta.index(ciudad_destino)
            ruta = ruta[:idx_destino + 1]
            
            distancia = sum(self.distancias[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
            costo = sum(self.costos[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
            
            # Calcular score con normalización
            score = self.peso_distancia * (distancia/self.dist_max) + \
                    (1 - self.peso_distancia) * (costo/self.cost_max)
            
            return Ruta(ruta, distancia, costo, score)
        return None
    
    def actualizar_feromonas(self, rutas: List[Ruta]):
        self.feromonas *= (1 - self.rho)        
        for ruta in rutas:
            if ruta is not None:
                delta = self.q / ruta.score
                for i in range(len(ruta.camino) - 1):
                    self.feromonas[ruta.camino[i]][ruta.camino[i+1]] += delta
                    self.feromonas[ruta.camino[i+1]][ruta.camino[i]] += delta        
        self.feromonas = np.clip(self.feromonas, 0.1, 2.0)
    
    def encontrar_rutas(self, 
                       ciudad_inicio: int, 
                       ciudad_destino: int,
                       num_iteraciones: int = 150) -> List[Ruta]:
        self.todas_rutas = []
        
        for iteracion in range(num_iteraciones):
            rutas_iteracion = []
            rutas_encontradas = 0
            
            for _ in range(self.num_hormigas):
                ruta = self.construir_ruta(ciudad_inicio, ciudad_destino)
                if ruta is not None:
                    rutas_iteracion.append(ruta)
                    rutas_encontradas += 1
                    if ruta not in self.todas_rutas:
                        self.todas_rutas.append(ruta)
            
            print(f"Rutas encontradas en esta iteración: {rutas_encontradas}")
            
            if rutas_iteracion:
                self.actualizar_feromonas(rutas_iteracion)
        
        return list(self.todas_rutas)
    
class RutasMexico:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de Rutas - México")
        
        # Datos de estados y coordenadas
        self.estados = [
            "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", 
            "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", 
            "Colima", "Durango", "Estado de México", "Guanajuato", 
            "Guerrero", "Hidalgo", "Jalisco", "Michoacán", 
            "Morelos", "Nayarit", "Nuevo León", "Oaxaca", 
            "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
            "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", 
            "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
        ]
        
        self.coordenadas = {
            "Aguascalientes": (-102.296, 21.882),
            "Baja California": (-116.596, 32.624),
            "Baja California Sur": (-110.310, 24.142),
            "Campeche": (-90.534, 19.844),
            "Chiapas": (-93.129, 16.754),
            "Chihuahua": (-106.069, 28.635),
            "Ciudad de México": (-99.133, 19.433),
            "Coahuila": (-100.964, 25.421),
            "Colima": (-103.724, 19.245),
            "Durango": (-104.670, 24.024),
            "Estado de México": (-99.631, 19.290),
            "Guanajuato": (-101.687, 21.019),
            "Guerrero": (-99.500, 17.547),
            "Hidalgo": (-98.763, 20.117),
            "Jalisco": (-103.344, 20.667),
            "Michoacán": (-101.184, 19.702),
            "Morelos": (-99.070, 18.921),
            "Nayarit": (-104.895, 21.505),
            "Nuevo León": (-100.309, 25.687),
            "Oaxaca": (-96.726, 17.073),
            "Puebla": (-98.207, 19.042),
            "Querétaro": (-100.390, 20.589),
            "Quintana Roo": (-88.296, 19.577),
            "San Luis Potosí": (-100.985, 22.156),
            "Sinaloa": (-107.398, 24.809),
            "Sonora": (-110.956, 29.073),
            "Tabasco": (-92.948, 17.989),
            "Tamaulipas": (-97.878, 23.735),
            "Tlaxcala": (-98.236, 19.318),
            "Veracruz": (-96.927, 19.174),
            "Yucatán": (-89.620, 20.967),
            "Zacatecas": (-102.583, 22.771)
        }
        
        self.crear_matrices()        
        self.imprimir_matriz_adyacencia()        
        self.crear_interfaz()
    
    def crear_matrices(self):
        num_estados = len(self.estados)
        self.matriz_distancias = np.zeros((num_estados, num_estados))
        self.matriz_costos = np.zeros((num_estados, num_estados))
        self.matriz_adyacencia = crear_matriz_adyacencia()
    
        COSTO_POR_KM = 20
        FACTOR_TERRENO = 1.2 
    
        for i in range(num_estados):
            for j in range(num_estados):
                if i != j and self.matriz_adyacencia[i][j]:
                    coord1 = self.coordenadas[self.estados[i]]
                    coord2 = self.coordenadas[self.estados[j]]
                
                    # Calcular distancia usando fórmula haversine
                    lon1, lat1 = coord1
                    lon2, lat2 = coord2
                    R = 6371  # Radio de la Tierra en km
                    dlon = np.radians(lon2 - lon1)
                    dlat = np.radians(lat2 - lat1)
                    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * \
                    np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
                    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
                    distancia = R * c                
                    self.matriz_distancias[i][j] = distancia
                    self.matriz_costos[i][j] = distancia * COSTO_POR_KM * FACTOR_TERRENO
    
    def imprimir_matriz_adyacencia(self):
        print("\nMatriz de Adyacencia con Distancias (km):")    
        print("     ", end="")
        for estado in self.estados:
            print(f"{estado[:4]:>7}", end="")
        print("\n" + "-" * (7 * len(self.estados) + 5))

        for i, estado1 in enumerate(self.estados):
            print(f"{estado1[:4]:<5}", end="")
            for j, estado2 in enumerate(self.estados):
                if i == j:
                    print("    -  ", end="")
                elif self.matriz_adyacencia[i][j]:
                    print(f"{self.matriz_distancias[i][j]:7.1f}", end="")
                else:
                    print("    -  ", end="")
            print()
    
        print("\nMatriz de Adyacencia con Costos (pesos):")    
        print("     ", end="")
        for estado in self.estados:
            print(f"{estado[:4]:>10}", end="")
        print("\n" + "-" * (10 * len(self.estados) + 5))    
        for i, estado1 in enumerate(self.estados):
            print(f"{estado1[:4]:<5}", end="")
            for j, estado2 in enumerate(self.estados):
                if i == j:
                    print("     -    ", end="")
                elif self.matriz_adyacencia[i][j]:
                    print(f"{self.matriz_costos[i][j]:10.2f}", end="")
                else:
                    print("     -    ", end="")
            print()
    
        print("\nResumen de Matrices:")
        print(f"Distancia máxima: {np.max(self.matriz_distancias):.2f} km")
        print(f"Costo máximo: ${np.max(self.matriz_costos):.2f}")    
        print("\nRutas de ejemplo:")
        for _ in range(3):
            idx_inicio = np.random.randint(len(self.estados))
            idx_fin = np.random.randint(len(self.estados))
        
            if idx_inicio != idx_fin and self.matriz_adyacencia[idx_inicio][idx_fin]:
                estado_inicio = self.estados[idx_inicio]
                estado_fin = self.estados[idx_fin]
                distancia = self.matriz_distancias[idx_inicio][idx_fin]
                costo = self.matriz_costos[idx_inicio][idx_fin]
            
                print(f"{estado_inicio} → {estado_fin}: {distancia:.1f} km, Costo: ${costo:.2f}")
        
    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)        
        ttk.Label(control_frame, text="Origen:").grid(row=0, column=0, padx=5, pady=5)
        self.origen_var = tk.StringVar()
        self.origen_combo = ttk.Combobox(control_frame, textvariable=self.origen_var, width=30)
        self.origen_combo['values'] = self.estados
        self.origen_combo.grid(row=0, column=1, padx=5, pady=5)        
        ttk.Label(control_frame, text="Destino:").grid(row=1, column=0, padx=5, pady=5)
        self.destino_var = tk.StringVar()
        self.destino_combo = ttk.Combobox(control_frame, textvariable=self.destino_var, width=30)
        self.destino_combo['values'] = self.estados
        self.destino_combo.grid(row=1, column=1, padx=5, pady=5)        
        ttk.Button(control_frame, text="Buscar Rutas", command=self.buscar_ruta).grid(
            row=2, column=0, columnspan=2, pady=10)        
        self.tipos_frame = ttk.LabelFrame(control_frame, text="Tipos de Rutas", padding="5")
        self.tipos_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))        
        self.ruta_seleccionada_var = tk.StringVar(value="optima")        
        self.info_frame = ttk.Frame(control_frame)
        self.info_frame.grid(row=4, column=0, columnspan=2, pady=10)        
        self.map_frame = ttk.Frame(main_frame)
        self.map_frame.grid(row=0, column=1, padx=5, pady=5)        
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas.get_tk_widget().pack()        
        self.actualizar_mapa_base()
    
    def mostrar_info_ruta(self, ruta: Ruta, color: str, numero: int, tipo: str):
        frame_ruta = ttk.Frame(self.info_frame)
        frame_ruta.pack(pady=5, fill='x')        
        radio = ttk.Radiobutton(frame_ruta, 
                               text=tipo.capitalize(),
                               variable=self.ruta_seleccionada_var,
                               value=tipo,
                               command=self.actualizar_visualizacion)
        radio.pack(side='left', padx=2)        
        color_label = ttk.Label(frame_ruta, text="■", foreground=color)
        color_label.pack(side='left', padx=2)        
        info_text = f"Distancia: {ruta.distancia:.1f}km, Costo: ${ruta.costo:.2f}"
        info_label = ttk.Label(frame_ruta, text=info_text)
        info_label.pack(side='left', padx=2)        
        frame_recorrido = ttk.Frame(frame_ruta)
        frame_recorrido.pack(pady=2, fill='x')
        ruta_text = " → ".join(self.estados[i] for i in ruta.camino)
        ttk.Label(frame_recorrido, text=f"Recorrido: {ruta_text}", wraplength=600).pack()
    
    def actualizar_mapa_base(self):
        self.ax.clear()        
        for i in range(len(self.estados)):
            for j in range(i + 1, len(self.estados)):
                if self.matriz_adyacencia[i][j]:
                    coord1 = self.coordenadas[self.estados[i]]
                    coord2 = self.coordenadas[self.estados[j]]
                    self.ax.plot([coord1[0], coord2[0]], 
                               [coord1[1], coord2[1]], 
                               'gray', alpha=0.2, linewidth=1)        
        for estado, coord in self.coordenadas.items():
            self.ax.plot(coord[0], coord[1], 'ko', markersize=5)
            self.ax.annotate(estado, (coord[0], coord[1]), 
                           xytext=(5, 5), 
                           textcoords='offset points', 
                           fontsize=8)
        
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('Mapa de Estados de México')
    
    def ordenar_rutas(self, rutas: List[Ruta]) -> Dict[str, Ruta]:
        rutas_validas = [r for r in rutas if r is not None]    
        if not rutas_validas:
            return {}    
        distancias = [r.distancia for r in rutas_validas]
        costos = [r.costo for r in rutas_validas]    
        dist_min, dist_max = min(distancias), max(distancias)
        costo_min, costo_max = min(costos), max(costos)

        def calcular_score_compuesto(ruta):
            dist_normalizada = (ruta.distancia - dist_min) / (dist_max - dist_min)
            costo_normalizado = (ruta.costo - costo_min) / (costo_max - costo_min)
            return dist_normalizada * 0.7 + costo_normalizado * 0.3 + \
                (0.2 if dist_normalizada > 0.7 else 0) + \
                (0.2 if costo_normalizado > 0.7 else 0)    
        rutas_ordenadas_por_score = sorted(rutas_validas, key=calcular_score_compuesto)    
        ruta_barata = min(rutas_validas, key=lambda x: x.costo)    
        rutas_no_baratas = [r for r in rutas_ordenadas_por_score if r != ruta_barata]
    
        return {
            "Ruta 1": rutas_no_baratas[0],  
            "1 divertida": rutas_no_baratas[len(rutas_no_baratas)//2],  
            "2 divertida": max(rutas_validas, key=lambda x: x.distancia), 
            "Optima": ruta_barata  # Más barata
        }
    
    def actualizar_visualizacion(self):
        if not hasattr(self, 'rutas_actuales'):
            return
            
        tipo_seleccionado = self.ruta_seleccionada_var.get()
        ruta = self.rutas_actuales[tipo_seleccionado]        
        self.ax.clear()
        self.actualizar_mapa_base()
        
        colores = {
            "Ruta 1": 'blue',
            "1 divertida": 'purple',
            "2 divertida": 'orange',
            "Optima": 'green'
        }
        
        puntos_x = [self.coordenadas[self.estados[i]][0] for i in ruta.camino]
        puntos_y = [self.coordenadas[self.estados[i]][1] for i in ruta.camino]
        self.ax.plot(puntos_x, puntos_y, 
                     c=colores.get(tipo_seleccionado, 'blue'), 
                     linewidth=3, 
                     alpha=0.8, 
                     label=f'Ruta {tipo_seleccionado}')
        
        origen_coord = self.coordenadas[self.estados[ruta.camino[0]]]
        destino_coord = self.coordenadas[self.estados[ruta.camino[-1]]]
        self.ax.plot(origen_coord[0], origen_coord[1], 'go', markersize=10, label='Origen')
        self.ax.plot(destino_coord[0], destino_coord[1], 'ro', markersize=10, label='Destino')
        self.ax.legend()
        self.canvas.draw()
    
    def buscar_ruta(self):
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        origen = self.origen_var.get()
        destino = self.destino_var.get()
        
        if not origen or not destino:
            messagebox.showwarning("Error", "Por favor seleccione origen y destino")
            return
        
        if origen == destino:
            messagebox.showwarning("Error", "El origen y destino deben ser diferentes")
            return
            
        idx_origen = self.estados.index(origen)
        idx_destino = self.estados.index(destino)
        
        aco = ACO(self.matriz_distancias, 
                  self.matriz_costos,
                  self.matriz_adyacencia,
                  num_hormigas=30,
                  peso_distancia=0.5)
        
        print(f"\nBuscando rutas de {origen} a {destino}...")
        tiempo_inicio = time.time()
        todas_rutas = aco.encontrar_rutas(idx_origen, idx_destino, num_iteraciones=150)
        tiempo_total = time.time() - tiempo_inicio
        print(f"Tiempo de búsqueda: {tiempo_total:.2f} segundos")
        
        if not todas_rutas:
            messagebox.showerror("Error", "No se encontraron rutas válidas")
            return
        
        self.rutas_actuales = self.ordenar_rutas(todas_rutas)
        
        colores = {
            "Ruta 1": 'blue',
            "1 divertida": 'purple',
            "2 divertida": 'orange',
            "Optima": 'green'
        }
        
        for tipo, ruta in self.rutas_actuales.items():
            self.mostrar_info_ruta(ruta, colores.get(tipo, 'blue'), 1, tipo)
            print(f"\nRuta {tipo}:")
            print(f"Distancia: {ruta.distancia:.2f} km")
            print(f"Costo: ${ruta.costo:.2f}")
            print("Camino:", " → ".join(self.estados[i] for i in ruta.camino))        
        self.ruta_seleccionada_var.set("Optima")
        self.actualizar_visualizacion()

if __name__ == "__main__":
    root = tk.Tk()
    app = RutasMexico(root)
    root.mainloop()
