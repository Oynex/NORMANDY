import pygame
from pygame.sprite import Sprite
import math

class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship, is_fat=False):
        super(Bullet, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.is_fat = is_fat
        
        if is_fat:
            # Create fat bullet surface
            self.image = pygame.Surface((ai_settings.fat_bullet_width, ai_settings.fat_bullet_height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.centerx = ship.rect.centerx  # Center horizontally on ship
            self.rect.bottom = ship.rect.top  # Start from ship's top
            
            # Store the bullet's position
            self.y = float(self.rect.y)
            self.speed_factor = ai_settings.fat_bullet_speed
            
            # Create collision rect (slightly smaller than visual)
            self.collision_rect = pygame.Rect(0, 0, 
                                           ai_settings.fat_bullet_width - 20,
                                           ai_settings.fat_bullet_height)
            self.collision_rect.center = self.rect.center
            
            # Create glow surface for fat bullet
            self.glow_surface = pygame.Surface((self.rect.width + ai_settings.fat_bullet_glow_radius * 2,
                                              self.rect.height + ai_settings.fat_bullet_glow_radius * 2),
                                             pygame.SRCALPHA)
            self.update_fat_glow()
            self.update_fat_bullet_surface()
        else:
            # Create normal bullet surface
            self.image = pygame.Surface((ai_settings.bullet_width, ai_settings.bullet_height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.centerx = ship.rect.centerx
            self.rect.top = ship.rect.top
            
            # Store the bullet's position
            self.y = float(self.rect.y)
            self.speed_factor = ai_settings.bullet_speed_factor
            
            # Create glow surface
            self.glow_surface = pygame.Surface((self.rect.width + ai_settings.bullet_glow_radius * 2,
                                              self.rect.height + ai_settings.bullet_glow_radius * 2),
                                             pygame.SRCALPHA)
            self.update_glow()
            self.update_bullet_surface()
            
            # Trail properties
            self.trail_positions = []
            self.trail_length = ai_settings.bullet_trail_length

    def update_fat_glow(self):
        self.glow_surface.fill((0, 0, 0, 0))
        center = (self.glow_surface.get_width() // 2, self.glow_surface.get_height() // 2)
        
        # Create a more intense glow effect
        for radius in range(self.ai_settings.fat_bullet_glow_radius * 2, 0, -1):
            alpha = int(255 * (radius / (self.ai_settings.fat_bullet_glow_radius * 2)))
            color = (*self.ai_settings.fat_bullet_glow_color, alpha)
            pygame.draw.rect(self.glow_surface, color,
                           (self.ai_settings.fat_bullet_glow_radius - radius,
                            self.ai_settings.fat_bullet_glow_radius - radius,
                            self.rect.width + radius * 2,
                            self.rect.height + radius * 2))

    def update_fat_bullet_surface(self):
        # Draw fat bullet with more intense gradient
        for i in range(self.rect.width):
            # Create a more visible gradient
            alpha = int(255 * (1 - (i / self.rect.width) ** 2))
            color = (*self.ai_settings.fat_bullet_color, alpha)
            pygame.draw.line(self.image, color, 
                           (i, 0), (i, self.rect.height - 1))

    def update_bullet_surface(self):
        # Draw bullet with gradient
        for i in range(self.rect.height):
            alpha = int(255 * (1 - i / self.rect.height))
            color = (*self.ai_settings.bullet_color, alpha)
            pygame.draw.line(self.image, color, 
                           (0, i), (self.rect.width - 1, i))

    def update_glow(self):
        self.glow_surface.fill((0, 0, 0, 0))
        center = (self.glow_surface.get_width() // 2, self.glow_surface.get_height() // 2)
        for radius in range(self.ai_settings.bullet_glow_radius, 0, -1):
            alpha = int(255 * (radius / self.ai_settings.bullet_glow_radius))
            color = (*self.ai_settings.bullet_glow_color, alpha)
            pygame.draw.circle(self.glow_surface, color, center, radius)

    def update(self):
        if self.is_fat:
            # Update fat bullet position (move upward)
            self.y -= self.speed_factor
            self.rect.y = self.y
            self.collision_rect.y = self.y
            
            # Remove if off screen
            if self.rect.bottom < 0:
                self.kill()
        else:
            # Update trail
            self.trail_positions.append((self.rect.centerx, self.rect.centery))
            if len(self.trail_positions) > self.trail_length:
                self.trail_positions.pop(0)
            
            # Update position
            self.y -= self.speed_factor
            self.rect.y = self.y

    def draw_trail(self):
        if len(self.trail_positions) > 1:
            points = []
            for i, pos in enumerate(self.trail_positions):
                alpha = int(self.ai_settings.bullet_trail_alpha * (i / len(self.trail_positions)))
                points.append((*pos, alpha))
            
            for i in range(len(points) - 1):
                start_pos, start_alpha = points[i][:2], points[i][2]
                end_pos, end_alpha = points[i + 1][:2], points[i + 1][2]
                
                # Create a surface for the trail segment
                trail_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                pygame.draw.line(trail_surface, (*self.ai_settings.bullet_color, (start_alpha + end_alpha) // 2),
                               (0, 0), (0, self.rect.height), self.rect.width // 2)
                
                # Position the trail segment
                trail_rect = trail_surface.get_rect(center=((start_pos[0] + end_pos[0]) // 2,
                                                          (start_pos[1] + end_pos[1]) // 2))
                self.screen.blit(trail_surface, trail_rect)

    def draw_bullet(self):
        if self.is_fat:
            # Draw fat bullet glow
            glow_pos = (self.rect.x - self.ai_settings.fat_bullet_glow_radius,
                       self.rect.y - self.ai_settings.fat_bullet_glow_radius)
            self.screen.blit(self.glow_surface, glow_pos)
            
            # Draw fat bullet with a slight offset for better visibility
            self.screen.blit(self.image, self.rect)
            
            # Draw a bright center line for better visibility
            center_y = self.rect.centery
            pygame.draw.line(self.screen, (255, 255, 255),
                           (self.rect.left, center_y),
                           (self.rect.right, center_y),
                           3)
        else:
            # Draw trail
            self.draw_trail()
            
            # Draw glow
            glow_pos = (self.rect.x - self.ai_settings.bullet_glow_radius,
                       self.rect.y - self.ai_settings.bullet_glow_radius)
            self.screen.blit(self.glow_surface, glow_pos)
            
            # Draw bullet
            self.screen.blit(self.image, self.rect)