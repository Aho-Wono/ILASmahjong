import sys
import pygame
from mahjong import Mahjong
from debug import printd

Game = Mahjong()

running = True
while running:
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
            #if wait_p_id == MY_PID:
                #actions = Game.kyoku.get_capable_sousa(MY_PID)
                #cmd = click_to_cmd(ev.pos, actions)

    # ② ロジックを 1 フレーム進める
    Game.step(cmd)         # None なら自動進行だけ

    # ③ 描画
    #draw(Game)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

