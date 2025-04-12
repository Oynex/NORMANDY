import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from ui import Scoreboard

def rundagame():
    # start pygame and the setting thingy
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("NORMANDY")
    bg = pygame.image.load('images/bg.bmp')

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
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

    # Main game 
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:

            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_explosions(explosions)

        gf.update_screen(bg, screen, stats, sb, ship, aliens, bullets, explosions, play_button)


rundagame()