import pygame

from src.utils.scale_image import scale_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, shotting: bool, x: int, y: int, sprite_sheet):
        super().__init__()

        self.frames = []
        self.load_frames(sprite_sheet)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

        self.speed = 700

    def load_frames(self, sprite_sheet):
        frame_width = 32
        frame_height = 32
        for i in range(6):
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            )
            scaled_frame = scale_image(frame, 2.5)

            self.frames.append(scaled_frame)

    def update(self, dt):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()

        self.rect.y -= self.speed * dt

        if self.rect.top < 0:
            self.kill()
