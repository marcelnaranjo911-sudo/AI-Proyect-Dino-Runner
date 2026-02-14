import copy
import random

def evolucionar(dinos, poblacion_size, DinoClass):

    dinos_ordenados = sorted(dinos, key=lambda d: d.fitness, reverse=True)
       
    top_10_dinos = dinos_ordenados[:10]
    
    padres = dinos_ordenados[:int(poblacion_size * 0.15)]
    
    nueva_poblacion = []
    
    campeon = DinoClass()
    campeon.cerebro = copy.deepcopy(top_10_dinos[0].cerebro)
    nueva_poblacion.append(campeon)
    
    while len(nueva_poblacion) < poblacion_size:
        padre = random.choice(padres)
        hijo = DinoClass()
        
        hijo.cerebro.W1 = copy.deepcopy(padre.cerebro.W1)
        hijo.cerebro.W2 = copy.deepcopy(padre.cerebro.W2)
        hijo.cerebro.b1 = copy.deepcopy(padre.cerebro.b1)
        hijo.cerebro.b2 = copy.deepcopy(padre.cerebro.b2)
        
        hijo.cerebro.mutar(0.12) 
        nueva_poblacion.append(hijo)
        
    return nueva_poblacion, top_10_dinos