import pygame
from src.vectors.explosion.explosion import Explosion
from src.vectors.alien.alien import Alien
from src.vectors.plane.plane import Plane
from src.audios.audios import Audios


def handle_alien_bullets(
    alien: Alien,
    plane: Plane,
    screen: pygame.Surface,
    dt: float,
    lose_playning: bool,
    theme: pygame.mixer_music,
    audios: Audios,
    boos_music: pygame.mixer_music,
    health_bar_plane: pygame.Surface,
    sprite_sheet_explosion: pygame.Surface,
    explosion_sprites: pygame.Surface,
):
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
                    boos_music.set_volume(0.75)
                    boos_music.play(-1)
            plane.hp -= 10
            alien.bullets.remove(bullet)
            explosion = Explosion(
                x=plane.rect.x + (plane.image.get_width() / 2),
                y=plane.rect.y,
                sprite_sheet=sprite_sheet_explosion,
            )
            explosion_sprites.add(explosion)
            explosion_sprites.update()
            explosion_sprites.draw(screen)

            health_bar_plane.hp = plane.hp
            audios.plane_bullet_explosion.play()

        elif bullet.rect.y > screen.get_height():
            alien.bullets.remove(bullet)
        else:
            bullet.update()
            screen.blit(bullet.image, bullet.rect)
