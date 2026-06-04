import random

import pygame

from settings import CLOUD_COLOR, W


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
