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
import math

dir = getdir.dir()


# ---------- pygame 初期化 ----------
pygame.init()
SCREEN_W, SCREEN_H = 950+300, 950
C_X, C_Y = SCREEN_H/2, SCREEN_H/2
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



def draw_hai(hai, x, y, rotate=0, rotate_all=0): # 牌を描画する関数
    # XY軸をどの向きに設定するかで変換する
    theta = math.radians(rotate_all)
    x = x*math.cos(theta) - y*math.sin(theta)
    y = x*math.sin(theta) + y*math.cos(theta)
    rotate += rotate_all
    
    
    # 背景の描画
    front = image_dic["front"]
    front =  pygame.transform.rotate(front, rotate) 
    rect = front.get_rect(topleft=(x, y))
    screen.blit(front, rect)

    # 牌の描画
    img = image_dic[hai]
    img = pygame.transform.rotate(img, rotate)
    rect = img.get_rect(topleft=(x, y))
    screen.blit(img, rect) 


def draw_players(Player):
    # 面前牌を描画
    x = C_X-400-50
    pid = Player.playerid
    for hai in ripai.ripai(Player.tehai["menzen"]):    
        x += 50
        draw_hai(hai, x, C_Y+400)
        
    # ツモ牌を描画
    tumohai = Player.tehai["tumo"]
    if tumohai != None:
        draw_hai(hai, x-50+110, C_Y+400)
    x = C_X+450

    # 鳴いた牌を描画
    for naki_li in Player.tehai["naki"]:
        for naki in naki_li:
            if len(naki) == 4: # カンのとき
                printd("カンを描画")
                hai = naki[0][0]
                
                if [n[1] for n in naki].count(pid) == 4: # 暗槓                  
                    draw_hai("back", x-50*1, C_Y+400)
                    draw_hai(hai, x-50*2, C_Y+400)
                    draw_hai(hai, x-50*3, C_Y+400)
                    draw_hai("back", x-50*4, C_Y+400)
                    x -= 210
                
                else:
                    if naki[3][1] != pid: # 大明槓
                        fromwho = naki[3][1]
                        if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                            draw_hai(hai, x-67, C_Y+400-17)
                            draw_hai(hai, x-67-50*1, C_Y+400)
                            draw_hai(hai, x-67-50*2, C_Y+400)
                            draw_hai(hai, x-67-50*3, C_Y+400)
                        elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                            draw_hai(hai, x-50, C_Y+400-17)
                            draw_hai(hai, x-50-67, C_Y+400)
                            draw_hai(hai, x-50-67-50, C_Y+400)
                            draw_hai(hai, x-50-67-50-50, C_Y+400)
                        elif (fromwho-pid)%4 == 2: # 下家から鳴いていた場合
                            draw_hai(hai, x-50, C_Y+400-17)
                            draw_hai(hai, x-50-50, C_Y+400)
                            draw_hai(hai, x-50-50-50, C_Y+400)
                            draw_hai(hai, x-50-50-50-67, C_Y+400)
                        x -= 227
                    elif naki[3][1] != pid: # 加槓
                        fromwho = naki[2][1]
                        mod4 = (fromwho-pid)%4
                        if mod4 == 1: # 上家から鳴いていた場合
                            draw_hai(hai, x-67, C_Y+400-17)
                            draw_hai(hai, x-67, C_Y+400-17+50)
                            draw_hai(hai, x-67-50, C_Y+400)
                            draw_hai(hai, x-67-50-50, C_Y+400)
                        elif mod4 == 2: # 対面から鳴いていた場合
                            draw_hai(hai, x-50, C_Y+400)
                            draw_hai(hai, x-50-67, C_Y+400-17)
                            draw_hai(hai, x-50-67, C_Y+400-17+50)
                            draw_hai(hai, x-50-67-50, C_Y+400)
                        elif mod4 == 3: # 下家から鳴いていた場合
                            draw_hai(hai, x-50, C_Y+400)
                            draw_hai(hai, x-50-50, C_Y+400)
                            draw_hai(hai, x-50-50-67, C_Y+400-17)
                            draw_hai(hai, x-50-50-67, C_Y+400-17+50)
                        x -= 177



def draw(game):
    screen.fill((0, 96, 0))                      # 緑の卓
    font = pygame.font.SysFont(None, 24)
    
    # 描画していく

    # 自分の手牌を描画
    ME = game.players[MY_PID]
    draw_players(ME)
                
            
            
    # デバッグ要素（？）

    # デバッグ要素ゾ
    info_tx = f"turn={game.whoturn},  phase={game.phase.name}, queue={game.queue}"
    info_surf = font.render(info_tx, True, (255, 255, 0))
    screen.blit(info_surf, (20, SCREEN_H - 40))
    
    csl = f"{game.get_capable_sousa_now()}"
    csl_surf = font.render(csl, True, (255,255,0))
    screen.blit(csl_surf, (1000, 50))

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
