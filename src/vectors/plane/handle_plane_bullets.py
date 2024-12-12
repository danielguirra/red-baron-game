import pygame
from src.vectors.explosion.explosion import Explosion
from src.vectors.alien.alien import Alien
from src.vectors.plane.plane import Plane
from src.audios.audios import Audios


def handle_plane_bullets(
    plane: Plane,
    alien: Alien,
    screen: pygame.Surface,
    dt: float,
    bullets: list,
    sprite_sheet_explosion: pygame.Surface,
    explosion_sprites: pygame.Surface,
    health_bar_alien: pygame.Surface,
    audios: Audios,
):
    for bullet in plane.bullets:
        bullet.rect.y -= 500 * dt

        if pygame.sprite.collide_rect(bullet, alien) and alien.live:
            alien.hp -= 1.5

            if alien.hp <= 50:
                alien.speed = 600

            health_bar_alien.hp = alien.hp
            health_bar_alien.drawX(screen, "red", "green")
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
