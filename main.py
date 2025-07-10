import sys
import pygame
from mahjong import Mahjong
from debug import printd
import random
import asyncio
import threading
import queue

# ---------- pygame 初期化 ----------
pygame.init()
SCREEN_W, SCREEN_H = 1024, 768
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Mahjong 1 Kyoku")
clock = pygame.time.Clock()

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
    return random.choice(actions) # とりまRandomで返すべ…

def draw(game):
    """
    とりあえず盤情報をテキストで描画するスタブ。
    本格実装では牌画像を blit してください。
    """
    screen.fill((0, 96, 0))                      # 緑の卓
    font = pygame.font.SysFont(None, 24)

    y = 20
    for Player in game.players:
        tx = Player.dbg()
        txt = font.render(tx, True, (255, 255, 255))
        screen.blit(txt, (20, y))
        y += 30

    # 現在フェーズなど
    info_tx = f"turn={game.whoturn},  phase={game.phase.name}, queue={game.queue}"
    info_surf = font.render(info_tx, True, (255, 255, 0))
    screen.blit(info_surf, (20, SCREEN_H - 40))


def loop_runner(loop):
    asyncio.set_event_loop(loop)  # このスレッドで `asyncio.get_event_loop()` が使える
    loop.run_forever()            # coroutine が投げ込まれるまで待ち続ける


ai_q: queue.Queue = queue.Queue()

loop = asyncio.new_event_loop()

threading.Thread(target=loop_runner, args=(loop,), daemon=True).start()

async def start_ai():
    # 1) 疑似思考ウェイト
    what_ai_can_do = Game.get_capable_sousa_now()
    printd("AI can do", what_ai_can_do)
    printd("START AI THINKING")
    await asyncio.sleep(0.5) # とりま待たせる
    AI_cmd = random.choice(what_ai_can_do)
    printd("FINISH AI THINKING")

    ai_q.put(AI_cmd)

    pygame.event.post(pygame.event.Event(AI_DONE))

def launch_ai():
    asyncio.run_coroutine_threadsafe(start_ai(), loop)


AI_DONE = pygame.USEREVENT + 1 
clock = pygame.time.Clock()

Game = Mahjong()
MY_PID = 0
AI_PIDS = [1,2,3]

waiting_ai = False

running = True
while running: # ここがtkinterでいうとこのmainloop()
    cmd = None

    # ① イベント取得
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if Game.queue[0] == MY_PID:
                printd("FINISH HUMAN THINKING")
                actions = Game.get_capable_sousa_now()
                # printd("actions:", actions)
                cmd  = click_to_cmd(ev.pos, actions)
        elif ev.type == AI_DONE:      # ← コルーチン完了通知
            cmd = ai_q.get()
            waiting_ai = False 

    # AIを起こす
    printd(waiting_ai)
    if (not waiting_ai) and Game.queue[0] in AI_PIDS: # AIが起きてなくかつAIのターンであるとき
        printd("LAUNCH AI")
        waiting_ai = True
        launch_ai()
            
    # ② ロジックを 1 フレーム進める
    Game.step(cmd)         # None なら自動進行だけ

    # ③ 描画
    draw(Game)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
