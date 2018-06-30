import pygame
from colors import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, color = blue, width = 40, height = 48):
        super(Player,self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.set_properties()
        self.sound = pygame.mixer.Sound("fiz.wav")

        self.hspeed = 0
        self.vspeed = 0

        self.level = None

    def set_properties(self):
        self.rect = self.image.get_rect()
        
        self.origin_x =  self.rect.centerx
        self.origin_y =  self.rect.centery

        self.speed = 5

    def change_speed(self, hspeed, vspeed):
        self.hspeed += hspeed
        self.vspeed += vspeed
        
    def set_pos(self, x, y):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def set_level(self, level):
        self.level = level
        self.set_pos(level.player_start_x, level.player_start_y)
    
    def set_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename).convert()
            self.set_properties()
    
    def update(self, collidable = pygame.sprite.Group(), event = None):

        self.exp_gravity()
        self.rect.x += self.hspeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if (self.hspeed > 0):
                # RIGHT DIRECTION
                self.rect.right = collided_object.rect.left
            elif (self.hspeed < 0):
                # LEFT DIRECTION
                self.rect.left = collided_object.rect.right
        
        self.rect.y += self.vspeed
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if (self.vspeed > 0):
                #DOWN DIRECTION
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            elif (self.vspeed <0 ):
                #UP DIRECTION
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

        if not(event == None ):   
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    self.hspeed = -self.speed
                if (event.key == pygame.K_RIGHT):
                    self.hspeed = self.speed
                if (event.key == pygame.K_UP):
                    if (self.vspeed == 0):
                        self.vspeed = -(self.speed) * 2
            
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT):
                    if (self.hspeed < 0) : self.hspeed = 0
                if (event.key == pygame.K_RIGHT):
                    if (self.hspeed > 0) : self.hspeed = 0
                    
    def exp_gravity(self, gravity = .35):
        if (self.vspeed == 0 ): self.vspeed = 1
        else: self.vspeed += gravity

        
class Block(pygame.sprite.Sprite):
    

    def __init__(self, x, y, width , height, color = blue ):
        super(Block,self).__init__()

        if (width < 0):
            x += width
            width = abs(width)
        if (height < 0):
            y += height
            height = abs(height) 


        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.sound = pygame.mixer.Sound("fiz.wav")

        self.rect = self.image.get_rect()
        
        #self.origin_x =  self.rect.centerx
        #self.origin_y =  self.rect.centery

        self.rect.x = x
        self.rect.y = y

class Level():
    
    def __init__(self, player_object):
        self.object_list = pygame.sprite.Group()
        self.player_object = player_object
        self.player_start = self.player_start_x, self.player_start_y = 0, 0
        
        self.world_shift_x = self.world_shift_y =  0

        self.left_viewbox = win_width/2 - win_width/8
        self.right_viewbox = win_width/2 + win_width/10
        #less change in the right direction and more in left

        self.up_viewbox = win_height/4
        self.down_viewbox = win_height/2 + win_width/8

    def update(self):

        self.object_list.update()

    def draw(self, window):
        window.fill(silver)
        self.object_list.draw(window)

    def shift_world(self, shift_x, shift_y):

        self.world_shift_x += shift_x
        self.world_shift_y += shift_y
        for each_object in self.object_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y

    def run_viewbox(self):

        if(self.player_object.rect.x <= self.left_viewbox):
            #( current x position of a player )
            view_difference = self.left_viewbox - self.player_object.rect.x
        # = how far we are able to go to the left - how far we have gone to he left
            self.player_object.rect.x = self.left_viewbox
            self.shift_world(view_difference, 0 )

        if(self.player_object.rect.x >= self.right_viewbox):
            view_difference = self.right_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.right_viewbox
            self.shift_world(view_difference, 0 )

        if (self.player_object.rect.y <= self.up_viewbox):
            view_difference = self.up_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.up_viewbox
            self.shift_world( 0, view_difference) 

        if (self.player_object.rect.y >= self.down_viewbox):
           view_difference = self.down_viewbox - self.player_object.rect.y
           self.player_object.rect.y = self.down_viewbox
           self.shift_world( 0, view_difference)


class Level_01(Level):

    #CONSTRUCTUR
    def __init__(self, Player_object):
        super(Level_01, self).__init__(Player_object)

        self.player_start = self.player_start_x, self.player_start_y = 100, 0

        level = [
            # [ x, y, width, height, color]
            [2, 124, 365, 47, black],
            
            [3, 14, 302, 0, black ],
            [0, 18, 122, 514, black ],
            [0, 0, 42, 18, black ],
            [0, 504, 45, 232, black ],
            [26, 584, 0, 0, black ],
            [26, 584, 0, 0, black ],
            [26, 584, 0, 0, black ],
            [16, 715, 36, 21, black ],
            [120, 127, 164, 38, black ],
            [277, 152, 46, 27, black ],
            [283, 172, 32, 163, black ],
            [385, 253, 225, 24, black ],
            [600, 276, 57, 65, black ],
            [643, 327, 136, 50, black ],
            [754, 370, 118, 51, black ],
            [846, 413, 109, 37, black ],
            [1025, 479, 163, 50, black ],
            [867, 546, 127, 36, black ],
            [771, 549, 124, 72, black ],
            [656, 601, 133, 33, black ],
            [562, 609, 132, 66, black ],
            [370, 647, 210, 55, black ],
            [141, 604, 186, 60, black ],
            [132, 490, 111, 77, black ],
            [68, 357, 81, 93, black ],
            [579, 676, 497, 60, black ],
            [1065, 633, 131, 103, black ],
            

        ]

        for block in level:
            block = Block(block[0], block[1], block[2], block[3], block[4])
            self.object_list.add(block)

if (__name__ == "__main__"):

    pygame.init()
    window_size = win_width, win_height = 650, 480
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("G jump")

    active_object_list = pygame.sprite.Group()
    player = Player()
    player.set_pos(40, 40)

    active_object_list.add(player)

    level_list =[]
    level_list.append(Level_01(player))

    current_level_number = 0
    current_level = level_list[current_level_number]

    player.set_level(current_level)
    
    clock = pygame.time.Clock()
    frames_per_second = 60

    #collidable_objects = pygame.sprite.Group()
    #collidable_objects.add(b_block, c_block)
    
    running = True
    while(running):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT)or \
               (event.type == pygame.KEYDOWN and \
               (event.type == pygame.K_ESCAPE or event.key == pygame.K_q)):
                 running = False
        
        #update functions
        player.update(current_level.object_list, event)
        event = None
        current_level.update()

        #logic Testing

        current_level.run_viewbox()

        #Draw Everything
        current_level.draw(window)
        active_object_list.draw(window)

        #Delay Framerate
        clock.tick( frames_per_second)

        #Update the Screen
        pygame.display.update()
    
    pygame.quit()


    
