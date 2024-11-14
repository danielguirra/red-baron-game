import pygame

bullet_1 = pygame.image.load("bullet-1.png")

bullet_2 = pygame.image.load("bullet-2.png")


class Bullet(pygame.sprite.Sprite):
    def __init__(self, shotting: bool):
        bullet = bullet_1

        if not shotting:
            bullet = bullet_2

        pygame.sprite.Sprite.__init__(self)

        self.image = bullet

        self.rect = self.image.get_rect()