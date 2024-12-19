import pygame
from src.utils.label import Label


def lose(screen: pygame.Surface):
    font = pygame.font.SysFont("comic sanss", 40)
    lose_text = font.render("YOU LosE", True, (255, 255, 255))
    lose_text_length_x = lose_text.get_width()

    screen.blit(
        lose_text,
        (
            (screen.get_width() - lose_text_length_x) / 2,
            screen.get_height() / 2.75,
        ),
    )

    play_again_label = Label(
        "Play Again",
        (255, 255, 255),
        screen,
    )
    rect = {
        "x": (screen.get_width() - 291) / 2,
        "y": screen.get_height() / 1.5,
    }
    Label("Click or Press ENTER", (125, 125, 125), screen, rect)
    return play_again_label
