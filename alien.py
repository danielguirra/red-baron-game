import pygame

alien_sprite = pygame.image.load("assets/leligena.png")


class Alien(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.image = alien_sprite

        self.rect = self.image.get_rect()
