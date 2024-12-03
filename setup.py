import pygame
from src.vectors.plane import Plane
from src.vectors.alien import Alien
from src.vectors.explosion import Explosion

from src.utils.health_bar import HealthBar
from src.utils.paused import paused
from src.utils.victory import Victory
from src.audios.audios import Audios


from src.utils.inactive_animation import inactive_animation

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


alien = Alien()
inverter = True
alien.rect.center = (player_pos.x, player_pos.y - 300)
alien_helth_bar = HealthBar(x=0, y=0, w=540, h=10, hp=alien.hp, max_hp=100)
alien_helth_50 = False

explosion_sprites = pygame.sprite.Group()
sprite_sheet_explosion = pygame.image.load("assets/Explosion.png")
sprite_sheet_explosion = sprite_sheet_explosion.convert_alpha()

fireball_sprites = pygame.sprite.Group()
sprite_sheet_fireball = pygame.image.load("assets/alien_shot/Fireball-All.png")
sprite_sheet_fireball = sprite_sheet_fireball.convert_alpha()

audios = Audios()
theme = audios.theme
theme.play(-1).set_volume(0.35)

boos_music = audios.boos

victory_playning = False

lose_playning = False

audios.plane_prop.play(-1).set_volume(0.25)

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
        max_x=screen.get_width() - 40,
        max_y=screen.get_height() - 60,
        victory=not alien.live,
    )

    [plane.current_sprite, plane, last_animation_time] = inactive_animation(
        INACTIVITY_THRESHOLD=INACTIVITY_THRESHOLD,
        ticks=pygame.time.get_ticks(),
        last_animation_time=last_animation_time,
        ANIMATION_INTERVAL=ANIMATION_INTERVAL,
        last_move_time=plane.last_move_time,
        current_sprite=plane.current_sprite,
        plane=plane,
    )

    alien_helth_bar.draw(screen)

    if alien.hp < 95:
        alien.fury = True

    if alien.fury and alien.live and not lose_playning:
        if alien.hp < 20:
            alien.shot_cooldown = 200
        alien.shot(
            alien.rect.x - alien.image.get_width(),
            alien.rect.y,
            sprite_sheet_fireball,
        )

    for bullet in alien.bullets:
        if lose_playning:
            break
        bullet.rect.y += screen.get_height() * dt

        if pygame.sprite.collide_rect(bullet, plane) and plane.alive:
            if plane.hp <= 0:
                theme.stop()
                plane.alive = False
                plane.rect.y = screen.get_height() + 500
                if plane.rect.y > screen.get_height():
                    plane.kill()
                    audios.alien_droping.play()
                    boos_music.play(-1)
                    lose_playning = True

            plane.hp = plane.hp - 10

            alien.bullets.remove(bullet)
            explosion = Explosion(
                x=plane.rect.x,
                y=plane.rect.y,
                sprite_sheet=sprite_sheet_explosion,
            )
            explosion_sprites.add(explosion)
            explosion_sprites.update()

            explosion_sprites.draw(screen)

            audios.plane_bullet_explosion.play()

        if bullet.rect.y > screen.get_height():
            alien.bullets.remove(bullet)
        else:
            bullet.update()
            screen.blit(bullet.image, bullet.rect)
    for bullet in plane.bullets:
        bullet.rect.y -= 500 * dt

        if pygame.sprite.collide_rect(bullet, alien) and alien.live:
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

            alien_position_x = alien.rect.x
            if alien.in_left:
                alien_position_x += alien.image.get_width() / 1.25

            explosion = Explosion(
                x=alien_position_x,
                y=alien.rect.y,
                sprite_sheet=sprite_sheet_explosion,
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
    if not alien.live:
        theme.stop()
        if not victory_playning:
            audios.victory.play(-1)
            victory_playning = True
        Victory(screen=screen)
    paused(pygame=pygame, screen=screen, clock=clock, pause=pause, keys=keys)
    pygame.display.flip()

pygame.quit()
