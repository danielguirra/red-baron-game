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
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, color1, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, color2, (self.x, self.y, self.w * ratio, self.h))

        if self.hp <= 0:
            pygame.draw.rect(surface, "gray", (self.x, self.y, self.w, self.h))

    def drawY(self, surface: pygame.Surface, color1: str, color2: str):
        # Calcula a proporção da vida restante
        ratio = self.hp / self.max_hp

        # Desenha o retângulo de fundo (cor1)
        pygame.draw.rect(surface, color1, (self.x, self.y, self.w, self.h))

        # Desenha o retângulo da barra de vida restante (cor2)
        pygame.draw.rect(
            surface,
            color2,
            (
                self.x,
                self.y + (self.h * (1 - ratio)),  # Ajusta a posição inicial em Y
                self.w,
                self.h * ratio,  # Ajusta a altura proporcional
            ),
        )

        # Quando a vida é 0, desenha em cinza
        if self.hp <= 0:
            pygame.draw.rect(surface, "gray", (self.x, self.y, self.w, self.h))
