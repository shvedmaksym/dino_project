import pygame
import random
from settings import W, NIGHT_DINO

class Star:
    def __init__(self):
        self.x = random.randint(0, W)
        self.y = random.randint(10, 140)
        self.size = random.randint(1, 3)
        self.blink_speed = random.uniform(0.02, 0.05)
        self.angle = random.uniform(0, 6.28)

    def update(self):
        self.angle += self.blink_speed

    def draw(self, surf, global_alpha):
        if global_alpha > 0.05:
            pygame.draw.rect(
                surf,
                (NIGHT_DINO[0], NIGHT_DINO[1], NIGHT_DINO[2]),
                (self.x, self.y, self.size, self.size),
            )