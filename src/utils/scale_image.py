import pygame


def scale_image(surface: pygame.Surface, value: float):
    return pygame.transform.scale(
        surface, (int(surface.get_width() * value), int(surface.get_height() * value))
    )
