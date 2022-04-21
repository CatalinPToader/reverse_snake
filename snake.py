from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import random

#variables
WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
SNAKE_BODY = (200, 0, 0)
BACKGROUND = (50, 50, 50)
CELL_WALL = (200, 200, 200)
CELL_SIZE = 40
TICKS = 1

update_time = 0
player_pos = [0, 0]
player_size = 19
player_dir = [0, -1]
close = False
score = 0

snake = []
snake_head = None

def main():
    global player_dir
    global update_time
    global close
    global score
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    player_pos = calc_player_pos()
    (snake_head, snake_body_list) = generate_snake()
    dir_snake = (1, 0)

    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_dir = [0, -1]
                elif event.key == pygame.K_s:
                    player_dir = [0, 1]
                elif event.key == pygame.K_d:
                    player_dir = [1, 0]
                elif event.key == pygame.K_a:
                    player_dir = [-1, 0]
        
        
        # Time based movement, player move only TICKS times per second
        t = pygame.time.get_ticks()
        if t - update_time > 1000 / TICKS:
            score += 1
            update_time = t
            x = player_pos[0] + player_dir[0] * CELL_SIZE
            y = player_pos[1] + player_dir[1] * CELL_SIZE
            
            if x < 0 or x > WIDTH:
                x = player_pos[0]
            if y < 0 or y > HEIGHT:
                y = player_pos[1]
            
            
            grid_pos = get_grid_from_player([x, y])
            if grid_pos == snake_head or grid_pos in snake_body_list:
                x = player_pos[0]
                y = player_pos[1]
            
            player_pos = [x, y]
            
            
            new_dir_snake = snake_move_dir(snake_head, player_pos)
            
            x = snake_head[0] + new_dir_snake[0]
            y = snake_head[1] + new_dir_snake[1]
            
            if not (x, y) in snake_body_list:
                snake_body_list = [snake_head] + snake_body_list
                snake_body_list.pop()
            
                snake_head = (x, y)
                dir_snake = new_dir_snake
            else:
                x = snake_head[0] + dir_snake[0]
                y = snake_head[1] + dir_snake[1]
                
                snake_body_list = [snake_head] + snake_body_list
                snake_body_list.pop()
            
                snake_head = (x, y)

        screen.fill(BACKGROUND)
        draw_grid(screen)
        draw_snake(snake_head, snake_body_list, screen)
        pygame.draw.circle(screen, RED, player_pos, player_size)
        
        pygame.display.update()
        
        if lose_cond(player_pos, snake_head):
            close = True

    pygame.time.wait(2000)
    print(f"Your score is : {score}")

# Get the grid position from screen position
def get_grid_from_player(player_pos):
    px = (player_pos[0] - CELL_SIZE / 2) / CELL_SIZE
    py = (player_pos[1] - CELL_SIZE / 2) / CELL_SIZE
    
    return (px, py)

# Check if player lost the game (same position as snake head)
def lose_cond(player_pos, head_snake):
    p_grid = get_grid_from_player(player_pos)
    
    return p_grid == head_snake

# Draw the background grid the game plays on
def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, CELL_WALL, rect, 1)

# Draw the snake
def draw_snake(head, body, screen):
    rect = (head[0] * CELL_SIZE, head[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    
    for pos in body:
        rect = (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SNAKE_BODY, rect)

# Get a random start position for player
def calc_player_pos():
    posX = 0
    posY = 0
    
    cellsX = WIDTH / CELL_SIZE
    cellsY = HEIGHT / CELL_SIZE
    
    startX = random.randint(0, cellsX - 1)
    startY = random.randint(1, cellsY - 1)
    
    posX = startX * CELL_SIZE + CELL_SIZE / 2
    posY = startY * CELL_SIZE + CELL_SIZE / 2
        
    return (posX, posY)

# Generate snake head and body list
def generate_snake():
    center = (int(WIDTH / CELL_SIZE / 2), int(HEIGHT / CELL_SIZE / 2))
    
    body = []
    body.append((center[0], center[1]-1))
    body.append((center[0], center[1]-2))
    
    return (center, body)

# Calculate where snake should move next
# TODO: Move body check here
def snake_move_dir(head, player_pos):
    (px, py) = get_grid_from_player(player_pos)
    x = head[0]
    y = head[1]
    
    
    diff_y = py - y
    diff_x = px - x
    
    if abs(diff_x) > abs(diff_y):
        if diff_x < 0:
            return [-1, 0]
        else:
            return [1, 0]
    else:
        if diff_y < 0:
            return [0, -1]
        else:
            return [0, 1]
    
      
main()