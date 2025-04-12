import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # milliseconds between frames
        
        # Create explosion frames
        self.frames = []
        for i in range(8):  # 8 frames for the explosion
            frame = pygame.Surface((size, size), pygame.SRCALPHA)
            # Draw a circle that changes size and color
            radius = int(size * (1 - i/8))  # Shrinking radius
            color = (255, 255 - i*32, 0)  # Color changes from yellow to red
            pygame.draw.circle(frame, color, (size//2, size//2), radius)
            self.frames.append(frame)
        
        self.image = self.frames[0]
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()  # Remove the explosion when animation is complete
            else:
                self.image = self.frames[self.frame]
    
    def draw(self, screen):
        # Draw the current frame of the explosion on the screen
        screen.blit(self.image, self.rect)