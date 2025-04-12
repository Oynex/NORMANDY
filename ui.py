import pygame.font
from pygame.sprite import Group
from ship import Ship
import math

class Scoreboard():

    def __init__(self, ai_settings, screen, stats):
        #scoreboard atrib
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, ai_settings.score_font_size)
        self.high_score_font = pygame.font.Font(None, ai_settings.high_score_font_size)
        self.level_font = pygame.font.Font(None, ai_settings.level_font_size)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

        # Animation properties
        self.score_pulse = 1.0
        self.pulse_direction = 0.01
        self.pulse_min = 0.8
        self.pulse_max = 1.2

    def update_pulse(self):
        self.score_pulse += self.pulse_direction
        if self.score_pulse > self.pulse_max:
            self.pulse_direction = -0.01
        elif self.score_pulse < self.pulse_min:
            self.pulse_direction = 0.01

    def create_glow_surface(self, text_surface, color):
        glow_surface = pygame.Surface(
            (text_surface.get_width() + self.ai_settings.ui_glow_radius * 2,
             text_surface.get_height() + self.ai_settings.ui_glow_radius * 2),
            pygame.SRCALPHA
        )
        
        for radius in range(self.ai_settings.ui_glow_radius, 0, -1):
            alpha = int(255 * (radius / self.ai_settings.ui_glow_radius))
            glow_color = (*color, alpha)
            pygame.draw.rect(glow_surface, glow_color,
                           (self.ai_settings.ui_glow_radius - radius,
                            self.ai_settings.ui_glow_radius - radius,
                            text_surface.get_width() + radius * 2,
                            text_surface.get_height() + radius * 2),
                           border_radius=5)
        
        return glow_surface

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_glow = self.create_glow_surface(self.score_image, self.ai_settings.ui_glow_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.high_score_font.render(high_score_str, True, self.text_color)
        self.high_score_glow = self.create_glow_surface(self.high_score_image, self.ai_settings.ui_glow_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        # Update pulse animation
        self.update_pulse()
        
        # Draw score with glow and pulse
        glow_pos = (self.score_rect.x - self.ai_settings.ui_glow_radius,
                   self.score_rect.y - self.ai_settings.ui_glow_radius)
        self.screen.blit(self.score_glow, glow_pos)
        
        # Scale and draw the score
        scaled_score = pygame.transform.scale(
            self.score_image,
            (int(self.score_image.get_width() * self.score_pulse),
             int(self.score_image.get_height() * self.score_pulse))
        )
        score_pos = (
            self.score_rect.centerx - scaled_score.get_width() // 2,
            self.score_rect.centery - scaled_score.get_height() // 2
        )
        self.screen.blit(scaled_score, score_pos)
        
        # Draw high score with glow
        high_score_glow_pos = (self.high_score_rect.x - self.ai_settings.ui_glow_radius,
                             self.high_score_rect.y - self.ai_settings.ui_glow_radius)
        self.screen.blit(self.high_score_glow, high_score_glow_pos)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        
        # Draw level with glow
        level_glow_pos = (self.level_rect.x - self.ai_settings.ui_glow_radius,
                         self.level_rect.y - self.ai_settings.ui_glow_radius)
        self.screen.blit(self.level_glow, level_glow_pos)
        self.screen.blit(self.level_image, self.level_rect)
        
        # Draw ships with glow
        for ship in self.ships:
            glow_surface = pygame.Surface(
                (ship.rect.width + self.ai_settings.ui_glow_radius * 2,
                 ship.rect.height + self.ai_settings.ui_glow_radius * 2),
                pygame.SRCALPHA
            )
            for radius in range(self.ai_settings.ui_glow_radius, 0, -1):
                alpha = int(255 * (radius / self.ai_settings.ui_glow_radius))
                glow_color = (*self.ai_settings.ui_glow_color, alpha)
                pygame.draw.rect(glow_surface, glow_color,
                               (self.ai_settings.ui_glow_radius - radius,
                                self.ai_settings.ui_glow_radius - radius,
                                ship.rect.width + radius * 2,
                                ship.rect.height + radius * 2))
            
            glow_pos = (ship.rect.x - self.ai_settings.ui_glow_radius,
                       ship.rect.y - self.ai_settings.ui_glow_radius)
            self.screen.blit(glow_surface, glow_pos)
            ship.blitme()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = "Level: {}".format(self.stats.level)
        self.level_image = self.level_font.render(level_str, True, self.text_color)
        self.level_glow = self.create_glow_surface(self.level_image, self.ai_settings.ui_glow_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = self.screen_rect.bottom - ship.rect.height
            self.ships.add(ship)