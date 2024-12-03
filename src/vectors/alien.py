import pygame
from src.vectors.explosion import Explosion
from src.vectors.fireball import Fireball
from src.audios.audios import Audios

audios = Audios()


class Alien(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/leligena.png")

        self.hp = 100

        self.fury = False

        self.speed = 300

        self.last_shot_time = 0

        self.shot_cooldown = 700

        self.bullets = pygame.sprite.Group()

        self.live = True

        self.in_left = False

        self.rect = self.image.get_rect()

    def death_animation(self, screen, sprite_sheet_explosion, explosion_sprites):
        explosion = Explosion(
            x=self.rect.x + 15, y=self.rect.y, sprite_sheet=sprite_sheet_explosion
        )
        explosion_sprites.add(explosion)
        explosion_sprites.update()

        explosion_sprites.draw(screen)
        self.kill()

    def alien_move(self, dt: float, inverter: bool, screen_width: int):
        maxX = screen_width - self.image.get_width()
        if not self.live:
            return
        if inverter and self.rect.x > 0:
            self.in_left = False
            self.rect.x -= self.speed * dt
            if self.rect.x <= 0:
                inverter = False
        if not inverter:
            self.in_left = True
            self.rect.x += self.speed * dt
            if self.rect.x >= maxX:
                inverter = True

        return self, inverter

    def shot(self, x: int, y: int, sprite_sheets):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            fireball = Fireball(x, y, sprite_sheets)
            fireball.rect.center = (
                self.rect.centerx,
                self.rect.bottom,
            )
            self.bullets.add(fireball)

            self.last_shot_time = current_time
            audios.alien_shot.set_volume(0.025)
            audios.alien_shot.play()
