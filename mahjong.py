from enum import Enum, auto
import mentsu_pattern

class Phase(Enum): # ゲームのMAP値を定義
    NEED_DRAW    = auto() # 新しい手番が来た直後
    WAIT_SELF    = auto() # ツモ直後／副露後
    WAIT_OTHERS = auto() # 打牌が確定した瞬間
    ROUND_END    = auto() # ツモ／ロン／流局が確定
# とりあえず1局まるまる遊べるようなものを作ります
# プレイヤーの状況を包括するクラスを作成
class PlayerInfo:
    ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()

    def __init__(self, playerid, tehai, kawa):  # コンストラクタ (初期化メソッド)
        self.playerid = playerid # プレイヤー名 
        self.tehai = tehai # 手牌の情報
        self.kawa = kawa # 河の情報
        self.ignored = []

    # そいつが現在立直しているかどうかの判定
    def ifrichi(self):
        result = False
        for s in self.kawa:
            if s[1]: result = True
        return result

    # そいつが現在鳴いているかどうかの判定
    def ifnaki(self):            
        result = False
        for n in self.tehai["naki"]: # 誰かからひとつでも鳴いてたらTrue
            fromwho_li = [nn[1] for nn in n]
            for f in fromwho_li:
                if f != self.playerid: result = True
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
 
        return f'{"_".join(ripai.ripai(self.tehai["menzen"]))} [{self.tehai["tumo"]}] {nakitx} \n {kawatx}'
    
    def kiru(self, hai):
        if self.tehai["tumo"] != None: #ツモ牌があれば面前に加えてから切る
            self.tehai["menzen"].append(self.tehai["tumo"])
            self.tehai["tumo"] = None
        self.tehai["menzen"].remove(hai)

    def iffuriten(self):
        for wtt in self.what_to_tempai():
            if wtt in self.kawa or wtt in self.ignored[:-1]:
                return True
        return False
    
    def what_to_tempai(self):
        if self.tehai["tumo"] == None:
            return ifagari.what_to_agari(self.menzen_li())
        else:
            return ifagari.what_to_agari(self.tehai["menzen"])

import ifagari
import info
import ripai
import random
from debug import printd
from debug import printc
import yaku

class Mahjong():
    ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()

    def __init__(self):
        self.reset_kyoku()

    def reset_kyoku(self):
        # 開局時の初期化を行う
        printd(f"START {info.read()["kyoku"].upper()}")

        # 4人分のクラスオブジェクトを作成（playersというリストにData_A, Data_B, Data_C, Data_Dが入ってるイメージ）
        # 基本的に4人のクラスはこのリストの中のオブジェクトとしてまとめて扱う（例えばData_A=…のようにして4つの管理はしないという意味）
        self.players = [
            PlayerInfo(
                playerid= playerid,
                tehai= {"menzen": [],
                        "naki": [],
                        "tumo": None
                        },
                kawa= [], 
                ) for playerid in [0, 1, 2, 3]
            ]

        # 山を作り、王牌や配牌を設定する→しようと思ってたけど毎回ランダムにツモればシャッフル山作る必要なくね？と思ったのでやっぱなし　河原ごめん！
        #haipai.haipai()
        self.YAMA = self.ALL_HAI*4 # すべての牌が入っている山を作成
        for Player in self.players: # ←ここでPlayerが大文字なのはクラスの変数名のイニシャルが慣習的に大文字だから
            haipai = []
            for i in range(13): # 親子で最初に13枚ずつ取る
                tumo = random.choice(self.YAMA)
                self.YAMA.remove(tumo)
                haipai.append(tumo)
            Player.tehai["menzen"] = haipai

        if True:
            self.players[0].tehai["menzen"] = "m1 m1 m1 m1 m2 m3 s2 s3 s4 s5 s6 s6 s6".split()

        # ドラの設定　最後にrandom.choiceしても良いがついで裏ドラも4個分押さえておく
        dora_omote = []
        dora_ura   = []
        for i in range(5):
            d_o = random.choice(self.YAMA)
            self.YAMA.remove(d_o)
            dora_omote.append(d_o)
            d_u = random.choice(self.YAMA)
            self.YAMA.remove(d_u)
            dora_ura.append(d_u)
        info.edit("dora_omote", dora_omote)
        info.edit("dora_ura", dora_ura)
        printd("dora:", dora_omote)
        printd("uradora:", dora_ura)

        info.edit("kancount", 0) # カンの初期化
        self.whoturn = info.getoya() # 誰が親かで最初にツモるひとを判定する (0~4)
        

        # 親に1牌ツモらせる
        oya_id = info.getoya()
        self.whoturn = oya_id - 1 # ひとつ下家のIDにしておく
    
        # ツモらせる操作
        self.whoturn = oya_id # カンのあとでなければ下家にターンをゆずる
        tumohai = random.choice(self.YAMA)
        self.YAMA.remove(tumohai)
        self.players[self.whoturn].tehai["tumo"] = tumohai

        self.phase = Phase.WAIT_SELF
        self.previous_cmd = [None, "kiru", None]
        self.agari_data = None # その局でだれが何をアガるかの変数
        
        self.queue = [oya_id]
        self.capable_sousa_now = self.get_capable_sousa_now()

    def get_capable_sousa(self):
        #printd("check capable_sousa, phase=", self.phase)
        capable_sousa_li = []

        if self.phase == Phase.WAIT_SELF:
            # この時点で、一人だけ14牌    
            Player = self.players[self.whoturn] # 対象プレイヤーを指定
            
            # 何切る問題はいずれの状態でも可能
            mzl = ripai.ripai(Player.menzen_li())
            for hai in mzl:
                kiru_cmd = [self.whoturn, "kiru", hai]
                if kiru_cmd not in capable_sousa_li:
                    capable_sousa_li.append(kiru_cmd)
                
            # 鳴いた後の操作でない場合、立直・ツモ・カンができる
            if self.previous_cmd[1] in ["kiru", "richi", "ankan", "kakan"]:
                # 立直判定
                if not Player.ifnaki(): # 鳴いていなければ聴牌判定に入る
                    for kiruhai in Player.menzen_li(): 
                        tehai_li_copied = Player.menzen_li()[:]
                        tehai_li_copied.remove(kiruhai)
                        for hai in self.ALL_HAI:
                            if ifagari.ifagari(tehai_li_copied + [hai]):
                                r_cmd = [self.whoturn, "richi", kiruhai]
                                if r_cmd not in capable_sousa_li:
                                    capable_sousa_li.append([self.whoturn, "richi", kiruhai]) # 重複・順序を調整

                # 槓判定（暗槓・加槓）（ツモ・カン時）
                # 立直していれば待ちが変わってしまう暗槓はできないのであとあと修正が必要
                # 未作成！
                for hai in self.ALL_HAI:
                    if Player.menzen_li().count(hai) == 4: # 暗槓判定
                        capable_sousa_li.append([self.whoturn, "ankan", hai])

                    for naki in Player.tehai["naki"]: # 加槓判定
                        if [i[0] for i in naki].count(hai) == 3 and (hai in Player.menzen_li()):
                            capable_sousa_li.append([self.whoturn, "kakan", hai])

                # ツモ和了判定
                if yaku.agari_capable(Player, Player.tehai["tumo"], self.previous_cmd[1]):
                    capable_sousa_li.append([self.whoturn, "tumo", Player.tehai["tumo"]])

        elif self.phase == Phase.WAIT_OTHERS:
            sousa_hai = self.previous_cmd[2] # 切られた牌をGet

            # この時点で、全員が13牌
            # 捨てられた牌について、他家が操作できるかの判定を行う
            for i_op, OtherPlayer in enumerate(self.players):
                if i_op == self.whoturn: continue # 自分自身の捨て牌・カン牌にはアクションできませんボケ

                # ロン判定
                if not OtherPlayer.iffuriten(): # フリテン判定を行う
                    if yaku.agari_capable(OtherPlayer, sousa_hai, self.previous_cmd[1]):
                        capable_sousa_li.append([i_op, "ron", sousa_hai])
                    
                if OtherPlayer.ifrichi(): continue # 立直していればロン判定のみで切り上げる
                
                # 立直してない場合
                # チー判定
                if i_op%4 == (self.whoturn+1)%4: # そもそも下家じゃないとチーできない
                    if len(sousa_hai) == 2: # 数牌判定
                        sh_mps, sh_n = sousa_hai[0], int(sousa_hai[1])
                        OPtm = OtherPlayer.tehai["menzen"]
                        if f"{sh_mps}{sh_n-2}" in OPtm and f"{sh_mps}{sh_n-1}" in OPtm:
                            capable_sousa_li.append([i_op, "chi", sousa_hai, -2, -1])
                        if f"{sh_mps}{sh_n-1}" in OPtm and f"{sh_mps}{sh_n+1}" in OPtm:
                            capable_sousa_li.append([i_op, "chi", sousa_hai, -1, +1])
                        if f"{sh_mps}{sh_n+1}" in OPtm and f"{sh_mps}{sh_n+2}" in OPtm:
                            capable_sousa_li.append([i_op, "chi", sousa_hai, +1, +2])

                # ポン判定
                if OtherPlayer.tehai["menzen"].count(sousa_hai) >= 2: # 面前手牌に2個以上該当牌があったらポンできる
                    capable_sousa_li.append([i_op, "pon", sousa_hai])

                # カン判定
                if OtherPlayer.tehai["menzen"].count(sousa_hai) >= 3: # 面前手牌に3個以上該当牌があったらカンできる
                    capable_sousa_li.append([i_op, "daiminkan", sousa_hai])

        # capable_suosa_liの優先度を設定し、対象プレイヤーを一人だけにする
        capable_sousa_li.sort(key=lambda x: ["kiru", "richi", "tumo", "ankan", "kakan", "ron", "daiminkan", "pon", "chi"].index(x[1]))
        if capable_sousa_li != []: # ひとりだけに絞る
            capable_sousa_li = [csl for csl in capable_sousa_li if csl[0] == capable_sousa_li[0][0]]
        
        return capable_sousa_li
    
    def get_queue(self):
        id_li = [gcs[0] for gcs in self.get_capable_sousa()]
        del_index_li = []
        for i, id in enumerate(id_li):
            if i != 0:
                if id == id_li[i-1]:
                    del_index_li.append(i)
        del_index_li.sort(reverse=True)
        for idx in del_index_li:
            id_li.pop(idx)

        return id_li

    def get_capable_sousa_now(self):
        if self.queue == []:
            return None
        else:
            queue = self.queue[0]
            csl = self.get_capable_sousa()
            csl_n = [cs for cs in csl if cs[0] == queue] 
            if self.phase == Phase.WAIT_OTHERS and csl_n != []:
                csl_n.append([queue, "ignore", None])
            return csl_n

    def do_cmd(self, cmd): # ダブロン・トリロンに対応するためcmdはリストにしている
        if cmd == None: 
            return # 何もしない
        
        # 何かしら操作が行われた場合
        print("do cmd:", cmd)
        
        p_id = int(cmd[0])
        Player = self.players[p_id]
        sousa = cmd[1]
        sousa_hai = cmd[2]

        # 選択された操作に基づいて処理を行う
        if sousa == "ignore": # 鳴ける・ロンできるのに無視した場合
            pass
        else: # 何かしらの操作が発生する場合
            if sousa == "ankan": # 暗槓
                for i in range(4):  Player.kiru(sousa_hai)
                Player.tehai["naki"].append([[sousa_hai, self.whoturn] for i in range(4)])
                info.edit("kancount", info.read()["kancount"] + 1)
                
            elif sousa == "kakan": # 明槓   
                # 該当牌のインデックスの取得
                for k_index, n in enumerate(Player.tehai["naki"]):
                    if [nn[0] for nn in n] == [sousa_hai for i in range(3)]:
                        Player.tehai["naki"][k_index].append([sousa_hai, self.whoturn])
                info.edit("kancount", info.read()["kancount"] + 1)

            elif sousa == "kiru": # 普通に切るとき
                Player.kiru(sousa_hai)
                Player.kawa.append([sousa_hai, False, False])

                for P in self.players:
                    if P.ifrichi():
                        P.ignored.append(sousa_hai)
            elif sousa == "richi": # 立直
                Player.kiru(sousa_hai)
                Player.kawa.append([sousa_hai, True, False])
                
                for P in self.players:
                    if P.ifrichi():
                        P.ignored.append(sousa_hai)
                
            elif sousa == "tumo": # ツモ和了
                by = yaku.best_yaku(Player, Player.tehai["tumo"], self.previous_cmd[1])
                self.agari_data = {
                    "whoagari": self.whoturn,
                    "whoagarare": None,
                    "tehai": Player.tehai,
                    "yaku": by[1],
                    "mentu_pattern": by[0]}

            elif sousa == "pon": # ポンの場合
                for i in range(2): Player.kiru(sousa_hai)
                Player.tehai["naki"].append([
                    [sousa_hai, p_id],
                    [sousa_hai, p_id],
                    [sousa_hai, self.whoturn],])
                
            elif sousa == "daiminkan": # カンの場合
                for i in range(3): Player.kiru(sousa_hai)
                Player.tehai["naki"].append([
                    [sousa_hai, p_id],
                    [sousa_hai, p_id],
                    [sousa_hai, p_id],
                    [sousa_hai, self.whoturn],])
                
                tumohai = random.choice(self.YAMA)
                self.YAMA.remove(tumohai)
                Player.tehai["tumo"] = tumohai
                
                info.edit("kancount", info.read()["kancount"] + 1)

            elif sousa == "chi": # チーの場合
                sh_mps, sh_n = sousa_hai[0], int(sousa_hai[1])
                ch_1 = f"{sh_mps}{sh_n+cmd[3]}"
                ch_2 = f"{sh_mps}{sh_n+cmd[4]}"
                Player.kiru(ch_1)
                Player.kiru(ch_2)
                Player.tehai["naki"].append([
                    [ch_1, p_id],
                    [ch_2, p_id],
                    [sousa_hai, self.whoturn],])
                
            elif sousa == "ron": # ロン和了
                by = yaku.best_yaku(Player, sousa_hai, self.previous_cmd[1])

                self.agari_data = {
                    "whoagari": p_id,
                    "whoagarare": self.whoturn,
                    "tehai": Player.tehai,
                    "yaku": by[1],
                    "mentu_pattern": by[0]}
                
        # フェーズ・キューの更新
        if sousa == "ignore":
            self.queue.pop(0) # キューをひとつ削除
            if self.queue == []: # もう誰も待機勢がいなくなったら
                self.phase = Phase.NEED_DRAW
            else:
                self.phase = Phase.WAIT_OTHERS
            self.capable_sousa_now = self.get_capable_sousa_now() # csnの更新
        else:
            # 何かしらの操作が発生している場合
            if sousa != "daiminkan":
                Player.tehai["tumo"] = None # 操作を行ったプレイヤーのツモ牌をNoneにする
            self.whoturn = p_id # 誰のターンかを更新する
            self.previous_cmd = cmd # 最後に直前に行われた操作を保存する

            if sousa in ["ron", "tumo"]:
                self.phase = Phase.ROUND_END
                self.queue = []
                self.capable_sousa_now = [] # csnの更新
            elif sousa in ["ankan", "kakan", "kiru", "richi"]:
                self.phase = Phase.WAIT_OTHERS
                self.queue = self.get_queue()
                self.capable_sousa_now = self.get_capable_sousa_now() # csnの更新
            elif sousa in ["pon", "chi", "daiminkan"]:
                self.phase = Phase.WAIT_SELF
                self.queue = [p_id] # ポンとかチーとかした人にアクセス権を移す
                self.capable_sousa_now = self.get_capable_sousa_now() # csnの更新
                self.whoturn = p_id
            else:
                raise Exception("do_cmd() coudn't find cmd")

        printd(self.dbg())

    def dbg(self):
        return "\n".join([P.dbg() for P in self.players])

    def finish_kyoku(self):
        # 未作成！！！
        printd("FINISHED")

    def step(self, cmd): # プレイヤー or AI の操作が必要になるまでゲームを進める
        # コマンドを実行する
        self.do_cmd(cmd)
        
        # 以下、自動進行
        while True:
            # ツモが必要
            if self.phase == Phase.NEED_DRAW:
                # ツモろうにも残り牌がなかったら局を終了する
                if len(self.YAMA) <= 4: # 残り牌が4敗以下（王牌を考慮して）になったらループを終わらせる
                    self.phase == Phase.ROUND_END
                    continue

                # ツモらせる操作
                if self.previous_cmd[1] not in ["ankan", "kakan"]:
                    self.whoturn = (self.whoturn + 1) % 4 # カンのあとでなければ下家にターンをゆずる

                tumohai = random.choice(self.YAMA)
                self.YAMA.remove(tumohai)
                self.players[self.whoturn].tehai["tumo"] = tumohai
                printd(f"{'-'*30} {self.whoturn} tumo {tumohai}")

                self.phase = Phase.WAIT_SELF # フェーズの更新
                self.queue = [self.whoturn] # キューの更新
                self.capable_sousa_now = self.get_capable_sousa_now() # csnの更新

                continue
                
            # 他家ロン／鳴き優先度決定処理
            if self.phase == Phase.WAIT_OTHERS:
                if self.queue == []:
                    self.phase = Phase.NEED_DRAW  
                    continue
                
                elif self.queue != []: # 他家の選択余地あり　→　一旦 UI へ制御返す
                    return 

            # 誰かの打牌待ち → 一旦 UI へ制御返す
            if self.phase == Phase.WAIT_SELF:
                self.queue = [self.whoturn]
                return

            # 局が終わった
            if self.phase == Phase.ROUND_END:
                return


            # 定義漏れ
            raise RuntimeError(f"未知フェーズ {self.phase}")

