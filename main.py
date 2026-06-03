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
small_font = pygame.font.SysFont("Arial", 18)

BG_COLOR = (247, 247, 244)
GROUND_COLOR = (83, 83, 80)
DINO_COLOR = (50, 50, 48)
CACTUS_COLOR = (83, 83, 80)


class Player:
    W, H = 32, 38

    def __init__(self):
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
        pygame.draw.rect(surf, BG_COLOR, (x + 26, y - 10, 4, 4))
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


score = 0.0
game_started = False
player = Player()
obstacles = []
spawn_timer = 0
START_SPEED = 6.5
game_speed = START_SPEED
MAX_SPEED = 16.0

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
        start_text = font.render("SPACE TO START", True, DINO_COLOR)
        screen.blit(title, (W // 2 - title.get_width() // 2, 120))
        screen.blit(start_text, (W // 2 - start_text.get_width() // 2, 180))
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
        player.draw(screen, game_speed)
        pygame.display.flip()
        clock.tick(FPS)
        continue


    if game_speed < MAX_SPEED:
        game_speed += 0.001

    score += game_speed / 50
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
            print(f"Game Over! Score: {int(score)}")
            pygame.quit()
            sys.exit()

        if obs.x < -60:
            obstacles.remove(obs)


    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
    player.draw(screen, game_speed)


    screen.blit(font.render(f"Score: {int(score)}", True, DINO_COLOR), (20, 20))


    boost = game_speed / START_SPEED
    boost_text = small_font.render(f"Speed: {boost:.1f}x", True, (120, 120, 120))
    screen.blit(boost_text, (W - boost_text.get_width() - 20, 25))

    pygame.display.flip()
    clock.tick(FPS)