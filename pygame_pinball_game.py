import pygame
import subprocess as sub
import time
import random
#from gpiozero import MCP3008,Button

#初始化pygame

pygame.init()

#設定視窗大小
FPS = 60
WIDTH = 800
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PONG")
clock = pygame.time.Clock()

#GPIO 設定
#r_pot = MCP3008(2)
#l_pot = MCP3008(0)
#up_pot = MCP3008(1)

key_pressed = pygame.key.get_pressed()
r_button = key_pressed[pygame.K_d]
l_button = key_pressed[pygame.K_a]
home_button = key_pressed[pygame.K_q]

# Game Menu 路徑
game_menu_path = '/home/raspberry/root/usb/Game_Menu/pygame_game_menu.py'

# 顏色設定
BLACK = (0,0,0)
WHITE = (255,255,255)

# BALL 設定
isThrow = False
isTurn = False

MAX_BALL_SPEED = 20
GRAVITY = 0.1
speed = 0
current_speed = 0

# 分數設定
POINT = 0
is_get_point = False

class Ball(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 30
        self.ball_vel_x,self.ball_vel_y = 0, 0

    def update(self):
        global isThrow,is_get_point,isTurn,current_speed

        key_pressed = pygame.key.get_pressed()

        if(isThrow):
            #self.rect.x += self.ball_vel_x
            self.rect.y += self.ball_vel_y
            self.rect.x -= current_speed
            current_speed -= GRAVITY

        if pygame.sprite.collide_rect(self,paddle_hit):
            random_y = random.randint(-10,-3)
            self.ball_vel_y = random_y      
            self.rect.x = self.rect.right
            current_speed *= -1
            self.ball_vel_y *= -1
        
        if pygame.sprite.collide_rect(self,paddle_hit_01):
            self.ball_vel_y -= 1
            self.rect.x = self.rect.left
            current_speed *= -1
            self.ball_vel_y *= -1

        if pygame.sprite.collide_rect(self,paddle_hit_02):
            self.ball_vel_y -= 1
            self.rect.x = self.rect.left
            current_speed *= -1
            self.ball_vel_y *= -1


        # ball第一次觸地
        #if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            #self.ball_vel_y *= -1
        
        #ball碰到底 重置
        if self.rect.right >= WIDTH:
            self.rect.x = 650
            self.rect.y = 30
            current_speed = 30
            self.ball_vel_y = 0
            isTurn = False
            isThrow = False
            is_get_point = False

class Paddle(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,480))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 0

class Paddle_Hit(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,480))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 0

class Paddle_Hit_01(pygame.sprite.Sprite ):
    ## 希望可以簡化，只用一個paddle_hit_01，可以更換座標
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 100

class Paddle_Hit_02(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 300
       
class PointArea_10(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 100

    def update(self):
        global POINT,is_get_point
        if pygame.sprite.collide_rect(self,ball) and is_get_point==False:
            POINT += 10
            is_get_point = True
            
class PointArea_20(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 200  

    def update(self):
        global POINT,is_get_point
        if pygame.sprite.collide_rect(self,ball) and is_get_point==False:
            POINT += 20
            is_get_point = True 

class PointArea_30(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 300 

    def update(self):
        global POINT,is_get_point
        if pygame.sprite.collide_rect(self,ball) and is_get_point==False:
            POINT += 30
            is_get_point = True

class PointArea_40(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 400 

    def update(self):
        global POINT,is_get_point
        if pygame.sprite.collide_rect(self,ball) and is_get_point==False:
            POINT += 40
            is_get_point = True

all_sprites = pygame.sprite.Group()

ball = Ball()
paddle = Paddle()
paddle_hit = Paddle_Hit()
paddle_hit_01 = Paddle_Hit_01()
paddle_hit_02 = Paddle_Hit_02()

point_area_10 = PointArea_10()
point_area_20 = PointArea_20()
point_area_30 = PointArea_30()
point_area_40 = PointArea_40()

all_sprites.add(ball,paddle,paddle_hit,paddle_hit_01,paddle_hit_02,point_area_10,point_area_20,point_area_30,point_area_40)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size,x,y,angle=0):
    
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True,WHITE)
    text_rect = text_surface.get_rect()
    rotated_surface = pygame.transform.rotate(text_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(x, y))
    surf.blit(rotated_surface, rotated_rect.topleft)
         
#遊戲標題畫面
def draw_init():
    draw_text(screen,"Pinball",64,300,240,90)  
    draw_text(screen,"Pressed any button to start",36,500,240,90)
    
    pygame.display.update()  
    waiting = True

    while waiting:
        clock.tick(FPS)
    #取得輸入
        for event in pygame.event.get(): 
            
            if event.type == pygame.QUIT:
                pygame.quit()

        key_pressed = pygame.key.get_pressed() 
        if key_pressed[pygame.K_q]:
            sub.Popen(["python",game_menu_path])
            pygame.quit()
        if key_pressed[pygame.K_j]:
            waiting = False

        #如果按Home鍵返回Menu 按r、l_button則開始遊戲
        if home_button:
            sub.Popen(["python",game_menu_path])
            pygame.quit()
        if r_button:
            waiting = False
        if l_button:
            waiting = False


press_time = 0
hold_time = 0
current_speed = speed
       
running = True
show_init = True

while running:
    #判斷先進入遊戲標題
    if(show_init):
        draw_init()
        show_init = False

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                press_time = time.time()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                hold_time = time.time() - press_time
                speed = min(MAX_BALL_SPEED,max(2,int(hold_time*10)))
                current_speed = speed
                isThrow = True
                




    ##按下Home鍵關閉遊戲回到MENU
    key_pressed = pygame.key.get_pressed() 
    if key_pressed[pygame.K_q]:
        sub.Popen(["python",game_menu_path])
        pygame.quit()

    if home_button:
        sub.Popen(["python",game_menu_path])
        pygame.quit()

    #更新遊戲
    
    
    if(current_speed >= 0):
        current_speed -= GRAVITY

    all_sprites.update()

    

    #畫面更新
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen,str(hold_time),12,30,30,90)
    draw_text(screen,str(POINT),36,60,30,90)
    pygame.display.update()

#遊戲結束
pygame.quit()
       