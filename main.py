""""
今日のにゅめー

その０：デバッグ
その１：ちょっとしたコツ
teki_detekuru_kankaku
saigo_teki_detekara_keika_jikan
game_over
の位置について
その２：ファイヤーボールを修正(押しっぱなし問題の解決) ← これがむずいmemo.txtを見てみよう！
その３：リスタート
"""


import pygame
import os
import random

TATE = 900
YOKO = 1200
TITLE = "TAKOYAKI OISHI"
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "imgs")
PLAYER_DIR = os.path.join(IMG_DIR, "resized_ningen2025.png")
BOSS_DIR = os.path.join(IMG_DIR, "mabuta.png")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
# ゲーム上の物体をしまう箱
all_sprites = pygame.sprite.Group()
# てきをしまう箱
teki_hako = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
boss_fireballs = pygame.sprite.Group() 
bgm_path = os.path.join(SOUNDS_DIR, "bgm.mp3")

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((YOKO, TATE))
pygame.mixer.music.load(bgm_path)
pygame.mixer.music.play(-1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.gazou = pygame.image.load(PLAYER_DIR).convert()
        self.image.blit(self.gazou, (0,0),(0,0,32,32))
        iro = self.image.get_at((0,0))
        self.image.set_colorkey(iro)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.vx = 0
        self.vy = 0
        self.uteru = True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] == True:
            self.vx = 1
        elif keys[pygame.K_LEFT] == True:
            self.vx = -1
        elif keys[pygame.K_UP] == True:
            self.vy = -1
        elif keys[pygame.K_DOWN] == True:
            self.vy = 1
        else:
            self.vx = 0
            self.vy = 0
        self.rect.x += self.vx
        self.rect.y += self.vy
        # もしもスペースを押したらファイヤーボールを出す
        # ファイヤーボールを初期化して、それをall_spritesにしまう
        if keys[pygame.K_SPACE]:
            if self.uteru:
                fireball = Fireball(x=self.rect.x, y=self.rect.y)
                fireballs.add(fireball)
                all_sprites.add(fireball)
                self.uteru = False
        else:
            self.uteru = True




class Teki(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.gazou = pygame.image.load(PLAYER_DIR).convert()
        self.image.blit(self.gazou, (0, 0), (0, 0, 32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = random.randint(0, 30)
        self.vx = 1
        self.vy = 0

    def update(self):
        self.rect.x += self.vx


class Fireball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        size = (16,16)
        self.image = pygame.Surface(size)
        self.image.fill((255,0,0))
        self.vx = -1
        self.rect = self.image.get_rect(center=(x,y))

    def update(self):
        self.rect.x += self.vx


class BossFireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        size = (16, 16)
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 255))  # 適宜見やすい色
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 6  # 右に飛ぶ

    def update(self):
        self.rect.x += self.vx
        # 画面外に出たら削除
        if self.rect.left > YOKO or self.rect.right < 0:
            self.kill()

# ボスを作ろう
# ボスの画像はBOSS_DIR
# ボスのパラメーター：サイズ、速さ、ライフ、
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        size = (64,64)
        self.image = pygame.Surface(size)
        self.image.fill((255,0,0))
        self.vx = -1
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        self.life = 50
        self.vx = 3
        self.last_shot_time = 0
        self.shot_interval = 2.0

    def update(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_shot_time > self.shot_interval:
            bf = BossFireball(self.rect.centerx, self.rect.centery)
            boss_fireballs.add(bf)
            all_sprites.add(bf)
            self.last_shot_time = current_time
        if self.life <= 0:
            self.kill()
        self.rect.y += self.vx
        if self.rect.y >= TATE:
            self.vx *= -1
        elif self.rect.y <= 0:
            self.vx *= -1




player = Player()
boss = Boss()
all_sprites.add(boss)
all_sprites.add(player)
teki_detekuru_kankaku = 0
saigo_teki_detekara_keika_jikan = 0

game_over = False

kurikaeshi = True
while kurikaeshi:
    current_time = pygame.time.get_ticks() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kurikaeshi = False

    teki_detekuru_kankaku = 1.5
    if current_time - saigo_teki_detekara_keika_jikan > teki_detekuru_kankaku:
        teki = Teki()
        teki_hako.add(teki)
        saigo_teki_detekara_keika_jikan = current_time
    atari = pygame.sprite.spritecollide(player, teki_hako, dokill=True)
    if atari:
        game_over = True

    boss_fb_hit_player = pygame.sprite.spritecollide(player, boss_fireballs, dokill=True)
    if boss_fb_hit_player:
        game_over = True


    boss_fire_hit = pygame.sprite.spritecollide(boss, fireballs, dokill=True)
    if boss_fire_hit:
        boss.life -= len(boss_fire_hit)
        print("boss life:", boss.life)
        if boss.life <= 0:
            boss.kill()  # ボス消滅

    

    if game_over:
        font = pygame.font.SysFont(None, 74)
        text = font.render('IKEMEN TAKAHASHI', True, (255, 255, 255))
        text_rect = text.get_rect(center=(YOKO / 2, TATE / 2))
        screen.blit(text, text_rect)
        font_small = pygame.font.SysFont(None, 24)
        restart_text = font_small.render('Press Space to Restart', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(YOKO / 2, TATE / 2 + 70))
        screen.blit(restart_text, restart_rect)
        # その３：リスタートモード
        # リスタート判定
        # pygame.key.get_pressed()でボタンの状態チェック
        # もしもスペースが押されていたら敵の箱とキャラクターを入れる箱を空っぽにする(箱.empty())
        # プレイヤーを初期化する
        # プレイヤーを箱に追加する
        # ゲームオーバーのフラッグをFalseにする
    else:
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        teki_hako.update()
        teki_hako.draw(screen)
    pygame.display.flip()
pygame.quit()
