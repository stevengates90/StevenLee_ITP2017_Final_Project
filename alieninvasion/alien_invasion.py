import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from background import Background
import game_functions as gf
import boss

def run_game(stage):
    #Initialize game and create a screen object.
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame .display.set_caption("Alien Invasion")

    #Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    #Make an alien
    alien = Alien(ai_settings, screen)


    #Create the background
    background = Background("0cc94a86ab2faeed8e31f1e404105e53.bmp", (0,0))

    #Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    #ebullets = Group()

    #Create the fleet of aliens.
    if stage <=2:
        gf.create_fleet(ai_settings, screen, ship, aliens)
    if stage == 3:
        alien = boss.Kokomon(ai_settings,screen)
        aliens.add(alien)
        bosshp = 100
    #Start the main loop for the game.
    while True:

        gf.check_events(ai_settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            if stage == 1:
                gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
                gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

            elif stage == 2:
                gf.update_bullets(ai_settings, screen, ship, aliens, bullets)

                for alien in aliens:
                    gf.check_aliens(ai_settings, stats, screen, ship, aliens, bullets)

                    alien.movedown()
            elif stage == 3:
                gf.update_bullets(ai_settings,screen,ship,aliens,bullets,True)
                if bosshp >1:
                    if pygame.sprite.groupcollide(bullets,aliens,True,False):
                        bosshp -=1
                if bosshp <=1:
                    pygame.sprite.groupcollide(bullets,aliens,True,True)
                alien.stayontop()
                gf.check_aliens(ai_settings, stats, screen, ship, aliens, bullets)
                gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets,background)
        print(len(bullets))
        if len(aliens) == 0:
            break

pygame.init()

#Play the Music
pygame.mixer.music.load('Hans Zimmer - Rangers Lead The Way Victory Theme HQ.mp3')
pygame.mixer.music.play(loops=0)
run_game(1)
run_game(2)
run_game(3)
pygame.init()
gf.winscreen()
