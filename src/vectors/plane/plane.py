from typing import List
import pygame
from src.vectors.plane.bullet import Bullet
from src.audios.audios import Audios

audios = Audios()


class Plane(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.space_pressed = False
        self.left_or_right = True
        self.hp = 100
        self.alive = True

        self.updown_image_propeller = 0
        self.right_image_propeller = 0
        self.leaf_image_propeller = 0
        self.is_alternating = False
        self.last_move_time = pygame.time.get_ticks()
        self.current_sprite = 0
        self.last_shot_time = 0
        self.bullets: List[Bullet] = []

        self.shot_cooldown = 200
        [self.image, self.rect] = self.get_plane_image(0)

        self.speed = 300

        self.turbo = False
        self.turbo_time = 0
        self.fire = False

    def get_plane_image(self, sprite: int):
        self.current_sprite = sprite

        self.propeller_images = [
            pygame.image.load("assets/redbaron-0.png"),
            pygame.image.load("assets/redbaron-1.png"),
            pygame.image.load("assets/redbaron-2.png"),
            pygame.image.load("assets/redbaron-3.png"),
            pygame.image.load("assets/redbaron-4.png"),
            pygame.image.load("assets/redbaron-5.png"),
        ]

        plane_image = self.propeller_images[sprite]

        plane_image_scaled = pygame.transform.scale(
            plane_image,
            (int(plane_image.get_width() * 3.5), int(plane_image.get_height() * 3.5)),
        )

        return [plane_image_scaled, plane_image_scaled.get_rect()]

    def plane_move(
        self,
        dt: float,
        keys: pygame.key.ScancodeWrapper,
        bullets: list,
        max_x: int,
        max_y: int,
        victory: bool,
    ):
        if not self.alive:
            return
        if self.turbo and pygame.time.get_ticks() - self.turbo_time >= 1000 * 5:
            self.turbo = False
            self.shot_cooldown *= 2
        if keys[pygame.K_t] and not self.turbo:
            self.turbo = True
            self.shot_cooldown /= 2
            self.turbo_time = pygame.time.get_ticks()

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y > 20:
            if self.updown_image_propeller == 0:
                [self.image, _] = self.get_plane_image(0)
                self.updown_image_propeller = 1
            else:
                [self.image, _] = self.get_plane_image(self.updown_image_propeller)
                self.updown_image_propeller = 0

            self.rect.y -= self.speed * dt
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.y < max_y:
            if self.updown_image_propeller == 0:
                [self.image, _] = self.get_plane_image(0)
                self.updown_image_propeller = 1
            else:
                [self.image, _] = self.get_plane_image(self.updown_image_propeller)
                self.updown_image_propeller = 0

            self.rect.y += self.speed * dt
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 0:
            if self.leaf_image_propeller == 4:
                [self.image, _] = self.get_plane_image(4)
                self.leaf_image_propeller = 5
            else:
                [self.image, _] = self.get_plane_image(5)
                self.leaf_image_propeller = 4

            self.rect.x -= self.speed * dt
            self.last_move_time = pygame.time.get_ticks()
            self.is_alternating = False
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < max_x:
            if self.right_image_propeller == 2:
                [self.image, _] = self.get_plane_image(2)
                self.right_image_propeller = 3
            else:
                [self.image, _] = self.get_plane_image(3)
                self.right_image_propeller = 2

            self.rect.x += self.speed * dt
            self.last_move_time = pygame.time.get_ticks()
            self.is_alternating = False

        current_time = pygame.time.get_ticks()
        if (
            keys[pygame.K_SPACE]
            and current_time - self.last_shot_time >= self.shot_cooldown
            and not victory
            and not self.fire
        ):
            self.fire = True
            bullet = Bullet(self.left_or_right)
            bullet.rect.center = (self.rect.x + 30, self.rect.y)

            bullets.append(bullet)
            self.last_shot_time = current_time
            self.left_or_right = not self.left_or_right
            audios.plane_bullet.play()
            self.fire = False
        self.bullets = bullets
