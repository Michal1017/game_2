import pygame
from pygame.locals import *
import random

class Bomb:
    def __init__(self,hero,parent_screen):
        self.parent_screen=parent_screen
        self.x=hero.x
        self.y=hero.y
        self.width=40
        self.height=40
        self.direction=hero.direction
        self.texture=pygame.image.load("resources/block.jpg")

    def draw(self):
        self.parent_screen.blit(self.texture,(self.x,self.y))


    def shoot(self):
        if(self.direction=='Right'):
            self.x+=2
        if(self.direction=='Left'):
            self.x-=2
        if(self.direction=='Up'):
            self.y-=2
        if(self.direction=='Down'):
            self.y+=2

class end_game:
    def __init__(self,parent_screen):
        self.x=960
        self.y=400
        self.height=40
        self.width=40
        self.parent_screen=parent_screen
        self.texture = pygame.image.load("resources/end_game.png").convert()

    def draw(self):
        self.parent_screen.blit(self.texture,(self.x,self.y))


class Obstacle:
    def __init__(self,parent_screen):
        self.x=random.randint(100,1000)
        self.y=random.randint(0,800)
        self.direction_y=0
        self.direction_x=0
        self.height=40
        self.width=40
        self.speed=0.5
        self.parent_screen=parent_screen
        self.texture=pygame.image.load("resources/obstacle.png").convert()

    def draw(self):
        self.parent_screen.blit(self.texture,(self.x,self.y))

    def move(self):
        if(self.direction_y==0):
            self.y-=self.speed
        if(self.direction_y==1):
            self.y+=self.speed
        if(self.direction_x==0):
            self.x-=self.speed
        if(self.direction_x==1):
            self.x+=self.speed
        if(self.y>=800-self.height):
            self.direction_y=0
        if(self.y<=0):
            self.direction_y=1
        if (self.x >= 1000-self.width):
            self.direction_x = 0
        if (self.x <= 0):
            self.direction_x = 1



class Hero:
    def __init__(self,parent_screen):
        self.x=0
        self.y=400
        self.width=40
        self.height=40
        self.angle=0
        self.parent_screen=parent_screen
        self.direction='Right'
        self.texture=pygame.image.load("resources/statek.png")
        self.bombs=[]

    def draw(self):
        self.parent_screen.blit(self.texture,(self.x,self.y))


    def move_up(self):
        self.y-=1
        self.direction='Up'
    def move_down(self):
        self.y+=1
        self.direction = 'Down'
    def move_left(self):
        self.x-=1
        self.direction = 'Left'
    def move_right(self):
        self.x+=1
        self.direction = 'Right'
    def shoot(self):
        self.bombs.append(Bomb(self,self.parent_screen))

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game")
        self.level=1
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((50, 100, 150))
        self.num_obst=2
        self.hero=Hero(self.surface)
        self.hero.draw()
        self.obstacles=[]
        for i in range(self.num_obst):
            obstacle=Obstacle(self.surface)
            self.obstacles.append(obstacle)
            self.obstacles[i].draw()
        self.end_game=end_game(self.surface)
        self.end_game.draw()


    def is_collision(self,x1,y1,width1,height1 ,x2,y2,width2,heigt2):
        if (x1 < x2 + width2 and x1 + width1 > x2 and y1 < y2 + heigt2 and height1 + y1 > y2):
            return True
        return False

    def horizontal_collision(self,x1,width1 ,x2,width2):
        if (x1 < x2 + width2 and x1 + width1 > x2):
            return True
        return False

    def vertical_collision(self,y1,height1 ,y2,heigt2):
        if (y1 < y2 + heigt2 and height1 + y1 > y2):
            return True
        return False

    def next_level(self):
        self.level+=1
        self.hero.x=0
        self.hero.y=400
        self.num_obst+=1
        self.obstacles.append(Obstacle(self.surface))
        for i in range(self.num_obst):
            self.obstacles[i].speed+=0.5
            self.obstacles[i].x=random.randint(100,1000)
            self.obstacles[i].y=random.randint(0,800)
        self.surface.fill((50, 100, 150))
        font = pygame.font.SysFont('arial', 50)
        line1 = font.render(f"LEVEL {self.level}", True, (255, 255, 255))
        self.surface.blit((line1), (400, 300))
        pygame.display.flip()
        pygame.time.delay(2000)


    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Level: {self.level}",True,(255,255,255))
        self.surface.blit(score,(800,10))

    def show_game_over(self):
        self.surface.fill((50, 100, 150))
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is over: Your level is {self.level}", True,(255,255,255))
        self.surface.blit((line1),(200,300))
        line2=font.render("To play again press Enter, To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()

    def reset(self):
        self.num_obst=2
        self.level=1
        self.hero=Hero(self.surface)
        self.obstacles = []
        for i in range(self.num_obst):
            obstacle = Obstacle(self.surface)
            self.obstacles.append(obstacle)



    def play(self):
        self.surface.fill((50, 100, 150))
        for i in range(self.num_obst):
            self.obstacles[i].draw()
            self.obstacles[i].move()
        self.hero.draw()
        self.end_game.draw()
        self.display_score()
        for i in range(len(self.hero.bombs)):
            self.hero.bombs[i].draw()
            self.hero.bombs[i].shoot()
        pygame.display.flip()

        for i in range(self.num_obst):
            for j in range(len(self.hero.bombs)):
                if(self.is_collision(self.obstacles[i].x, self.obstacles[i].y, self.obstacles[i].width,
                                  self.obstacles[i].height, self.hero.bombs[j].x, self.hero.bombs[j].y, self.hero.bombs[j].width,
                                  self.hero.bombs[j].height) == True):

                    self.hero.bombs.pop(j)

        for i in range(self.num_obst):
            if (self.is_collision(self.obstacles[i].x, self.obstacles[i].y, self.obstacles[i].width,
                                  self.obstacles[i].height, self.hero.x, self.hero.y, self.hero.width,
                                  self.hero.height) == True):
                raise "Game over"

        if (self.is_collision(self.end_game.x, self.end_game.y, self.end_game.width, self.end_game.height, self.hero.x,
                              self.hero.y, self.hero.width, self.hero.height) == True):
            self.next_level()


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.hero.y > 0:
            self.hero.move_up()
        if keys[pygame.K_DOWN] and self.hero.y < 800 - self.hero.height:
            self.hero.move_down()
        if keys[pygame.K_LEFT] and self.hero.x > 0:
            self.hero.move_left()
        if keys[pygame.K_RIGHT] and self.hero.x < 1000 - self.hero.width:
            self.hero.move_right()
        pygame.time.delay(10)

    def run(self):
        running=True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key ==K_RETURN:
                        pause=False
                    elif event.key ==K_w:
                        self.hero.shoot()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                self.reset()
                pause = True

if __name__ == "__main__":
    print('Game start')
    game=Game()
    game.run()