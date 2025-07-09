import sys
import pygame
from mahjong import Mahjong
from debug import printd

# ---------- 初期化 ----------
pygame.init()
SCREEN_W, SCREEN_H = 1024, 768
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Mahjong 1 Kyoku")
clock = pygame.time.Clock()

# ゲームロジック
Game = Mahjong()

# 自分（ローカル）のプレイヤー ID　※今回は 0 固定
MY_PID = 0

def click_to_cmd(pos, actions):
    """
    クリック座標 → Cmd へ変換するダミー関数
    実装例:
        1) 画面下部の手牌エリアを矩形で決め打ち
        2) 押された牌 index を計算
        3) actions から該当する 'kiru' を返す
    ここでは一番先頭の行動をそのまま返す簡易版
    """
    if not actions:
        return None
    return actions[0]      # ← とりあえず最優先で切らせる

def draw(game):
    """
    とりあえず盤情報をテキストで描画するスタブ。
    本格実装では牌画像を blit してください。
    """
    screen.fill((0, 96, 0))                      # 緑の卓
    font = pygame.font.SysFont(None, 24)

    y = 20
    for pid, player in enumerate(game.players):
        tx = f"P{pid} : {' '.join(player.menzen_li())}"
        txt = font.render(tx, True, (255, 255, 255))
        screen.blit(txt, (20, y))
        y += 30

    # 現在フェーズなど
    info_tx = f"turn={game.whoturn}  phase={game.phase.name}"
    info_surf = font.render(info_tx, True, (255, 255, 0))
    screen.blit(info_surf, (20, SCREEN_H - 40))



Game = Mahjong()

running = True
while running: # ここがtkinterでいうとこのmainloop()
    cmd = None

    # ① イベント取得
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            # いま誰の入力待ち？
            wait_p_id = Game.wait_p_id       # Mahjong から直接読む
            printd(f"WAITING {wait_p_id}")
            cmd = None
            
            if wait_p_id == MY_PID:
                actions = Game.get_capable_sousa(MY_PID)
                cmd = click_to_cmd(ev.pos, actions)

    # ② ロジックを 1 フレーム進める
    Game.step(cmd)         # None なら自動進行だけ

    # ③ 描画
    draw(Game)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
