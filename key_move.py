# 1 - インポート
import sys

import pygame
from pygame.locals import *

# 2 - ゲームの初期化
pygame.init()
WIDTH = 400
HEIGHT = 800
(p_x,p_y) = (200,400)
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# 2.1 player に関する設定
p_v = 3

# 2.2 player の laser に関する設定
p_lasers=[]
p_laser_v = 5
enemies = []

# 3 - 画像の読み込み
player = pygame.image.load("resources/images/player.png")
p_laser_surface = pygame.image.load("resources/images/p_laser.png")
enemy_surface = pygame.image.load("resources/images/enemy.png")

# 3.1 - 画像のサイズ
p_width = player.get_width()
p_height = player.get_height()
e_width = enemy_surface.get_width()
e_height = enemy_surface.get_height()

p_laser_width = p_laser_surface.get_width()
p_laser_height = p_laser_surface.get_height()

# 4 - ループの実行
while True:

    # 5 - 画面を一度消す
    screen.fill(0)

    # 6 - 画面に描画する
    screen.blit(player,(p_x,p_y))

    # 6.1 player の レーザーを描画
    for p_laser_i, p_laser in enumerate(p_lasers):
        p_laser[1] -= p_laser_v

        screen.blit(p_laser_surface,p_laser)

    # 7 - 画面を更新する
    pygame.display.flip()
    pygame.time.wait(20)

    # 8 - イベントを確認
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key ==  K_SPACE:
                p_lasers.append([p_x + p_width/2 - p_laser_width/2, p_y - p_laser_height])

    # 9 - player の動作
    pressed_key = pygame.key.get_pressed()
    if pressed_key[K_LEFT]:
        if p_x > 0:
            p_x -= p_v
    if pressed_key[K_RIGHT]:
        if p_x < WIDTH - p_width:
            p_x += p_v
    if pressed_key[K_UP]:
        if p_y > 0:
            p_y -= p_v
    if pressed_key[K_DOWN]:
        if p_y < HEIGHT - p_height:
            p_y += p_v






        # enough - 隠し要素
        if k>=1:
            screen.blit(kowa,(0,0))