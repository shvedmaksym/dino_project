import random
import sys

import pygame

import settings
from cloud import Cloud
from player import Player
from settings import (
    BG_COLOR,
    CACTUS_COLOR,
    CLOUD_COLOR,
    DAY_BG,
    DAY_CACTUS,
    DAY_CLOUD,
    DAY_DINO,
    DAY_GROUND,
    DINO_COLOR,
    FPS,
    GROUND,
    GROUND_COLOR,
    H,
    MAX_SPEED,
    NIGHT_BG,
    NIGHT_CACTUS,
    NIGHT_CLOUD,
    NIGHT_DINO,
    NIGHT_GROUND,
    RECORD_ANN_COLOR,
    START_SPEED,
    W,
)
from star import Star

pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

stars = [Star() for _ in range(25)]


def reset_game():
    global score, game_speed, obstacles, clouds, spawn_timer, game_over, new_high_score_reached
    score = 0.0
    game_speed = START_SPEED
    obstacles = []
    clouds = [Cloud(random.randint(0, 2400)) for _ in range(8)]
    spawn_timer = 0
    game_over = False
    new_high_score_reached = False
    settings.night_alpha = 0.0
    player.reset()
    BG_COLOR[:] = DAY_BG
    GROUND_COLOR[:] = DAY_GROUND
    DINO_COLOR[:] = DAY_DINO
    CACTUS_COLOR[:] = DAY_CACTUS
    CLOUD_COLOR[:] = DAY_CLOUD


def lerp_color(current, target, speed=0.02):
    for i in range(3):
        current[i] += (target[i] - current[i]) * speed


def update_game_colors(current_score):
    # === ЗМІНА ТЕПЕР ВІДБУВАЄТЬСЯ КОЖНІ 311 ОЧОК ===
    is_night = (int(current_score) // 311) % 2 == 1

    if is_night:
        target_bg, target_ground, target_dino, target_cactus, target_cloud = (
            NIGHT_BG,
            NIGHT_GROUND,
            NIGHT_DINO,
            NIGHT_CACTUS,
            NIGHT_CLOUD,
        )
        settings.HI_SCORE_COLOR = (180, 180, 180)
        settings.night_alpha += (1.0 - settings.night_alpha) * 0.02
    else:
        target_bg, target_ground, target_dino, target_cactus, target_cloud = (
            DAY_BG,
            DAY_GROUND,
            DAY_DINO,
            DAY_CACTUS,
            DAY_CLOUD,
        )
        settings.HI_SCORE_COLOR = (150, 150, 150)
        settings.night_alpha += (0.0 - settings.night_alpha) * 0.02

    lerp_color(BG_COLOR, target_bg)
    lerp_color(GROUND_COLOR, target_ground)
    lerp_color(DINO_COLOR, target_dino)
    lerp_color(CACTUS_COLOR, target_cactus)
    lerp_color(CLOUD_COLOR, target_cloud)


def draw_moon(surf, global_alpha):
    if global_alpha > 0.05:
        mx, my = W - 150, 50
        pygame.draw.circle(surf, NIGHT_GROUND, (mx, my), 22)
        pygame.draw.circle(surf, (int(BG_COLOR[0]), int(BG_COLOR[1]), int(BG_COLOR[2])), (mx - 8, my - 4), 20)


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


def run_game():
    global score, game_speed, obstacles, clouds, spawn_timer, game_over
    global new_high_score_reached, high_score, game_started

    while True:
        update_game_colors(score)

        screen.fill(BG_COLOR)

        for star in stars:
            star.update()
            star.draw(screen, settings.night_alpha)
        draw_moon(screen, settings.night_alpha)

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
            hi_score_surf = font.render(f"HI: {high_score}", True, settings.HI_SCORE_COLOR)
            screen.blit(final_score_surf, (20, 20))
            screen.blit(hi_score_surf, (20, 50))

        else:
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

            hi_text = font.render(f"HI {high_score:05d}", True, settings.HI_SCORE_COLOR)
            cur_text = font.render(f"{int(score):05d}", True, DINO_COLOR)
            screen.blit(hi_text, (20, 20))
            screen.blit(cur_text, (hi_text.get_width() + 40, 20))

            boost = game_speed / START_SPEED
            boost_text = small_font.render(f"Speed: {boost:.1f}x", True, (120, 120, 120))
            screen.blit(boost_text, (W - boost_text.get_width() - 20, 25))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()
