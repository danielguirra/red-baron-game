import pygame


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
