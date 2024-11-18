import pygame
from bullet import Bullet

plane_sprites = [
    pygame.image.load("assets/redbaron-0.png"),
    pygame.image.load("assets/redbaron-1.png"),
    pygame.image.load("assets/redbaron-2.png"),
    pygame.image.load("assets/redbaron-3.png"),
    pygame.image.load("assets/redbaron-4.png"),
    pygame.image.load("assets/redbaron-5.png"),
]


class Plane(pygame.sprite.Sprite):
    def __init__(self, sprite: int):
        plane = plane_sprites[sprite]

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(
            plane, (int(plane.get_width() * 3.5), int(plane.get_height() * 3.5))
        )

        self.speed = 300

        self.rect = self.image.get_rect()


def plane_move(
    updown_image_propeller: int,
    leaf_image_propeller: int,
    right_image_propeller: int,
    dt: float,
    keys: pygame.key.ScancodeWrapper,
    space_pressed: bool,
    shoting: bool,
    plane: Plane,
    last_move_time: int,
    is_alternating: bool,
    bullets: list,
):
    if keys[pygame.K_w]:
        if updown_image_propeller == 0:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 1
        else:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 0

        plane.rect.y -= plane.speed * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False
    if keys[pygame.K_s]:
        if updown_image_propeller == 0:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 1
        else:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 0
        plane.rect.y += plane.speed * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False
    if keys[pygame.K_a] and plane.rect.x > 0:
        if leaf_image_propeller == 4:
            plane.image = Plane(leaf_image_propeller).image
            leaf_image_propeller = 5
        else:
            plane.image = Plane(leaf_image_propeller).image
            leaf_image_propeller = 4
        plane.rect.x -= plane.speed * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False
    if keys[pygame.K_d] and plane.rect.x < 490:
        if right_image_propeller == 2:
            plane.image = Plane(right_image_propeller).image
            right_image_propeller = 3
        else:
            plane.image = Plane(right_image_propeller).image
            right_image_propeller = 2
        plane.rect.x += plane.speed * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False

    if keys[pygame.K_SPACE] and not space_pressed:
        bullet = Bullet(shoting)
        bullet.rect.center = (plane.rect.x + 30, plane.rect.y)

        bullets.append(bullet)
        shoting = not shoting
        space_pressed = True
    if not keys[pygame.K_SPACE]:
        space_pressed = False
    # Teste para aumentar a velocidade
    # if keys[pygame.K_p]:
    #     plane.speed = plane.speed + 20

    return [
        last_move_time,
        is_alternating,
        space_pressed,
        shoting,
        plane,
        right_image_propeller,
        leaf_image_propeller,
        updown_image_propeller,
    ]
