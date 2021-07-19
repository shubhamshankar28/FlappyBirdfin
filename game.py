import pygame
from pygame.locals import *
import random
pygame.init()
clock = pygame.time.Clock()
fps=60
screen_width = 864
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")
# game variables
fly= False
go= False
groundcoord = 0
scrollspeed = 4
pipe_gap = 150
freq = 1500
passed=False
score=0
restart = pygame.image.load('img/restart.png')
def resetvals():
    pipe_group.empty()
    bird1.rect.x=100
    bird1.rect.y = (screen_height/2)
    return 0

# define font
font = pygame.font.SysFont('Bahaus 93',60)
#color
white = (255,255,255)
last_time = pygame.time.get_ticks() - freq
class Button():
    def __init__(self,img,x,y):
        self.image=img;
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos)==True):
            if(pygame.mouse.get_pressed()[0] == 1):
                action=True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.index=0
        self.counter=0
        self.images = []
        for i in range(3):
            img = pygame.image.load(f'img/bird{i+1}.png')
            self.images.append(img)

        self.image=self.images[self.index]
        self.rect=self.image.get_rect()

        self.rect.center = [x,y]
        self.click=False
        self.vel=0
    def update(self):
        #gravity
        #print(self.vel)
        if(fly):
            self.vel=self.vel+0.5
            #if(self.vel>50):
            #    self.vel=50
            if(self.vel>8):
                self.vel=8

            if(self.rect.bottom<768):
                self.rect.y=self.rect.y+int(self.vel)
        #upward
        if(go == False):
            if(pygame.mouse.get_pressed()[0]==1 and self.click==False):
                self.click=True
                self.vel=-10
            if(pygame.mouse.get_pressed()[0]==0):
                self.click=False
            self.counter=self.counter+1;
            if(self.counter==5):
                self.counter=0
                self.index=(self.index+1)%3
            self.image=self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index],-2*self.vel)
        else:
             self.image = pygame.transform.rotate(self.images[self.index],90)
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,flag):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if(flag==0):
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y-int(pipe_gap/2)]

        else:
            self.rect.topleft = [x,y+int(pipe_gap/2)]
    def update(self):
        self.rect.x=self.rect.x - scrollspeed
        if(self.rect.right<0):
            self.kill()

def texttoimg(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img , (x,y))
bird_group = pygame.sprite.Group()
bird1 = Bird(100,(screen_height/2))
bird_group.add(bird1)

pipe_group = pygame.sprite.Group()

#load images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')
rb = Button(restart,int(screen_width/2),int(screen_height/2))
run = True
while(run):
    clock.tick(fps)
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundcoord,730))
    time_now = pygame.time.get_ticks()

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    if (len(pipe_group)>0):
#        print(f"{pipe_group.sprites()[0].rect.left} and {pipe_group.sprites()[0].rect.right} ")
        if(bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right and passed==False):
            passed=True
        if(passed==True and bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right ):
            passed=False
            score=score+1
    texttoimg(str(score),font,white,int(screen_width/2),30)
    if(bird1.rect.bottom>730):
        go=True
        fly=False
    if(pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or bird1.rect.top<0):
        go=True

    if(go==False and fly==True):
        if(time_now-last_time>=freq):
            last_time=time_now
            x = random.randint(-100,100)
            pipe1 = Pipe(screen_width , (screen_height/2)+x,1)
            pipe2 = Pipe(screen_width,(screen_height/2)+x,0)
            pipe_group.add(pipe1)
            pipe_group.add(pipe2)
        groundcoord=groundcoord-scrollspeed


        pipe_group.update()
    if(go == True):
        if(rb.draw()==True):
            print("gameover")
            go=False
            score=resetvals()


    if(abs(groundcoord)>35):
        groundcoord=0
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            run=False
        if(event.type==pygame.MOUSEBUTTONDOWN and fly==False and go == False):
            fly=True

    pygame.display.update()
pygame.quit()
