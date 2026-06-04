import pygame
from settings import GROUND, G, JUMP_F, DINO_COLOR, BG_COLOR

class Player:
    W, H = 32, 38

    def __init__(self):
        self.reset()

    def reset(self):
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
        self.y  += self.vy
        self.frame += 1
        if self.y >= GROUND - self.H - 10:
            self.y     = float(GROUND - self.H - 10)
            self.vy    = 0.0
            self.jumps = 0

    def draw(self, surf, current_speed):
        x, y = int(self.x), int(self.y)
        c = DINO_COLOR
        on_ground = self.y >= GROUND - self.H - 10
        adj_anim_speed = max(2, 7 - int(current_speed // 4))
        leg = (self.frame // adj_anim_speed) % 2

        pygame.draw.rect(surf, c, (x - 8,  y + 15, 10,  7), border_radius=2)
        pygame.draw.rect(surf, c, (x - 12, y + 18,  6,  5), border_radius=2)
        pygame.draw.rect(surf, c, (x,      y +  6, 28, 26), border_radius=4)
        pygame.draw.rect(surf, c, (x + 14, y -  2, 14, 12), border_radius=3)
        pygame.draw.rect(surf, c, (x + 10, y - 14, 22, 16), border_radius=4)
        pygame.draw.rect(surf, c, (x + 12, y - 22,  6, 10), border_radius=2)
        pygame.draw.rect(surf, c, (x + 20, y - 18,  5,  7), border_radius=2)
        pygame.draw.rect(surf, BG_COLOR, (x + 26, y - 10, 4, 4))
        pygame.draw.rect(surf, c, (x + 25, y +  1,  8,  4), border_radius=2)
        pygame.draw.rect(surf, c, (x + 16, y + 30,  8,  5), border_radius=2)

        if on_ground:
            if leg == 0:
                pygame.draw.rect(surf, c, (x +  3, y + 32, 8, 14), border_radius=2)
                pygame.draw.rect(surf, c, (x + 15, y + 32, 7, 10), border_radius=2)
            else:
                pygame.draw.rect(surf, c, (x +  3, y + 32, 7, 10), border_radius=2)
                pygame.draw.rect(surf, c, (x + 15, y + 32, 8, 14), border_radius=2)
        else:
            pygame.draw.rect(surf, c, (x +  3, y + 32, 8, 11), border_radius=2)
            pygame.draw.rect(surf, c, (x + 15, y + 32, 8, 11), border_radius=2)

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H + 10)