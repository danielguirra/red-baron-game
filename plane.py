import pygame


plane_sprites = [
    pygame.image.load("assets/redbaron-0.png"),
    pygame.image.load("assets/redbaron-1.png"),
    pygame.image.load("assets/redbaron-2.png"),
    pygame.image.load("assets/redbaron-3.png"),
    pygame.image.load("assets/redbaron-4.png"),
    pygame.image.load("assets/redbaron-5.png"),
]


class Plane(pygame.sprite.Sprite):
    def __init__(self, key: int):
        plane = plane_sprites[key]

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(
            plane, (int(plane.get_width() * 3.5), int(plane.get_height() * 3.5))
        )

        self.rect = self.image.get_rect()
