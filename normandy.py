import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
import time

def rundagame():
    # start pygame and the setting thingy
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("NORMANDY")
    bg = pygame.image.load('images/bg.bmp')
    
    # Load and scale the background for menu
    menu_bg = pygame.transform.scale(bg, (ai_settings.screen_width, ai_settings.screen_height))
    
    # Create a semi-transparent overlay
    overlay = pygame.Surface((ai_settings.screen_width, ai_settings.screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black with 50% opacity

    # Integrate game start logic into the start menu
    def display_start_menu():
        # Load custom font or use system font
        try:
            title_font = pygame.font.Font('fonts/space_age.ttf', 100)  # You'll need to add this font
            menu_font = pygame.font.Font('fonts/space_age.ttf', 50)
        except:
            title_font = pygame.font.Font(None, 100)
            menu_font = pygame.font.Font(None, 50)

        # Create text surfaces
        title_text = title_font.render("NORMANDY", True, (255, 255, 255))
        start_text = menu_font.render("Press ENTER to Start", True, (255, 255, 255))
        controls_text = menu_font.render("Controls: Arrow keys to move, Space to shoot", True, (255, 255, 255))
        
        # Create a pulsing effect for the start text
        pulse_speed = 0.01
        pulse_min = 0.5
        pulse_max = 1.0
        pulse_value = pulse_min
        
        # Create a rotating ship preview
        ship_preview = Ship(ai_settings, screen, is_player=False)
        ship_preview.rect.centerx = ai_settings.screen_width // 2
        ship_preview.rect.centery = ai_settings.screen_height // 2
        rotation_angle = 0
        
        # Create stars for background animation
        stars = []
        for _ in range(100):
            x = pygame.math.Vector2(
                pygame.math.Vector2(ai_settings.screen_width, ai_settings.screen_height).rotate(
                    pygame.math.Vector2(1, 0).angle_to(pygame.math.Vector2(1, 0))
                )
            )
            stars.append({
                'pos': pygame.math.Vector2(
                    pygame.math.Vector2(ai_settings.screen_width, ai_settings.screen_height).rotate(
                        pygame.math.Vector2(1, 0).angle_to(pygame.math.Vector2(1, 0))
                    )
                ),
                'speed': pygame.math.Vector2(0, -1).rotate(pygame.math.Vector2(1, 0).angle_to(pygame.math.Vector2(1, 0)))
            })

        clock = pygame.time.Clock()
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Reset game settings and start the game
                    ai_settings.initialize_dynamic_settings()
                    pygame.mouse.set_visible(False)
                    stats.game_active = True
                    sb.prep_score()
                    sb.prep_high_score()
                    sb.prep_level()
                    sb.prep_ships()
                    aliens.empty()
                    bullets.empty()
                    gf.create_fleet(ai_settings, screen, ship, aliens)
                    ship.center_ship()
                    return

            # Update animations
            pulse_value += pulse_speed
            if pulse_value > pulse_max:
                pulse_speed = -pulse_speed
            elif pulse_value < pulse_min:
                pulse_speed = -pulse_speed
                
            rotation_angle = (rotation_angle + 1) % 360
            
            # Update star positions
            for star in stars:
                star['pos'] += star['speed']
                if star['pos'].x < 0 or star['pos'].x > ai_settings.screen_width or \
                   star['pos'].y < 0 or star['pos'].y > ai_settings.screen_height:
                    star['pos'] = pygame.math.Vector2(
                        pygame.math.Vector2(ai_settings.screen_width, ai_settings.screen_height).rotate(
                            pygame.math.Vector2(1, 0).angle_to(pygame.math.Vector2(1, 0))
                        )
                    )

            # Draw everything
            screen.blit(menu_bg, (0, 0))
            screen.blit(overlay, (0, 0))
            
            # Draw stars
            for star in stars:
                pygame.draw.circle(screen, (255, 255, 255), (int(star['pos'].x), int(star['pos'].y)), 2)
            
            # Draw title with glow effect
            for offset in range(5, 0, -1):
                glow_color = (255, 255, 255, 50 - offset * 10)
                glow_surface = title_font.render("NORMANDY", True, glow_color)
                screen.blit(glow_surface, 
                          (ai_settings.screen_width // 2 - title_text.get_width() // 2 - offset,
                           ai_settings.screen_height // 3 - offset))
            screen.blit(title_text, 
                       (ai_settings.screen_width // 2 - title_text.get_width() // 2,
                        ai_settings.screen_height // 3))
            
            # Draw rotating ship
            rotated_ship = pygame.transform.rotate(ship_preview.image, rotation_angle)
            ship_rect = rotated_ship.get_rect(center=ship_preview.rect.center)
            screen.blit(rotated_ship, ship_rect)
            
            # Draw pulsing start text
            scaled_start = pygame.transform.scale(start_text, 
                (int(start_text.get_width() * pulse_value),
                 int(start_text.get_height() * pulse_value)))
            screen.blit(scaled_start,
                       (ai_settings.screen_width // 2 - scaled_start.get_width() // 2,
                        ai_settings.screen_height * 2 // 3))
            
            # Draw controls in a styled box
            box_padding = 20
            box_width = controls_text.get_width() + 2 * box_padding
            box_height = controls_text.get_height() + 2 * box_padding
            box_x = ai_settings.screen_width // 2 - box_width // 2
            box_y = ai_settings.screen_height * 3 // 4 - box_height // 2
            
            # Draw box with gradient border
            pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
            for i in range(3):
                pygame.draw.rect(screen, (100 + i * 50, 100 + i * 50, 100 + i * 50),
                               (box_x - i, box_y - i, box_width + 2 * i, box_height + 2 * i), 1)
            
            screen.blit(controls_text,
                       (box_x + box_padding, box_y + box_padding))
            
            pygame.display.flip()
            clock.tick(60)

    # construct da ship
    ship = Ship(ai_settings, screen)
    # Active bullet storage
    bullets = Group()
    aliens = Group()
    # Active explosion storage
    explosions = Group()
    # call the reaper
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #store stats & scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Call the start menu before the game loop
    display_start_menu()

    # Main game 
    while True:

        gf.check_events(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
        if stats.game_active:

            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_explosions(explosions)

        gf.update_screen(bg, screen, stats, sb, ship, aliens, bullets, explosions)


rundagame()