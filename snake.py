from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import random

#variables
WIDTH = 1000
HEIGHT = 600
FOOD = (0, 255, 255)
PLAYER = (255, 255, 0)
SNAKE_HEAD = (255, 0, 0)
SNAKE_BODY = (200, 0, 0)
BACKGROUND = (50, 50, 50)
CELL_WALL = (200, 200, 200)
WALL = (255, 255, 255)
CELL_SIZE = 40
TICKS = 1

update_time = 0
player_pos = [0, 0]
player_size = 19
player_dir = [0, -1]
close = False
score = 0

walls = []

snake = []
snake_head = None
snake_length = 3
food = None

def main():
    global player_dir
    global update_time
    global close
    global score
    global food
    global snake_length
    global walls
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_font = pygame.font.SysFont('Arial', 30)
    
    start = False
    

    walls = generate_walls()
    (snake_head, snake_body_list) = generate_snake()
    dir_snake = (1, 0)
    
    player_pos = calc_player_pos(snake_head)

    won = False
    
    text_surface = game_font.render("Pick Speed by pressing [1-3]", False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)
    
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    TICKS = 1
                    start = True
                elif event.key == pygame.K_2:
                    TICKS = 1.5
                    start = True
                elif event.key == pygame.K_3:
                    TICKS = 2
                    start = True
                
        pygame.display.update()
                
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
        
        screen.fill(BACKGROUND)
        playerDist = dist_to_player(snake_head, player_pos)
        # Time based movement, player move only TICKS times per second
        t = pygame.time.get_ticks()
        if t - update_time > 1000 / TICKS:
            if  playerDist >= 2:
                score += 1 * snake_length / 3

            update_time = t
            
            dir_snake = snake_move_dir(player_pos, snake_head, snake_body_list, walls)
            
            if dir_snake[0] == 0 and dir_snake[1] == 0:
                won = True
            
            x = snake_head[0] + dir_snake[0]
            y = snake_head[1] + dir_snake[1]
            
            snake_body_list = [snake_head] + snake_body_list
            if len(snake_body_list) >= snake_length:
                snake_body_list.pop()
        
            snake_head = (x, y)
            
            x = player_pos[0] + player_dir[0] * CELL_SIZE
            y = player_pos[1] + player_dir[1] * CELL_SIZE
            
            grid_pos = get_grid_from_player([x, y])
            if not snake_collision(grid_pos, snake_head, snake_body_list, walls) and get_grid_from_player((x, y)) != food:
                player_pos = [x, y]
                
            if food == None:
                food = spawnFood(player_pos, snake_head, snake_body_list, walls)
            else:
                if snake_head == food:
                    snake_length += 1
                    food = None
                    
        draw_grid(screen)
        draw_walls(screen, walls)
        if food:
            draw_food(screen, food)
        draw_snake(snake_head, snake_body_list, screen)
        if lose_cond(player_pos, snake_head):
            close = True
        else:
            pygame.draw.circle(screen, PLAYER, player_pos, player_size)
        
        if playerDist < 2:
            rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            pygame.draw.rect(screen, SNAKE_HEAD, rect, int(WIDTH / 100))

        pygame.display.update()

    pygame.time.wait(2000)
    screen.fill(BACKGROUND)
    if not won:
        text_surface = game_font.render(f"You Lost! Your score is : {int(score)}", False, (255, 255, 255))
    else:
        text_surface = game_font.render(f"YOU WON!!! Your score is : {int(score)}", False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(5000)


# Spawns a random food pellet in a valid position
def spawnFood(player_pos, head, body_list, walls):
    grid_pos_p = get_grid_from_player(player_pos)
    
    possible = []
    for x in range(0, int(WIDTH / CELL_SIZE)):
        for y in range(0, int(HEIGHT / CELL_SIZE)):
            if not snake_collision((x,y), head, body_list, walls) and (x, y) != grid_pos_p:
                possible.append((x,y))
                
    return random.choice(possible)
        

# Get the grid position from screen position
def get_grid_from_player(player_pos):
    px = (player_pos[0] - CELL_SIZE / 2) / CELL_SIZE
    py = (player_pos[1] - CELL_SIZE / 2) / CELL_SIZE
    
    return (px, py)

def screen_to_grid(pos):
    return (pos[0] / CELL_SIZE, pos[1] / CELL_SIZE)

# Check if player lost the game (same position as snake head)
def lose_cond(player_pos, head_snake):
    p_grid = get_grid_from_player(player_pos)
    
    return p_grid == head_snake

# Draws the food pellet to the screen
def draw_food(screen, food):
    x = food[0] * CELL_SIZE + CELL_SIZE / 2
    y = food[1] * CELL_SIZE + CELL_SIZE / 2
    pygame.draw.circle(screen, FOOD, (x, y), player_size)
    
def draw_walls(screen, walls):
    for (x, y) in walls:
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, WALL, rect)

# Draw the background grid the game plays on
def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, CELL_WALL, rect, 1)

# Draw the snake
def draw_snake(head, body, screen):
    rect = (head[0] * CELL_SIZE, head[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, SNAKE_HEAD, rect)
    
    for pos in body:
        rect = (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SNAKE_BODY, rect)

# Get a random start position for player
def calc_player_pos(head):
    posX = 0
    posY = 0
    
    cellsX = WIDTH / CELL_SIZE
    cellsY = HEIGHT / CELL_SIZE
    
    dist = 0
    
    while dist < 5:
        startX = random.randint(0, cellsX - 1)
        startY = random.randint(1, cellsY - 1)

        
        posX = startX * CELL_SIZE + CELL_SIZE / 2
        posY = startY * CELL_SIZE + CELL_SIZE / 2
        
        dist = dist_to_player(head, (posX, posY))
        
    return (posX, posY)


def in_range(x, a, b):
    return a <= x and x < b

def dist_from_side(x, side_size):
    dist = 0
    
    x = x / CELL_SIZE
    
    if x > side_size / CELL_SIZE / 2:
        dist += side_size / CELL_SIZE - x - 1
    else:
        dist += x
        
    return dist

def generate_walls():
    walls = []
    
    max_allowed_x = WIDTH / CELL_SIZE / 3
    max_allowed_y = HEIGHT / CELL_SIZE / 3
    
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            distx = dist_from_side(x, WIDTH)
            disty = dist_from_side(y, HEIGHT)
            if (distx == 2 or disty == 2) and in_range(distx, 2, max_allowed_x) and in_range(disty, 2, max_allowed_y):
                walls.append((x, y))
                
    return walls

# Generate snake head and body list
def generate_snake():
    center = (int(WIDTH / CELL_SIZE / 2), int(HEIGHT / CELL_SIZE / 2))
    
    body = []
    body.append((center[0], center[1]-1))
    body.append((center[0], center[1]-2))
    
    return (center, body)

# Returns true for collision with edges or snake
def snake_collision(pos_to_check, snake_head, snake_body_list, wall_list):
    x = pos_to_check[0]
    y = pos_to_check[1]
    
    if x < 0 or x * CELL_SIZE >= WIDTH:
        return True
    if y < 0 or y * CELL_SIZE >= HEIGHT:
        return True
    
    if pos_to_check == snake_head:
        return True
    if pos_to_check in snake_body_list:
        return True
    for wall in wall_list:
        if screen_to_grid(wall) == pos_to_check:
            return True
    
    return False

# Calculate distance to player
def dist_to_player(pos, player_pos):
    (px, py) = get_grid_from_player(player_pos)
    
    diff_x = abs(px - pos[0])
    diff_y = abs(py - pos[1])
    
    return diff_x + diff_y

# Calculate where snake should move next
def snake_move_dir(player_pos, head, body_list, walls):
    dirs = {}
    dirs['W'] = [1, 0]
    dirs['E'] = [-1, 0]
    dirs['N'] = [0, 1]
    dirs['S'] = [0, -1]
    
    dist = {}
    
    for dir in dirs:
        dir_vals = dirs[dir]
        x = head[0] + dir_vals[0]
        y = head[1] + dir_vals[1]
        
        if not snake_collision((x, y), head, body_list, walls):
            dist[dir] = dist_to_player((x, y), player_pos)
            
    min_dist = 1000
    min_dir = None
    for dir in dist:
        val = dist[dir]
        if val < min_dist:
            min_dir = dir
            min_dist = val
    
    if min_dir == None:
        return [0, 0]
    return dirs[min_dir]

      
main()