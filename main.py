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
import info
import tensukeisan

import chappy_choice


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
font = pygame.font.SysFont(None, 32)
font_jp = pygame.font.SysFont("Meiryo", 25)
#font_jp.set_bold(True)
font_jp_deka = pygame.font.SysFont("Meiryo", 40)

cmd_font = pygame.font.SysFont(None, 30)

clickmap = []

def draw_node(img, x, y, rotate_all = 0, clm_cmd = None, anchor = "center"):
    # XY軸をどの向きに設定するかで変換する
    theta = math.radians(rotate_all)
    x_converted = C_X + (x - C_X) * math.cos(theta) + (y - C_Y) * math.sin(theta)
    y_converted = C_Y - (x - C_X) * math.sin(theta) + (y - C_Y) * math.cos(theta)

    img = pygame.transform.rotate(img, rotate_all)        
    rect = img.get_rect()
    setattr(rect, anchor, (x_converted, y_converted))
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
                        
                elif naki[3][1] == pid: # 加槓
                    fromwho = naki[2][1]
                    mod4 = (fromwho-pid)%4
                    if mod4 == 1: # 上家から鳴いていた場合
                        draw_hai(hai, x-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y, C_Y+400+H_XY-H_X, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_Y-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                    elif mod4 == 2: # 対面から鳴いていた場合
                        draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y, C_Y+400+H_XY-H_X, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_Y-H_X, C_Y+400, rotate_all=rotate_all)
                    elif mod4 == 3: # 下家から鳴いていた場合
                        draw_hai(hai, x-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X, C_Y+400, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY, rotate=90, rotate_all=rotate_all)
                        draw_hai(hai, x-H_X-H_X-H_Y, C_Y+400+H_XY-H_X, rotate=90, rotate_all=rotate_all)
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

    # 点数を描画
    score = info.read()["score"][pid]
    score_surf = font.render(str(score), True, COLOR.YELLOW)
    draw_node(score_surf, C_X, C_Y+80, rotate_all=rotate_all)

    # ここからプレイヤーのみの描画
    if pid == MY_PID:
        # デバッグ描画
        #info_tx = f"ignored={" ".join(Player.ignored[:-1])}"
        #info_surf = font.render(info_tx, True, COLOR.YELLOW)
        #screen.blit(info_surf, (C_X+20, C_Y+20))
        
        # 何待ちか描画
        wtt = Player.what_to_tempai()
        x = 300/(len(wtt)+1)
        for i, hai in enumerate(wtt):
            draw_node(image_dic["front"], SCREEN_H+x*(i+1), C_Y+400+H_Y/2-1)
            draw_node(image_dic[hai], SCREEN_H+x*(i+1), C_Y+400+H_Y/2-1)

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

    # 真ん中のやつ
    kawa_w = H_X*6+H_G
    rect = pygame.Rect(C_X-kawa_w/2, C_Y-kawa_w/2, kawa_w, kawa_w)   # 四角形の領域
    pygame.draw.rect(screen, COLOR.RIGHT, rect, border_radius=10)
    
    # クリックマップを作製
    global clickmap
    clickmap = []
    
    # プレーヤー関連情報を描画する
    for i in range(4):
        draw_player(i)
    
    # 局情報を描画
    w2 = 120
    rect = pygame.Rect(C_X-w2/2, C_Y-w2/2, w2, w2)   # 四角形の領域
    pygame.draw.rect(screen, COLOR.GRAY, rect, border_radius=20)

    kyoku = info.read()["kyoku"]
    kyoku = {"t": "東", "n":"南"}[kyoku[0]] + str(kyoku[1]) + "局"
    hon = str(info.read()["hon"]) + "本場"
    kyoku_surf = font_jp.render(kyoku, True, COLOR.WHITE)
    hon_surf = font_jp.render(hon, True, COLOR.WHITE)
    draw_node(kyoku_surf, C_X, C_Y, anchor="midbottom")
    draw_node(hon_surf, C_X, C_Y, anchor="midtop")

    # 王牌表示
    dorasu = info.read()["kancount"] + 1
    # 表ドラ表示
    dora_omote = info.read()["dora_omote"]
    for i in range(5):
        if i+1 <= dorasu:
            hai = ["front", dora_omote[i]]
        else:
            hai = ["back"]
        for h in hai:
            img = image_dic[h]
            draw_node(img, SCREEN_H+150-H_X*2+H_X*i, 750)
    # 表ドラ表示
    dora_ura = info.read()["dora_ura"]
    agari_data = Game.agari_data
    ifuradora = False
    if agari_data != None:
        whoagari = agari_data["whoagari"]
        if Game.players[whoagari].ifrichi(): # 上がった人が立直してたら裏ドラをチラ見させる
            ifuradora = True
    for i in range(5):
        if i+1 <= dorasu and ifuradora:
            hai = ["front", dora_ura[i]]
        else:
            hai = ["back"]
        for h in hai:
            img = image_dic[h]
            draw_node(img, SCREEN_H+150-H_X*2+H_X*i, 750+H_Y)
        
    
    
    
    # デバッグ要素ゾ
    info_tx = f"whoturn={Game.whoturn}, queue={Game.queue},  phase={Game.phase.name}, GAMESTATE={game_state}"
    info_surf = font.render(info_tx, True, COLOR.BLACK)
    screen.blit(info_surf, (20, 20))
    
    # 可能なコマンドを箇条書きで描画する
    y = 30
    if Game.queue != []:
        if Game.queue[0] == MY_PID: # 自分のときしか描画しないお！
            for i in Game.capable_sousa_now:
                # 切るだけのやつは描画しなくて十分でさぁ
                if i[1] == "kiru": continue

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

    if result == None: # 流局の場合
        printd("流局")
    else: # 誰かしら上がってて結果を表示せなあかん場合
        y = 30 + 1
        # 役の表示
        yaku_li = Game.agari_data["yaku"]
        for yaku in yaku_li:
            yaku_surf = font_jp.render(yaku, True, COLOR.BLACK)
            draw_node(yaku_surf, SCREEN_H + 30, y, anchor="topleft")
            y += 30
        y+=30
        
        # 符・翻の表示
        fuhan = f"{result[1]}符 {result[2]}翻"
        fuhan_surf = font_jp.render(fuhan, True, COLOR.WHITE)
        draw_node(fuhan_surf, SCREEN_H + 30, y, anchor="topleft")

        # 点数の表示
        y+=30
        tensu_li = sorted(result[0])
        if tensu_li.count(0) == 2: # 放銃の場合
            tensu = f"{max(tensu_li)}"
        elif tensu_li.count(tensu_li[0]) == 3: # 親のツモの場合
            tensu = f"{-tensu_li[0]}オール"
        else:
            tensu = f"{-tensu_li[1]}・{-tensu_li[0]}" # 子のツモの場合
        tensu_surf = font_jp.render(tensu, True, COLOR.WHITE)
        draw_node(tensu_surf, SCREEN_H + 30, y, anchor="topleft")



def draw_title():
    # ステージの描画
    pygame.draw.rect(screen, COLOR.TAKU, (0, 0, SCREEN_H+300, SCREEN_H)) # 卓の外側だけテスト描画

    info_tx = f"画面クリックでスタート"
    info_surf = font_jp_deka.render(info_tx, True, COLOR.WHITE)
    draw_node(info_surf, C_X+150, C_Y)

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
    #await asyncio.sleep(0.5) # とりま待たせる

    if True:
        # 河原依頼
        situations = {
            "kawa_li": None,
            "tehai": None,
            "naki" : None,
            "whoturn" : Game.whoturn
        }
        playerinfo_li = Game.players[:]
        situations["kawa_li"] = [playerinfo_li[0].kawa , playerinfo_li[1].kawa , playerinfo_li[2].kawa , playerinfo_li[3].kawa]
        situations["tehai"] = playerinfo_li[Game.whoturn].tehai
        situations["naki"] = [playerinfo_li[0].tehai["naki"] , playerinfo_li[1].tehai["naki"] , playerinfo_li[2].tehai["naki"] , playerinfo_li[3].tehai["naki"]]
        
        try:
            AI_cmd = await asyncio.wait_for(
            chappy_choice.chappy_choice(situations=situations, what_ai_can_do= what_ai_can_do), # 待機時間が発生する関数
                timeout=1)
        except asyncio.TimeoutError:
            printd("ChatGPT Timeout")
            AI_cmd = random.choice(what_ai_can_do)
        except Exception:
            printd("ChatGPT Error")
            AI_cmd = random.choice(what_ai_can_do)
        

    printd("FINISH AI THINKING")

    print("AI_CMD:", AI_cmd)

    ai_q.put(AI_cmd)

    pygame.event.post(pygame.event.Event(AI_DONE))

def launch_ai():
    asyncio.run_coroutine_threadsafe(start_ai(), loop)


AI_DONE = pygame.USEREVENT + 1 

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
                info.edit("score", [25000,25000,25000,25000])
                game_state = STATE_PLAY
                waiting_ai = False
                
                # あとあと変える箇所ー 未作成！
                MY_PID = random.choice([0,1,2,3])

                MY_PID = 0

                AI_PIDS = [0,1,2,3]
                AI_PIDS.remove(MY_PID)


            continue        # タイトル中は他イベント無視

        if game_state == STATE_RESULT: # 結果見てる状態
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: # クリックされたら
                game_state = STATE_RESET
                # 点数移動を行う
                if result != None:
                    score = info.read()["score"]
                    for i,t in enumerate(result[0]):
                        score[i] += t
                info.edit("score", score)

                printd("STATE_RESULT→STATE_RESET")
            continue

        if game_state == STATE_RESET:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: # クリックされたら
                # 次局へ移る
                kyoku = info.read()["kyoku"]
                kyoku_index = "t1 t2 t3 t4 n1 n2 n3 n4".split().index(kyoku)

                if kyoku_index == 7: # ゲーム終了
                    game_state = STATE_TITLE
                else:
                    if info.getoya() == (Game.agari_data["whoagari"] if Game.agari_data != None else None): # 連荘
                        info.edit("hon", info.read()["hon"]+1)
                    else: # 親流れ
                        info.edit("kyoku", "t1 t2 t3 t4 n1 n2 n3 n4".split()[kyoku_index+1])

                    game_state = STATE_PLAY
                    # 局情報をリセットして新しい局に移らす                
                    Game.reset_kyoku()
                    printd("STATE_RESET→STATE_PLAY")
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
            if Game.agari_data == None:
                result = None
            else:   
                result = tensukeisan.tensukeisan(Game) # 点数計算に移る


    # 描画
    if game_state == STATE_PLAY: # ゲーム中
        draw()
    if game_state == STATE_RESULT: # 結果表示
        draw_result()
    if game_state == STATE_RESET:
        draw_result()
    if game_state == STATE_TITLE: # タイトル画面
        draw_title()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
