import pygame
from src.vectors.explosion.explosion import Explosion
from src.vectors.alien.fireball import Fireball
from src.vectors.alien.laser import Laser
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

        self.alien_inverter_left_right = True

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

    def alien_move(self, dt: float, screen_width: int):
        maxX = screen_width - self.image.get_width()
        if not self.live:
            return
        if self.alien_inverter_left_right and self.rect.x > 0:
            self.in_left = False
            self.rect.x -= self.speed * dt
            if self.rect.x <= 0:
                self.alien_inverter_left_right = False
        if not self.alien_inverter_left_right:
            self.in_left = True
            self.rect.x += self.speed * dt
            if self.rect.x >= maxX:
                self.alien_inverter_left_right = True

        return self

    def shot(self, x: int, y: int, sprite_sheets):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            if self.hp < 30:
                fireball = Fireball(x, y, sprite_sheets)
                fireball.rect.center = (
                    self.rect.centerx,
                    self.rect.bottom,
                )
                self.bullets.add(fireball)

                self.last_shot_time = current_time
                audios.alien_shot.set_volume(0.12)
                audios.alien_shot.play()
                return
            else:
                laser = Laser(x, y, sprite_sheets)
                laser.rect.center = (
                    self.rect.centerx,
                    self.rect.bottom,
                )
                self.bullets.add(laser)

                self.last_shot_time = current_time
                audios.alien_shot.set_volume(0.06)
                audios.alien_shot.play()
                return
