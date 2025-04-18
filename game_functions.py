import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from explosion import Explosion




def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key ==  pygame.K_LEFT:  
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_r:
        fire_fat_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_t:  # Debug key to lose a life
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not stats.game_active:
                # Start a new game when P is pressed
                start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
            else:
                check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, ship, aliens, bullets, mouse_x, mouse_y):
    # Removed the play_button argument as it is now obsolete
    pass  # Functionality removed as play_button is no longer used

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def fire_fat_bullet(ai_settings, screen, ship, bullets):
    """Fire a fat bullet if within bullet limit."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship, is_fat=True)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions)

def update_explosions(explosions):
    """Update and remove finished explosions."""
    for explosion in explosions.copy():
        explosion.update()  # Update the explosion animation
        # No need to check for 'finished', as 'self.kill()' removes it automatically

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosions):
    """Respond to bullet-alien collisions."""
    # Check for fat bullet collisions first
    for bullet in bullets.sprites():
        if bullet.is_fat:
            # Get all aliens that collide with the fat bullet
            fat_collisions = pygame.sprite.spritecollide(bullet, aliens, True)
            if fat_collisions:
                for alien in fat_collisions:
                    # Create explosion at alien's position
                    explosion = Explosion(alien.rect.center, alien.rect.width)
                    explosions.add(explosion)
                stats.score += ai_settings.alien_points * len(fat_collisions)
                sb.prep_score()
                check_high_score(stats, sb)
            break  # Only one fat bullet at a time

    # Check for normal bullet collisions
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            for alien in aliens_hit:
                # Create explosion at alien's position
                explosion = Explosion(alien.rect.center, alien.rect.width)
                explosions.add(explosion)
            stats.score += ai_settings.alien_points * len(aliens_hit)
            sb.prep_score()
        check_high_score(stats, sb)
    
    # Check if all aliens are destroyed and all explosions are finished
    if len(aliens) == 0 and len(explosions) == 0:
        # If the entire fleet is destroyed and all explosions are done, start a new level
        bullets.empty()
        ai_settings.increase_speed()
        
        # Increase level
        stats.level += 1
        sb.prep_level()
        
        # Create new fleet
        create_fleet(ai_settings, screen, ship, aliens)
        
        # Center the ship
        ship.center_ship()
        
        # Pause briefly to show level transition
        pygame.time.delay(500)  # 500ms pause

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (2* alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the reaper fleet.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Decrement ships_left.
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #no. ship update on UI
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)



def update_screen(bg, screen, stats, sb, ship, aliens, bullets, explosions):
    screen.blit(bg, (0, 0))
    
    if stats.game_active:
        # Draw game elements
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        
        # Draw explosions
        for explosion in explosions:
            explosion.draw(screen)
            
        # Draw score information
        sb.show_score()
    else:
        # Draw game over screen
        font = pygame.font.SysFont(None, 74)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        press_p_text = font.render("Press P to Play Again", True, (255, 255, 255))
        
        game_over_rect = game_over_text.get_rect()
        press_p_rect = press_p_text.get_rect()
        
        game_over_rect.centerx = screen.get_rect().centerx
        game_over_rect.centery = screen.get_rect().centery - 50
        press_p_rect.centerx = screen.get_rect().centerx
        press_p_rect.centery = screen.get_rect().centery + 50
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(press_p_text, press_p_rect)
        
        # Show final score
        sb.show_score()
    
    pygame.display.flip()

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Start a new game."""
    # Reset game settings
    ai_settings.initialize_dynamic_settings()
    ai_settings.bullet_width = 3  # Reset bullet width to initial value
    
    # Reset game statistics
    stats.reset_stats()
    stats.game_active = True
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    
    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()
    
    # Create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # Hide the mouse cursor
    pygame.mouse.set_visible(False)