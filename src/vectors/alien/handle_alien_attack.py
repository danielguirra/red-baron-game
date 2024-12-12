from src.vectors.alien.alien import Alien
from src.vectors.plane.plane import Plane
import pygame


def handle_alien_attack(
    alien: Alien,
    plane: Plane,
    lose_playning: bool,
    left_alien_shot: bool,
    sprite_sheet_laser: pygame.Surface,
    sprite_sheet_fireball: pygame.Surface,
):
    if alien.hp < 95:
        alien.fury = True

    if alien.fury and alien.live and not lose_playning and plane.alive:
        shot_sprite = sprite_sheet_laser
        x = alien.rect.x - alien.image.get_width()

        if alien.hp < 30:
            alien.shot_cooldown = 200
            shot_sprite = sprite_sheet_fireball

        alien.shot(
            x,
            alien.rect.y,
            shot_sprite,
        )

        return not left_alien_shot
    return left_alien_shot
