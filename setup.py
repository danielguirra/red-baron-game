import pygame
from bullet import Bullet
from plane import Plane

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

shoting = True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
bullets = []
space_pressed = False


ANIMATION_INTERVAL = 0.025
INACTIVITY_THRESHOLD = 0.02
last_move_time = pygame.time.get_ticks()
last_animation_time = pygame.time.get_ticks()
is_alternating = False
current_sprite = 0

plane = Plane(current_sprite)
plane.rect.center = (player_pos.x, player_pos.y)
updown_image_propeller = 0

leaf_image_propeller = 4

right_image_propeller = 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    screen.fill("gray")
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        if updown_image_propeller == 0:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 1
        else:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 0

        plane.rect.y -= 300 * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False
    if keys[pygame.K_s]:
        if updown_image_propeller == 0:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 1
        else:
            plane.image = Plane(updown_image_propeller).image
            updown_image_propeller = 0
        plane.rect.y += 300 * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False
    if keys[pygame.K_a]:
        if leaf_image_propeller == 4:
            plane.image = Plane(leaf_image_propeller).image
            leaf_image_propeller = 5
        else:
            plane.image = Plane(leaf_image_propeller).image
            leaf_image_propeller = 4
        plane.rect.x -= 300 * dt
        last_move_time = pygame.time.get_ticks()
        is_alternating = False
    if keys[pygame.K_d]:
        if right_image_propeller == 2:
            plane.image = Plane(right_image_propeller).image
            right_image_propeller = 3
        else:
            plane.image = Plane(right_image_propeller).image
            right_image_propeller = 2
        plane.rect.x += 300 * dt
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

    if pygame.time.get_ticks() - last_move_time > INACTIVITY_THRESHOLD * 1000:
        is_alternating = True

    if is_alternating and (
        pygame.time.get_ticks() - last_animation_time > ANIMATION_INTERVAL * 1000
    ):
        current_sprite = 1 if current_sprite == 0 else 0
        plane.image = Plane(current_sprite).image
        last_animation_time = pygame.time.get_ticks()

    for bullet in bullets:
        bullet.rect.y -= 500 * dt
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        screen.blit(bullet.image, bullet.rect)

    screen.blit(plane.image, plane.rect)
    pygame.display.flip()

pygame.quit()
