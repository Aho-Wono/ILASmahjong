import sys
import pygame
from mahjong import Mahjong
from debug import printd
import random
import asyncio
import threading
import queue
import getdir
import ripai

dir = getdir.dir()


# ---------- pygame 初期化 ----------
pygame.init()
SCREEN_W, SCREEN_H = 950, 950
C_X, C_Y = SCREEN_W/2, SCREEN_W/2
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

# ゲームコード → ファイル名 のマッピング
hai_dir = f"{dir}/assets/hai/edited"
hai_path = {
    **{f"m{i}": f"{hai_dir}/m{i}.png"  for i in range(1, 10)},
    **{f"p{i}": f"{hai_dir}/p{i}.png"  for i in range(1, 10)},
    **{f"s{i}": f"{hai_dir}/s{i}.png"  for i in range(1, 10)},
    "ton":  f"{hai_dir}/ton.png",
    "nan":  f"{hai_dir}/nan.png",
    "sha":  f"{hai_dir}/sha.png",
    "pei":  f"{hai_dir}/pei.png",
    "haku": f"{hai_dir}/haku.png",
    "hatu": f"{hai_dir}/hatsu.png",
    "chun": f"{hai_dir}/chun.png",
    "back": f"{hai_dir}/Back.png",
    "front": f"{hai_dir}/Front.png",
}

image_dic = {}
shrink = 12
for hai in hai_path:
    raw_image = pygame.image.load(hai_path[hai]).convert_alpha()
    image_dic[hai] = pygame.transform.scale(raw_image, (raw_image.get_width()/shrink, raw_image.get_height()/shrink))



def draw_hai(hai, x, y): # 牌を描画する関数
    front = image_dic["front"]
    rect = front.get_rect(topleft=(x, y))
    screen.blit(front, rect)

    img = image_dic[hai]
    rect = img.get_rect(topleft=(x, y))
    screen.blit(img, rect) 

def draw(game):
    screen.fill((0, 96, 0))                      # 緑の卓
    font = pygame.font.SysFont(None, 24)
    
    # 描画していく

    # 自分の手牌を描画
    # 面前牌を描画
    x = C_X-400
    for hai in ripai.ripai(game.players[MY_PID].tehai["menzen"]):    
        x += 50
        draw_hai(hai, x, C_Y+450-50)
    
    



    # デバッグ要素ゾ
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
    # printd(waiting_ai)
    if Game.queue != []:
        if (not waiting_ai) and Game.queue[0] in AI_PIDS and cmd == None: # AIが起きてなくかつAIのターンでかつcmdがNone=AIがまだ触ってないとき
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
