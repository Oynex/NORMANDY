import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from ui import Scoreboard

def rundagame():
    # start pygame and the setting thingy
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("NORMANDY")
    bg = pygame.image.load('images/bg.bmp')

    # Integrate game start logic into the start menu
    def display_start_menu():
        font = pygame.font.Font(None, 74)
        title_text = font.render("NORMANDY", True, (255, 255, 255))
        instruction_text = font.render("Press ENTER to Start", True, (255, 255, 255))

        while True:
            screen.fill((0, 0, 0))
            screen.blit(title_text, (ai_settings.screen_width // 2 - title_text.get_width() // 2, ai_settings.screen_height // 3))
            screen.blit(instruction_text, (ai_settings.screen_width // 2 - instruction_text.get_width() // 2, ai_settings.screen_height // 2))

            # Dynamically calculate the box size based on the text dimensions
            padding = 20
            control_text = font.render("Controls: Arrow keys to move, Space to shoot", True, (255, 255, 255))
            box_width = control_text.get_width() + 2 * padding
            box_height = control_text.get_height() + 2 * padding
            box_x = ai_settings.screen_width // 2 - box_width // 2
            box_y = ai_settings.screen_height // 1.5 - box_height // 2

            # Draw the dynamically sized box
            pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

            # Render and display the control instructions inside the box
            screen.blit(control_text, (box_x + padding, box_y + padding))
            
            pygame.display.flip()

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