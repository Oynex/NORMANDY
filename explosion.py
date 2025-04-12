import pygame
from pygame.sprite import Sprite
import math
import random

class Explosion(Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30  # Faster animation
        
        # Create particles
        self.particles = []
        for _ in range(20):  # More particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            particle = {
                'pos': list(center),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'size': random.uniform(2, 4),
                'life': random.randint(20, 40),
                'color': random.choice([
                    (255, 255, 0),  # Yellow
                    (255, 165, 0),  # Orange
                    (255, 0, 0),    # Red
                    (255, 255, 255) # White
                ])
            }
            self.particles.append(particle)
        
        # Create shockwave
        self.shockwave = {
            'radius': 0,
            'max_radius': size * 2,
            'width': 2,
            'color': (255, 255, 255)
        }
        
    def update(self):
        now = pygame.time.get_ticks()
        
        # Update particles
        for particle in self.particles[:]:
            particle['life'] -= 1
            particle['size'] -= 0.1
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.particles.remove(particle)
        
        # Update shockwave
        if self.shockwave['radius'] < self.shockwave['max_radius']:
            self.shockwave['radius'] += 5
            self.shockwave['width'] = max(1, self.shockwave['width'] - 0.1)
            self.shockwave['color'] = (
                max(0, self.shockwave['color'][0] - 5),
                max(0, self.shockwave['color'][1] - 5),
                max(0, self.shockwave['color'][2] - 5)
            )
        
        # Check if explosion is complete
        if not self.particles and self.shockwave['radius'] >= self.shockwave['max_radius']:
            self.kill()
    
    def draw(self, screen):
        # Draw shockwave
        if self.shockwave['radius'] < self.shockwave['max_radius']:
            pygame.draw.circle(screen, self.shockwave['color'],
                             (int(self.center[0]), int(self.center[1])),
                             int(self.shockwave['radius']),
                             int(self.shockwave['width']))
        
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 40))
            color = (*particle['color'], alpha)
            pygame.draw.circle(screen, color,
                             (int(particle['pos'][0]), int(particle['pos'][1])),
                             int(particle['size']))
            
            # Draw particle trail
            if particle['life'] > 20:  # Only draw trail for newer particles
                trail_length = 5
                for i in range(trail_length):
                    pos = (
                        particle['pos'][0] - particle['vel'][0] * i,
                        particle['pos'][1] - particle['vel'][1] * i
                    )
                    trail_alpha = int(alpha * (1 - i / trail_length))
                    trail_color = (*particle['color'], trail_alpha)
                    pygame.draw.circle(screen, trail_color,
                                     (int(pos[0]), int(pos[1])),
                                     int(particle['size'] * (1 - i / trail_length)))