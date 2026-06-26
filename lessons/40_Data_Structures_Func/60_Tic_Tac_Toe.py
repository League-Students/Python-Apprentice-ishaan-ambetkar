import pygame
import random
import sys

# Initialize and setup display
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
BLOCK_SIZE = 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Paper Minecraft")
clock = pygame.time.Clock()

# Colors and Block Types
COLORS = {0: (135, 206, 235), 1: (120, 72, 32), 2: (50, 200, 50), 3: (100, 100, 100)}
AIR, DIRT, GRASS, STONE = 0, 1, 2, 3

# World Generation
WORLD_COLS, WORLD_ROWS = 100, 40
world = [[AIR for _ in range(WORLD_COLS)] for _ in range(WORLD_ROWS)]
ground_height = WORLD_ROWS // 2
for x in range(WORLD_COLS):
    ground_height = max(15, min(WORLD_ROWS - 5, ground_height + random.choice([-1, 0, 1])))
    for y in range(WORLD_ROWS):
        if y == ground_height: world[y][x] = GRASS
        elif y > ground_height and y < ground_height + 4: world[y][x] = DIRT
        elif y >= ground_height + 4: world[y][x] = STONE

# Player and Camera
player_rect = pygame.Rect(300, 100, 24, 54)
vel_y, gravity, player_speed = 0, 0.6, 5
camera_x = 0
selected_block = DIRT

def check_collision(rect, dx, dy):
    predicted = rect.move(dx, dy)
    start_x = max(0, predicted.left // BLOCK_SIZE)
    end_x = min(WORLD_COLS, (predicted.right // BLOCK_SIZE) + 1)
    start_y = max(0, predicted.top // BLOCK_SIZE)
    end_y = min(WORLD_ROWS, (predicted.bottom // BLOCK_SIZE) + 1)
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if world[y][x] != AIR and predicted.colliderect(pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)):
                return True
    return False

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYDOWN and event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
            selected_block = {pygame.K_1: DIRT, pygame.K_2: GRASS, pygame.K_3: STONE}[event.key]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = (mx + camera_x) // BLOCK_SIZE, my // BLOCK_SIZE
            if 0 <= gx < WORLD_COLS and 0 <= gy < WORLD_ROWS:
                if event.button == 1: world[gy][gx] = AIR
                elif event.button == 3 and world[gy][gx] == AIR: world[gy][gx] = selected_block

    # Movement and Physics
    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) * player_speed - (keys[pygame.K_a] or keys[pygame.K_LEFT]) * player_speed
    if not check_collision(player_rect, dx, 0): player_rect.x += dx
    vel_y = min(15, vel_y + gravity)
    if not check_collision(player_rect, 0, vel_y): player_rect.y += vel_y
    else:
        if vel_y > 0: player_rect.y = (player_rect.bottom // BLOCK_SIZE) * BLOCK_SIZE - player_rect.height
        vel_y = 0
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and check_collision(player_rect, 0, 1): vel_y = -11

    # Camera
    camera_x = max(0, min(player_rect.x - SCREEN_WIDTH // 2, WORLD_COLS * BLOCK_SIZE - SCREEN_WIDTH))
    
    # Rendering
    screen.fill(COLORS[AIR])
    for y in range(WORLD_ROWS):
        for x in range(max(0, camera_x // BLOCK_SIZE), min(WORLD_COLS, (camera_x + SCREEN_WIDTH) // BLOCK_SIZE + 1)):
            if world[y][x] != AIR:
                rect = pygame.Rect(x * BLOCK_SIZE - camera_x, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, COLORS[world[y][x]], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    
    player_draw = player_rect.copy(); player_draw.x -= camera_x
    pygame.draw.rect(screen, (255, 100, 100), player_draw)
    pygame.draw.rect(screen, (0, 0, 0), player_draw, 2)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()