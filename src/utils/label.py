import pygame


class Label:
    def __init__(self, text: str, color: pygame.Color, screen, rect=None):
        self.font = pygame.font.SysFont("comic sanss", 40)
        self.text = self.font.render(text, True, color)

        if rect is None:
            self.rect = pygame.Rect(
                (screen.get_width() - self.text.get_width()) / 2,
                screen.get_height() / 1.75,
                self.text.get_width(),
                self.text.get_height(),
            )
        else:
            self.rect = pygame.Rect(
                rect["x"],
                rect["y"],
                self.text.get_width(),
                self.text.get_height(),
            )

        screen.blit(self.text, self.rect.topleft)
