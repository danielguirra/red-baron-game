import pygame


def paused(pygame: pygame, screen: pygame.Surface, pause: bool, clock, keys):
    if keys[pygame.K_p]:
        pause = not pause
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            font = pygame.font.SysFont("commic sanss", 40)
            pause_text = font.render("PAUSE", True, (0, 0, 0))

            pause_text_lenght_x = pause_text.get_width()

            screen.blit(
                pause_text,
                (
                    ((screen.get_width() - pause_text_lenght_x) / 2),
                    screen.get_height() / 2.75,
                ),
            )
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break
            pygame.display.update()
            clock.tick(15)
