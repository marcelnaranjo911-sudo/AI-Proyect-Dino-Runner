import pygame
import random

ANCHO = 800
ALTO = 400
SUELO = 350

class Obstaculo:
    def __init__(self, velocidad, tipo_forzado=None):
        self.velocidad = velocidad
        self.x = ANCHO + random.randint(0, 100)
        
        opcion = tipo_forzado if tipo_forzado else random.choices([0, 1, 2, 3], weights=[40, 30, 15, 15])[0]
        
        if opcion == 3: 
            self.tipo = "pajaro"
            self.ancho = 50
            self.alto = 35
            self.y = random.choice([SUELO - 35, SUELO - 80, SUELO - 110])
            self.color = (0, 100, 255)
        elif opcion == 2: 
            self.tipo = "grupo"
            self.ancho = 70
            self.alto = 50
            self.y = SUELO - self.alto
            self.color = (200, 0, 50)
        elif opcion == 1: 
            self.tipo = "cactus_grande"
            self.ancho = 40
            self.alto = 70
            self.y = SUELO - self.alto
            self.color = (0, 150, 0)
        else: 
            self.tipo = "cactus"
            self.ancho = 30
            self.alto = 45
            self.y = SUELO - self.alto
            self.color = (0, 200, 0)

    def actualizar(self, velocidad):
        self.x -= velocidad 

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.alto))

class Dinosaurio:
    def __init__(self):
        self.x = 60
        self.y = SUELO - 40
        self.ancho = 40
        self.alto = 40
        
        self.vel_y = 0
        self.en_aire = False
        self.gravedad_normal = 0.8
        self.gravedad_fuerte = 2.5
        self.fuerza_salto = -14

    def saltar(self, sosteniendo):
        if not self.en_aire:
            self.en_aire = True
            self.vel_y = self.fuerza_salto
        
        if self.en_aire and self.vel_y < 0 and not sosteniendo:
             self.vel_y += (self.gravedad_fuerte - self.gravedad_normal)

    def actualizar(self):
        self.vel_y += self.gravedad_normal
        self.y += self.vel_y

        if self.y >= SUELO - self.alto:
            self.y = SUELO - self.alto
            self.vel_y = 0
            self.en_aire = False

    def dibujar(self, ventana):
        color = (100, 100, 100)
        pygame.draw.rect(ventana, color, (self.x, self.y, self.ancho, self.alto))