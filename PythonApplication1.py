import pygame
import os
import random

from os import path
from pygame.locals import *

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BG = (17,166,41)
COLUMN = 3
ROW = 3

def random_mole_position():
    random_tanah = random.choice(tanah_list_rect)
    mole_rect.midtop = random_tanah.midbottom
    return random_tanah[1] - 70

def draw_tanah():
    x,y = 0,0
    for row in range(ROW):
        x = 0
        for column in range(COLUMN):
            display.blit(tanah,(x*200+140,y*200+100))
            pygame.draw.rect(display, WHITE, (x*200+140,y*200+150,100,100))
            rect =  pygame.Rect(x*200+140,y*200+120,100,50)
            #pygame.draw.rect(display, BLUE, (rect))
            tanah_list_rect.append(rect)
            x+=1
        y+=1

def draw_text(text,font_size,font_color,x,y):
    font = pygame.font.SysFont(None,font_size)
    font_surface = font.render(text,True,font_color)
    display.blit(font_surface,(x,y))

def draw_countdown():
    global countdown, last_countdown
    now = pygame.time.get_ticks()
    if now - last_countdown > 1000:
        last_countdown = now
        countdown -= 1
    draw_text(str(countdown),40,BLACK,600//2, 20)

pygame.init()
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pukul Tikus")
pygame.display.update()

pygame.mouse.set_visible(False)
mouse_pos = (0,0)
hitung_mundur = 3
last_update = pygame.time.get_ticks()
score = 0
pos = 0
countdown = 10
last_countdown = pygame.time.get_ticks()
game_over = False



palus = []
for i in range(1,3):
    img = pygame.image.load(path.join(img_folder, 'palu{}.png'.format(i))).convert_alpha()
    palus.append(img)
palu_img = palus[0]
palu_rect = palu_img.get_rect()
tanah = pygame.transform.scale(pygame.image.load('tanah.png'), (100,50))
tanah_list_rect = []
mole = pygame.transform.scale(pygame.image.load('mole.png'), (70,70))
mole_rect = mole.get_rect()

open = True
while open:
    for event in pygame.event.get():
        if event.type == QUIT:
            open = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                if mole_rect.collidepoint(mouse_pos):
                    score += 1
                    pos = random_mole_position()
                else:
                    pos = random_mole_position()
                    palu_img = palus[1]
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                palu_img = palus[0]

        if event.type == KEYUP:
            if event.key == K_r and game_over:
                score = 0
                pos = 0
                countdown = 10
                hitung_mundur = 3
                game_over = False

        mouse_pos = pygame.mouse.get_pos()
        palu_rect.center = (mouse_pos[0], mouse_pos[1])
        
    pygame.display.flip()

    now = pygame.time.get_ticks()
    if now - last_update > 1000 and hitung_mundur > 0:
        last_update = now
        hitung_mundur -= 1
        pos = random_mole_position()

    mole_rect.y -= 3
    if mole_rect.y <= pos:
        mole_rect.y = pos

    display.fill(WHITE)
    if hitung_mundur > 0:
        draw_text(str(hitung_mundur), 40, BLACK, 800//2, 20)
    else:
        display.blit(mole, mole_rect)
        if not game_over:
            draw_countdown()
            draw_text(f"Score: {score}", 35, BLACK, 10, 25)

    draw_tanah()

    if countdown < 0:
        game_over = True
        draw_text("Permainan Selesai", 40,BLACK,600//2-20,800//2 - 200)
        draw_text(f"Score Anda: {score}", 40,BLACK,600//2 - 20,800//2 - 40)
        draw_text("Tekan Tombol \"R\" Untuk Merestart", 40,BLACK,600//2 - 100,800//2+75)

    display.blit(palu_img, palu_rect)

pygame.quit()
quit()