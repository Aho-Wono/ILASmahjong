import ifagari
import info
import ripai
import random
from debug import printd
from debug import printc
import yaku

ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()


# とりあえず1局まるまる遊べるようなものを作ります
# プレイヤーの状況を包括するクラスを作成
class PlayerInfo:
    def __init__(self, name, tehai, kawa):  # コンストラクタ (初期化メソッド)
        self.name = name # プレイヤー名 
        self.tehai = tehai # 手牌の情報
        self.kawa = kawa # 河の情報

    # そいつが現在立直しているかどうかの判定
    def ifrichi(self):
        return any(hai[1] in self.kawa) # 河に一つでも立直してるやつがあれば



# 4人分のクラスオブジェクトを作成（playersというリストにData_A, Data_B, Data_C, Data_Dが入ってるイメージ）
# 基本的に4人のクラスはこのリストの中のオブジェクトとしてまとめて扱う（例えばData_A=…のようにして4つの管理はしないという意味）
players = [
    PlayerInfo(
        name= playername,
        tehai= {"menzen": ["m1", "m2", "m3", "ton", "nan", "nan", "m9", "s1", "s2", "s3"],
                "naki": [["ton", 0], ["ton", 0], ["ton", 1], ["ton", 0]],
                "tumo": None
                },
        kawa= []
        ) for playername in ["現役", "1浪", "2浪", "3浪"]
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

# 四槓流れ・ドラめくり用に場において何回槓されたかのカウントを作る
kan_count = 0

# ツモってゆく
whoturn = info.read()["oya"] # 誰が親かで最初にツモるひとを判定する (0~4)
printd("oya: ", whoturn)

while True: # 1ループ1ツモ
    Player = players[whoturn]


    tumohai = random.choice(YAMA)
    YAMA.remove(tumo)


    while True:
            
        # tumoの更新
        Player.tehai["tumo"] = tumohai

        if True: # デバッグ用
            Player.tehai["menzen"] = "m1 m2 m2 m2 m6 m6 m8 m8 s1 s1 s2 ton ton".split()
            Player.tehai["naki"] = [[["m1", 0], ["m1", 0], ["m1", 1]]]
            Player.tehai["tumo"] = "m2"


        printc(players[whoturn])
        
        # あとで扱いやすいよう、ツモと手牌を一体化したリストを作成する
        tehai_li = Player.tehai["menzen"] + [Player.tehai["tumo"]]


        # プレイヤーのtehaiが更新されたので、プレイヤー側に操作をお願いする
        # プレイヤーがその状況で可能な操作（何を切るか以外）を抜き出す（重労働）
        capable_sousa = {
            "kiru": tehai_li,
            "tumo": [],
            "richi": [],
            "kan" : [],
        }
        
        # ツモ和了可能かの判定（yaku.yakuが完成していないのでデバッグしてません！！！）
        yaku_pattern_li = yaku.yaku(Player)
        if len(yaku_pattern_li) >= 1: # 成立する役の組み合わせがあったら
            for yaku_pattern in yaku_pattern_li: 
                # 手役が役の中に存在すればツモ可能
                for teyaku in yaku.teyaku_li():
                    if teyaku in yaku_pattern:
                        capable_sousa["tumo"] == Player.tehai["tumo"]
        
        # 立直可能かの判定（つまり聴牌判定）
        menzen = True
        for naki in Player.tehai["naki"]: # 暗槓対策
            if naki[1] != whoturn:  
                menzen = False
        if menzen: # 鳴いていなければ聴牌判定に入る
            printd("menzenhantei")
            whichtotempai = []
            for kiruhai in tehai_li: 
                tehai_li_copied = tehai_li[:]
                tehai_li_copied.remove(kiruhai)
                for hai in ALL_HAI:
                    if ifagari.ifagari(tehai_li_copied + [hai]): whichtotempai.append(kiruhai)

            capable_sousa["richi"] = ripai.ripai(set(whichtotempai)) # 重複・順序を調整
        
        # 槓ができるかどうかの判定（暗槓・加槓）
        # 立直していれば待ちが変わってしまう暗槓はできないのであとあと修正が必要！！！！そしてまだ修正してない！！！！WHOOOO
        for hai in ALL_HAI:
            if tehai_li.count(hai) == 4: # 暗槓判定
                capable_sousa["kan"].append([hai, "ankan"])
            for naki in Player.tehai["naki"]: # 加槓判定
                if [i[0] for i in naki].count(hai) == 3 and (hai in tehai_li):
                    capable_sousa["kan"].append([hai, "kakan"])

        # プレイヤーに選ばせる
        sousa = input(f"操作を選んでください: {[i for i in list(capable_sousa)]}")
        
        if sousa != "kiru":
            continue ##あとあと作成～～～～
        else: 
            printd("牌を切ります")
            break # 何かしら切る場合はループを解除

    # 最後にプレイヤーのツモ牌をNoneにする
    Player.tehai["tumo"] = None

    # ここでとりあえず一人のプレイヤーのターンは確定で終わり
    # ここからは切った牌に対する他プレイヤーの選択肢を提示していく

    # 槍槓・暗槓に対してロンができるかどうかの判定を行う
    # めんどくさいからまだつくらない



    # 一人一人のプレイヤーに対して、できる操作を調べていく
    tacha_capable_sousa_li = []
    for i_op, OtherPlayer in enumerate(players):


        tacha_capable_sousa = {
            "pon": [],
            "chi": [],
            "kan" : [],
            "ron": []
        }

        if i_op == whoturn: # 自分自身の捨て牌にはアクションできませんボケ
            tacha_capable_sousa_li.append(tacha_capable_sousa)
        else:
            # ロン判定


            if OtherPlayer.ifrichi(): # 立直していればロン判定のみで切り上げる
                tacha_capable_sousa_li.append(tacha_capable_sousa)
            else:
                # チー判定
                print()

                # ポン判定
    
    # 操作をリストアップしたら、優先度の判定をしていく
    #
    #              うんち
    #

    # 行われた操作によっては次のwhoturnが変わるぜ
    


    # 誰もなんにもしなかった場合、whoturnを次の人にする
    whoturn = (whoturn + 1) % 4




    break
