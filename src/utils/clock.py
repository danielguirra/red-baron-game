import pygame


def clock_timer(time: float, screen: pygame.Surface):
    font = pygame.font.SysFont("comic sans ms", 22)

    time_text = f"{time:.1f}"

    time_surface = font.render(time_text, True, (255, 255, 255))

    x = screen.get_width() - time_surface.get_width() - 5
    y = 40

    screen.blit(time_surface, (x, y))
