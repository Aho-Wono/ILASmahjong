import ifagari
import info
import ripai
import random
from debug import printd
from debug import printc


ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()



# とりあえず1局まるまる遊べるようなものを作ります
# プレイヤーの状況を包括するクラスを作成
class PlayerInfo:
    def __init__(self, name, tehai, kawa):  # コンストラクタ (初期化メソッド)
        self.name = name # プレイヤー名 
        self.tehai = tehai # 手牌の情報
        self.kawa = kawa # 河の情報

# 4人分のクラスオブジェクトを作成（playersというリストにData_A, Data_B, Data_C, Data_Dが入ってるイメージ）
# 基本的に4人のクラスはこのリストの中のオブジェクトとしてまとめて扱う（例えばData_A=…のようにして4つの管理はしないという意味）
players = [
    PlayerInfo(
        name= playername,
        tehai= {"menzen": [],
                "naki": [],
                "tumo": None
                },
        kawa= []
        ) for playername in ["田中", "佐藤", "藤原", "David"]
    ]

# 山を作り、王牌や配牌を設定する→しようと思ってたけど毎回ランダムにツモればシャッフル山作る必要なくね？と思ったのでやっぱなし　河原ごめん！
#haipai.haipai()
YAMA = ALL_HAI*4 # すべての牌が入っている山を作成
for Player in players: # ←ここでPlayerが大文字なのはクラスの変数名のイニシャルが慣習的に大文字だから
    haipai = []
    for i in range(13): # 親子で最初に13枚ずつ取る
        tumo = random.choice(YAMA)
        YAMA.remove(tumo)
        haipai.append(tumo)
    Player.tehai["menzen"] = haipai

# ドラの設定　最後にrandom.choiceしても良いがついで裏ドラも4個分押さえておく
dora_omote = []
dora_ura   = []
for i in range(4):
    d_o = random.choice(YAMA)
    YAMA.remove(d_o)
    dora_omote.append(d_o)
    d_u = random.choice(YAMA)
    YAMA.remove(d_u)
    dora_ura.append(d_u)
printd("dora:", dora_omote)
printd("uradora:", dora_ura)

# ツモってゆく
whoturn = info.read()["oya"] # 誰が親かで最初にツモるひとを判定する (0~4)
printd("oya: ", whoturn)

while True: # 1ループ1ツモ
    Player = players[whoturn]
    tumohai = random.choice(YAMA)
    YAMA.remove(tumo)

    # tumoの更新
    Player.tehai["tumo"] = tumohai

    for デバッグ用 in [1111]:
        Player.tehai["tumo"] = "m1"
        Player.tehai["menzen"] = "m2 m2 m4 m4 m6 m6 m8 m8 s1 s1 s2 ton ton".split()


    printc(players[whoturn])

    # プレイヤーのtehaiが更新されたので、プレイヤー側に操作をお願いする
    # プレイヤーがその状況で可能な操作（何を切るか以外）を抜き出す（重労働）
    capable_sousa = {
        "tumo": [],
        "richi": [],
        "kan" : [],
    }
    
    # ツモ和了可能かの判定
    
    # 立直可能かの判定（つまり聴牌判定）
    menzen = True
    for naki in Player.tehai["naki"]: # 暗槓対策
        if naki[1] != whoturn:  
            menzen = False
    if menzen: # 鳴いていなければ聴牌判定に入る
        printd("menzenhantei")
        tehai_li = Player.tehai["menzen"] + [Player.tehai["tumo"]]
        whichtotempai = []
        for kiruhai in tehai_li: 
            tehai_li_copied = tehai_li[:]
            tehai_li_copied.remove(kiruhai)
            for hai in ALL_HAI:
                if ifagari.ifagari(tehai_li_copied + [hai]): whichtotempai.append(kiruhai)

        capable_sousa["richi"] = ripai.ripai(set(whichtotempai)) # 重複・順序を調整
    
    # 槓ができるかどうかの判定
    
    printd("capable_sousa:", capable_sousa)

    # 最後にプレイヤーのツモ牌をNoneにする
    Player.tehai["tumo"] = None

    break
