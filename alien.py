import pygame
from explosion import Explosion

alien_sprite = pygame.image.load("assets/leligena.png")


class Alien(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.image = alien_sprite

        self.hp = 100

        self.speed = 230

        self.live = True

        self.rect = self.image.get_rect()

    def death_animation(self, screen, sprite_sheet_explosion, explosion_sprites):
        explosion = Explosion(
            x=self.rect.x + 15, y=self.rect.y, sprite_sheet=sprite_sheet_explosion
        )
        explosion_sprites.add(explosion)
        explosion_sprites.update()

        explosion_sprites.draw(screen)
        self.kill()


def alien_move(alien: Alien, dt: float, inverter: bool):
    if not alien.live:
        return
    if inverter and alien.rect.x > 0:
        alien.rect.x -= alien.speed * dt
        if alien.rect.x <= 0:
            inverter = False
    if not inverter:
        alien.rect.x += alien.speed * dt
        if alien.rect.x >= 540:
            inverter = True

    return alien, inverter
