import sys
import pygame
from time import sleep
from bullet import  Bullet
from alien import Alien
import boss
from pygame import *
import random as r
def check_events(ai_settings, screen, ship, bullets):
    '''Respond to keypresses and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    ''' Respond to keypresses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_LCTRL:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_RCTRL:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    ''' Respond to key releases'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_settings, screen, ship, alien, bullets,background):
    '''Update images on the screen and flip to the new screen.'''
    #Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    screen.blit(background.image, background.rect)
    #Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.draw(screen)

    #Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets, bosstage = False):
    '''Update position of bullets and of old bullets.'''
    #Update bullet position.
    bullets.update()

#def update_enemy_bullets(ai_settings, screen, aliens, boss, ebullets):
    #ebullets.update()

    #Check for any bullets that have hit aliens.
    #If so, get rid of the bullet and the alien.
    if bosstage == False:
        pygame.sprite.groupcollide(bullets, aliens, True, True)



    #remove bullet if it goes too far
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)




    if len(aliens)== 0:
        #Destroy existing bullets and create new fleet.
        bullets.empty()
        #create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire a bullet if limit not reached yet.'''
    #Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def boss_bullet(ai_settings, screen, boss, bullets):
    random = r.random()
    if random > .5:
        new_bullet = Bullet(ai_settings, screen, boss)

        bullets.add(new_bullet)

    #Make the most recently drawn screen visible.

def create_fleet(ai_settings, screen, ship, aliens):
    '''Create a full fleet of aliens.'''
    #Create ana lien and find the number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def create_boss(ai_settings, screen, ship, aliens):
    alien = boss.Kokomon(ai_settings, screen)
    aliens.add(alien)

#def boss_bullet(ai_settings,screen,boss,aliens):
   # if fps

def get_number_aliens_x(ai_settings, alien_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Create an alien and place it in a the row.'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    '''
    Check if the fleet is at an edge
        and then update the position of all aliens in the fleet
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    Hit_Bottom_Flag = False
    for alien in aliens.sprites():
        if(alien.rect.y>800):
            Hit_Bottom_Flag = True
            break

    #Look for alien-ship collision.
    if pygame.sprite.spritecollideany(ship, aliens) or Hit_Bottom_Flag:
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        print ("Ship Hit!!")

    #Look for aliens hitting the bottom of the screen.
        check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_aliens(ai_settings, stats, screen, ship, aliens, bullets):


    #Look for alien-ship collision.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        print ("Ship Hit!!")

    #Look for aliens hitting the bottom of the screen.
        check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    '''Respond to ship being hit by alien.'''
    if stats.ships_left > 0:
        #Decrement ship_left.
        stats.ships_left -= 1

        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(0.5)

    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    '''Check if any aliens have reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def winscreen():
    screen = pygame.display.set_mode((1200,800))
    pygame .display.set_caption("Alien Invasion")
    font = pygame.font.Font(None,150)
    text = font.render("You Win!",1,(255,255,255))
    while True:
        screen.fill((0,0,0))
        screen.blit(text,(350,350))
        display.update()
        for ev in event.get():
            if ev.type == QUIT:
                exit()

