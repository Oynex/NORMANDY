class Settings():

    def __init__(self):

        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 10 

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # score increase rate
        self.score_scale = 1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullet_width = 3
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.1
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_points = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_width += 3
        self.alien_points = int(self.alien_points * self.score_scale)