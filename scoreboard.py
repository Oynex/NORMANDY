import pygame.font
from pygame.sprite import Group
from ship import Ship
import time

class Scoreboard():
    """A class to report scoring information."""
    
    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        # Font settings for scoring information.
        self.text_color = (255, 255, 255)  # White text for visibility
        self.font = pygame.font.SysFont(None, 48)
        self.label_font = pygame.font.SysFont(None, 36)
        
        # Animation variables
        self.pulse_alpha = 255
        self.pulse_direction = -1
        self.last_pulse_time = time.time()
        self.score_scale = 1.0
        self.high_score_scale = 1.0
        self.level_scale = 1.0
        self.last_score_update = 0
        self.last_high_score_update = 0
        self.last_level_update = 0
        
        # Glow effect settings
        self.glow_color = (100, 149, 237)  # Cornflower blue for a sci-fi feel
        self.glow_alpha = 128
        
        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, None)  # Remove background color
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        self.last_score_update = time.time()
    
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, None)  # Remove background color
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20  # Same top alignment as score
        self.last_high_score_update = time.time()
    
    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True,
                self.text_color, None)  # Remove background color
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 30  # Increased spacing
        self.last_level_update = time.time()
    
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen, is_player=False)
            # Scale down the ship image for life indicators
            original_size = ship.image.get_size()
            new_size = (original_size[0] // 2, original_size[1] // 2)  # Half the size
            ship.image = pygame.transform.scale(ship.image, new_size)
            ship.rect = ship.image.get_rect()
            # Position ships in top-left corner
            ship.rect.x = 10 + ship_number * (ship.rect.width + 5)  # Reduced spacing
            ship.rect.y = 10
            self.ships.add(ship)
    
    def create_fancy_box(self, width, height, alpha=128, has_label=False, label_width=0):
        """Create a fancy box with gradient and glow effect."""
        # Calculate total width based on content
        total_width = width + 20  # Base padding for value section
        if has_label:
            total_width += label_width + 50  # Label width + padding (increased from 40 to 50)
        total_height = height + 20  # Base padding
        
        box_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        
        # Create outer glow
        glow_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        glow_color = (*self.glow_color, int(self.pulse_alpha * 0.3))
        self.draw_rounded_rect(glow_surface, (0, 0, total_width, total_height), glow_color, 8, 4)
        box_surface.blit(glow_surface, (0, 0))
        
        # Create gradient background
        gradient_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        for y in range(total_height):
            alpha_val = int(alpha * (1 - y/total_height * 0.7))
            pygame.draw.line(gradient_surface, (0, 0, 0, alpha_val), (0, y), (total_width, y))
        
        # Apply rounded corners to gradient
        self.draw_rounded_rect(box_surface, (0, 0, total_width, total_height), (0, 0, 0, alpha), 8)
        box_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        # Draw main border
        border_color = (255, 255, 255, self.pulse_alpha)
        self.draw_rounded_rect(box_surface, (0, 0, total_width, total_height), border_color, 8, 2)
        
        if has_label:
            # Draw vertical separator line
            separator_x = label_width + 25  # Position separator after label (increased from 20 to 25)
            pygame.draw.line(box_surface, border_color, 
                           (separator_x, 10), 
                           (separator_x, total_height - 10), 2)
        
        return box_surface, separator_x if has_label else None

    def draw_rounded_rect(self, surface, rect, color, radius, width=0):
        """Draw a rounded rectangle with the given parameters."""
        x, y, w, h = rect
        
        # Draw the main rectangle
        if width == 0:  # Filled
            pygame.draw.rect(surface, color, (x+radius, y, w-2*radius, h))
            pygame.draw.rect(surface, color, (x, y+radius, w, h-2*radius))
        else:  # Outlined
            pygame.draw.rect(surface, color, (x+radius, y, w-2*radius, h), width)
            pygame.draw.rect(surface, color, (x, y+radius, w, h-2*radius), width)
        
        # Draw the corner circles
        pygame.draw.circle(surface, color, (x+radius, y+radius), radius, width)
        pygame.draw.circle(surface, color, (x+w-radius, y+radius), radius, width)
        pygame.draw.circle(surface, color, (x+radius, y+h-radius), radius, width)
        pygame.draw.circle(surface, color, (x+w-radius, y+h-radius), radius, width)

    def update_animation(self):
        """Update animation effects."""
        current_time = time.time()
        
        # Update pulse effect with smoother transition
        if current_time - self.last_pulse_time > 0.03:  # Faster update for smoother pulse
            self.pulse_alpha += self.pulse_direction * 3  # Slower pulse speed
            if self.pulse_alpha <= 150:  # Higher minimum for better visibility
                self.pulse_direction = 1
            elif self.pulse_alpha >= 255:
                self.pulse_direction = -1
            self.last_pulse_time = current_time
        
        # Update score scale with more dramatic effect
        if current_time - self.last_score_update < 0.5:
            progress = (0.5 - (current_time - self.last_score_update)) * 2
            self.score_scale = 1.0 + progress * 0.3  # 30% size increase
        else:
            self.score_scale = 1.0
            
        # Update high score scale
        if current_time - self.last_high_score_update < 0.5:
            progress = (0.5 - (current_time - self.last_high_score_update)) * 2
            self.high_score_scale = 1.0 + progress * 0.3
        else:
            self.high_score_scale = 1.0
            
        # Update level scale
        if current_time - self.last_level_update < 0.5:
            progress = (0.5 - (current_time - self.last_level_update)) * 2
            self.level_scale = 1.0 + progress * 0.3
        else:
            self.level_scale = 1.0
    
    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.update_animation()
        
        # Draw score box
        score_label = self.label_font.render("SCORE", True, self.text_color)
        score_value = pygame.transform.scale(self.score_image, 
            (int(self.score_rect.width * self.score_scale), 
             int(self.score_rect.height * self.score_scale)))
        
        # Create score box with dynamic label section
        box, separator_x = self.create_fancy_box(score_value.get_width() + 20, 
                                               max(score_value.get_height(), score_label.get_height()) + 20,
                                               has_label=True,
                                               label_width=score_label.get_width())
        box_x = self.screen_rect.right - box.get_width() - 20
        box_y = 20
        
        # Draw box and contents
        self.screen.blit(box, (box_x, box_y))
        # Draw label vertically centered in its section
        label_rect = score_label.get_rect()
        label_rect.centerx = box_x + (separator_x // 2)  # Center in label section
        label_rect.centery = box_y + box.get_height() // 2
        self.screen.blit(score_label, label_rect)
        # Draw value centered in its section
        value_rect = score_value.get_rect()
        value_rect.centerx = box_x + separator_x + ((box.get_width() - separator_x) // 2)
        value_rect.centery = box_y + box.get_height() // 2
        self.screen.blit(score_value, value_rect)
        
        # Draw high score box
        high_score_label = self.label_font.render("HIGH SCORE", True, self.text_color)
        high_score_value = pygame.transform.scale(self.high_score_image,
            (int(self.high_score_rect.width * self.high_score_scale),
             int(self.high_score_rect.height * self.high_score_scale)))
        
        # Create high score box with dynamic label section
        box, separator_x = self.create_fancy_box(high_score_value.get_width() + 20,
                                               max(high_score_value.get_height(), high_score_label.get_height()) + 20,
                                               has_label=True,
                                               label_width=high_score_label.get_width())
        box_x = (self.screen_rect.width - box.get_width()) // 2
        box_y = 20
        
        # Draw box and contents
        self.screen.blit(box, (box_x, box_y))
        # Draw label vertically centered in its section
        label_rect = high_score_label.get_rect()
        label_rect.centerx = box_x + (separator_x // 2)
        label_rect.centery = box_y + box.get_height() // 2
        self.screen.blit(high_score_label, label_rect)
        # Draw value centered in its section
        value_rect = high_score_value.get_rect()
        value_rect.centerx = box_x + separator_x + ((box.get_width() - separator_x) // 2)
        value_rect.centery = box_y + box.get_height() // 2
        self.screen.blit(high_score_value, value_rect)
        
        # Draw level box
        level_label = self.label_font.render("LEVEL", True, self.text_color)
        level_value = pygame.transform.scale(self.level_image,
            (int(self.level_rect.width * self.level_scale),
             int(self.level_rect.height * self.level_scale)))
        
        # Create level box with dynamic label section
        box, separator_x = self.create_fancy_box(level_value.get_width() + 20,
                                               max(level_value.get_height(), level_label.get_height()) + 20,
                                               has_label=True,
                                               label_width=level_label.get_width())
        box_x = self.screen_rect.right - box.get_width() - 20
        box_y = box.get_height() + 40
        
        # Draw box and contents
        self.screen.blit(box, (box_x, box_y))
        # Draw label vertically centered in its section
        label_rect = level_label.get_rect()
        label_rect.centerx = box_x + (separator_x // 2)
        label_rect.centery = box_y + box.get_height() // 2
        self.screen.blit(level_label, label_rect)
        # Draw value centered in its section
        value_rect = level_value.get_rect()
        value_rect.centerx = box_x + separator_x + ((box.get_width() - separator_x) // 2)
        value_rect.centery = box_y + box.get_height() // 2
        self.screen.blit(level_value, value_rect)
        
        # Draw lives box
        if self.ships:
            lives_label = self.label_font.render("LIVES", True, self.text_color)
            ships_width = sum(ship.rect.width for ship in self.ships) + (len(self.ships) - 1) * 5
            ships_height = self.ships.sprites()[0].rect.height
            
            # Create lives box with dynamic label section
            box, separator_x = self.create_fancy_box(ships_width + 20,
                                                   max(ships_height, lives_label.get_height()) + 20,
                                                   has_label=True,
                                                   label_width=lives_label.get_width())
            box_x = 20
            box_y = 20
            
            # Draw box and contents
            self.screen.blit(box, (box_x, box_y))
            # Draw label vertically centered in its section
            label_rect = lives_label.get_rect()
            label_rect.centerx = box_x + (separator_x // 2)
            label_rect.centery = box_y + box.get_height() // 2
            self.screen.blit(lives_label, label_rect)
            
            # Draw ships centered in value section
            ships_start_x = box_x + separator_x + 10
            ships_y = box_y + (box.get_height() - ships_height) // 2
            for ship in self.ships:
                ship.rect.x = ships_start_x + (ship.rect.width + 5) * list(self.ships).index(ship)
                ship.rect.y = ships_y
                ship.blitme() 