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
    def __init__(self, playerid, tehai, kawa):  # コンストラクタ (初期化メソッド)
        self.playerid = playerid # プレイヤー名 
        self.tehai = tehai # 手牌の情報
        self.kawa = kawa # 河の情報

    # そいつが現在立直しているかどうかの判定
    def ifrichi(self):
        result = False
        for s in self.kawa:
            if s[1]: result = True
        return result

    # そいつが現在鳴いているかどうかの判定
    def ifnaki(self):            
        result = True
        for n in self.tehai["naki"]: # 誰かからひとつでも鳴いてたらFalse
            fromwho_li = [nn[1] for nn in n]
            for f in fromwho_li:
                if f != fromwho_li: result == False
        return result
    
    def menzen_li(self):
        if self.tehai["tumo"] != None:
            return self.tehai["menzen"] + [self.tehai["tumo"]]
        else:
            return self.tehai["menzen"] 
    def dbg(self):
        nakitx = ""
        for i in self.tehai["naki"]:
            for ii in i: 
                if ii[1] == self.playerid: nakitx += f" {ii[0]}"
                else:                      nakitx += f" {ii[0]}'"

        kawatx = ""
        for i in self.kawa:
            if i[1]: kawatx += "_" + i[0] + " "
            else:    kawatx += i[0] + " "
 
        return f"{"_".join(ripai.ripai(self.tehai["menzen"]))} [{self.tehai["tumo"]}] {nakitx} \n {kawatx}"
        


# 4人分のクラスオブジェクトを作成（playersというリストにData_A, Data_B, Data_C, Data_Dが入ってるイメージ）
# 基本的に4人のクラスはこのリストの中のオブジェクトとしてまとめて扱う（例えばData_A=…のようにして4つの管理はしないという意味）
players = [
    PlayerInfo(
        playerid= playerid,
        tehai= {"menzen": [],
                "naki": [],
                "tumo": None
                },
        kawa= []
        ) for playerid in [0, 1, 2, 3]
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
for i in range(5):
    d_o = random.choice(YAMA)
    YAMA.remove(d_o)
    dora_omote.append(d_o)
    d_u = random.choice(YAMA)
    YAMA.remove(d_u)
    dora_ura.append(d_u)
info.write(info.read() | {"dora_omote":dora_omote})
info.write(info.read() | {"dora_ura":dora_ura})
printd("dora:", dora_omote)
printd("uradora:", dora_ura)

# 四槓流れ・ドラめくり用に場において何回槓されたかのカウントを作る
kan_count = 0

# ツモってゆく
whoturn = int(info.read()["kyoku"][1]) - 1 # 誰が親かで最初にツモるひとを判定する (0~4)

# その局でだれが何をアガるかの変数
agari_data = []

# ここのループでは、「捨てられた直後 → 牌を捨てる」を1ループとする（紆余曲折の末これがもっとも整って良い）
sousa = None # ループ内でどんな操作が行われるか
sousa_hai = None # ループ内の操作の対象牌
ifkan = False

while True: 
    # この時点で、全員が13牌

    # 捨てられた牌について、他家が操作できるかの判定を行う
    ifmove = False # 捨牌が鳴かれるかどうかの変数
    if sousa_hai != None: # 開局以外の場合
        printd("check tacha_capable_sousa")
        tacha_capable_sousa_li = []
        for i_op, OtherPlayer in enumerate(players):
            if i_op == whoturn: continue # 自分自身の捨て牌・カン牌にはアクションできませんボケ
            
            # ロン判定
            # 槍槓・国士の暗槓の要素について未作成！
            if yaku.agari_capable(OtherPlayer, sousa_hai, sousa):
                tacha_capable_sousa_li.append([whoturn, "ron"])
            
            if OtherPlayer.ifrichi(): continue # 立直していればロン判定のみで切り上げる
            
            # 立直してない場合
            # チー判定
            if i_op%4 == (whoturn+1)%4: # そもそも下家じゃないとチーできない
                if len(sousa_hai) == 2: # 数牌判定
                    sh_mps, sh_n = sousa_hai[0], int(sousa_hai[1])
                    OPtm = OtherPlayer.tehai["menzen"]
                    if any([f"{sh_mps}{sh_n-2}" in OPtm and f"{sh_mps}{sh_n-1}" in OPtm,
                        f"{sh_mps}{sh_n-1}" in OPtm and f"{sh_mps}{sh_n+1}" in OPtm,
                        f"{sh_mps}{sh_n+1}" in OPtm and f"{sh_mps}{sh_n+2}" in OPtm
                        ]):
                        tacha_capable_sousa_li.append([i_op, "chi"])

            # ポン判定
            if OtherPlayer.tehai["menzen"].count(sousa_hai) >= 2: # 面前手牌に2個以上該当牌があったらポンできる
                tacha_capable_sousa_li.append([i_op, "pon"])

            # カン判定
            if OtherPlayer.tehai["menzen"].count(sousa_hai) >= 3: # 面前手牌に3個以上該当牌があったらカンできる
                tacha_capable_sousa_li.append([i_op, "daiminkan"])

        printd("tacha_capable_sousa_li:", tacha_capable_sousa_li)

        # 操作をリストアップしたら、優先度の判定をしていく
        # まずはロンが含まれてるか否かの判定をする
        
        tacha_capable_sousa_li.sort(key=lambda x: ["ron", "daiminkan", "pon", "chi"].index(x[1]))

        tacha_ron_li = [tcsl[0] for tcsl in tacha_capable_sousa_li if tcsl[1] == "ron"]
        tacha_without_ron_li = [tcsl for tcsl in tacha_capable_sousa_li if tcsl[1] != "ron"] 
        printd("ron_li:", tacha_ron_li)

        # まず他家プレイヤーにロンの選択をさせる
        for tcsl in tacha_ron_li:
            # 他家プレイヤーに選択させる
            ifmove_q = input(f"{tcsl} で動きますか？:")
            if ifmove_q == "y": # 他家が選択を承認したら 
                ifmove = True
                MovingPlayer = players[tcsl[0]]
                agari_data.append({
                    "whoagari": tcsl[0],
                    "woagarare": whoturn,
                    "tehai": MovingPlayer.tehai,
                    "yaku":  yaku.best_yaku(MovingPlayer, sousa_hai, sousa), })

        if len(agari_data) != 0: # ロンがひとつでも承認されたらbreak
            break

        for tcsl in tacha_without_ron_li:
            # 他家プレイヤーに選択させる
            ifmove_q = input(f"{tcsl} で動きますか？:")
            if ifmove_q == "y": # 他家が選択を承認したら 
                ifmove = True
                MovingPlayer = players[tcsl[0]]

                # 承認された操作を実際に行う
                if tcsl[1] == "pon": # ポンの場合
                    for i in range(2): MovingPlayer.tehai["menzen"].remove(sousa_hai)
                    MovingPlayer.tehai["naki"].append([
                        [sousa_hai, tcsl[0]],
                        [sousa_hai, tcsl[0]],
                        [sousa_hai, whoturn],])
                elif tcsl[1] == "daiminkan": # カンの場合
                    for i in range(3): MovingPlayer.tehai["menzen"].remove(sousa_hai)
                    MovingPlayer.tehai["naki"].append([
                        [sousa_hai, tcsl[0]],
                        [sousa_hai, tcsl[0]],
                        [sousa_hai, tcsl[0]],
                        [sousa_hai, whoturn],])
                elif tcsl[1] == "chi": # チーの場合
                    # チー候補を見つける
                    chi_koho = []

                    sh_mps, sh_n = sousa_hai[0], int(sousa_hai[1])
                    MPtm = MovingPlayer.tehai["menzen"]
                    if f"{sh_mps}{sh_n-2}" in MPtm and f"{sh_mps}{sh_n-1}" in MPtm: chi_koho.append([f"{sh_mps}{sh_n-2}", f"{sh_mps}{sh_n-1}"])
                    if f"{sh_mps}{sh_n-1}" in MPtm and f"{sh_mps}{sh_n+1}" in MPtm: chi_koho.append([f"{sh_mps}{sh_n-1}", f"{sh_mps}{sh_n+1}"])
                    if f"{sh_mps}{sh_n+1}" in MPtm and f"{sh_mps}{sh_n+2}" in MPtm: chi_koho.append([f"{sh_mps}{sh_n+1}", f"{sh_mps}{sh_n+2}"])
                    
                    # チー候補をプレイヤーに絞り込ませる
                    if len(chi_koho) == 1:
                        chi_sousa = chi_koho[0]
                    else:
                        chi_n = int(input(f"どれにしますか？（インデックスで）{chi_koho}"))
                        chi_sousa = chi_koho[chi_n]
                    
                    for i in range(2): MovingPlayer.tehai["menzen"].remove(chi_sousa[i])
                    MovingPlayer.tehai["naki"].append([
                        [chi_sousa[0], tcsl[0]],
                        [chi_sousa[1], tcsl[0]],
                        [sousa_hai, whoturn],])

                whoturn = tcsl[0] # あとのループ内の対象プレイヤーを確定させる
                break
        
        if not ifmove: # 捨てられた牌に対して誰も動かなかったら
            whoturn = (whoturn + 1) % 4 # 下家にターンをゆずる
            
    else : # 開局時 
        printd(f"START {info.read()["kyoku"]}")
    
    printd(f"~ start {whoturn} turn", "~"*64)
    
    if not ifmove: # ターンが鳴き後でなかったらツモらせる
        tumohai = random.choice(YAMA)
        YAMA.remove(tumohai)
        players[whoturn].tehai["tumo"] = tumohai
    else: tumohai = None # 混乱を避けるため tumohaiをいちおう定義する
    
    # この時点で、一人だけ14牌    
    Player = players[whoturn] # 対象プレイヤーを指定
    



    capable_sousa = { # プレイヤーができる操作を指定
        "tumo": [],
        
        "kiru": Player.menzen_li(),
        "richi": [],
        "ankan" : [],
        "kakan" : [],
    }

    # 鳴いた後の操作でない場合、立直・ツモ・カンができる
    if not ifmove:
        # 立直判定
        if Player.ifrichi(): # 鳴いていなければ聴牌判定に入る
            whichtotempai = []
            for kiruhai in Player.menzen_li(): 
                tehai_li_copied = Player.menzen_li()[:]
                tehai_li_copied.remove(kiruhai)
                for hai in ALL_HAI:
                    if ifagari.ifagari(tehai_li_copied + [hai]): whichtotempai.append(kiruhai)
            capable_sousa["richi"] = ripai.ripai(set(whichtotempai)) # 重複・順序を調整

        # 槓判定（暗槓・加槓）（ツモ・カン時）
        # 立直していれば待ちが変わってしまう暗槓はできないのであとあと修正が必要
        # 未作成！
        for hai in ALL_HAI:
            if Player.menzen_li().count(hai) == 4: # 暗槓判定
                capable_sousa["ankan"].append(hai)

            for naki in Player.tehai["naki"]: # 加槓判定
                if [i[0] for i in naki].count(hai) == 3 and (hai in Player.menzen_li()):
                    capable_sousa["kakan"].append(hai)

        # 和了判定
        if yaku.agari_capable(Player, tumohai, sousa):
            capable_sousa["tumo"] = Player.tehai["tumo"]
            

    # プレイヤー側に、可能操作から操作を選ばせる
    for P in players:
        printd(f"({P.playerid}) {P.dbg()}")
    printd("capable_sousa: ", capable_sousa)

    sinp = input("sousa:").split()
    sousa, sousa_hai = sinp[0], sinp[1]
    # ←これはあとあとプレイヤー選択依存変数にする

    # 選択された操作に基づいて処理を行う
    if sousa == "ankan": # 暗槓
        for i in range(4):  Player.tehai["menzen"].remove(sousa_hai)
        Player.tehai["naki"].append([[sousa_hai, whoturn] for i in range(4)])
        
    elif sousa == "kakan": # 明槓   
        # 該当牌のインデックスの取得
        for k_index, n in Player.naki:
            if [nn[0] for nn in n] == [sousa_hai for i in range(3)]:
                Player.tehai["naki"][k_index].append([sousa_hai, whoturn])

    elif sousa == "kiru": # 普通に切るとき
        Player.tehai["menzen"].remove(sousa_hai)
        if not ifmove: # 鳴き後に切るときは手牌に牌を追加しない 
            Player.tehai["menzen"].append(tumohai)
        Player.kawa.append([sousa_hai, False])
    elif sousa == "richi": # 立直
        Player.tehai["menzen"].remove(sousa_hai)
        Player.tehai["menzen"].append(tumohai)
        Player.kawa.append([sousa_hai, True])
    
    elif sousa == "tumo": # ツモ和了
        agari_data.append({
            "whoagari": whoturn,
            "woagarare": None,
            "tehai": Player.tehai,
            "yaku":  yaku.best_yaku(Player, tumohai, sousa), })
        break

    # 最後にプレイヤーのツモ牌をNoneにする
    Player.tehai["tumo"] = None
    
    print(f"~ end {whoturn} turn", "~"*64)


printd("agari_data:", agari_data)
if len(agari_data) == 0:
    printd("RYUKYOKU")
else:
    printd("AGARI")
print(f"[{info.read()["kyoku"]} end]")