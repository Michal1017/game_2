import pygame
from pygame.locals import *
import random

# creating class bomb
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

# shooting fuction for bomb
    def shoot(self):
        if(self.direction=='Right'):
            self.x+=2
        if(self.direction=='Left'):
            self.x-=2
        if(self.direction=='Up'):
            self.y-=2
        if(self.direction=='Down'):
            self.y+=2

# class with screen with is showing when game is ended
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

# obstacle class
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

# fuction which operate moving of obstacles
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


# hero class - space ship which we are controlling
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
        self.change_of_direction=False
        self.last_direction='Right'

    def draw(self):
        self.parent_screen.blit(self.texture,(self.x,self.y))

# fuctions which operate moving of hero
    def move_up(self):
        self.y-=1
        self.direction='Up'
        if(self.last_direction!=self.direction):
            if(self.last_direction=='Right'):
                pygame.transform.rotate(self.texture,90)
                print(self.last_direction, ' ', self.direction)
            if (self.last_direction == 'Left'):
                pygame.transform.rotate(self.texture, -90)
            if (self.last_direction == 'Down'):
                pygame.transform.rotate(self.texture, 180)
            self.last_direction=self.direction


    def move_down(self):
        self.y+=1
        self.direction = 'Down'
        if(self.last_direction!=self.direction):
            if(self.last_direction=='Right'):
                pygame.transform.rotate(self.texture,-90)
            if (self.last_direction == 'Left'):
                pygame.transform.rotate(self.texture, 90)
            if (self.last_direction == 'Up'):
                pygame.transform.rotate(self.texture, 180)
            self.last_direction=self.direction
    def move_left(self):
        self.x-=1
        self.direction = 'Left'
        if(self.last_direction!=self.direction):
            if(self.last_direction=='Right'):
                pygame.transform.rotate(self.texture,180)
            if (self.last_direction == 'Up'):
                pygame.transform.rotate(self.texture, -90)
            if (self.last_direction == 'Down'):
                pygame.transform.rotate(self.texture, 90)
            self.last_direction=self.direction
    def move_right(self):
        self.x+=1
        self.direction = 'Right'
        if(self.last_direction!=self.direction):
            if(self.last_direction=='Up'):
                pygame.transform.rotate(self.texture,90)
            if (self.last_direction == 'Left'):
                pygame.transform.rotate(self.texture, 180)
            if (self.last_direction == 'Down'):
                pygame.transform.rotate(self.texture, 90)
            self.last_direction=self.direction

# function which operates shooting
    def shoot(self):
        self.bombs.append(Bomb(self,self.parent_screen))


# main class which operates game phisics
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

# function which operates collision between two objects
    def is_collision(self,x1,y1,width1,height1 ,x2,y2,width2,heigt2):
        if (x1 < x2 + width2 and x1 + width1 > x2 and y1 < y2 + heigt2 and height1 + y1 > y2):
            return True
        return False

# functions which operate from which side is collision
    def horizontal_collision(self,x1,width1 ,x2,width2):
        if (x1 < x2 + width2 and x1 + width1 > x2):
            return True
        return False

    def vertical_collision(self,y1,height1 ,y2,heigt2):
        if (y1 < y2 + heigt2 and height1 + y1 > y2):
            return True
        return False


# function which operates level uping
    def next_level(self):
        self.level+=1
        self.hero.x=0
        self.hero.y=400
        self.obstacles.clear()
        self.num_obst=self.level+1
        for i in range(self.num_obst):
            obstacle=Obstacle(self.surface)
            self.obstacles.append(obstacle)
            self.obstacles[i].draw()
        self.obstacles.append(Obstacle(self.surface))
        for i in range(self.num_obst):
            self.obstacles[i].speed+=0.2*i
            self.obstacles[i].direction_x=random.randint(0,1)
            self.obstacles[i].direction_y = random.randint(0, 1)
            self.obstacles[i].x=random.randint(100,1000)
            self.obstacles[i].y=random.randint(0,800)
        self.surface.fill((50, 100, 150))
        font = pygame.font.SysFont('arial', 50)
        line1 = font.render(f"LEVEL {self.level}", True, (255, 255, 255))
        self.surface.blit((line1), (400, 300))
        pygame.display.flip()
        pygame.time.delay(2000)

# function which operates displaing score
    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Level: {self.level}",True,(255,255,255))
        self.surface.blit(score,(800,10))


# function which operates showing game over screen
    def show_game_over(self):
        self.surface.fill((50, 100, 150))
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is over: Your level is {self.level}", True,(255,255,255))
        self.surface.blit((line1),(200,300))
        line2=font.render("To play again press Enter, To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()


# function which operates reset game after loose and restarting game
    def reset(self):
        self.num_obst=2
        self.level=1
        self.hero=Hero(self.surface)
        self.obstacles = []
        for i in range(self.num_obst):
            obstacle = Obstacle(self.surface)
            self.obstacles.append(obstacle)


# function which operates gameplay of whole game
    def play(self):
        #displaing objects
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
    # opereting collisions
        for i in range(self.num_obst):
            for j in range(len(self.hero.bombs)):
                if(self.is_collision(self.obstacles[i].x, self.obstacles[i].y, self.obstacles[i].width,
                                  self.obstacles[i].height, self.hero.bombs[j].x, self.hero.bombs[j].y, self.hero.bombs[j].width,
                                  self.hero.bombs[j].height) == True):

                    self.hero.bombs.pop(j)
                    self.obstacles.pop(i)
                    self.num_obst-=1

        for i in range(self.num_obst):
            if (self.is_collision(self.obstacles[i].x, self.obstacles[i].y, self.obstacles[i].width,
                                  self.obstacles[i].height, self.hero.x, self.hero.y, self.hero.width,
                                  self.hero.height) == True):
                raise "Game over"

        if (self.is_collision(self.end_game.x, self.end_game.y, self.end_game.width, self.end_game.height, self.hero.x,
                              self.hero.y, self.hero.width, self.hero.height) == True):
            self.next_level()

    # contrilling
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

    #  operating actions apart from main gameplay like quiting game etc.
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