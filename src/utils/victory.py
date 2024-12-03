import pygame


def Victory(screen: pygame.Surface):
    font = pygame.font.SysFont("comic sanss", 40)
    victory_text = font.render("VICTORY", True, (0, 0, 0))
    victory_text_length_x = victory_text.get_width()

    screen.blit(
        victory_text,
        (
            (screen.get_width() - victory_text_length_x) / 2,
            screen.get_height() / 2.75,
        ),
    )
