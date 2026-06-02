import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

# Налаштування екрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run: Pro Version")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Налаштування гравця (Діно)
player_width = 40
player_height = 60
player_x = 50
player_base_y = SCREEN_HEIGHT - player_height - 50
player_y = player_base_y
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Фізика подвійного стрибка
jump_speed = 0
gravity = 0.8
jump_force = 14
jumps_left = 2


# Клас перешкоди
class Obstacle:
    def __init__(self):
        self.type = random.randint(1, 2)  # 1 - одинарна, 2 - подвійна
        self.width = 30 * self.type
        self.height = 50
        self.x = SCREEN_WIDTH + 50
        self.y = SCREEN_HEIGHT - self.height - 50
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)


# Змінні для керування перешкодами
obstacles = []
spawn_timer = 0
# Визначаємо першу випадкову дистанцію (паузу) до появи перешкоди
next_spawn_time = random.randint(60, 180)

clock = pygame.time.Clock()

# Головний цикл гри
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Логіка стрибків
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jumps_left > 0:
                    jump_speed = -jump_force
                    jumps_left -= 1

    # Гравітація
    jump_speed += gravity
    player_y += jump_speed

    # Перевірка приземлення
    if player_y >= player_base_y:
        player_y = player_base_y
        jump_speed = 0
        jumps_left = 2

    player_rect.y = player_y

    # --- ЛОГІКА ПЕРЕШКОД З ХАОТИЧНОЮ ДИСТАНЦІЄЮ ---
    spawn_timer += 1
    if spawn_timer > next_spawn_time:
        obstacles.append(Obstacle())
        spawn_timer = 0
        # Кожен раз нова випадкова дистанція для наступного ворога
        next_spawn_time = random.randint(50, 160)

    for obs in obstacles[:]:
        obs.move()
        obs.draw(screen)

        # Перевірка на програш
        if player_rect.colliderect(obs.rect):
            print(f"Game Over! Ви зіткнулися з {'подвійною' if obs.type == 2 else 'одинарною'} перешкодою.")
            pygame.quit()
            sys.exit()

        # Видалення об'єктів поза екраном
        if obs.x < -obs.width:
            obstacles.remove(obs)

    # Малювання гравця та землі
    pygame.draw.rect(screen, GREEN, player_rect)
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 2)

    pygame.display.update()
    clock.tick(60)