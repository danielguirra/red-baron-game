import pygame
from plane import Plane
from alien import Alien
from explosion import Explosion

from health_bar import HealthBar
from paused import paused
from audios import Audios


from inactive_animation import inactive_animation

pygame.init()


screen = pygame.display.set_mode((540, 740))

icon = pygame.image.load("assets/redbaron-0.png")

pygame.display.set_icon(icon)

pygame.display.set_caption("Barão Vermelhão VS LELIGENA")
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
bullets = []
space_pressed = False


ANIMATION_INTERVAL = 0.025
INACTIVITY_THRESHOLD = 0.02

last_move_time = pygame.time.get_ticks()
last_animation_time = pygame.time.get_ticks()


plane = Plane()
plane.rect.center = (player_pos.x, player_pos.y + 300)
updown_image_propeller = 0

leaf_image_propeller = 4

right_image_propeller = 2

alien = Alien()
inverter = True
alien.rect.center = (player_pos.x, player_pos.y - 300)
alien_helth_bar = HealthBar(x=0, y=0, w=540, h=10, hp=alien.hp, max_hp=100)
alien_helth_50 = False

explosion_sprites = pygame.sprite.Group()
sprite_sheet_explosion = pygame.image.load("assets/Explosion.png")
sprite_sheet_explosion = sprite_sheet_explosion.convert_alpha()


audios = Audios()
audios.theme.play(-1).set_volume(0.35)

audios.plane_prop.play(-1).set_volume(0.75)

pause = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    explosion_sprites.update()
    screen.fill("gray")
    explosion_sprites.draw(screen)
    keys = pygame.key.get_pressed()

    plane.plane_move(
        dt=dt,
        keys=keys,
        bullets=bullets,
    )

    [plane, last_animation_time] = inactive_animation(
        INACTIVITY_THRESHOLD=INACTIVITY_THRESHOLD,
        ticks=pygame.time.get_ticks(),
        last_animation_time=last_animation_time,
        ANIMATION_INTERVAL=ANIMATION_INTERVAL,
        last_move_time=last_move_time,
        plane=plane,
    )

    alien_helth_bar.draw(screen)

    for bullet in plane.bullets:
        bullet.rect.y -= 500 * dt

        if pygame.sprite.collide_rect(bullet, alien):
            alien.hp = alien.hp - 1

            if alien.hp <= 50 and not alien_helth_50:
                alien.speed = alien.speed * 2
                alien_helth_50 = True

            alien_helth_bar.hp = alien.hp
            alien_helth_bar.draw(screen)
            bullets.remove(bullet)

            if alien.hp <= 0:
                alien.death_animation(screen, sprite_sheet_explosion, explosion_sprites)
                alien.live = False
                audios.alien_droping.play()
                alien.kill()
                continue

            if not alien.live:
                continue

            explosion = Explosion(
                x=alien.rect.x, y=alien.rect.y, sprite_sheet=sprite_sheet_explosion
            )
            explosion_sprites.add(explosion)
            explosion_sprites.update()

            explosion_sprites.draw(screen)

            audios.plane_bullet_explosion.play()

        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        screen.blit(bullet.image, bullet.rect)

    if alien.live:
        alien_moving = alien.alien_move(dt, inverter, screen.get_width())
        if alien_moving:
            alien = alien_moving[0]
            inverter = alien_moving[1]
            screen.blit(alien.image, alien.rect)
    else:
        alien.rect.y = 3000

    screen.blit(plane.image, plane.rect)
    paused(pygame=pygame, screen=screen, clock=clock, pause=pause, keys=keys)
    pygame.display.flip()

pygame.quit()
