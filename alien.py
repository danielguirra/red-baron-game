import pygame

alien_sprite = pygame.image.load("assets/leligena.png")


class Alien(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.image = alien_sprite

        self.speed = 150

        self.rect = self.image.get_rect()


def alien_move(alien: Alien, dt: float, inverter: bool):
    if inverter and alien.rect.x > 0:
        alien.rect.x -= alien.speed * dt
        if alien.rect.x <= 0:
            inverter = False
    if not inverter:
        alien.rect.x += alien.speed * dt
        if alien.rect.x >= 540:
            inverter = True

    return alien, inverter
