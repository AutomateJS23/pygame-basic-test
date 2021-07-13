import pygame
import pygame_menu
import random

pygame.init()

WIN_WIDTH, WIN_HEIGHT = 300, 300
WIN = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
pygame.display.set_caption('Cat Revenge')
pygame.display.set_icon(pygame.image.load('img/caticon.jpeg'))
clock = pygame.time.Clock()
bg = pygame.image.load('img/bg.jpg').convert()
bg = pygame.transform.scale(bg , (776, 320))
myfont = pygame.font.SysFont("monospace", 16)
myhero_die = pygame.font.SysFont("monospace", 24)

walk_right_image = ['img/walkRight/1.png', 'img/walkRight/2.png', 'img/walkRight/3.png',
             'img/walkRight/4.png','img/walkRight/5.png']
standing_cat = ['img/catcute.png', 'img/caticon.jpeg']

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = ""
        self.count_score = None
        self.left = False
        self.right = False
        self.isJump = False
        self.standing = False
        self.jumpCount = 16
        self.count_image = 0
        self.count_standing = 0
        self.speed = 2
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(center = (self.x , self.y))
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.animation_frame = len(walk_right_image)+2
        self.current_frame = 0
        
    def draw(self):
        self.rect = self.surf.get_rect(center = (self.x , self.y))
        if self.orientation == "Right":
            self.image = pygame.image.load(walk_right_image[self.count_image])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            WIN.blit(self.image, self.rect)
        elif self.orientation == "Left":
            self.image = pygame.image.load(walk_right_image[self.count_image])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            WIN.blit(self.image, self.rect)
        else:
            #self.image = pygame.image.load(standing_cat[self.count_standing])
            self.image = pygame.image.load(walk_right_image[self.count_standing])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            WIN.blit(self.image, self.rect)
        
    def move(self):
        if self.left:
            if self.x> self.width/2:
                self.current_frame+=1
                if self.current_frame >= self.animation_frame:
                    self.current_frame = 0
                    self.count_image = (self.count_image + 1) % len(walk_right_image)
                #self.rect.move_ip(*self.velocity)
                self.x-=self.speed
                self.left = False
        if self.right:
            if self.x<WIN_WIDTH-100:
                self.current_frame+=1
                if self.current_frame >= self.animation_frame:
                    self.current_frame = 0
                    self.count_image = (self.count_image + 1) % len(walk_right_image)
                #self.rect.move_ip(*self.velocity)
                self.x+=self.speed
                self.right = False
        if self.isJump:
            if self.jumpCount >= -16:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount**2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.jumpCount = 16
                self.isJump = False   
        if self.standing:
            self.current_frame+=1
            if self.current_frame >= self.animation_frame:
                self.current_frame = 0
                self.count_standing = (self.count_standing + 1) % len(walk_right_image)
        
    def die(self):
        return False

class Enemies(pygame.sprite.Sprite):
    def __init__(self, image,x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.drop_check = False
        self.speed = 1
        self.imgaepath = image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.surf = pygame.Surface((self.width, self.height))
    def draw(self):
        self.rect = self.surf.get_rect(center = (self.x , self.y))
        WIN.blit(self.image, self.rect)
    def move(self):
        self.x -= self.speed
    def drop(self, enemy_y):
        if self.drop_check:
            self.y += self.speed
            self.drop_check = False
        else:
            self.y = enemy_y
            self.move()
            

def game_start():
    # -- player --
    hero_x = 50
    hero_y = 230 
    hero_width = 30
    hero_height = 48
    hero = Player(hero_x, hero_y, hero_width, hero_height)
    # -- enemy object --
    enemy_width = 20
    enemy_height = 25
    enemy_x = 1000
    enemy_y = 240
    enemy_obj1 = Enemies('img/enemy.png', random.randrange(160, WIN_WIDTH+2500), 
                            random.randrange(0, WIN_HEIGHT-250), enemy_width ,enemy_height)
    enemy_obj2 = Enemies('img/enemy.png', random.randrange(160, WIN_WIDTH+3500), 
                        random.randrange(0, WIN_HEIGHT-250), enemy_width, enemy_height)
    enemy_obj3 = Enemies('img/enemy.png', enemy_x, enemy_y, enemy_width, enemy_height)
    # -- sprite group enemies --
    sprite_enemies = pygame.sprite.Group()
    sprite_enemies.add(enemy_obj1)
    sprite_enemies.add(enemy_obj2)
    sprite_enemies.add(enemy_obj3)
    # -- sprite group all -- 
    sprite_all = pygame.sprite.Group()
    sprite_all.add(hero)
    sprite_all.add(enemy_obj1)
    sprite_all.add(enemy_obj2)
    sprite_all.add(enemy_obj3)
    bgX = 0
    bgX2 = bg.get_width()
    start_time = pygame.time.get_ticks()
    game_on = True
    while game_on:
        pygame.time.delay(10)
        clock.tick(60)
        bgX -= 1.4
        bgX2 -= 1.4
        if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
            bgX = bg.get_width()
    
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #game_on = False
                pygame.quit()
        
        keys = pygame.key.get_pressed()
        hero.standing = True
        hero.orientation = ""
        if keys[pygame.K_UP]:
            hero.isJump = True
            hero.standing = False
        if keys[pygame.K_LEFT]:
            hero.left = True
            hero.orientation = "Left"
            hero.standing = False
        if keys[pygame.K_RIGHT]:
            hero.right = True
            hero.orientation = "Right"
            hero.standing = False

        # -- background and score time --
        if start_time:
            hero.count_score = int((pygame.time.get_ticks() - start_time) / 1000)
            screen_text_score = myfont.render(f'Score : {hero.count_score}', True, (0, 0, 0))
        # -- bg -- 
        WIN.blit(bg, (bgX, 0))  # draws our first bg image
        WIN.blit(bg, (bgX2, 0))  # draws the seconf bg image
        #WIN.blit(bg, [0, 0])
        # -- hero cat --
        hero.move()
        hero.draw()
        #-- enemy spawn right --
        enemy_obj3.draw()
        enemy_obj3.move()
        enemy_obj1.draw()
        enemy_obj2.draw()
        
        # -- enemy move --
        if enemy_obj3.x < 0:
            enemy_obj3.x = random.randrange(WIN_WIDTH, WIN_WIDTH+100)
        # -- enemy drop_check -- 
        if enemy_obj1.y < hero.y:
            enemy_obj1.drop_check = True
            enemy_obj1.drop(enemy_y)
        else:
            enemy_obj1.drop(enemy_y)
            if enemy_obj1.x < 0:
                enemy_obj1.x = random.randrange(160, WIN_WIDTH-5)
                enemy_obj1.y = random.randrange(0, WIN_HEIGHT-250)
        if enemy_obj2.y < hero.y:
            enemy_obj2.drop_check = True
            enemy_obj2.drop(enemy_y)
        else:
            enemy_obj2.drop(enemy_y)
            if enemy_obj2.x < 0:
                enemy_obj2.x = random.randrange(160, WIN_WIDTH-5)
                enemy_obj2.y = random.randrange(0, WIN_HEIGHT-250)
        
        if pygame.sprite.spritecollideany(hero, sprite_enemies):
            print('Hero Die')
            hero.isJump = True
            game_on = False
        # -- WIN Score --
        WIN.blit(screen_text_score, (5, 10))
        pygame.display.update()
    main_menu(False, str(hero.count_score))
    #pygame.quit()

def main_menu(flag, score):
    if flag:
        menu = pygame_menu.Menu('Welcome', 250, 250, theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Play', game_start)
        menu.add.button('Exit', pygame_menu.events.EXIT)
        menu.mainloop(WIN)
    else:
        menu_d = pygame_menu.Menu('You Die', 250, 250,  theme=pygame_menu.themes.THEME_BLUE)
        menu_d.add.text_input(f'Your Score : {score}', '')
        menu_d.add.button('Play again', game_start)
        menu_d.add.button('Exit', pygame_menu.events.EXIT)
        menu_d.mainloop(WIN)

def main():
    main_menu(True, None)
if __name__=='__main__':
    main()