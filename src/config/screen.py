import pygame


def Screen(
    sizeX: int,
    sizeY: int,
):
    icon = pygame.image.load("assets/redbaron-0.png")
    title = "Barão Vermelhão VS LELIGENA"
    display = pygame.display

    display.set_icon(icon)

    display.set_caption(title)

    return display.set_mode((sizeX, sizeY))
