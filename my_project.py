import pygame
import sys

pygame.init()


W, H = 800, 400
GROUND = H - 80
FPS = 60
G = 0.6
JUMP_F = -12.0
DOUBLE_JUMP_F = -10.0


screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dino Game: Double Jump")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 24, bold=True)


score = 0.0
score_speed = 0.15
acceleration = 0.0002
max_speed = 3.0

x, y = 100, float(GROUND - 40)
vy = 0.0
on_ground = True
jump_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:

                if jump_count < 2:
                    if jump_count == 0:
                        vy = JUMP_F
                    else:
                        vy = DOUBLE_JUMP_F

                    jump_count += 1
                    on_ground = False


    vy += G
    y += vy


    if y >= GROUND - 40:
        y = float(GROUND - 40)
        vy = 0.0
        on_ground = True
        jump_count = 0


    score += score_speed
    if score_speed < max_speed:
        score_speed += acceleration


    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (83, 83, 83), (0, GROUND), (W, GROUND), 2)
    pygame.draw.rect(screen, (83, 83, 83), (int(x), int(y), 40, 40))

    score_txt = font.render(str(int(score)).zfill(5), True, (83, 83, 83))
    screen.blit(score_txt, (W - 100, 20))

    pygame.display.flip()
    clock.tick(FPS)