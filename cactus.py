import pygame
import random
from settings import GROUND, CACTUS_COLOR, BG_COLOR, DAY_BG, NIGHT_BG

class AdvancedCactus:
    def __init__(self, x_pos):
        self.w = random.randint(16, 22)
        self.h = random.randint(50, 75)
        self.x = float(x_pos)
        self.y = GROUND - self.h

        self.has_left_branch  = random.choice([True, False])
        self.has_right_branch = random.choice([True, False])

        self.left_branch_y  = random.randint(15, self.h - 20)
        self.right_branch_y = random.randint(20, self.h - 15)

        self.branch_w = random.randint(10, 15)
        self.branch_h = random.randint(15, 25)

        self.needles = []
        for _ in range(random.randint(5, 10)):
            nx = random.randint(2, self.w - 4)
            ny = random.randint(5, self.h - 5)
            self.needles.append((nx, ny))

    def update(self, speed):
        self.x -= speed

    def draw(self, surf):
        x_i = int(self.x)
        y_i = int(self.y)

        if self.has_left_branch:
            bx = x_i - self.branch_w
            by = y_i + self.left_branch_y
            pygame.draw.rect(surf, CACTUS_COLOR, (bx, by, self.branch_w, 8), border_radius=2)
            pygame.draw.rect(surf, CACTUS_COLOR, (bx, by - self.branch_h, 8, self.branch_h), border_radius=2)

        if self.has_right_branch:
            bx = x_i + self.w
            by = y_i + self.right_branch_y
            pygame.draw.rect(surf, CACTUS_COLOR, (bx, by, self.branch_w, 8), border_radius=2)
            pygame.draw.rect(surf, CACTUS_COLOR, (bx + self.branch_w - 8, by - self.branch_h, 8, self.branch_h), border_radius=2)

        pygame.draw.rect(surf, CACTUS_COLOR, (x_i, y_i, self.w, self.h), border_radius=4)

        needle_color = DAY_BG if BG_COLOR[0] > 100 else NIGHT_BG
        for nx, ny in self.needles:
            pygame.draw.rect(surf, needle_color, (x_i + nx, y_i + ny, 2, 2))

    def get_rect(self):
        left_ext  = self.branch_w if self.has_left_branch  else 0
        right_ext = self.branch_w if self.has_right_branch else 0

        full_x = int(self.x) - left_ext
        full_w = self.w + left_ext + right_ext

        highest_y = int(self.y)
        if self.has_left_branch:
            highest_y = min(highest_y, int(self.y) + self.left_branch_y - self.branch_h)
        if self.has_right_branch:
            highest_y = min(highest_y, int(self.y) + self.right_branch_y - self.branch_h)

        full_h = GROUND - highest_y
        return pygame.Rect(full_x, highest_y, full_w, full_h)