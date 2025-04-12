class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)
        self.fps = 60

        # Ship settings
        self.ship_limit = 3
        self.ship_glow_color = (0, 255, 255)  # Cyan glow
        self.ship_glow_radius = 5

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)  # Red
        self.bullet_glow_color = (255, 100, 100)  # Light red glow
        self.bullet_glow_radius = 3
        self.bullets_allowed = 5
        self.bullet_trail_length = 5  # Number of trail segments
        self.bullet_trail_alpha = 50  # Alpha value for trail

        # Fat bullet settings
        self.fat_bullet_width = self.screen_width  # As wide as the screen
        self.fat_bullet_height = self.bullet_height  # Same height as normal bullets
        self.fat_bullet_color = (255, 0, 0)  # Red
        self.fat_bullet_glow_color = (255, 50, 50)  # Darker red glow
        self.fat_bullet_glow_radius = 10
        self.fat_bullet_speed = 15  # Faster than normal bullets

        # Alien settings
        self.fleet_drop_speed = 10
        self.alien_glow_color = (255, 0, 255)  # Purple glow
        self.alien_glow_radius = 4
        self.alien_animation_speed = 0.1  # Speed of alien animation

        # Explosion settings
        self.explosion_colors = [
            (255, 255, 0),  # Yellow
            (255, 165, 0),  # Orange
            (255, 0, 0)     # Red
        ]
        self.explosion_particles = 20  # Number of particles per explosion
        self.explosion_lifetime = 30  # Frames

        # UI settings
        self.ui_glow_color = (0, 255, 0)  # Green glow
        self.ui_glow_radius = 2
        self.score_font_size = 48
        self.high_score_font_size = 36
        self.level_font_size = 32

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # score increase rate
        self.score_scale = 1.5  # Increased for more rewarding gameplay
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.1
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_points = 50  # Increased base points

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_width += 3
        self.alien_points = int(self.alien_points * self.score_scale)
        # Increase visual effects with level
        self.ship_glow_radius = int(self.ship_glow_radius + 0.5)
        self.bullet_glow_radius = int(self.bullet_glow_radius + 0.3)
        self.alien_glow_radius = int(self.alien_glow_radius + 0.4)