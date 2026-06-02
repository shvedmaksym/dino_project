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

game_started = False
score = 0

x, y = 100, float(GROUND - 40)
vy = 0.0
on_ground = True
player_width = 40
player_height = 40

player_rect = pygame.Rect(x, int(y), player_width, player_height)

leg_state = 0
animation_timer = 0
animation_speed = 6

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
                elif on_ground:
                    vy        = JUMP_F
                    on_ground = False

    if not game_started:
        title = font.render("DINO RUN", True, DINO_COLOR)
        start_text = font.render("Натисни ПРОБІЛ щоб почати", True, DINO_COLOR)
        screen.blit(title, (W//2 - title.get_width()//2, 120))
        screen.blit(start_text, (W//2 - start_text.get_width()//2, 180))
        
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND, W, H - GROUND))
        pygame.draw.rect(screen, DINO_COLOR, (x, int(y), player_width, player_height - 8))
        pygame.draw.rect(screen, DINO_COLOR, (x + 8, int(y) + player_height - 8, 5, 8))
        pygame.draw.rect(screen, DINO_COLOR, (x + player_width - 13, int(y) + player_height - 8, 5, 8))
        
        pygame.display.flip()
        clock.tick(FPS)
        continue

    score += 1

    if not on_ground:
        leg_state = 0
    else:
        animation_timer += 1
        if animation_timer >= animation_speed:
            leg_state = 1 - leg_state
            animation_timer = 0

    vy += G
    y  += vy
    if y >= GROUND - 40:
        y         = float(GROUND - 40)
        vy        = 0.0
        on_ground = True

    player_rect.y = int(y)

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

    pygame.draw.rect(screen, DINO_COLOR, (x, int(y), player_width, player_height - 8))
    
    left_leg_x = x + 8
    right_leg_x = x + player_width - 13
    legs_y = int(y) + player_height - 8
    
    if leg_state == 0:
        pygame.draw.rect(screen, DINO_COLOR, (left_leg_x, legs_y, 5, 8))
        pygame.draw.rect(screen, DINO_COLOR, (right_leg_x, legs_y, 5, 4))
    else:
        pygame.draw.rect(screen, DINO_COLOR, (left_leg_x, legs_y, 5, 4))
        pygame.draw.rect(screen, DINO_COLOR, (right_leg_x, legs_y, 5, 8))

    screen.blit(font.render(f"Score: {score // 8}", True, DINO_COLOR), (10, 10))

    pygame.display.flip()
    clock.tick(FPS)