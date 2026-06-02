import pygame
import random
import sys

pygame.init()

# Налаштування
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
GRAY = (100, 100, 100)

# Динозавр
player_x = 60
player_y = SCREEN_HEIGHT - 110
player_width = 40
player_height = 60
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

velocity_y = 0
gravity = 0.85
jump_force = -17
jumps_left = 2

# Стан гри
game_started = False
score = 0
font = pygame.font.SysFont("Arial", 28, bold=True)
small_font = pygame.font.SysFont("Arial", 20)

# Перешкоди
obstacles = []
spawn_timer = 0
game_speed = 7

clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_started:
                game_started = True
            elif jumps_left > 0:
                velocity_y = jump_force
                jumps_left -= 1

    if not game_started:
        # Стартовий екран
        title = font.render("DINO RUN", True, BLACK)
        start_text = small_font.render("Натисни ПРОБІЛ щоб почати", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 180))
        
        # Статичний динозавр
        pygame.draw.rect(screen, GREEN, player_rect)
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT-50), (SCREEN_WIDTH, SCREEN_HEIGHT-50), 3)
        
        pygame.display.update()
        clock.tick(60)
        continue

    # === ГРА ЙДЕ ===
    score += 1

    # Гравітація
    velocity_y += gravity
    player_y += velocity_y

    if player_y >= SCREEN_HEIGHT - 110:
        player_y = SCREEN_HEIGHT - 110
        velocity_y = 0
        jumps_left = 2

    player_rect.y = int(player_y)

    # Спавн кактусів
    spawn_timer += 1
    if spawn_timer > 80:          # регулює частоту
        if random.random() < 0.75:   # іноді 2 кактуси
            obs = pygame.Rect(SCREEN_WIDTH + 20, SCREEN_HEIGHT - 100, 28, 50)
            obstacles.append(obs)
            if random.random() < 0.35:  # шанс на другий кактус
                obs2 = pygame.Rect(SCREEN_WIDTH + 70, SCREEN_HEIGHT - 100, 28, 50)
                obstacles.append(obs2)
        spawn_timer = 0

    # Рух і малювання кактусів
    for obs in obstacles[:]:
        obs.x -= game_speed
        pygame.draw.rect(screen, GRAY, obs)

        # Колізія
        if player_rect.colliderect(obs):
            print(f"Game Over! Твій рахунок: {score // 8}")
            pygame.quit()
            sys.exit()

        if obs.x < -50:
            obstacles.remove(obs)

    # Малювання динозавра
    pygame.draw.rect(screen, GREEN, player_rect)

    # Земля
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT-50), (SCREEN_WIDTH, SCREEN_HEIGHT-50), 3)

    # Рахунок
    score_text = font.render(f"{score // 8}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 120, 20))

    pygame.display.update()
    clock.tick(60)