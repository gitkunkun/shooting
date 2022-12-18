# 1 - インポート
import random
import sys

import pygame
from pygame.locals import *

# 2 - ゲームの初期化
pygame.init()
WIDTH = 400
HEIGHT = 800
(p_x, p_y) = (200, 400)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 2.1 player に関する設定
p_v = 3

# 2.2 player の laser に関する設定
p_lasers = []
p_laser_v = 5

# 2.3 enemy に関する設定
e_v = 1
enemies = []
enemies_max_len = 100
enemy_frequency = 100
enemy_timer = enemy_frequency

# 2.4 enemy の laser に関する設定
e_laser_v = 2
e_lasers = []
e_laser_frequency = 100
e_laser_timer = e_laser_frequency

# 2.5 castle に関する設定
castle_size = (64, 64)
positions = [(0, 700), (100, 700), (200, 700), (300, 700)]
castle_hp_init = 5
castle_hp_list = [castle_hp_init] * 4
castles_rect = [pygame.Rect(positions[i], castle_size) for i in range(4)]

# 2.6 文字に関する設定
font_hp = pygame.font.Font(None, 55)

# 3 - 画像の読み込み
player = pygame.image.load("resources/images/player.png")
castle = pygame.image.load("resources/images/sio.jpeg")
p_laser_surface = pygame.image.load("resources/images/rere.jpeg")
enemy_surface = pygame.image.load("resources/images/teki.png")
e_laser_surface = pygame.image.load("resources/images/kai.png")

# 3.1 - 画像のサイズ
p_width = player.get_width()
p_height = player.get_height()

p_laser_width = p_laser_surface.get_width()
p_laser_height = p_laser_surface.get_height()

e_width = enemy_surface.get_width()
e_height = enemy_surface.get_height()

e_laser_width = e_laser_surface.get_width()
e_laser_height = e_laser_surface.get_height()

# 4 - ループの実行
while True:

    # 5 - 画面を一度消す
    screen.fill(0)

    # 6 - 画面に描画する
    screen.blit(player, (p_x, p_y))

    # 6.1 player の レーザーを描画
    for p_laser_i, p_laser in enumerate(p_lasers):
        p_laser[1] -= p_laser_v
        if p_laser[1] < -p_laser_height:
            p_lasers.pop(p_laser_i)

        screen.blit(p_laser_surface, p_laser)

    # 6.2 敵描画
    enemy_timer -= 10
    if enemy_timer <= 0 and len(enemies) < enemies_max_len:
        enemies.append([random.randint(0, WIDTH - e_width), -e_height])
        enemy_timer = enemy_frequency

    for enemy_i, enemy in enumerate(enemies):
        enemy[1] += e_v
        if enemy[1] > HEIGHT:
            enemies.pop(enemy_i)
        screen.blit(enemy_surface, enemy)

        # 6.2.1 - e_lasers へ追加
        e_laser_timer -= 5
        if e_laser_timer <= 0:
            e_lasers.append(
                [enemy[0] + e_width / 2 - e_laser_width / 2, enemy[1] + e_laser_height]
            )
            e_laser_timer = e_laser_frequency

        # 6.2.2 - player の攻撃によって敵を削除
        enemy_rect = pygame.Rect(enemy_surface.get_rect())
        enemy_rect.left, enemy_rect.top = enemy

        for p_laser_i, p_laser in enumerate(p_lasers):
            p_raser_rect = pygame.Rect(p_laser_surface.get_rect())
            p_raser_rect.left, p_raser_rect.top = p_laser
            if enemy_rect.colliderect(p_raser_rect):
                enemies.pop(enemy_i)
                p_lasers.pop(p_laser_i)

    # 6.3 - 敵のレーザー描画
    for e_laser_i, e_laser in enumerate(e_lasers):
        e_laser[1] += e_laser_v
        if e_laser[1] > HEIGHT:
            e_lasers.pop(e_laser_i)
        screen.blit(e_laser_surface, e_laser)

        # 6.3.1 - 敵のレーザーと城の当たり判定
        e_laser_rect = pygame.Rect(e_laser_surface.get_rect())
        e_laser_rect.left, e_laser_rect.top = e_laser

        for castle_rect_i, castle_rect in enumerate(castles_rect):
            if castle_rect.colliderect(e_laser_rect):
                e_lasers.pop(e_laser_i)
                if castle_hp_list[castle_rect_i] > 0:
                    castle_hp_list[castle_rect_i] -= 1

    # 6.4 castle を描画
    for castle_i, castle_hp in enumerate(castle_hp_list):
        if castle_hp >= 1:
            screen.blit(castle, positions[castle_i])

        # 6.4.1 HP を表示
        hp = castle_hp_list[castle_i]
        hp_text = "*" * hp
        text = font_hp.render(hp_text, False, (255, 255, 255))
        hp_position = [positions[castle_i][0], positions[castle_i][1] + castle_size[1]]
        screen.blit(text, hp_position)

    # 7 - 画面を更新する
    pygame.display.flip()
    pygame.time.wait(20)

    # 8 - イベントを確認
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                p_lasers.append(
                    [p_x + p_width / 2 - p_laser_width / 2, p_y - p_laser_height]
                )

    # 9 - player の動作
    pressed_key = pygame.key.get_pressed()
    if pressed_key[K_a]:
        if p_x > 0:
            p_x -= p_v
    if pressed_key[K_d]:
        if p_x < WIDTH - p_width:
            p_x += p_v
    if pressed_key[K_w]:
        if p_y > 0:
            p_y -= p_v
    if pressed_key[K_s]:
        if p_y < HEIGHT - p_height:
            p_y += p_v