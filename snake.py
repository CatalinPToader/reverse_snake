import time
import pygame
import sys
import random

#variables

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
BACKGROUND = (50, 50, 50)
CELL_WALL = (200, 200, 200)
CELL_SIZE = 40
player_pos = [0, 0]
player_size = 19
close = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player_pos = calc_player_pos()

    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            x = player_pos[0]
            y = player_pos[1]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    y -= CELL_SIZE
                elif event.key == pygame.K_s:
                    y += CELL_SIZE
                elif event.key == pygame.K_d:
                    x += CELL_SIZE
                elif event.key == pygame.K_a:
                    x -= CELL_SIZE

                player_pos = [x, y]
            
        screen.fill(BACKGROUND)
        draw_grid(screen)
                
        pygame.draw.circle(screen, RED, player_pos, player_size)
        
        pygame.display.update()

# Draw the background grid the game plays on
def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, CELL_WALL, rect, 1)

# Get a random start position for player
def calc_player_pos():
    posX = 0
    posY = 0
    
    cellsX = WIDTH / CELL_SIZE
    cellsY = HEIGHT / CELL_SIZE
    
    startX = random.randint(0, cellsX - 1)
    startY = random.randint(0, cellsY - 1)
    
    posX = startX * CELL_SIZE + CELL_SIZE / 2
    posY = startY * CELL_SIZE + CELL_SIZE / 2
        
    return (posX, posY)
            
main()