import pygame
from plane import Plane
from alien import Alien, alien_move
from explosion import Explosion
from plane import plane_move
from plane import plane_audios
from health_bar import HealthBar
from paused import paused


from inactive_animation import inactive_animation

pygame.init()


screen = pygame.display.set_mode((540, 740))

icon = pygame.image.load("assets/redbaron-0.png")

pygame.display.set_icon(icon)

pygame.display.set_caption("Barão Vermelhão VS LELIGENA")
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


theme_audio = pygame.mixer.Sound("assets/audio/theme.wav")
theme_audio.play(-1).set_volume(0.35)

plane_audios[0].play(-1).set_volume(0.75)

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

    [
        last_move_time,
        is_alternating,
        space_pressed,
        shoting,
        plane,
        right_image_propeller,
        leaf_image_propeller,
        updown_image_propeller,
    ] = plane_move(
        updown_image_propeller=updown_image_propeller,
        leaf_image_propeller=leaf_image_propeller,
        right_image_propeller=right_image_propeller,
        dt=dt,
        keys=keys,
        space_pressed=space_pressed,
        shoting=shoting,
        plane=plane,
        bullets=bullets,
        last_move_time=last_move_time,
        is_alternating=is_alternating,
    )

    [is_alternating, current_sprite, plane, last_animation_time] = inactive_animation(
        last_move_time,
        INACTIVITY_THRESHOLD,
        pygame.time.get_ticks(),
        is_alternating,
        last_animation_time,
        ANIMATION_INTERVAL,
        current_sprite,
        plane,
    )

    alien_helth_bar.draw(screen)

    for bullet in bullets:
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
                pygame.mixer.Sound("assets/audio/droping.wav").play()
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

            plane_audios[2].play()

        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        screen.blit(bullet.image, bullet.rect)

    if alien.live:
        alien_moving = alien_move(alien, dt, inverter)
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
