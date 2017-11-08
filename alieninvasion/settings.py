class Settings():
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''Initialize the game's settings.'''
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


        #Ship settings
        self.ship_speed_factor = 40
        self.ship_limit = 1

        #Bullet settings
        self.bullet_speed_factor = 100
        self.bullet_width = 10
        self.bullet_height = 25
        self.bullet_color = 220, 20, 60
        self.bullets_allowed = 100

        #Alien settings
        self.alien_speed_factor = 15
        self.fleet_drop_speed = 10
        #Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #Kokomon settings
        self.Kokomon_speed_factor = 25
