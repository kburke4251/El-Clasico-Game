# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "El Clasico"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors 
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img = pygame.image.load('assets/images/messi.png').convert_alpha()
laser_img = pygame.image.load('assets/images/soccer_ball.png').convert_alpha()
mob_img = pygame.image.load('assets/images/goal.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/ramos.png').convert_alpha()
back_img = pygame.image.load('assets/images/field.jpg').convert_alpha()
menu = pygame.image.load('assets/images/elclasico.jpg').convert_alpha()
keeper_img = pygame.image.load('assets/images/keeper.png').convert_alpha()


# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
BACKGROUND = pygame.mixer.Sound('assets/sounds/background.ogg')
SHOOT = pygame.mixer.Sound('assets/sounds/kick.ogg')
NET = pygame.mixer.Sound('assets/sounds/net.ogg')
WHISTLE = pygame.mixer.Sound('assets/sounds/whistle.ogg')
BACKGROUND.set_volume(.2)
SHOOT.set_volume(5)
NET.set_volume(1)


# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 5
        self.health = 3
        

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed
     
    def shoot(self):
        print("Pew!")
        SHOOT.play()
        
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):
        global hit_listship
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        hit_listship = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        crash_listship = pygame.sprite.spritecollide(self, mobs, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_listship:
            self.health -= 1
            fleet.score += 1

        if self.health is 0:
            self.kill()
            

        if len(crash_listship) > 0:
            self.kill()

        

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
    
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 5
        
    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3

    def drop_bomb(self):
        print("BWamp")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        global hit_listmob
        hit_listmob = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        crash_listmob = pygame.sprite.spritecollide(self, player, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_listmob:
            self.health -= 1
            player.num_hits += 1
            

        if self.health is 0:
            self.kill()
            player.score += 1
            fleet2.speed += .5
            fleet.speed += .5

        if len(crash_listmob) > 0:
            self.kill()



class Gk(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3


    def update(self):
        global hit_listgks
        hit_listgks = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        crash_listgks = pygame.sprite.spritecollide(self, player, True,
                                               pygame.sprite.collide_mask)

        for hit in hit_listgks:
            self.health -= 1
            player.num_hits += 1
            

        if self.health is 0:
            self.kill()
            fleet2.speed += .5
            fleet.speed += .5

        if len(crash_listgks) > 0:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
    
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 10

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet2():
    def __init__(self, gks):
        self.gks = gks
        self.speed = 3
        self.drop = 15
        self.moving_right = True
        self.bomb_rate = 60

    def move(self):
        hits_edge = False

        for g in gks:
            if self.moving_right:
                g.rect.x += self.speed

                if g.rect.right >= WIDTH:
                    hits_edge = True
            else:
                g.rect.x -= self.speed

                if g.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for g in gks:
            g.rect.y += self.drop

    def update(self):
        self.move()
    
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.drop = 15
        self.moving_right = True
        self.bomb_rate = 60

    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop

    def choose_bomber(self):
        global mob_list
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand  is 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()


        
# Game helper functions
def show_title_screen():
    screen.blit(menu, (0,0))
    title_text = FONT_XL.render("El Clasico", 1, RED)
    w = title_text.get_width()
    screen.blit(title_text, [WIDTH/2 - w/2, 204])

def show_win_screen():
    BACKGROUND.stop()
    win_screen = FONT_XL.render("You Win!", 1, WHITE)
    w = win_screen.get_width()
    screen.blit(win_screen, [WIDTH/2 - w/2, 204])

def show_lose_screen():
    BACKGROUND.stop()
    lose_screen = FONT_XL.render("You Lose!", 1, WHITE)
    w = lose_screen.get_width()
    screen.blit(lose_screen, [WIDTH/2 - w/2, 204])

def show_stats():
    barcelona = str(player.score)
    real = str(fleet.score)


    score_txt = FONT_LG.render("Barcelona " + barcelona + "-" + real + " Real Madrid", 1, WHITE)
    w = score_txt.get_width()
    screen.blit(score_txt, [WIDTH/2 - w/2, 5])

def accuracy_end():
    global accuracy
    if player.num_shots > 0:
        accuracy = round((player.num_hits/player.num_shots) * 100)

        accuracy_txt = FONT_LG.render("Accuracy = " + str(accuracy) + "%", 1, WHITE)
        w = accuracy_txt.get_width()
        screen.blit(accuracy_txt, [WIDTH/2 - w/2,650])

        if accuracy > 40:
            player.score += 1
   

def check_end():
    global stage
    if len(mobs) is 0:
        stage = WIN
        WHISTLE.play()
    if len(player) is 0:
        stage = LOSE
        WHISTLE.play()

def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, fleet2, bombs, gks

    BACKGROUND.play(-1)
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 25

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    player.num_shots=0
    player.num_hits = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 100, mob_img)
    mob2 = Mob(300, 100, mob_img)
    mob3 = Mob(500, 100, mob_img)

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3)

    gk1 = Gk(100, 200, keeper_img)
    gk2 = Gk(300, 200, keeper_img)
    gk3 = Gk(500, 200, keeper_img)

    gks = pygame.sprite.Group()
    gks.add(gk1, gk2, gk3)

    fleet = Fleet(mobs)
    fleet.score = 0

    fleet2 = Fleet2(gks)
    fleet2.score = 0



    ''' set stage '''
    stage = START
    done = False

    
# Game loop
done = False
BACKGROUND.play(-1)
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            done = True
        elif event.type is pygame.KEYDOWN:
            if event.key is pygame.K_ESCAPE:
                done = True
            elif stage is START:
                if event.key is pygame.K_SPACE:
                    stage = PLAYING
            elif stage is PLAYING:
                if event.key is pygame.K_SPACE:
                    ship.shoot()
                    player.num_shots += 1
            elif stage is WIN or LOSE:
                if event.key is pygame.K_SPACE:
                    setup()

    pressed = pygame.key.get_pressed()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage is PLAYING:
        if pressed[pygame.K_LEFT]:
           ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        elif pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

        player.update()
        lasers.update()
        mobs.update()
        fleet.update()
        fleet2.update()
        gks.update()
        bombs.update()
        

        check_end()
        
        
    

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    

    
    if stage is START:
        show_title_screen()
    if stage is PLAYING:
        screen.blit(back_img, (0,0))
        player.draw(screen)
        lasers.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        gks.draw(screen)
        show_stats()
    if stage is WIN:
        show_win_screen()
        show_stats()
        accuracy_end()
    if stage is LOSE:
        show_lose_screen()
        show_stats()
        accuracy_end()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
