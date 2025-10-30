import simpy
import random
import numpy as np

# Parámetros de la simulación
NUM_AGENTES = 20
ANCHO_MUNDO = 100
ALTO_MUNDO = 100

TASA_RECUPERACION_NATURAL = 0.1
GASTO_POR_MOVIMIENTO = 0.05
EFECTO_INTERACCION = 0.2

NUM_PUESTOS_RECARGA = 5
ENERGIA_CRITICA = 2.0
TIEMPO_RECARGA = 10.0

TIEMPO_SIMULACION = 100
DT = 1.0

class Agente:
    def __init__(self, id, posicion_inicial, env, estacion_recarga):
        self.id = id
        self.posicion = np.array(posicion_inicial, dtype=float)
        self.velocidad = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.env = env
        self.estacion_recarga = estacion_recarga
        self.energia = 10.0
        
    def proceso_recarga(self):
        with self.estacion_recarga.request() as req:
            yield req
            yield self.env.timeout(TIEMPO_RECARGA)
            self.energia = 10.0
    
    def actualizar_estado(self):
        inflow = TASA_RECUPERACION_NATURAL * DT
        outflow = GASTO_POR_MOVIMIENTO * DT
        self.energia += inflow - outflow
        
        self.posicion += self.velocidad * DT
        
        if self.posicion[0] <= 0 or self.posicion[0] >= ANCHO_MUNDO:
            self.velocidad[0] *= -1
        if self.posicion[1] <= 0 or self.posicion[1] >= ALTO_MUNDO:
            self.velocidad[1] *= -1
        
        if self.energia < ENERGIA_CRITICA:
            self.env.process(self.proceso_recarga())