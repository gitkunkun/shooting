# 1 - インポート
import random
import sys
import math

import pygame
from pygame import mixer
from pygame.locals import *

# 2 - ゲームの初期化
pygame.init()
mixer.init()
WIDTH = 400
HEIGHT = 700
(p_x, p_y) = (150, 500)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
k = 0
s = 0

# 2.1 player に関する設定
p_v = 20

# 2.2 player の laser に関する設定
p_lasers = []
p_laser_v = 50
a = 0
b=5

# 2.3 enemy に関する設定
e_v = 8
enemies = []
enemies_max_len = 100000
enemy_frequency = 100
enemy_timer = enemy_frequency

# 2.4 enemy の laser に関する設定
e_laser_v = 13
e_lasers = []
e_laser_frequency = 100
e_laser_timer = e_laser_frequency

# 2.5 castle に関する設定
castle_size = (64, 64)
positions = [(50, 600), (120, 600), (190, 600), (260, 600)]
castle_hp_init = b
castle_hp_list = [castle_hp_init] * 4
castles_rect = [pygame.Rect(positions[i], castle_size) for i in range(4)]

# 2.6 文字に関する設定
font_top = pygame.font.Font(None, 40)
font_hp = pygame.font.Font(None, 55)
font_clock = pygame.font.Font(None, 100)
font_counter = pygame.font.Font(None, 45)
font_score = pygame.font.Font(None, 50)

# 2.7 タイマーに関する設定
GAME_TIME = 30000
start_time = 0
timer_height = 70

# 2.8 画面遷移に関する設定
# 0 -> 「TOP」, 1 -> 「PLAY」, 2 -> 「SCORE」
scene = 0

# 3 - 画像の読み込み
player = pygame.image.load("resources/images/player.png")
castle = pygame.image.load("resources/images/sio.png")
p_laser_surface = pygame.image.load("resources/images/l1.png")
enemy_surface = pygame.image.load("resources/images/teki.png")
e_laser_surface = pygame.image.load("resources/images/kai.png")
teki_sinnda = pygame.image.load("resources/images/p1.tiff")
teki_sinnda2 = pygame.image.load("resources/images/p2.tiff")
p_speciallaser_surface = pygame.image.load("resources/images/l.png")
haikei = pygame.image.load("resources/images/haikei.jpeg")
haikei2 = pygame.image.load("resources/images/m.png")
haikei3 = pygame.image.load("resources/images/r.jpeg")
haikei4 = pygame.image.load("resources/images/images.jpeg")

# 3.1 - 画像のサイズ
p_width = player.get_width()
p_height = player.get_height()

p_laser_width = p_laser_surface.get_width()
p_laser_height = p_laser_surface.get_height()

e_width = enemy_surface.get_width()
e_height = enemy_surface.get_height()

e_laser_width = e_laser_surface.get_width()
e_laser_height = e_laser_surface.get_height()

# 3.2 - 各種カウンター
p_laser_counter = 0
p_hit_enemy_counter = 0
fight_time_counter = 0

# 3.3 - bgm の再生
mixer.music.load("./resources/bgm/mh1.mp3")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# 3.4 - スコアの計算
def calc_score(result, hit_rate, result_hp, fight_time_counter):

    score = 0
    score += result * 100
    score += hit_rate * 100
    score += result_hp * 10
    score += fight_time_counter * 5

    return math.floor(score)


# 4 - ループの実行
while True:

    # 5 - 画面を一度消す
    screen.fill(1)

    # 5 - 画面を一度消す
    screen.fill(1)

    # 5.1 - 「TOP」画面
    if scene == 0:
        screen.blit(haikei,(0,0))
        screen.blit(haikei2,(25,450))
        screen.blit(haikei3,(0,0))
        text = font_top.render("Select level 1~9", False, (200, 0, 0))
        screen.blit(text,(90, HEIGHT - 210))
        texts = font_top.render("UNIVERSE WARS", False, (255, 255, 0))
        screen.blit(texts,(85,40))
        texts1 = font_top.render("Finish [f]", False, (255, 255, 0))
        screen.blit(texts1,(10,650))
    # 5.2 - 「PLAY」画面
    if scene == 1:

        # 6 - 画面に描画する
        screen.blit(haikei4,(0,0))
        screen.blit(player, (p_x, p_y))

        # 6.1 player の レーザーを描画
        for p_laser_i, p_laser in enumerate(p_lasers):
            p_laser[1] -= p_laser_v
            if p_laser[1] < -p_laser_height:
                p_lasers.pop(p_laser_i)
                continue
            screen.blit(p_laser_surface, p_laser)


        # 6.2 敵描画
        enemy_timer -= ((a)//3)+4
        if enemy_timer <= 0 and len(enemies) < enemies_max_len:
            enemies.append(
                [random.randint(0, WIDTH - e_width), -e_height + timer_height]
            )
            enemy_timer = enemy_frequency

        for enemy_i, enemy in enumerate(enemies):
            enemy[1] += e_v
            if enemy[1] > HEIGHT:
                enemies.pop(enemy_i)
                k+=1
                continue
            screen.blit(enemy_surface, enemy)

            # 6.2.1 - e_lasers へ追加
            e_laser_timer -= (a//2)+1.5
            if e_laser_timer <= 0:
                e_lasers.append(
                    [
                        enemy[0] + e_width / 2 - e_laser_width / 2,
                        enemy[1] + e_laser_height,
                    ]
                )
                e_laser_timer = e_laser_frequency
                e_laser_sound = mixer.Sound("./resources/se/e_laser.mp3")
                e_laser_sound.set_volume(0.5)
                e_laser_sound.play()

            # 6.2.2 - player の攻撃によって敵を削除
            enemy_rect = pygame.Rect(enemy_surface.get_rect())
            enemy_rect.left, enemy_rect.top = enemy

            for p_laser_i, p_laser in enumerate(p_lasers):
                p_laser_rect = pygame.Rect(p_laser_surface.get_rect())
                p_laser_rect.left, p_laser_rect.top = p_laser
                if enemy_rect.colliderect(p_laser_rect):
                    screen.blit(teki_sinnda,enemy_rect)
                    enemies.pop(enemy_i)
                    p_lasers.pop(p_laser_i)
                    p_hit_enemy_counter += 1
                    p_laser_hit_sound = mixer.Sound("./resources/se/p_laser_hit.mp3")
                    p_laser_hit_sound.play()

        # 6.3 - 敵のレーザー描画
        for e_laser_i, e_laser in enumerate(e_lasers):
            e_laser[1] += e_laser_v
            if e_laser[1] > HEIGHT:
                e_lasers.pop(e_laser_i)
                continue
            screen.blit(e_laser_surface, e_laser)

            # 6.3.1 - 敵のレーザーと城の当たり判定
            e_laser_rect = pygame.Rect(e_laser_surface.get_rect())
            e_laser_rect.left, e_laser_rect.top = e_laser

            for castle_rect_i, castle_rect in enumerate(castles_rect):
                if castle_rect.colliderect(e_laser_rect):
                    if castle_hp_list[castle_rect_i] > 0 and len(e_lasers)>=e_laser_i+1:
                        e_lasers.pop(e_laser_i)
                        castle_hp_list[castle_rect_i] -= 1
                        e_laser_castle_hit_sounde = mixer.Sound(
                            "./resources/se/e_laser_castle_hit.mp3"
                        )
                        e_laser_castle_hit_sounde.set_volume(1)
                        e_laser_castle_hit_sounde.play()

        # 6.4 castle を描画
        for castle_i, castle_hp in enumerate(castle_hp_list):
            if castle_hp >= 1:
                screen.blit(castle, positions[castle_i])

            # 6.4.1 HP を表示
            hp = castle_hp_list[castle_i]
            hp_text = "*" * hp
            text = font_hp.render(hp_text, False, (255, 255, 255))
            hp_position = [
                positions[castle_i][0],
                positions[castle_i][1] + castle_size[1],
            ]
            screen.blit(text, hp_position)

        # 6.5 ゲームタイマーを表示
        pygame.draw.rect(screen, (40, 40, 40), Rect(0, 0, WIDTH, timer_height))
        now_time = pygame.time.get_ticks() - start_time
        fight_time_counter = now_time / 1000
        left_time = (GAME_TIME - now_time) // 1000 if (GAME_TIME - now_time) >= 0 else 0
        time_text = font_clock.render(str(left_time), False, (0, 0, 255))
        screen.blit(time_text, (0, 0))

        lasers_text = font_counter.render(
            "lasers : " + str(p_laser_counter), False, (255, 255, 255)
        )
        screen.blit(lasers_text, (100, 20))
        hit_text = font_counter.render(
            "hit : " + str(p_hit_enemy_counter), False, (255, 255, 255)
        )
        screen.blit(hit_text, (270, 20))

        # 6.6 - スコア画面への遷移
        if sum(castle_hp_list) <= 0 or left_time <= 0 or k>=1:
            p_hit_enemy_counter += 1
            kekka = mixer.Sound("./resources/se/jan.mp3")
            kekka.play()
            scene = 2
    # 5.3 - 「SCORE」画面
    if scene == 2:

        # 5.3.1 - 勝敗を表示
        result = 1 if sum(castle_hp_list) > 0 else 0
        if k>=1:
            result-=1
        else:
            result-=0
        result_char = "Win" if result else "Lose"
        result_text = font_score.render(result_char, False, (255, 255, 0))
        screen.blit(result_text, (20, 20))

        # 5.3.2 - 命中率を表示
        try:
            hit_rate = p_hit_enemy_counter / p_laser_counter
        except ZeroDivisionError:
            hit_rate = 0
            p_hit_enemy_counter -= 1
        hit_percent = "{:.0%}".format(p_hit_enemy_counter / p_laser_counter)
        hit_rate_text = font_score.render(
            "Hit Rate : " + hit_percent, False, (255, 255, 255)
        )
        screen.blit(hit_rate_text, (20, 100))

        # 5.3.3 - 城の残りの HP を表示
        result_hp = sum(castle_hp_list)
        result_hp_text = font_score.render(
            "Remaining HP : " + str(result_hp), False, (255, 255, 255)
        )
        screen.blit(result_hp_text, (20, 200))

        # 5.3.4 - プレイ時間を表示
        result_time_text = font_score.render(
            "Fight Time : " + str(fight_time_counter), False, (255, 255, 255)
        )
        screen.blit(result_time_text, (20, 300))

        # 5.3.5 - スコアを表示
        score = calc_score(result, hit_rate, result_hp, fight_time_counter)
        score_text = font_score.render("Score : " + str(score), False, (255, 217, 0))
        screen.blit(score_text, (20, 400))
        if s <= score:
            kakusi = font_score.render("Best score!!!",False,(255,255,0))
            screen.blit(kakusi,(20,450))
            s = score

            

        # 5.3.6 - ガイド文章を表示
        guid_text = font_score.render("Top [t], Replay [r]",False,(255,255,255))
        screen.blit(guid_text, (20, 600))
        uwa = mixer.Sound("./resources/se/uwa.mp3")
        uwa.play()
        


        # enough - 隠し要素


    # 7 - 画面を更新する
    pygame.display.flip()
    pygame.time.wait(20)

    # 8 - イベントを確認
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == K_1 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=1
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_2 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=2
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_3 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=3
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_4 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=4
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_5 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=5
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_6 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=6
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_7 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=7
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_8 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=8
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_9 and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=9
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()
            if event.key == K_h and scene == 0:
                start_time = pygame.time.get_ticks()
                a+=10
                scene = 1
                hajime = mixer.Sound("./resources/se/hajime.mp3")
                hajime.play()

            if event.key == K_RETURN and scene == 1:
                p_lasers.append(
                    [p_x + p_width / 2 - p_laser_width / 2, p_y - p_laser_height]
                )
                p_laser_counter += 1
                p_laser_sound = mixer.Sound("./resources/se/p_laser.mp3")
                p_laser_sound.play()

            if event.key == K_r and scene == 2:
                start_time = pygame.time.get_ticks()
                castle_hp_list = [castle_hp_init] * 4
                p_laser_counter = 0
                p_hit_enemy_counter = 1
                p_lasers = []
                enemies = []
                e_lasers = []
                p_x, p_y = (200, 400) 
                scene = 1
            if event.key == K_t and scene == 2:
                castle_hp_list = [castle_hp_init] * 4
                p_laser_counter = 0
                p_hit_enemy_counter = 0
                p_lasers = []
                enemies = []
                e_lasers = []
                p_x, p_y = (200, 400)
                score = 0
                scene = 0
                a = 0
            if event.key == K_f and scene == 2:
                pygame.quit()
                sys.exit(0)

    # 9 - player の動作
    pressed_key = pygame.key.get_pressed()
    if scene == 1:
        if pressed_key[K_a]:
            if p_x > 0:
                p_x -= p_v
        if pressed_key[K_d]:
            if p_x < WIDTH - p_width:
                p_x += p_v
        if pressed_key[K_w]:
            if p_y > timer_height:
                p_y -= p_v
        if pressed_key[K_s]:
            if p_y < HEIGHT - p_height:
                p_y += p_v
        if pressed_key[K_f]:
            pygame.quit()
            sys.exit(0)
    if pressed_key[K_f]:
        pygame.quit()
        sys.exit(0)