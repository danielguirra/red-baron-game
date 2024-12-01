import pygame


class Audios:
    def __init__(self) -> None:
        pygame.mixer.init(44100, -16, 2, 512)
        self.plane_bullet = pygame.mixer.Sound("assets/audio/heavy.wav")
        self.plane_prop = pygame.mixer.Sound("assets/audio/airplane_prop.ogg")
        self.plane_bullet_explosion = pygame.mixer.Sound(
            "assets/audio/explosion-shoot.wav"
        )

        self.theme = pygame.mixer.Sound("assets/audio/theme.wav")

        self.alien_droping = pygame.mixer.Sound("assets/audio/droping.wav")
