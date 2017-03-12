
import sys

import random

import pygame



WIDTH = 800

HEIGHT = 600



class Enemy():

    MIN_SIZE = 15

    MAX_SIZE = 40

    

    def __init__(self):

        self.size = random.randint(self.MIN_SIZE, self.MAX_SIZE)

        self.rect = pygame.Rect(random.randint(0, WIDTH), 0-self.size,

                                self.size, self.size)

        self.surface = pygame.Surface((self.rect.width, self.rect.height))

        self.speed = random.randint(10,30)

        self.color = (random.randint(130, 255), random.randint(130, 255), random.randint(130, 255))

        self.surface.fill(self.color)

    

    def move(self, nitro):

        self.rect.bottom += (0.5 + 0.5 * nitro) * self.speed

    

    def draw(self, surface):

        surface.blit(self.surface, self.rect)



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



class Player():

    def __init__(self, x):

        self.rect = pygame.Rect(x, HEIGHT-50, 25, 25)

        self.surface = pygame.Surface((25, 25))

        self.color = (255, 255, 255)

        self.surface.fill(self.color)

    

    def draw(self, surface):

        surface.blit(self.surface, self.rect)

    

    def move(self, dest):

        self.rect.centerx = dest

        self.rect.left = max(0, self.rect.left)

        self.rect.right = min(WIDTH, self.rect.right)



class Game():

    def __init__(self, surface):

        pygame.init()

        self.surface = surface

        self.intro()

    

    def _check_collisions(self, enemies, player):

        for enemy in enemies:

            if enemy.rect.colliderect(player.rect):

                return True

        return False

    

    def intro(self):

        self.surface.fill((10,110,10))

        title = pygame.font.Font(None, 60).render("DODGER", True, (255, 255, 255))

        instructions = pygame.font.Font(None, 30).render("Press any key to play", True, (255, 255, 255))

        self.surface.blit(title, ((WIDTH-title.get_rect().width)/2, 20))

        self.surface.blit(instructions, ((WIDTH-instructions.get_rect().width)/2, 70))

        pygame.display.update()        

        while True:

            for e in pygame.event.get():

                if e.type == pygame.QUIT:

                    sys.exit(0)

                if e.type == pygame.KEYDOWN:

                    self.play()

    

    def play(self):

        # initialize variables

        clock = pygame.time.Clock()

        enemies = []

        enemymanager = EnemyManager()

        player = Player(pygame.mouse.get_pos()[0])

        score = 0

        lives = 3

        nitro = 0

        

        while lives > 0:

            for e in pygame.event.get():

                if e.type == pygame.QUIT:

                    sys.exit(0)

                if e.type == pygame.MOUSEMOTION:

                    player.move(e.pos[0])

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                    nitro = 1

                if e.type == pygame.MOUSEBUTTONUP and e.button == 1:

                    nitro = 0

            

            # draw surface
            if lives == 3:
              self.surface.fill((10,110,10))
            elif lives == 2:
              self.surface.fill((255,160,0))
            elif lives == 1:
              self.surface.fill((210,30,30))
            

            # draw enemies

            for enemy in enemies:

                enemy.move(nitro)

                enemy.draw(self.surface)

                if enemy.rect.top > HEIGHT:

                    enemies.remove(enemy)

            if enemymanager.generate() and len(enemies) < 41:

                enemies.append(Enemy())

            

            # draw player

            player.draw(self.surface)

            

            # increment score

            score += len(enemies) * (1 + (3*nitro))

            

            # check for collisions - if so, remove all enemies and subtract a life

            if self._check_collisions(enemies, player):

                enemies = []

                lives -= 1

            

            pygame.display.update()

            print (("Score: {0}").format(score))

            clock.tick(60)

        sys.exit(0)

        

if __name__ == '__main__':

    pygame.init()

    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    g = Game(surface)
