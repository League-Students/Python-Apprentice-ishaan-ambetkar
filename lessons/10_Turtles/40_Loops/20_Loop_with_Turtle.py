import pygame
import sys

# 1. Initialize Pygame and Setup Constants
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_subplots()[0] if hasattr(pygame, 'set_subplots') else pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Smash Brawler")

# Colors
BACKGROUND = (30, 30, 40)
STAGE_COLOR = (120, 120, 130)
BLAST_ZONE_COLOR = (200, 50, 50)

# 2. Define the Stage (The Floating Platform)
class Stage:
    def __init__(self):
        self.rect = pygame.Rect(200, 450, 600, 40)

    def draw(self, surface):
        pygame.draw.rect(surface, STAGE_COLOR, self.rect)
        # Draw small under-ledge to look like a floating island
        pygame.draw.polygon(surface, (80, 80, 85), [
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
            (self.rect.right - 50, self.rect.bottom + 30),
            (self.rect.left + 50, self.rect.bottom + 30)
        ])

# 3. Define the Fighter Class
class Fighter:
    def __init__(self, x, y, color, controls, name):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.color = color
        self.controls = controls
        self.name = name
        
        # Physics attributes
        self.vx = 0
        self.vy = 0
        self.speed = 6
        self.jump_power = -14
        self.gravity = 0.6
        self.is_grounded = False
        
        # Smash Bros mechanics
        self.damage_percent = 0
        self.stocks = 3
        
        # Combat states
        self.facing_right = True
        self.is_attacking = False
        self.attack_cooldown = 0
        self.hitstun = 0
        self.spawn_pos = (x, y)

    def handle_input(self, keys):
        if self.hitstun > 0:
            return  # Cannot move while stunned from getting hit

        # Horizontal movement
        if keys[self.controls['left']]:
            self.vx = -self.speed
            self.facing_right = False
        elif keys[self.controls['right']]:
            self.vx = self.speed
            self.facing_right = True
        else:
            # Apply friction on ground, drift in air
            self.vx *= 0.8 if self.is_grounded else 0.95

        # Jumping
        if keys[self.controls['jump']] and self.is_grounded:
            self.vy = self.jump_power
            self.is_grounded = False

        # Attacking
        if keys[self.controls['attack']] and self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 20  # frames until next attack

    def update(self, stage):
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.hitstun > 0:
            self.hitstun -= 1

        # Apply gravity
        self.vy += self.gravity
        if self.vy > 15:  # Terminal velocity
            self.vy = 15

        # Move horizontally and check blast zones
        self.rect.x += int(self.vx)
        if self.hitstun > 0:
            self.vx *= 0.95  # Decay knockback momentum over time

        # Move vertically
        self.rect.y += int(self.vy)

        # Platform Collision Detection
        self.is_grounded = False
        # Only collide when falling down through the top of the stage
        if self.vy >= 0:
            if (self.rect.right > stage.rect.left and 
                self.rect.left < stage.rect.right and 
                self.rect.bottom >= stage.rect.top and 
                self.rect.bottom - self.vy <= stage.rect.top):
                
                self.rect.bottom = stage.rect.top
                self.vy = 0
                self.is_grounded = True

        # End attack animation quickly
        if self.attack_cooldown < 12:
            self.is_attacking = False

        # Blast Zone Out of Bounds Check (Stock Loss)
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.lose_stock()

    def get_hitbox(self):
        # Generate an attacking hitbox in front of the character
        if self.is_attacking:
            if self.facing_right:
                return pygame.Rect(self.rect.right, self.rect.y + 15, 35, 30)
            else:
                return pygame.Rect(self.rect.left - 35, self.rect.y + 15, 35, 30)
        return None

    def take_damage(self, base_damage, launch_angle_x, launch_angle_y):
        self.damage_percent += base_damage
        # Smash Scaling Formula: Higher damage = massive knockback force
        knockback_factor = 1 + (self.damage_percent / 50.0)
        self.vx = launch_angle_x * knockback_factor
        self.vy = launch_angle_y * knockback_factor
        self.hitstun = int(12 * knockback_factor)

    def lose_stock(self):
        self.stocks -= 1
        self.damage_percent = 0
        self.vx = 0
        self.vy = 0
        self.rect.x, self.rect.y = self.spawn_pos
        self.hitstun = 0

    def draw(self, surface):
        # Draw character body
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        
        # Draw eyes indicating facing direction
        eye_color = (255, 255, 255)
        if self.facing_right:
            pygame.draw.rect(surface, eye_color, (self.rect.right - 12, self.rect.y + 12, 6, 6))
        else:
            pygame.draw.rect(surface, eye_color, (self.rect.left + 6, self.rect.y + 12, 6, 6))

        # Draw attack swing visual
        hitbox = self.get_hitbox()
        if hitbox:
            pygame.draw.rect(surface, (255, 255, 100), hitbox)

# 4. Initialize Core Game Entities
stage = Stage()

# Keyboard assignments for local multiplayer
p1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'attack': pygame.K_f}
p2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'attack': pygame.K_SLASH}

player1 = Fighter(350, 300, (230, 50, 50), p1_controls, "Player 1")
player2 = Fighter(600, 300, (50, 100, 230), p2_controls, "Player 2")
font = pygame.font.SysFont("Arial", 24, bold=True)

# 5. Main Loop Execution Engine
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keyboard state
    keys = pygame.key.get_pressed()

    # Update Physics and Actions
    player1.handle_input(keys)
    player2.handle_input(keys)
    
    player1.update(stage)
    player2.update(stage)

    # Combat Collision Detection (Hitbox interacting with opposing Hurtbox)
    p1_hitbox = player1.get_hitbox()
    p2_hitbox = player2.get_hitbox()

    if p1_hitbox and p1_hitbox.colliderect(player2.rect) and player2.hitstun == 0:
        # P1 hits P2: launch right or left based on orientation
        launch_dir = 7 if player1.facing_right else -7
        player2.take_damage(8, launch_dir, -6)

    if p2_hitbox and p2_hitbox.colliderect(player1.rect) and player1.hitstun == 0:
        # P2 hits P1: launch right or left based on orientation
        launch_dir = 7 if player2.facing_right else -7
        player1.take_damage(8, launch_dir, -6)

    # Rendering Stage / Visual Output Layout
    screen.fill(BACKGROUND)
    stage.draw(screen)
    player1.draw(screen)
    player2.draw(screen)

    # Render Smash Heads Up Display (HUD) UI
    p1_text = font.render(f"{player1.name}: {player1.damage_percent}%  | Stocks: {player1.stocks}", True, player1.color)
    p2_text = font.render(f"{player2.name}: {player2.damage_percent}%  | Stocks: {player2.stocks}", True, player2.color)
    screen.blit(p1_text, (50, 550))
    screen.blit(p2_text, (650, 550))

    # Check End Game Win Condition
    if player1.stocks <= 0 or player2.stocks <= 0:
        winner = "Player 2" if player1.stocks <= 0 else "Player 1"
        win_text = font.render(f"GAME OVER - {winner} WINS!", True, (255, 215, 0))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
