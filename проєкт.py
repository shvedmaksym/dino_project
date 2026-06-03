import pygame
import random
import sys

pygame.init()

W, H = 800, 400
GROUND = H - 80
FPS = 60
G = 0.6
JUMP_F = -13.0

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

BG_COLOR = (247, 247, 244)
GROUND_COLOR = (83, 83, 80)
DINO_COLOR = (50, 50, 48)
CACTUS_COLOR = (83, 83, 80)

class Player:
    W, H = 40, 46

    def __init__(self):
        self.x     = 90
        self.y     = float(GROUND - self.H - 10)
        self.vy    = 0.0
        self.jumps = 0
        self.frame = 0
        self.trail = []

    def jump(self):
        if self.jumps < 2:
            self.vy     = JUMP_F if self.jumps == 0 else JUMP_F * 0.78
            self.jumps += 1

    def update(self):
        self.vy    += G
        self.y     += self.vy
        self.frame += 1
        if self.y >= GROUND - self.H - 10:
            self.y     = float(GROUND - self.H - 10)
            self.vy    = 0.0
            self.jumps = 0
        self.trail.append((self.x + self.W // 2, int(self.y + self.H // 2)))
        if len(self.trail) > 8:
            self.trail.pop(0)

    def draw(self, surf):
        x, y      = int(self.x), int(self.y)
        c         = DINO_COLOR
        on_ground = self.jumps == 0
        leg       = (self.frame // 6) % 2

        pygame.draw.rect(surf, c, (x - 10, y + 18, 12, 8),  border_radius=3)
        pygame.draw.rect(surf, c, (x - 14, y + 22, 8,  6),  border_radius=2)
        pygame.draw.rect(surf, c, (x,      y + 8,  34, 32), border_radius=4)
        pygame.draw.rect(surf, c, (x + 18, y - 2,  16, 14), border_radius=3)
        pygame.draw.rect(surf, c, (x + 14, y - 16, 28, 18), border_radius=5)
        pygame.draw.rect(surf, c, (x + 16, y - 26, 8,  12), border_radius=3)
        pygame.draw.rect(surf, c, (x + 26, y - 22, 6,   8), border_radius=2)
        pygame.draw.rect(surf, BG_COLOR, (x + 34, y - 10, 5, 5))
        pygame.draw.rect(surf, c,  (x + 32, y + 2,  10, 5), border_radius=2)
        pygame.draw.rect(surf, c,  (x + 22, y + 36, 10, 6), border_radius=2)

        if on_ground:
            if leg == 0:
                pygame.draw.rect(surf, c, (x + 4,  y + 38, 10, 18), border_radius=3)
                pygame.draw.rect(surf, c, (x + 18, y + 38,  9, 12), border_radius=3)
            else:
                pygame.draw.rect(surf, c, (x + 4,  y + 38,  9, 12), border_radius=3)
                pygame.draw.rect(surf, c, (x + 18, y + 38, 10, 18), border_radius=3)
        else:
            pygame.draw.rect(surf, c, (x + 4,  y + 38, 10, 14), border_radius=3)
            pygame.draw.rect(surf, c, (x + 18, y + 38, 10, 14), border_radius=3)

    def get_rect(self):
        return pygame.Rect(int(self.x) + 2, int(self.y) - 6, self.W + 6, self.H + 16)

score = 0
game_started = False

player = Player()

obstacles = []
spawn_timer = 0
game_speed = 6

while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                else:
                    player.jump()

    if not game_started:
        title = font.render("DINO RUN", True, DINO_COLOR)
        start_text = font.render("Натисни ПРОБІЛ щоб почати", True, DINO_COLOR)
        screen.blit(title, (W//2 - title.get_width()//2, 120))
        screen.blit(start_text, (W//2 - start_text.get_width()//2, 180))
        
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    score += 1

    player.update()

    spawn_timer += 1
    if spawn_timer > 90:
        if random.random() < 0.75:
            h1 = random.randint(30, 45)
            obs = pygame.Rect(W + 20, GROUND - h1, 14, h1)
            obstacles.append(obs)
            
            if random.random() < 0.40:
                h2 = random.randint(30, 45)
                obs2 = pygame.Rect(W + 20 + 14 + 14, GROUND - h2, 14, h2)
                obstacles.append(obs2)
        spawn_timer = 0

    player_rect = player.get_rect()
    for obs in obstacles[:]:
        obs.x -= game_speed
        pygame.draw.rect(screen, CACTUS_COLOR, obs)
        if obs.height >= 35:
            pygame.draw.rect(screen, CACTUS_COLOR, (obs.x - 4, obs.y + obs.height // 2, 4, 4))
            pygame.draw.rect(screen, CACTUS_COLOR, (obs.x - 4, obs.y + obs.height // 2 - 6, 4, 6))
            pygame.draw.rect(screen, CACTUS_COLOR, (obs.x + obs.width, obs.y + obs.height // 3, 4, 4))
            pygame.draw.rect(screen, CACTUS_COLOR, (obs.x + obs.width, obs.y + obs.height // 3 - 8, 4, 8))

        if player_rect.colliderect(obs):
            print(f"Game Over! Твій рахунок: {score // 8}")
            pygame.quit()
            sys.exit()

        if obs.x < -50:
            obstacles.remove(obs)

    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
    player.draw(screen)

    screen.blit(font.render(f"Score: {score // 8}", True, DINO_COLOR), (10, 10))

    pygame.display.flip()
    clock.tick(FPS)