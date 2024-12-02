import pygame
from src.vectors.bullet import Bullet
from src.audios.audios import Audios

audios = Audios()


class Plane(pygame.sprite.Sprite):
    def __init__(
        self,
    ):
        super().__init__()
        self.space_pressed = False
        self.left_or_right = True
        self.life = 100

        self.updown_image_propeller = 0
        self.right_image_propeller = 0
        self.leaf_image_propeller = 0
        self.is_alternating = False
        self.last_move_time = pygame.time.get_ticks()
        self.current_sprite = 0
        self.last_shot_time = 0
        self.shot_cooldown = 120
        [self.image, self.rect] = self.get_plane_image(0)
        self.speed = 300

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
    ):
        if keys[pygame.K_w] and self.rect.y > 20:
            if self.updown_image_propeller == 0:
                [self.image, _] = self.get_plane_image(0)
                self.updown_image_propeller = 1
            else:
                [self.image, _] = self.get_plane_image(self.updown_image_propeller)
                self.updown_image_propeller = 0

            self.rect.y -= self.speed * dt
        if keys[pygame.K_s] and self.rect.y < max_y:
            if self.updown_image_propeller == 0:
                [self.image, _] = self.get_plane_image(0)
                self.updown_image_propeller = 1
            else:
                [self.image, _] = self.get_plane_image(self.updown_image_propeller)
                self.updown_image_propeller = 0

            self.rect.y += self.speed * dt
        if keys[pygame.K_a] and self.rect.x > 0:
            if self.leaf_image_propeller == 4:
                [self.image, _] = self.get_plane_image(4)
                self.leaf_image_propeller = 5
            else:
                [self.image, _] = self.get_plane_image(5)
                self.leaf_image_propeller = 4

            self.rect.x -= self.speed * dt
            self.last_move_time = pygame.time.get_ticks()
            self.is_alternating = False
        if keys[pygame.K_d] and self.rect.x < max_x:
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
        ):
            bullet = Bullet(self.left_or_right)
            bullet.rect.center = (self.rect.x + 30, self.rect.y)

            bullets.append(bullet)
            self.last_shot_time = current_time
            self.left_or_right = not self.left_or_right
            audios.plane_bullet.play()
        self.bullets = bullets
