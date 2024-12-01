import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, shotting: bool):
        bullet = pygame.image.load("assets/bullet-1.png")

        if not shotting:
            bullet = pygame.image.load("assets/bullet-2.png")

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(
            bullet, (int(bullet.get_width() * 2), int(bullet.get_height() * 2))
        )

        self.rect = self.image.get_rect()
