import pygame
import random
import os 
from juego import Dinosaurio, Obstaculo, ANCHO, ALTO
from evolucion import evolucionar

POBLACION_SIZE = 500
FPS = 60

class DinoIA(Dinosaurio):
    def __init__(self):
        super().__init__()
        from red_neuronal import RedNeuronal
        self.cerebro = RedNeuronal()
        self.fitness = 0
        self.vivo = True

def dibujar_texto(ventana, texto, x, y, tamano=30, color=(0,0,0)):
    fuente = pygame.font.SysFont("Arial", tamano, bold=True)
    img = fuente.render(texto, True, color)
    rect = img.get_rect(center=(x, y))
    ventana.blit(img, rect)

def modo_entrenamiento(ventana, reloj):
   
    dinos = [DinoIA() for _ in range(POBLACION_SIZE)]
    
    cargados = 0
    for i in range(10): 
        archivo = f"top_dino_{i}.npz"
        if os.path.exists(archivo):
            if dinos[i].cerebro.cargar(archivo):
                cargados += 1
    
    print(f"--- INICIO ENTRENAMIENTO: Se cargaron {cargados} cerebros previos ---")
    
    velocidad = 7
    puntos = 0
    generacion = 1
    tiempo_spawn = 0
    obstaculos = []

    corriendo = True
    while corriendo:
        ventana.fill((255, 255, 255))
        pygame.draw.line(ventana, (0,0,0), (0, 350), (ANCHO, 350), 2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); return 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: 
                    corriendo = False

        if tiempo_spawn <= 0:
            obstaculos.append(Obstaculo(velocidad))
            tiempo_spawn = random.randint(30, 90)
        else:
            tiempo_spawn -= 1

        proximo_obs = None
        for obs in obstaculos[:]:
            obs.actualizar(velocidad)
            obs.dibujar(ventana)
            if obs.x < -100:
                obstaculos.remove(obs)
                puntos += 1
            if obs.x + obs.ancho > 60 and proximo_obs is None:
                proximo_obs = obs
        
        if proximo_obs is None:
            proximo_obs = Obstaculo(velocidad)
            proximo_obs.x = 2000

        dinos_vivos = 0
        for dino in dinos:
            if dino.vivo:
                dinos_vivos += 1
                dino.fitness += 1
                
                inputs = [
                    velocidad / 20.0,
                    (proximo_obs.x - dino.x) / ANCHO,
                    proximo_obs.y / ALTO,
                    proximo_obs.ancho / 100.0,
                    proximo_obs.alto / 100.0,
                    dino.y / ALTO,
                    dino.vel_y / 20.0
                ]
                
                output = dino.cerebro.pensar(inputs)
                
                if output[0] > 0.5:
                    dino.saltar(output[1] > 0.5)
                
                dino.actualizar()
                dino.dibujar(ventana)

                if pygame.Rect(dino.x, dino.y, dino.ancho, dino.alto).colliderect(
                    pygame.Rect(proximo_obs.x, proximo_obs.y, proximo_obs.ancho, proximo_obs.alto)):
                    dino.vivo = False
                    dino.fitness -= 5

        if dinos_vivos == 0:
            
            dinos, top_10_anteriores = evolucionar(dinos, POBLACION_SIZE, DinoIA)
            
            print(f"Gen {generacion} terminada. Guardando Top 10...")
            for i, mejor_dino in enumerate(top_10_anteriores):
                mejor_dino.cerebro.guardar(f"top_dino_{i}.npz")
            
            generacion += 1
            obstaculos = []
            tiempo_spawn = 0
            velocidad = 7
            puntos = 0

        dibujar_texto(ventana, f"GEN: {generacion}", 100, 30)
        dibujar_texto(ventana, f"VIVOS: {dinos_vivos}", 100, 60)
        
            
        dibujar_texto(ventana, "ESC para Menú", ANCHO//2, 380, 20, (100,100,100))

        if puntos > 0 and puntos % 500 == 0:
            velocidad += 0.2

        pygame.display.update()
        reloj.tick(FPS)

def modo_prueba(ventana, reloj):
    dino = DinoIA()
    
    exito = dino.cerebro.cargar("top_dino_0.npz")
    
    if not exito:
        print("No hay datos guardados para probar.")
        return 

    obstaculos = []
    velocidad = 7
    tiempo_spawn = 0
    puntos = 0
    game_over = False

    while True:
        ventana.fill((240, 240, 255))
        pygame.draw.line(ventana, (0,0,0), (0, 350), (ANCHO, 350), 2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: return

        if not game_over:
            if tiempo_spawn <= 0:
                obstaculos.append(Obstaculo(velocidad))
                tiempo_spawn = random.randint(30, 90)
            else:
                tiempo_spawn -= 1

            proximo_obs = None
            for obs in obstaculos[:]:
                obs.actualizar(velocidad)
                obs.dibujar(ventana)
                if obs.x < -100:
                    obstaculos.remove(obs)
                    puntos += 1
                if obs.x + obs.ancho > 60 and proximo_obs is None:
                    proximo_obs = obs
            
            if proximo_obs is None: 
                proximo_obs = Obstaculo(velocidad)
                proximo_obs.x = 2000

            inputs = [
                velocidad / 20.0,
                (proximo_obs.x - dino.x) / ANCHO,
                proximo_obs.y / ALTO,
                proximo_obs.ancho / 100.0,
                proximo_obs.alto / 100.0,
                dino.y / ALTO,
                dino.vel_y / 20.0
            ]
            
            output = dino.cerebro.pensar(inputs)
            if output[0] > 0.5:
                dino.saltar(output[1] > 0.5)
            
            dino.actualizar()
            dino.dibujar(ventana)

            if pygame.Rect(dino.x, dino.y, dino.ancho, dino.alto).colliderect(
                pygame.Rect(proximo_obs.x, proximo_obs.y, proximo_obs.ancho, proximo_obs.alto)):
                game_over = True
        
        else:
            dibujar_texto(ventana, "¡CHOQUE!", ANCHO//2, ALTO//2, 50, (255,0,0))
            dibujar_texto(ventana, "ESC para salir", ANCHO//2, ALTO//2 + 50, 30)

        dibujar_texto(ventana, f"SCORE: {puntos}", 100, 30, 20, color=(0,0,150))
        
        pygame.display.update()
        reloj.tick(FPS)

def menu_principal():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Dino IA - Menú Principal")
    reloj = pygame.time.Clock()

    while True:
        ventana.fill((255, 255, 255))
        
        dibujar_texto(ventana, "PROYECTO DINO IA", ANCHO//2, 80, 50)
        
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        btn_train = pygame.Rect(ANCHO//2 - 100, 150, 200, 50)
        color_train = (100, 200, 100) if btn_train.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(ventana, color_train, btn_train)
        dibujar_texto(ventana, "ENTRENAR", ANCHO//2, 175, 25)

        btn_test = pygame.Rect(ANCHO//2 - 100, 230, 200, 50)
        color_test = (100, 100, 200) if btn_test.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(ventana, color_test, btn_test)
        dibujar_texto(ventana, "VER MEJOR IA", ANCHO//2, 255, 25)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_train.collidepoint(mouse_pos):
                    modo_entrenamiento(ventana, reloj)
                if btn_test.collidepoint(mouse_pos):
                    modo_prueba(ventana, reloj)

        pygame.display.update()
        reloj.tick(FPS)

if __name__ == "__main__":
    menu_principal()