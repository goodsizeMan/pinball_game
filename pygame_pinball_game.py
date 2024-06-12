import pygame
import subprocess as sub
from gpiozero import MCP3008,Button

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
r_pot = MCP3008(2)
l_pot = MCP3008(0)
up_pot = MCP3008(1)

r_button = Button(26)
l_button = Button(14)
home_button = Button(16)

#Game Menu 路徑
game_menu_path = '/home/raspberry/root/usb/Game_Menu/pygame_game_menu.py'

#顏色設定
BLACK = (0,0,0)
WHITE = (255,255,255)

class Ball(pygame.sprite.Sprite):
     
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 240
        self.ball_vel_x,self.ball_vel_y = 3, 3

    def update(self):
        global isThrow
        if(isThrow):
            self.rect.x += self.ball_vel_x
            self.rect.y += self.ball_vel_y
        

        # ball第一次觸地
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.ball_vel_y *= -1
        
        #ball碰到底 重置

all_sprites = pygame.sprite.Group()
l_player = L_Player()
r_player = R_Player()
ball = Ball()
all_sprites.add(l_player,r_player,ball)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size,x,y):
    
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
         
#遊戲標題畫面
def draw_init():
    draw_text(screen,"PONG",64,400,100)  
    draw_text(screen,"Pressed any button to START",36,400,200)
    
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
        if home_button.is_pressed:
            sub.Popen(["python",game_menu_path])
            pygame.quit()
        if r_button.is_pressed:
            waiting = False
        if l_button.is_pressed:
            waiting = False



        
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

    ##按下Home鍵關閉遊戲回到MENU
    key_pressed = pygame.key.get_pressed() 
    if key_pressed[pygame.K_q]:
        sub.Popen(["python",game_menu_path])
        pygame.quit()

    if home_button.is_pressed:
        sub.Popen(["python",game_menu_path])
        pygame.quit()

    #更新遊戲
    all_sprites.update()

    #畫面更新
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.update()

#遊戲結束
pygame.quit()
       