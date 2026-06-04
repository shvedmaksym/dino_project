import math
import random

import pygame

from settings import NIGHT_DINO, W


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
        current_alpha = int((abs(math.sin(self.angle)) * 155 + 100) * global_alpha)
        current_alpha = max(0, min(255, current_alpha))
        star_c = (NIGHT_DINO[0], NIGHT_DINO[1], NIGHT_DINO[2])
        if current_alpha > 0:
            pygame.draw.rect(surf, star_c, (self.x, self.y, self.size, self.size))
