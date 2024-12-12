import pygame
from src.vectors.plane.plane import Plane
from src.vectors.alien.alien import Alien

from src.utils.health_bar import HealthBar
from src.utils.paused import paused
from src.utils.victory import Victory
from src.utils.lose import lose
from src.audios.audios import Audios
from src.config.screen import Screen
from src.vectors.alien.handle_alien_attack import handle_alien_attack
from src.vectors.alien.handle_alien_bullets import handle_alien_bullets
from src.vectors.plane.handle_plane_bullets import handle_plane_bullets

from src.utils.inactive_animation import inactive_animation

pygame.init()


screen = Screen(
    540,
    740,
)


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


alien = Alien()
alien.rect.center = (player_pos.x, player_pos.y - 300)
health_bar_alien = HealthBar(x=0, y=0, w=540, h=10, hp=alien.hp, max_hp=100)

plane = Plane()
plane.rect.center = (player_pos.x, player_pos.y + 300)
health_bar_plane = HealthBar(
    x=0,
    y=screen.get_height() / 2.20,
    w=10,
    h=screen.get_height() / 2.25,
    hp=plane.hp,
    max_hp=100,
)


explosion_sprites = pygame.sprite.Group()
sprite_sheet_explosion = pygame.image.load("assets/Explosion.png")
sprite_sheet_explosion = sprite_sheet_explosion.convert_alpha()

fireball_sprites = pygame.sprite.Group()
sprite_sheet_fireball = pygame.image.load("assets/alien_shot/Fireball-All.png")
sprite_sheet_fireball = sprite_sheet_fireball.convert_alpha()

laser_sprites = pygame.sprite.Group()
sprite_sheet_laser = pygame.image.load("assets/alien_shot/Laser/laser.png")
sprite_sheet_laser = sprite_sheet_laser.convert_alpha()

audios = Audios()
theme = pygame.mixer.music
theme.load("assets/audio/theme.wav")
theme.play(-1)
theme.set_volume(0.09)

boos_music = pygame.mixer.music


win = True
lose_playning = False

left_alien_shot = False

plane_prop_audio = audios.plane_prop
plane_prop_audio.play(-1).set_volume(0.25)

pause = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if lose_playning:
        pygame.mixer.music.stop()
        boos_music.load("assets/audio/boos-loop.wav")
        boos_music.play(-1)
        lose_playning = not lose_playning

    if not plane.alive:
        plane_prop_audio.stop()
    dt = clock.tick(60) / 1000
    explosion_sprites.update()
    screen.fill("gray")
    explosion_sprites.draw(screen)
    keys = pygame.key.get_pressed()

    if plane.alive:
        plane.plane_move(
            dt=dt,
            keys=keys,
            bullets=bullets,
            max_x=screen.get_width() - 40,
            max_y=screen.get_height() - 60,
            victory=not alien.live,
        )

        (plane.current_sprite, plane, last_animation_time) = inactive_animation(
            INACTIVITY_THRESHOLD=INACTIVITY_THRESHOLD,
            ticks=pygame.time.get_ticks(),
            last_animation_time=last_animation_time,
            ANIMATION_INTERVAL=ANIMATION_INTERVAL,
            last_move_time=plane.last_move_time,
            current_sprite=plane.current_sprite,
            plane=plane,
        )

        handle_plane_bullets(
            plane,
            alien,
            screen,
            dt,
            plane.bullets,
            sprite_sheet_explosion,
            explosion_sprites,
            health_bar_alien,
            audios,
        )
        health_bar_plane.drawY(screen, "red", "white")

    if alien.live:
        if alien.hp < 95:
            alien.fury = True

            left_alien_shot = handle_alien_attack(
                alien,
                plane,
                lose_playning,
                left_alien_shot,
                sprite_sheet_laser,
                sprite_sheet_fireball,
            )

        lose_playning = handle_alien_bullets(
            alien,
            plane,
            screen,
            dt,
            lose_playning,
            theme,
            audios,
            boos_music,
            health_bar_plane,
            sprite_sheet_explosion,
            explosion_sprites,
        )
        alien.alien_move(dt, screen.get_width())

        screen.blit(alien.image, alien.rect)
        health_bar_alien.drawX(screen, "red", "green")
    else:
        alien.rect.y = 3000
        alien.kill()

    screen.blit(plane.image, plane.rect)

    if not alien.live:
        plane_prop_audio.stop()
        theme.stop()
        win = Victory(screen=screen, win=win)

    if not plane.alive:
        lose(screen=screen)
    paused(pygame, screen, clock, pause, keys)
    pygame.display.flip()

pygame.quit()
