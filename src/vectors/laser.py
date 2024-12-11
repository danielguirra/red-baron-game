import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet):
        super().__init__()
        self.frames = []
        self.load_frames(sprite_sheet)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

    def load_frames(self, sprite_sheet):
        frame_width = 16
        frame_height = 16
        scale_factor = 3
        for i in range(6):
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            )

            scaled_frame = pygame.transform.scale(
                frame, (frame_width * scale_factor, frame_height * scale_factor)
            )
            self.frames.append(scaled_frame)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 756:
            self.last_update = now
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
