import pygame


class HealthBar:
    def __init__(self, x: int, y: int, w: int, h: int, hp: int, max_hp: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.max_hp = max_hp

    def drawX(self, surface: pygame.Surface, color1: str, color2: str):
        if self.hp <= 0:
            return
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, color1, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, color2, (self.x, self.y, self.w * ratio, self.h))

    def drawY(self, surface: pygame.Surface, color1: str, color2: str):
        if self.hp <= 0:
            return
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, color1, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(
            surface,
            color2,
            (
                self.x,
                self.y + (self.h * (1 - ratio)),
                self.w,
                self.h * ratio,
            ),
        )
