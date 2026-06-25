import random
import sys
import pygame

# Initialize Pygame
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FPS = 60

# Colors (R, G, B)
GRAY = (60, 60, 60)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# --- Screen Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ultimate Car Racer")
clock = pygame.time.Clock()


class PlayerCar:

    def __init__(self):
        self.width = 45
        self.height = 80
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 120
        self.speed = 8

    def move(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 80:
            self.x -= self.speed
        if (
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        ) and self.x < SCREEN_WIDTH - 80 - self.width:
            self.x += self.speed

    def draw(self, surface):
        # Main car body
        pygame.draw.rect(
            surface, RED, (self.x, self.y, self.width, self.height), border_radius=8
        )
        # Cabin/Windshield
        pygame.draw.rect(
            surface,
            BLACK,
            (self.x + 5, self.y + 20, self.width - 10, 25),
            border_radius=4,
        )
        # Wheels
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 10, 5, 15))
        pygame.draw.rect(
            surface, BLACK, (self.x + self.width, self.y + 10, 5, 15)
        )
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 55, 5, 15))
        pygame.draw.rect(
            surface, BLACK, (self.x + self.width, self.y + 55, 5, 15)
        )

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class EnemyCar:

    def __init__(self, speed):
        self.width = 45
        self.height = 80
        # Spawn within the road boundaries
        self.x = random.randint(80, SCREEN_WIDTH - 80 - self.width)
        self.y = random.randint(-600, -100)
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        # Main car body
        pygame.draw.rect(
            surface, BLUE, (self.x, self.y, self.width, self.height), border_radius=8
        )
        # Cabin/Windshield
        pygame.draw.rect(
            surface,
            WHITE,
            (self.x + 5, self.y + 35, self.width - 10, 25),
            border_radius=4,
        )
        # Wheels
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 10, 5, 15))
        pygame.draw.rect(
            surface, BLACK, (self.x + self.width, self.y + 10, 5, 15)
        )
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 55, 5, 15))
        pygame.draw.rect(
            surface, BLACK, (self.x + self.width, self.y + 55, 5, 15)
        )

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def draw_road(surface, lane_offset):
    # Road background
    pygame.draw.rect(surface, GRAY, (70, 0, SCREEN_WIDTH - 140, SCREEN_HEIGHT))
    # Side solid lines
    pygame.draw.rect(surface, WHITE, (70, 0, 5, SCREEN_HEIGHT))
    pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH - 75, 0, 5, SCREEN_HEIGHT))

    # Moving center dashed lines
    line_width = 6
    line_height = 40
    gap = 30
    x_pos = SCREEN_WIDTH // 2 - line_width // 2

    y_pos = lane_offset - line_height
    while y_pos < SCREEN_HEIGHT:
        pygame.draw.rect(surface, YELLOW, (x_pos, y_pos, line_width, line_height))
        y_pos += line_height + gap


def show_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("arial", size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


def main():
    player = PlayerCar()
    enemies = []
    base_enemy_speed = 5
    max_enemies = 3

    score = 0
    lane_offset = 0
    road_speed = 7

    # Populate initial enemies
    for _ in range(max_enemies):
        enemies.append(EnemyCar(base_enemy_speed))

    game_over = False
    running = True

    while running:
        clock.tick(FPS)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    # Reset game state
                    player = PlayerCar()
                    enemies = [
                        EnemyCar(base_enemy_speed) for _ in range(max_enemies)
                    ]
                    score = 0
                    base_enemy_speed = 5
                    road_speed = 7
                    game_over = False

        if not game_over:
            # --- Game Logic ---
            keys = pygame.key.get_pressed()
            player.move(keys)

            # Move road lines
            lane_offset += road_speed
            if lane_offset >= 70:  # line_height + gap
                lane_offset = 0

            # Update and manage enemies
            for enemy in enemies:
                enemy.update()

                # Check if enemy went off-screen (Score point)
                if enemy.y > SCREEN_HEIGHT:
                    score += 1
                    enemies.remove(enemy)
                    # Dynamic difficulty: speed increases slightly every 5 points
                    current_speed = base_enemy_speed + (score // 5)
                    road_speed = 7 + (score // 5)
                    enemies.append(EnemyCar(current_speed))

                # Collision detection
                if player.get_rect().colliderect(enemy.get_rect()):
                    game_over = True

            # Ensure enemy counts match constraints if removals caused a gap
            while len(enemies) < max_enemies:
                current_speed = base_enemy_speed + (score // 5)
                enemies.append(EnemyCar(current_speed))

        # --- Drawing Graphics ---
        screen.fill((34, 139, 34))  # Grass background color
        draw_road(screen, lane_offset)

        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # HUD / UI Text overlay
        show_text(screen, f"Score: {score}", 28, SCREEN_WIDTH // 2, 30)

        if game_over:
            # Semi-transparent overlay background
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            show_text(
                screen, "GAME OVER", 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED
            )
            show_text(
                screen,
                f"Final Score: {score}",
                30,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 10,
            )
            show_text(
                screen,
                "Press SPACE to Restart",
                22,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 70,
                YELLOW,
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()