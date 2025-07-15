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


input_active = False        # クリックで欄をアクティブにする例
buffer       = ""           # 入力中の文字列
done_lines   = []           # Enter確定済みの行を溜める

input_rect = pygame.Rect(40, 150, 560, 40)   # 入力欄の位置・サイズ

# 牌画像を読み込む
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
shrink = 15
H_Y = 800/shrink # 描画する牌の横の長さ
H_X = 600/shrink # 描画する牌の縦の長さ
H_XY = H_Y-H_X
H_G = 10 # 描画する牌の隙間

FUCHI = (SCREEN_H-(C_Y+400)-H_Y)

for hai in hai_path:
    raw_image = pygame.image.load(hai_path[hai]).convert_alpha()
    image_dic[hai] = pygame.transform.scale(raw_image, (raw_image.get_width()/shrink, raw_image.get_height()/shrink))

# pygameで使ういろんな変数をここで定義する
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GRAY = (30, 30, 30)
RED   = (255,   0,   0)
YELLOW = (255, 255, 0)
TAKU = (0, 96, 0)
RIGHT = (0, 96*3/2, 0)

font = pygame.font.SysFont(None, 24)
cmd_font = pygame.font.SysFont(None, 30)


def draw_hai(hai, x, y, rotate=0, clm_mode = False): # 牌を描画する関数
    # XY軸をどの向きに設定するかで変換する
    theta = math.radians(rotate_all)
    x_converted = C_X + (x - C_X) * math.cos(theta) + (y - C_Y) * math.sin(theta)
    y_converted = C_Y - (x - C_X) * math.sin(theta) + (y - C_Y) * math.cos(theta)

    rotate += rotate_all
    
    anchor_by_rot = {
        0:   "topleft",
        90:  "bottomleft",
        180: "bottomright",
        270: "topright",
    }

    if hai != "back": # 牌裏牌でない限り背景を描画
        # 背景の描画
        front = image_dic["front"]
        front =  pygame.transform.rotate(front, rotate)
        rect = front.get_rect(**{anchor_by_rot[rotate_all]: (x_converted, y_converted)})
        screen.blit(front, rect)

    # 牌の描画
    img = image_dic[hai]
    img = pygame.transform.rotate(img, rotate)
    rect = img.get_rect(**{anchor_by_rot[rotate_all]: (x_converted, y_converted)})
    screen.blit(img, rect)
    if clm_mode:
        clickmap.append((rect, [MY_PID, "kiru", hai])) # クリックマップに登録 


def draw_players():
    global rotate_all
    

    for i in [0,1,2,3]:
        rotate_all = [0, 90, 180, 270][i]
        pid = (MY_PID+i)%4
        Player = Game.players[pid]
        clm_mode = True if i == 0 else False

        # 面前牌を描画
        x = FUCHI + H_X*2 + H_G
        for hai in ripai.ripai(Player.tehai["menzen"]):    
            draw_hai(hai, x, C_Y+400, clm_mode=clm_mode)
            x += H_X
            
        # ツモ牌を描画
        tumohai = Player.tehai["tumo"]
        if tumohai != None:
            draw_hai(tumohai, x+H_G, C_Y+400, clm_mode=clm_mode)
        
        x = SCREEN_H - (FUCHI + 1) # この１はピクセル調整

        # 鳴いた牌を描画
        for naki in Player.tehai["naki"]:
            if len(naki) == 4: # カンのとき
                hai = naki[0][0]
                
                if [n[1] for n in naki].count(pid) == 4: # 暗槓                  
                    draw_hai("back", x-H_X*1, C_Y+400)
                    draw_hai(hai, x-H_X*2, C_Y+400)
                    draw_hai(hai, x-H_X*3, C_Y+400)
                    draw_hai("back", x-H_X*4, C_Y+400)
                    x -= H_X*4 + H_G
                
                else:
                    if naki[3][1] != pid: # 大明槓
                        fromwho = naki[3][1]
                        if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                            draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90)
                            draw_hai(hai, x-H_Y-H_X*1, C_Y+400)
                            draw_hai(hai, x-H_Y-H_X*2, C_Y+400)
                            draw_hai(hai, x-H_Y-H_X*3, C_Y+400)
                        elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                            draw_hai(hai, x-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                            draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_Y-H_X-H_X, C_Y+400)
                        elif (fromwho-pid)%4 == 3: # 下家から鳴いていた場合
                            draw_hai(hai, x-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_X-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                        x -= H_Y + H_X*3 + H_G
                            
                    elif naki[3][1] != pid: # 加槓
                        fromwho = naki[2][1]
                        mod4 = (fromwho-pid)%4
                        if mod4 == 1: # 上家から鳴いていた場合
                            draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90)
                            draw_hai(hai, x-H_Y, C_Y+400+H_XY+H_X, rotate=90)
                            draw_hai(hai, x-H_Y-H_X, C_Y+400)
                            draw_hai(hai, x-H_Y-H_X-H_X, C_Y+400)
                        elif mod4 == 2: # 対面から鳴いていた場合
                            draw_hai(hai, x-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                            draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY+H_X, rotate=90)
                            draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400)
                        elif mod4 == 3: # 下家から鳴いていた場合
                            draw_hai(hai, x-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_X, C_Y+400)
                            draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                            draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY+H_X, rotate=90)
                        x -= H_Y + H_X*2 + H_G
            elif len(naki) == 3 and [n[0] for n in naki].count(naki[0][0]) == 3: # ポンのとき
                hai = naki[0][0]
                fromwho = naki[2][1]
                if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                    draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90)
                    draw_hai(hai, x-H_Y-H_X*1, C_Y+400)
                    draw_hai(hai, x-H_Y-H_X*2, C_Y+400)
                elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                    draw_hai(hai, x-H_X, C_Y+400)
                    draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                    draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400)
                elif (fromwho-pid)%4 == 3: # 下家から鳴いていた場合
                    draw_hai(hai, x-H_X, C_Y+400)
                    draw_hai(hai, x-H_X-H_X, C_Y+400)
                    draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                x -= H_Y + H_X*2 + H_G
            else: # チーのとき
                hai_1 = naki[0][0]
                hai_2 = naki[1][0]
                hai_3 = naki[2][0]
                fromwho = naki[2][1]
                if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                    draw_hai(hai_3, x-H_Y, C_Y+400+H_XY, rotate=90)
                    draw_hai(hai_2, x-H_Y-H_X*1, C_Y+400)
                    draw_hai(hai_1, x-H_Y-H_X*2, C_Y+400)
                elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                    draw_hai(hai_2, x-H_X, C_Y+400)
                    draw_hai(hai_3, x-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                    draw_hai(hai_1, x-H_X-H_Y-H_X, C_Y+400)
                elif (fromwho-pid)%4 == 3: # 下家から鳴いていた場合
                    draw_hai(hai_2, x-H_X, C_Y+400)
                    draw_hai(hai_1, x-H_X-H_X, C_Y+400)
                    draw_hai(hai_3, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90)
                x -= H_Y + H_X*2 + H_G

        # 河を描画




def click_to_cmd(pos):
    # クリックした座標からコマンドを返すイメージ
    for rect, cmd in clickmap:
        if rect.collidepoint(pos):
            return cmd
    return None

clickmap = []

def draw(Game: Mahjong):
    # ステージの描画
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_H, SCREEN_H)) # 卓の外側
    FUCHI_ = FUCHI-5
    pygame.draw.rect(screen, TAKU, (FUCHI_, FUCHI_, SCREEN_H-FUCHI_*2, SCREEN_H-FUCHI_*2)) # 緑の卓
    pygame.draw.rect(screen, RIGHT, (SCREEN_H, 0, 300, SCREEN_H)) # 右の操作画面
    pygame.draw.rect(screen, RIGHT, (C_X-150, C_Y-150, 300, 300)) # 真ん中のやつ
    

    # クリックマップを作製
    global clickmap
    clickmap = []
    
    # 牌を描画する
    draw_players()
    
    # デバッグ要素ゾ
    info_tx = f"whoturn={Game.whoturn}, queue={Game.queue},  phase={Game.phase.name}, capable_sousa_now={Game.capable_sousa_now}"
    info_surf = font.render(info_tx, True, YELLOW)
    screen.blit(info_surf, (20, 20))
    
    # 可能なコマンドを箇条書きで描画する
    y = 30
    if Game.queue != []:
        if Game.queue[0] == MY_PID: # 自分のときしか描画しないお！
            for i in Game.capable_sousa_now:

                rect = pygame.draw.rect(screen, WHITE, (SCREEN_H + 30, y+1, 300-30*2, 28))
                clickmap.append((rect, i)) # クリックマップに登録

                #csn_surf = cmd_font.render("  ".join(i[1:]), True, BLACK,)
                csn_surf = cmd_font.render(f"{i}", True, BLACK,)
                
                rect      = csn_surf.get_rect()   # ① まだ原点 (0,0)
                rect.center = (SCREEN_H + 150, y+15)
                screen.blit(csn_surf, rect)
                y += 30


def loop_runner(loop):
    asyncio.set_event_loop(loop)  # このスレッドで `asyncio.get_event_loop()` が使える
    loop.run_forever()            # coroutine が投げ込まれるまで待ち続ける


ai_q: queue.Queue = queue.Queue()

loop = asyncio.new_event_loop()

threading.Thread(target=loop_runner, args=(loop,), daemon=True).start()

async def start_ai():
    # 1) 疑似思考ウェイト
    what_ai_can_do = Game.capable_sousa_now
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
        elif ev.type == AI_DONE:      # ← コルーチン完了通知
            cmd = ai_q.get()
            waiting_ai = False 
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: # マウスのクリックを取得する
            cmd = click_to_cmd(ev.pos)
            print(cmd)

    # AIを起こす
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
    clock.tick(30)

pygame.quit()
sys.exit()
