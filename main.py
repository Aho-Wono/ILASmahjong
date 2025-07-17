import sys
import pygame
from mahjong import Mahjong, Phase
from debug import printd
import random
import asyncio
import threading
import queue
import getdir
import ripai
import math


DIR = getdir.dir()


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
hai_dir = f"{DIR}/assets/hai/edited"
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
SHRINK = 15
H_Y = 800/SHRINK # 描画する牌の横の長さ
H_X = 600/SHRINK # 描画する牌の縦の長さ
H_XY = H_Y-H_X
H_G = 10 # 描画する牌の隙間

FUCHI = (SCREEN_H-(C_Y+400)-H_Y)

def shrink(img, num):
    return pygame.transform.scale(img, (img.get_width()/num, img.get_height()/num))


# 各画像の読み込み
for hai in hai_path:
    raw_image = pygame.image.load(hai_path[hai]).convert_alpha()
    image_dic[hai] = shrink(raw_image, SHRINK)
image_dic["richibo"] = shrink(pygame.image.load(f"{DIR}/assets/richibo.png").convert_alpha(), 10)

class COLOR():
    WHITE = (255, 255, 255)
    BLACK = (  0,   0,   0)
    GRAY = (30, 30, 30)
    RED   = (255,   0,   0)
    YELLOW = (255, 255, 0)
    TAKU = (0, 96, 0)
    RIGHT = (0, 96*3/2, 0)

# pygameで使ういろんな変数をここで定義する
font = pygame.font.SysFont(None, 24)
cmd_font = pygame.font.SysFont(None, 30)

clickmap = []

def draw_node(img, x, y, rotate_all = 0, clm_cmd = None, anchor = "center"):
    # XY軸をどの向きに設定するかで変換する
    theta = math.radians(rotate_all)
    x_converted = C_X + (x - C_X) * math.cos(theta) + (y - C_Y) * math.sin(theta)
    y_converted = C_Y - (x - C_X) * math.sin(theta) + (y - C_Y) * math.cos(theta)

    img = pygame.transform.rotate(img, rotate_all)        
    rect = img.get_rect()
    rect.center = (x_converted, y_converted)
    screen.blit(img, rect)

    # クリックマップへの登録
    if clm_cmd != None:
        clickmap.append(rect, clm_cmd)


def draw_hai(hai, x, y, rotate=0, clm_mode = False, iftrans = False, rotate_all = 0): # 牌を描画する関数 
    
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

        # 背景の描画
    front = image_dic["front"]
    front =  pygame.transform.rotate(front, rotate)
    if iftrans: front.set_alpha(128)        
    rect = front.get_rect(**{anchor_by_rot[rotate_all]: (x_converted, y_converted)})
    if clm_mode and rect.collidepoint(POS):
        rect.y -= 10   
    screen.blit(front, rect)

    # 牌の描画
    img = image_dic[hai]
    img = pygame.transform.rotate(img, rotate)
    if iftrans: img.set_alpha(128)
    rect = img.get_rect(**{anchor_by_rot[rotate_all]: (x_converted, y_converted)})
    if clm_mode and rect.collidepoint(POS):
        rect.y -= 10   
    screen.blit(img, rect)
    if clm_mode:
        clickmap.append((rect, [MY_PID, "kiru", hai])) # クリックマップに登録 

def draw_player(pid):    
    rotate_all = [0, 90, 180, 270][(pid-MY_PID)%4]
    
    Player = Game.players[pid]
    if pid == MY_PID and Game.whoturn == MY_PID:
        if Player.ifrichi():
            clm_mode_menzen = False
        else:
            clm_mode_menzen = True
        clm_mode_tumo = True
    else:
        clm_mode_menzen = False
        clm_mode_tumo = False



    # 面前牌を描画
    x = FUCHI + H_X*2 + H_G
    for hai in ripai.ripai(Player.tehai["menzen"]):    
        draw_hai(hai, x, C_Y+400, clm_mode=clm_mode_menzen, rotate_all=rotate_all)
        x += H_X
        
    # ツモ牌を描画
    tumohai = Player.tehai["tumo"]
    if tumohai != None:
        draw_hai(tumohai, x+H_G, C_Y+400, clm_mode=clm_mode_tumo, rotate_all=rotate_all)
    
    x = SCREEN_H - (FUCHI + 1) # この１はピクセル調整

    # 鳴いた牌を描画
    for naki in Player.tehai["naki"]:
        if len(naki) == 4: # カンのとき
            hai = naki[0][0]
            
            if [n[1] for n in naki].count(pid) == 4: # 暗槓                  
                draw_hai("back", x-H_X*1, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai, x-H_X*2, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai, x-H_X*3, C_Y+400, rotate_all=rotate_all)
                draw_hai("back", x-H_X*4, C_Y+400, rotate_all=rotate_all)
                x -= H_X*4 + H_G
            
            else:
                if naki[3][1] != pid: # 大明槓
                    fromwho = naki[3][1]
                    if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                        draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X*1, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X*2, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X*3, C_Y+400, rotate_all=rotate_all)
                    elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                        draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                    elif (fromwho-pid)%4 == 3: # 下家から鳴いていた場合
                        draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                    x -= H_Y + H_X*3 + H_G
                        
                elif naki[3][1] != pid: # 加槓
                    fromwho = naki[2][1]
                    mod4 = (fromwho-pid)%4
                    if mod4 == 1: # 上家から鳴いていた場合
                        draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y, C_Y+400+H_XY+H_X, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                    elif mod4 == 2: # 対面から鳴いていた場合
                        draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY+H_X, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
                    elif mod4 == 3: # 下家から鳴いていた場合
                        draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY+H_X, rotate=90, rotate_all=rotate_all)
                    x -= H_Y + H_X*2 + H_G
        elif len(naki) == 3 and [n[0] for n in naki].count(naki[0][0]) == 3: # ポンのとき
            hai = naki[0][0]
            fromwho = naki[2][1]
            if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                draw_hai(hai, x-H_Y-H_X*1, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai, x-H_Y-H_X*2, C_Y+400, rotate_all=rotate_all)
            elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
            elif (fromwho-pid)%4 == 3: # 下家から鳴いていた場合
                draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai, x-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
            x -= H_Y + H_X*2 + H_G
        else: # チーのとき
            hai_1 = naki[0][0]
            hai_2 = naki[1][0]
            hai_3 = naki[2][0]
            fromwho = naki[2][1]
            if (fromwho-pid)%4 == 1: # 上家から鳴いていた場合
                draw_hai(hai_3, x-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                draw_hai(hai_2, x-H_Y-H_X*1, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai_1, x-H_Y-H_X*2, C_Y+400, rotate_all=rotate_all)
            elif (fromwho-pid)%4 == 2: # 対面から鳴いていた場合
                draw_hai(hai_2, x-H_X, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai_3, x-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                draw_hai(hai_1, x-H_X-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
            elif (fromwho-pid)%4 == 3: # 下家から鳴いていた場合
                draw_hai(hai_2, x-H_X, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai_1, x-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                draw_hai(hai_3, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
            x -= H_Y + H_X*2 + H_G

    # 河を描画
    x, y = C_X-H_X*3, C_Y + (H_X*6+H_G)/2
    k_count = 0
    for k in Player.kawa:
        k_count += 1

        if k[1]: # 立直牌の場合
            draw_hai(k[0], x, y+(H_Y-H_X), iftrans=k[2], rotate=90, rotate_all=rotate_all)
            x += H_Y
        else: # 立直牌じゃない場合
            draw_hai(k[0], x, y, iftrans=k[2], rotate=0, rotate_all=rotate_all)
            x += H_X
        
        if k_count%6 == 0: # 河の段数をリセット
            x = C_X-H_X*3 
            y += H_Y

    # 立直棒を描画
    if Player.ifrichi():
        draw_node(image_dic["richibo"], C_X, C_Y+H_X*3-H_G, rotate_all=rotate_all)

    # ここからプレイヤーのみの描画
    if pid == MY_PID:
        # デバッグ描画
        info_tx = f"ignored={" ".join(Player.ignored[:-1])}"
        info_surf = font.render(info_tx, True, COLOR.YELLOW)
        screen.blit(info_surf, (C_X+20, C_Y+20))

        # 何待ちか描画
        wtt = Player.what_to_tempai()
        x = 300/(len(wtt)+1)
        for i, hai in enumerate(wtt):
            draw_node(image_dic["front"], SCREEN_H+x*(i+1), C_Y+400-H_Y/2)
            draw_node(image_dic[hai], SCREEN_H+x*(i+1), C_Y+400-H_Y/2)

def click_to_cmd(pos):
    # クリックした座標からコマンドを返すイメージ
    for rect, cmd in clickmap:
        if rect.collidepoint(pos):
            return cmd
    return None

def draw():
    # ステージの描画
    pygame.draw.rect(screen, COLOR.GRAY, (0, 0, SCREEN_H, SCREEN_H)) # 卓の外側
    FUCHI_ = FUCHI-10
    pygame.draw.rect(screen, COLOR.TAKU, (FUCHI_, FUCHI_, SCREEN_H-FUCHI_*2, SCREEN_H-FUCHI_*2)) # 緑の卓
    pygame.draw.rect(screen, COLOR.RIGHT, (SCREEN_H, 0, 300, SCREEN_H)) # 右の操作画面

    kawa_w = H_X*6+H_G
    pygame.draw.rect(screen, COLOR.RIGHT, (C_X-kawa_w/2, C_Y-kawa_w/2, kawa_w, kawa_w)) # 真ん中のやつ
    

    # クリックマップを作製
    global clickmap
    clickmap = []
    
    # 牌を描画する
    for i in range(4):
        draw_player(i)
    
    # デバッグ要素ゾ
    info_tx = f"whoturn={Game.whoturn}, queue={Game.queue},  phase={Game.phase.name}, GAMESTATE={game_state}"
    info_surf = font.render(info_tx, True, COLOR.BLACK)
    screen.blit(info_surf, (20, 20))
    
    # 可能なコマンドを箇条書きで描画する
    y = 30
    if Game.queue != []:
        if Game.queue[0] == MY_PID: # 自分のときしか描画しないお！
            for i in Game.capable_sousa_now:

                rect = pygame.draw.rect(screen, COLOR.WHITE, (SCREEN_H + 30, y+1, 300-30*2, 28))
                clickmap.append((rect, i)) # クリックマップに登録

                #csn_surf = cmd_font.render("  ".join(i[1:]), True, BLACK,)
                csn_surf = cmd_font.render(f"{i}", True, COLOR.BLACK)
                
                rect      = csn_surf.get_rect()   # ① まだ原点 (0,0)
                rect.center = (SCREEN_H + 150, y+15)
                screen.blit(csn_surf, rect)
                y += 30

def draw_result():
    draw()

    # 結果を表示する（まずは仮表示）
    info_tx = f"agari_data={Game.agari_data}"
    info_surf = font.render(info_tx, True, COLOR.YELLOW)
    screen.blit(info_surf, (20, 50))

def draw_title():
    # ステージの描画
    pygame.draw.rect(screen, COLOR.GRAY, (0, 0, SCREEN_H, SCREEN_H)) # 卓の外側だけテスト描画

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

waiting_ai = False

STATE_TITLE  = 0
STATE_PLAY   = 1
STATE_RESULT = 2
STATE_RESET  = 3

game_state = STATE_TITLE


running = True
while running: # ここがtkinterでいうとこのmainloop()
    cmd = None
    POS = pygame.mouse.get_pos()

    # ① イベント取得
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: # ばつぼたん
            running = False

        if game_state == STATE_TITLE: # タイトル
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                Game = Mahjong()        # 新しい半荘／局を開始
                game_state = STATE_PLAY
                waiting_ai = False
                                
                MY_PID = 0
                AI_PIDS = [1,2,3]
            continue        # タイトル中は他イベント無視

        if game_state == STATE_RESULT: # 結果待ち
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: # クリックされたら
                game_state = STATE_RESET
            continue

        if game_state == STATE_RESET:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: # クリックされたら
                game_state = STATE_PLAY
            continue



        # --------- ここから対局中 (STATE_PLAY) ---------
        if game_state == STATE_PLAY:  

            if ev.type == AI_DONE:  # AIの思考終了
                cmd = ai_q.get()
                waiting_ai = False 

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: # クリックされたら
                cmd = click_to_cmd(ev.pos)
            

    # イベント取得外の処理
    if game_state == STATE_PLAY:
        # AIを起こす
        if Game.queue != []:
            if (not waiting_ai) and Game.queue[0] in AI_PIDS and cmd == None: # AIが起きてなくかつAIのターンでかつcmdがNone=AIがまだ触ってないとき
                printd("LAUNCH AI")
                waiting_ai = True
                launch_ai()
                
        Game.step(cmd) # None なら自動進行だけ

        if Game.phase == Phase.ROUND_END: # ゲームが終了すればその局の結果開示に移る
            game_state = STATE_RESULT
    if game_state == STATE_RESULT:
        # agaridataを取得し、アガったひとの手を開示する or テンパイのひとの手を開示し、点数を表示する
        printd(Game.agari_data)
        # 未作成！！！！
    if game_state == STATE_RESET:
        # 点数移動・リセットを行う
        # 未作成！！！
        Game.reset_kyoku()

    # 描画
    if game_state == STATE_PLAY:
        draw()
    if game_state == STATE_RESULT:
        draw_result()
    if game_state == STATE_TITLE:
        draw_title()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
