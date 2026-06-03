import pygame
import random
import sys

pygame.init()

W, H = 800, 400
GROUND = H - 80
FPS = 60
G = 0.6
JUMP_F = -12.0

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

# === НАЛАШТУВАННЯ ПАЛІТР ДНЯ ТА НОЧІ ===
DAY_BG          = (247, 247, 244)
DAY_GROUND      = (83, 83, 80)
DAY_DINO        = (50, 50, 48)
DAY_CACTUS      = (83, 83, 80)
DAY_CLOUD       = (210, 210, 210)

NIGHT_BG        = (32, 32, 34)
NIGHT_GROUND    = (170, 170, 173)
NIGHT_DINO      = (230, 230, 233)
NIGHT_CACTUS    = (170, 170, 173)
NIGHT_CLOUD     = (70, 70, 75)

# Поточні робочі кольори (ініціалізуємо денними)
BG_COLOR = DAY_BG
GROUND_COLOR = DAY_GROUND
DINO_COLOR = DAY_DINO
CACTUS_COLOR = DAY_CACTUS
CLOUD_COLOR = DAY_CLOUD

HI_SCORE_COLOR = (150, 150, 150)
RECORD_ANN_COLOR = (255, 0, 0)


class Cloud:
    def __init__(self, start_x=None):
        if start_x is not None:
            self.x = start_x
        else:
            self.x = W + random.randint(100, 800)

        self.y = random.randint(20, 150)
        self.w = random.randint(50, 90)

    def update(self, game_speed):
        self.x -= (game_speed / 4)

    def draw(self, surf):
        pygame.draw.ellipse(surf, CLOUD_COLOR, (self.x, self.y, self.w, 28))
        pygame.draw.ellipse(surf, CLOUD_COLOR, (self.x + 18, self.y - 12, self.w - 15, 30))
        pygame.draw.ellipse(surf, CLOUD_COLOR, (self.x + 30, self.y + 6, self.w - 25, 22))


class Player:
    W, H = 32, 38

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 80
        self.y = float(GROUND - self.H - 10)
        self.vy = 0.0
        self.jumps = 0
        self.frame = 0

    def jump(self):
        if self.jumps < 2:
            self.vy = JUMP_F if self.jumps == 0 else JUMP_F * 0.8
            self.jumps += 1

    def update(self):
        self.vy += G
        self.y += self.vy
        self.frame += 1
        if self.y >= GROUND - self.H - 10:
            self.y = float(GROUND - self.H - 10)
            self.vy = 0.0
            self.jumps = 0

    def draw(self, surf, current_speed):
        x, y = int(self.x), int(self.y)
        c = DINO_COLOR
        on_ground = (self.y >= GROUND - self.H - 10)
        adj_anim_speed = max(2, 7 - int(current_speed // 4))
        leg = (self.frame // adj_anim_speed) % 2
        pygame.draw.rect(surf, c, (x - 8, y + 15, 10, 7), border_radius=2)
        pygame.draw.rect(surf, c, (x - 12, y + 18, 6, 5), border_radius=2)
        pygame.draw.rect(surf, c, (x, y + 6, 28, 26), border_radius=4)
        pygame.draw.rect(surf, c, (x + 14, y - 2, 14, 12), border_radius=3)
        pygame.draw.rect(surf, c, (x + 10, y - 14, 22, 16), border_radius=4)
        pygame.draw.rect(surf, c, (x + 12, y - 22, 6, 10), border_radius=2)
        pygame.draw.rect(surf, c, (x + 20, y - 18, 5, 7), border_radius=2)
        pygame.draw.rect(surf, BG_COLOR, (x + 26, y - 10, 4, 4)) # Використовує динамічний BG_COLOR для ока
        pygame.draw.rect(surf, c, (x + 25, y + 1, 8, 4), border_radius=2)
        pygame.draw.rect(surf, c, (x + 16, y + 30, 8, 5), border_radius=2)
        if on_ground:
            if leg == 0:
                pygame.draw.rect(surf, c, (x + 3, y + 32, 8, 14), border_radius=2)
                pygame.draw.rect(surf, c, (x + 15, y + 32, 7, 10), border_radius=2)
            else:
                pygame.draw.rect(surf, c, (x + 3, y + 32, 7, 10), border_radius=2)
                pygame.draw.rect(surf, c, (x + 15, y + 32, 8, 14), border_radius=2)
        else:
            pygame.draw.rect(surf, c, (x + 3, y + 32, 8, 11), border_radius=2)
            pygame.draw.rect(surf, c, (x + 15, y + 32, 8, 11), border_radius=2)

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H + 10)


def reset_game():
    global score, game_speed, obstacles, clouds, spawn_timer, game_over, new_high_score_reached
    score = 0.0
    game_speed = START_SPEED
    obstacles = []
    clouds = [Cloud(random.randint(0, 2400)) for _ in range(8)]
    spawn_timer = 0
    game_over = False
    new_high_score_reached = False
    player.reset()
    update_game_colors(0) # Скидаємо кольори на денні


# === ФУНКЦІЯ ОНОВЛЕННЯ КОЛЬОРІВ (ДЕНЬ / НІЧ) ===
def update_game_colors(current_score):
    global BG_COLOR, GROUND_COLOR, DINO_COLOR, CACTUS_COLOR, CLOUD_COLOR, HI_SCORE_COLOR
    
    # Визначаємо цикл дня і ночі кожні 700 очок (700 очок день, 700 очок ніч і т.д.)
    # Поділ на 700 дає нам номер циклу. Якщо остача від ділення на 2 дорівнює 1 — вмикається ніч.
    is_night = (int(current_score) // 700) % 2 == 1
    
    if is_night:
        BG_COLOR = NIGHT_BG
        GROUND_COLOR = NIGHT_GROUND
        DINO_COLOR = NIGHT_DINO
        CACTUS_COLOR = NIGHT_CACTUS
        CLOUD_COLOR = NIGHT_CLOUD
        HI_SCORE_COLOR = (180, 180, 180) # Робимо текст рекорду трохи чіткішим вночі
    else:
        BG_COLOR = DAY_BG
        GROUND_COLOR = DAY_GROUND
        DINO_COLOR = DAY_DINO
        CACTUS_COLOR = DAY_CACTUS
        CLOUD_COLOR = DAY_CLOUD
        HI_SCORE_COLOR = (150, 150, 150)


START_SPEED = 6.5
MAX_SPEED = 16.0

score = 0.0
high_score = 0
game_started = False
game_over = False
new_high_score_reached = False
player = Player()
obstacles = []
clouds = [Cloud(random.randint(0, 2400)) for _ in range(8)]
spawn_timer = 0
game_speed = START_SPEED

while True:
    # Динамічно оновлюємо палітру кольорів залежно від поточного прогресу очок
    update_game_colors(score)

    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                elif not game_started:
                    game_started = True
                else:
                    player.jump()

    # Малюємо хмари спочатку (вони на задньому плані)
    for cloud in clouds:
        cloud.draw(screen)

    if not game_started:
        title = font.render("DINO RUN", True, DINO_COLOR)
        start_text = font.render("SPACE TO START", True, DINO_COLOR)
        screen.blit(title, (W // 2 - title.get_width() // 2, 120))
        screen.blit(start_text, (W // 2 - start_text.get_width() // 2, 180))
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
        player.draw(screen, game_speed)

    elif game_over:
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
        for obs in obstacles:
            pygame.draw.rect(screen, CACTUS_COLOR, obs, border_radius=3)
        player.draw(screen, 0)

        if new_high_score_reached:
            header_text = large_font.render("NEW RECORD! WOW!", True, RECORD_ANN_COLOR)
        else:
            header_text = large_font.render("GAME OVER", True, DINO_COLOR)

        restart_text = font.render("PRESS SPACE TO RESTART", True, DINO_COLOR)
        screen.blit(header_text, (W // 2 - header_text.get_width() // 2, H // 2 - 60))
        screen.blit(restart_text, (W // 2 - restart_text.get_width() // 2, H // 2 + 10))

        final_score_surf = font.render(f"Score: {int(score)}", True, DINO_COLOR)
        hi_score_surf = font.render(f"HI: {high_score}", True, HI_SCORE_COLOR)
        screen.blit(final_score_surf, (20, 20))
        screen.blit(hi_score_surf, (20, 50))

    else:
        # Рух хмар
        for cloud in clouds[:]:
            cloud.update(game_speed)
            if cloud.x < -200:
                clouds.remove(cloud)
                clouds.append(Cloud(W + random.randint(200, 1000)))

        if game_speed < MAX_SPEED:
            game_speed += 0.001
        score += game_speed / 50

        if high_score > 0 and int(score) > high_score and not new_high_score_reached:
            new_high_score_reached = True
        if int(score) > high_score:
            high_score = int(score)

        player.update()

        spawn_timer += game_speed / 6
        if spawn_timer > 95:
            if random.random() < 0.8:
                h = random.randint(40, 65)
                obs = pygame.Rect(W + 20, GROUND - h, 18, h)
                obstacles.append(obs)
                if random.random() < 0.35:
                    h2 = random.randint(40, 55)
                    obs2 = pygame.Rect(W + 55, GROUND - h2, 18, h2)
                    obstacles.append(obs2)
            spawn_timer = 0

        player_rect = player.get_rect()
        for obs in obstacles[:]:
            obs.x -= game_speed
            pygame.draw.rect(screen, CACTUS_COLOR, obs, border_radius=3)
            if obs.height > 45:
                pygame.draw.rect(screen, CACTUS_COLOR, (obs.x - 6, obs.y + 15, 6, 12), border_radius=2)
                pygame.draw.rect(screen, CACTUS_COLOR, (obs.x + obs.width, obs.y + 10, 6, 15), border_radius=2)
            if player_rect.colliderect(obs):
                game_over = True
            if obs.x < -60:
                obstacles.remove(obs)

        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
        player.draw(screen, game_speed)

        hi_text = font.render(f"HI {high_score:05d}", True, HI_SCORE_COLOR)
        cur_text = font.render(f"{int(score):05d}", True, DINO_COLOR)
        screen.blit(hi_text, (20, 20))
        screen.blit(cur_text, (hi_text.get_width() + 40, 20))

        boost = game_speed / START_SPEED
        boost_text = small_font.render(f"Speed: {boost:.1f}x", True, (120, 120, 120))
        screen.blit(boost_text, (W - boost_text.get_width() - 20, 25))

    pygame.display.flip()
    clock.tick(FPS)