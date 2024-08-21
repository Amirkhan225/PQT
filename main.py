import pygame
import sys
import json

pygame.init()
window_width=800
window_height=600
window=pygame.display.set_mode((window_width,window_height))
clock=pygame.time.Clock()
pygame.display.set_caption("Platformer game")
# font = pygame.font.Font(None,36)


FPS=30
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
class Player:
    def __init__(self,window_width,window_height):
        self.width=50
        self.height=50
        self.x=window_width//2-self.width//2
        self.y=window_height-self.height
        self.speed=5
        self.jump=False
        self.jump_count=0
    def draw(self,window):
        pygame.draw.rect(window,BLUE,(self.x,self.y,self.width,self.height))
    def move(self,keys):
        if keys[pygame.K_LEFT]:
            self.x-=self.speed
        if keys[pygame.K_RIGHT]:
            self.x+=self.speed
        if keys[pygame.K_SPACE] and not self.jump:
            self.jump_count=20
            self.jump=True
    def update(self):
        if self.jump_count>=0:
            self.y-=15
            self.jump_count-=1
        for platform in platforms:
            if self.y + self.height>=platform.y and self.y+self.height<platform.y+10 and self.x+self.width>=platform.x and self.x<=platform.x+platform.w:
                self.y=platform.y-self.height
                self.jump=False
        self.y+=10*(self.y/(window_height-self.height))
        if self.y> window_height -self.height:
            self.y=window_height -self.height
            self.jump=False
class Platforms:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
    def draw(self,window):
        pygame.draw.rect(window,RED,(self.x,self.y,self.w,self.h))
levels=10
index=0
class Goal:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.w=50
        self.h=50
    def draw(self,window):
        pygame.draw.rect(window,GREEN,(self.x,self.y,self.w,self.h))
    def update(self):
        global platforms, goal
        if player.x+player.width>=self.x and player.x<=self.x+self.w and player.y+player.height>=self.y and player.y<=self.y +self.h:
            print("Goal reached!")
            platforms=[]
            for d in levels[index]['platforms']:
                platform=Platforms(d['x'],d['y'],d['w'],d['h'])
                platforms.append(platform)
                goal=Goal(levels[index]['goal']['x'],levels[index]['goal']['y'])
                player.x=window_width//2-self.w//2
                player.y=window_height-self.h
with open('levels.json') as f:
    levels=json.load(f)
platforms=[]
for d in levels[0]['platforms']:
    platform=Platforms(d['x'],d['y'],d['w'],d['h'])
    platforms.append(platform)
goal=Goal(levels[0]['goal']['x'],levels[0]['goal']['y'])
player=Player(window_width,window_height)

while True:
    window.fill(BLACK)
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys=pygame.key.get_pressed()
    player.move(keys)
    player.update()
    player.draw(window)
    for platform in platforms:
        platform.draw(window)
    goal.draw(window)
    goal.update()

    pygame.display.update()
    clock.tick(40)