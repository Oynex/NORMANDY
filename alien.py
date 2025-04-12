import pygame
from pygame.sprite import Sprite
import math
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the alien's exact position
        self.x = float(self.rect.x)
        
        # Animation properties
        self.animation_offset = 0
        self.animation_speed = ai_settings.alien_animation_speed
        self.animation_direction = 1
        
        # Create glow surface
        self.glow_surface = pygame.Surface((self.rect.width + ai_settings.alien_glow_radius * 2,
                                          self.rect.height + ai_settings.alien_glow_radius * 2),
                                         pygame.SRCALPHA)
        self.update_glow()
        
        # Particle effects
        self.particles = []
        self.particle_timer = 0
        self.particle_delay = random.randint(10, 30)

    def update_glow(self):
        self.glow_surface.fill((0, 0, 0, 0))
        center = (self.glow_surface.get_width() // 2, self.glow_surface.get_height() // 2)
        for radius in range(self.ai_settings.alien_glow_radius, 0, -1):
            alpha = int(255 * (radius / self.ai_settings.alien_glow_radius))
            color = (*self.ai_settings.alien_glow_color, alpha)
            pygame.draw.circle(self.glow_surface, color, center, radius)

    def update_particles(self):
        # Create new particles
        self.particle_timer += 1
        if self.particle_timer >= self.particle_delay:
            self.particle_timer = 0
            self.particle_delay = random.randint(10, 30)
            
            # Create particles around the alien
            for _ in range(3):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, self.rect.width // 2)
                pos = [
                    self.rect.centerx + math.cos(angle) * distance,
                    self.rect.centery + math.sin(angle) * distance
                ]
                particle = {
                    'pos': pos,
                    'size': random.uniform(1, 3),
                    'life': random.randint(10, 20),
                    'color': self.ai_settings.alien_glow_color,
                    'speed': [
                        random.uniform(-1, 1),
                        random.uniform(-1, 1)
                    ]
                }
                self.particles.append(particle)
        
        # Update existing particles
        for particle in self.particles[:]:
            particle['life'] -= 1
            particle['size'] -= 0.1
            particle['pos'][0] += particle['speed'][0]
            particle['pos'][1] += particle['speed'][1]
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 20))
            color = (*particle['color'], alpha)
            pygame.draw.circle(self.screen, color,
                             (int(particle['pos'][0]), int(particle['pos'][1])),
                             int(particle['size']))

    def update(self):
        # Update animation
        self.animation_offset += self.animation_speed * self.animation_direction
        if abs(self.animation_offset) > 5:
            self.animation_direction *= -1
        
        # Update position
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
        # Update particles
        self.update_particles()

    def blitme(self):
        # Draw glow
        glow_pos = (self.rect.x - self.ai_settings.alien_glow_radius,
                   self.rect.y - self.ai_settings.alien_glow_radius)
        self.screen.blit(self.glow_surface, glow_pos)
        
        # Draw particles
        self.draw_particles()
        
        # Draw alien with animation offset
        self.screen.blit(self.image, (self.rect.x, self.rect.y + self.animation_offset))

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

