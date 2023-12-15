# Francesco Pio Nocerino
# loSpaccaBit
# Macchina vs Ostacoli, il gioco consiste nel spostare la macchinina grazie al sensore di neurosky
import pygame
from module.NeuroPy import NeuroPy
from tqdm import tqdm
import random
import sys

# Inizializza Pygame
pygame.init()

# Impostazioni della finestra
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("NeuroCar")

# Colori
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Dimensioni della macchinina
car_width = 50
car_height = 30

# Velocità della macchinina
car_speed = 5

# Inizializza la barra di avanzamento per il movimento della macchinina
car_position_bar = tqdm(total=width - car_width, desc="Posizione", position=0, leave=True)

# Variabile per la direzione della macchinina
car_direction = 0

# Inizializza il sensore NeuroPy
object1 = NeuroPy("porta_com", 115200, '7d55')

# Imposta i callback per i dati del sensore
def attention_callback(value):
    global car_direction
    if value > 50:
        car_direction = 1
    else: 
        car_direction = -1
    
def meditation_callback(value):
    pass

object1.setCallBack("attention", attention_callback)
object1.setCallBack("meditation", meditation_callback)

# Avvia il monitoraggio del sensore
object1.start()

# Inizializza variabili per gli ostacoli
obstacle_size = 30
obstacle_speed = 5
obstacle_frequency = 30  # Controllo della frequenza di generazione degli ostacoli
obstacles = []

# Variabile per il conteggio degli ostacoli colpiti
obstacle_hits = 0

# Funzione per generare un nuovo ostacolo
def generate_obstacle():
    obstacle_x = random.randint(0, width - obstacle_size)
    obstacle_y = 0
    obstacles.append((obstacle_x, obstacle_y))

score = 0

car_x = width//2
car_speed = 5
# Loop principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica tasti premuti
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genera ostacoli con una certa frequenza
    if random.randint(1, obstacle_frequency) == 1:
        generate_obstacle()

    # Muovi la macchinina
    try:
        car_x += car_direction * car_speed
        car_x = max(0, min(width - car_width, car_x))
        if car_x == 0 or car_x == width - car_width:
            car_direction *= -1  # Cambia la direzione quando tocca i bordi


    except ValueError as e:
        print(f"Errore durante il movimento della macchinina: {e}")
        running = False

    for i, obstacle in enumerate(obstacles):
        obstacle_x, obstacle_y = obstacle
        obstacle_y += obstacle_speed
        obstacles[i] = (obstacle_x, obstacle_y)
        if car_x < obstacle_x + obstacle_size and car_x + car_width > obstacle_x and height - car_height < obstacle_y + obstacle_size and height - car_height + car_height > obstacle_y:
            print("Ostacolo colpito!")
            obstacle_hits += 1
            if obstacle in obstacles:
                obstacles.remove(obstacle)
        elif obstacle_y > height - car_height:
            # Incrementa lo score solo quando l'ostacolo è superato
            score += 1


    # Rimuovi gli ostacoli usciti dallo schermo
    obstacles = [(x, y) for x, y in obstacles if y < height]

    # Verifica il conteggio degli ostacoli colpiti
    if obstacle_hits >= 3:
        print("Hai perso!")
        print("Il tuo punteggio è:", score)
        running = False

    # Disegna la macchinina, gli ostacoli e lo sfondo
    screen.fill(white)
    pygame.draw.rect(screen, black, [car_x, height - car_height, car_width, car_height])
    for obstacle in obstacles:
        pygame.draw.rect(screen, red, [obstacle[0], obstacle[1], obstacle_size, obstacle_size])

    # Disegna lo score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Aggiorna la barra di avanzamento
    car_position_bar.update(car_direction * car_speed)

    # Aggiorna lo schermo
    pygame.time.Clock().tick(30)

# Ferma il sensore NeuroPy
object1.stop()

# Chiudi la barra di avanzamento
car_position_bar.close()

# Chiudi la finestra di Pygame
pygame.quit()
sys.exit()
