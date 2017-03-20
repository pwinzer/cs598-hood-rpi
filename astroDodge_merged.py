#!/usr/bin/python

import sys
import random
import pygame
import time
import sys
import os.path

WIDTH = 800
HEIGHT = 600
score = 0
numbers = []

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (211,211,211)
tomato = (255,9,71)
enemy_images = ["mars.png", "pluto.png", "uranus.png"]

class Enemy(pygame.sprite.Sprite):
    MIN_SIZE = 15
    MAX_SIZE = 40 

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randint(self.MIN_SIZE, self.MAX_SIZE)
        enemy_image = enemy_images[random.randint(0,len(enemy_images)-1)]
        self.image = pygame.transform.scale(pygame.image.load(enemy_image), (self.size, self.size))
        self.rect = pygame.Rect(random.randint(0, WIDTH), 0-self.size,
                                self.size, self.size)
        self.speed = random.randint(1,5)
        self.plain = pygame.sprite.RenderPlain(self) #PDW#

    def move(self, increase):
        self.rect.bottom += self.speed + increase  

    def draw(self):
        self.plain.draw(screen)


class EnemyManager():
    def __init__(self):
        self.counter = 0
        self.rate = 100   

    def generate(self):
        self.counter += self.rate
        self.rate += 0.5
        if self.counter > 1000:
            self.counter %= 1000
            return True
        return False


class Player(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        player_image = "player.png"
        self.image = pygame.transform.scale(pygame.image.load(player_image), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.y = HEIGHT-50
        self.plain = pygame.sprite.RenderPlain(self) 
        laser_sound = "laser.wav"
        self.laser_sound = pygame.mixer.Sound(laser_sound) 
        self.laser_sound.set_volume(0.15)
        self.projectiles = []
    
    def shoot(self) :
        self.laser_sound.play()
        p = Projectile(self.rect.centerx, self.rect.centery, screen)
        self.projectiles.append(p)

    def remove(self,proj) :
       	self.projectiles.remove(proj)
		
    def draw(self):
        self.plain.draw(screen)


    def move(self, dest):
        self.rect.centerx = dest
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

		
class Projectile(object) :
    def __init__(self, x, y, screen) :
        self.size = 6
        self.rect = pygame.Rect(x, HEIGHT-50, 6, 6)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.speed = 10
        self.color = red
        self.surface.fill(self.color)

    def move(self):
        self.rect.bottom -= 0.5 * self.speed
   
    def draw(self, surface):
        surface.blit(self.surface, self.rect)

		
class Game():
    def __init__(self, surface):
        pygame.init()
        self.surface = surface
        explosion_sound = "atari_boom.wav"
        self.explosion_sound = pygame.mixer.Sound(explosion_sound) 
        background_music = "groovy.ogg"
        self.music = pygame.mixer.Sound(background_music) 
        self.intro()
    
    def _check_collisions(self, enemies, player):
        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                self.explosion_sound.play()
                return True
        return False
		
    def _check_projectile_collisions(self, enemies, player):
        for enemy in enemies:	    
            for projectile in player.projectiles:
                if enemy.rect.colliderect(projectile.rect):
                    player.remove(projectile)	
                    enemies.remove(enemy)
                    return False

    def quitgame(self):
        pygame.quit()
        quit()
        
    def intro(self):
        global score
        global numbers      
        scores_height = 210
        position = 0
        write_score()
        numbers = sort_scores()
        write_sorted()        
        ship_horizontal = 20
        ship_vertical = 50       
        
        self.music.play()

        while True:      
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            background_image = "background.png"
            background = pygame.transform.scale(pygame.image.load(background_image), (WIDTH, HEIGHT)).convert()
            screen.blit(background,(0,0))
            
            ship_image = "ship.png"
            ship = pygame.transform.scale(pygame.image.load(ship_image), (70, 70)).convert()
            
            screen.blit(ship,(ship_horizontal,ship_vertical))
            if ship_horizontal < 700 and ship_vertical == 50:
                ship_horizontal += 5
            if ship_vertical < 510 and ship_horizontal == 700:
                ship_vertical += 5
            if ship_horizontal > 20 and ship_vertical == 510:
                ship_horizontal -= 5
            if ship_vertical > 50 and ship_horizontal == 20:
                ship_vertical -= 5
               
        
            title = pygame.font.Font(None, 60).render('ASTRODODGE', True, tomato)
            self.surface.blit(title, ((WIDTH-title.get_rect().width)/2, 170))
            high_score_prompt = pygame.font.SysFont('monospace', 30).render(("HIGH SCORES: "), True, tomato)
            self.surface.blit(high_score_prompt, ((WIDTH-high_score_prompt.get_rect().width)/2, scores_height))
            if numbers == []:
                instructions = pygame.font.SysFont('monospace', 30).render('0', True, tomato)
                self.surface.blit(instructions, ((WIDTH-instructions.get_rect().width)/2, scores_height + 40))
            else:
              for num in range(0,len(numbers)):
                instructions = pygame.font.SysFont('monospace', 30).render(str(numbers[num]), True, tomato)
                self.surface.blit(instructions, ((WIDTH-instructions.get_rect().width)/2, scores_height + (40+num*30)))

            button("PLAY", 150,450,100,50, white, blue, self.play)
            button("QUIT", 550,450,100,50, white, green, self.quitgame)
            
            #print(mouse)
            pygame.display.update()
                         
    def play(self):
        # initialize variables
        clock = pygame.time.Clock()
        enemies = []
        enemymanager = EnemyManager()
        player = Player(pygame.mouse.get_pos()[0])
        increase = 0
        lives = 3
        global score
        global numbers
        score = 0
        background_image = "background.png"
        background = pygame.transform.scale(pygame.image.load(background_image), (WIDTH, HEIGHT)).convert()

        while lives > 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                if e.type == pygame.KEYDOWN :
                    if e.key == pygame.K_SPACE :
                        player.shoot() 
                if e.type == pygame.MOUSEMOTION:
                    player.move(e.pos[0])
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    nitro = 1
                if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    nitro = 0
      
            # draw surface
            screen.blit(background,(0,0)) 
       
            # draw enemies
            for enemy in enemies:
                enemy.move(increase)
                enemy.draw()
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
            if enemymanager.generate() and len(enemies) < 41:
                enemies.append(Enemy())
            if score < 0 and score < 10000:
                increase = 0
            if score > 10000 and score < 40000:
                increase = 1
            if score > 40000 and score < 80000:
                increase = 2
            if score > 80000 and score < 100000:
                increase = 4
            message = ('Score: ' + str(score))
            font = pygame.font.Font(None, 40)
            text = font.render(message, 1, white)
            screen.blit(text, (600,50))
            
            # draw player
            player.draw()
			
            # draw projectiles
            for i in range(0, len(player.projectiles)):
            	player.projectiles[i].move()
            	player.projectiles[i].draw(self.surface)
           
            # increment score
            score += len(enemies)
               
            # check for collisions - if so, remove all enemies and subtract a life
            if self._check_collisions(enemies, player):
                enemies = []
                player.projectiles = []
                lives -= 1
                if lives > 0:
                    time.sleep(1)
                if lives == 0:
                    gameover()
                    self.music.stop()
                    self.intro()
					
            # check for projectile collisions - if so, remove enemy affected
            self._check_projectile_collisions(enemies, player)
			
            #print(score)
            pygame.display.update()
            clock.tick(60)
        sys.exit(0)


#changes color of buttons when hover         
def button(msg, x, y, w, h, i, a, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, a,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, i,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x+(w/2), y+(h/2))
    screen.blit(textSurf, textRect)
#reads list from .txt file and returns sorted list    
def sort_scores():
    scores_numbers = []
    with open('scores.txt','r') as file:
        for line in file:
            num = str(line).replace('\n','')
            scores_numbers.append(int(num))
    sorted_numbers = sorted(scores_numbers, reverse=True)
    file.close()
    return sorted_numbers
#write a sorted list to a file named "scores.txt"
def write_sorted():
    global numbers
    open_file = open('scores.txt','w')
    x = 0
    for element in numbers:
        open_file.write(str(element) + '\n')
        x += 1
        if x == 5:
            break
    open_file.close()


def write_score():
    global score
    if score != 0:
        with open('scores.txt','a') as myfile:
            myfile.write(str(score) + '\n')
        myfile.close()
    else:
        f = open('scores.txt', 'a')
        f.close()
            
    

def gameover():
    global numbers
    global score
    if numbers == [] or score > numbers[0]:
      message_display("HIGH SCORE!")
    else:
      message_display("GAME OVER!")
		
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((WIDTH/2), (HEIGHT/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()           



if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AstroDodge')
    screen = pygame.display.get_surface()
    g = Game(surface)
