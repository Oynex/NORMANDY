import pygame
from pygame.sprite import Sprite
import math

class Ship(Sprite):
    def __init__(self, ai_settings, screen, is_player=True):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Only position at bottom center if it's the player ship
        if is_player:
            self.rect.centerx = self.screen_rect.centerx
            self.rect.bottom = self.screen_rect.bottom
            self.center = float(self.rect.centerx)
        else:
            # For non-player ships (like life indicators), position will be set after creation
            self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        
        # Animation properties
        self.thruster_particles = []
        self.thruster_timer = 0
        self.thruster_delay = 2  # frames between particles
        
        # Create glow surface
        self.glow_surface = pygame.Surface((self.rect.width + ai_settings.ship_glow_radius * 2,
                                          self.rect.height + ai_settings.ship_glow_radius * 2),
                                         pygame.SRCALPHA)
        self.update_glow()

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center
        
        # Update thruster particles
        self.update_thruster()
    
    def update_thruster(self):
        # Create new particles
        self.thruster_timer += 1
        if self.thruster_timer >= self.thruster_delay:
            self.thruster_timer = 0
            particle = {
                'pos': [self.rect.centerx, self.rect.bottom],
                'size': 3,
                'life': 20,
                'color': (0, 255, 255)
            }
            self.thruster_particles.append(particle)
        
        # Update existing particles
        for particle in self.thruster_particles[:]:
            particle['life'] -= 1
            particle['size'] -= 0.1
            particle['pos'][1] += 2  # Move downward
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.thruster_particles.remove(particle)
    
    def update_glow(self):
        self.glow_surface.fill((0, 0, 0, 0))
        center = (self.glow_surface.get_width() // 2, self.glow_surface.get_height() // 2)
        for radius in range(self.ai_settings.ship_glow_radius, 0, -1):
            alpha = int(255 * (radius / self.ai_settings.ship_glow_radius))
            color = (*self.ai_settings.ship_glow_color, alpha)
            pygame.draw.circle(self.glow_surface, color, center, radius)

    def draw_thruster(self):
        for particle in self.thruster_particles:
            pygame.draw.circle(self.screen, particle['color'],
                             (int(particle['pos'][0]), int(particle['pos'][1])),
                             int(particle['size']))

    def blitme(self):
        # Only draw thrusters for player ship
        if hasattr(self, 'moving_right') and (self.moving_right or self.moving_left):
            # Draw glow
            glow_pos = (self.rect.x - self.ai_settings.ship_glow_radius,
                       self.rect.y - self.ai_settings.ship_glow_radius)
            self.screen.blit(self.glow_surface, glow_pos)
            
            # Draw ship
            self.screen.blit(self.image, self.rect)
            
            # Draw thruster
            self.draw_thruster()
        else:
            # For life indicators, just draw the ship without effects
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
