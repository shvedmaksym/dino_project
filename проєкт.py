import pygame
import sys

pygame.init()

W, H    = 800, 400
GROUND  = H - 80
FPS     = 60
G       = 0.6
JUMP_F  = -13.0

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dino Game")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 24)

score      = 0
x, y       = 100, float(GROUND - 40)
vy         = 0.0
on_ground  = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                vy        = JUMP_F
                on_ground = False

    vy += G
    y  += vy
    if y >= GROUND - 40:
        y         = float(GROUND - 40)
        vy        = 0.0
        on_ground = True

    score += 1

    screen.fill((247, 247, 244))
    pygame.draw.rect(screen, (83, 83, 80), (0, GROUND, W, H - GROUND))
    pygame.draw.rect(screen, (50, 50, 48), (int(x), int(y), 40, 40))
    screen.blit(font.render(f"Score: {score}", True, (50, 50, 48)), (10, 10))

    pygame.display.flip()
    clock.tick(FPS)