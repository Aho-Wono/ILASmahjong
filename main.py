import ifagari
import info
import ripai
import random
from debug import printd
from debug import printc
import yaku


# とりあえず1局まるまる遊べるようなものを作ります
# プレイヤーの状況を包括するクラスを作成
class PlayerInfo:
    def __init__(self, playerid, tehai, kawa, status):  # コンストラクタ (初期化メソッド)
        self.playerid = playerid # プレイヤー名 
        self.tehai = tehai # 手牌の情報
        self.kawa = kawa # 河の情報
        self.status = status
        self.ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()

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
                if f != fromwho_li: result = True
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
 
        return f"{self.status} {"_".join(ripai.ripai(self.tehai["menzen"]))} [{self.tehai["tumo"]}] {nakitx} \n {kawatx}"
    
    def kiru(self, hai):
        self.tehai["menzen"].remove(hai)




class Kyoku():
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
                status= "wait", # draw, naki, wait, 
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

        if True: # デバッグ用
            self.players[0].tehai["menzen"] = "m1 m1 m1 m2 m3 m4 m5 m6 m7 m8 m9 m9 m9".split()
            self.players[1].tehai["menzen"] = "p1 p1 p1 p2 p3 p4 p5 p6 p7 p8 p9 p9 p9".split()
            self.players[2].tehai["menzen"] = "s1 s1 s1 s2 s3 s4 s5 s6 s7 s8 s9 s9 s9".split()
            self.players[3].tehai["menzen"] = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun".split()

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
        self.whoturn = info.oya() # 誰が親かで最初にツモるひとを判定する (0~4)
        
        self.phase = "hai_kiru_before"
        self.previous_cmd = None
        self.agari_data = [] # その局でだれが何をアガるかの変数


        # 親に1牌ツモらせる
        tumohai = random.choice(self.YAMA)
        self.YAMA.remove(tumohai)
        self.players[0].tehai["tumo"] = tumohai
        self.players[0].status = "tumo"

    def get_capable_sousa(self):
        printd("check capable_sousa, phase=", self.phase)
        capable_sousa_li = []

        if self.phase == "hai_kiru_before":
            # この時点で、一人だけ14牌    
            Player = self.players[self.whoturn] # 対象プレイヤーを指定
            
            # 何切る問題はいずれの状態でも可能
            for hai in Player.menzen_li():
                capable_sousa_li.append([self.whoturn, "kiru", hai])
                
            # 鳴いた後の操作でない場合、立直・ツモ・カンができる
            if Player.status == "tumo":
                # 立直判定
                if Player.ifrichi(): # 鳴いていなければ聴牌判定に入る
                    for kiruhai in Player.menzen_li(): 
                        tehai_li_copied = Player.menzen_li()[:]
                        tehai_li_copied.remove(kiruhai)
                        for hai in self.ALL_HAI:
                            if ifagari.ifagari(tehai_li_copied + [hai]):
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
                if yaku.agari_capable(Player, Player.tehai["tumo"], self.get_previous_sousa()):
                    capable_sousa_li.append([self.whoturn, "tumo", Player.tehai["tumo"]])
                
            self.phase = "hai_kiru_after"

        elif self.phase == "hai_kiru_after":
            sousa_hai = self.previous_cmd[2] # 切られた牌をGet

            # この時点で、全員が13牌
            # 捨てられた牌について、他家が操作できるかの判定を行う
            for i_op, OtherPlayer in enumerate(self.players):
                if i_op == self.whoturn: continue # 自分自身の捨て牌・カン牌にはアクションできませんボケ

                # ロン判定
                # フリテン要素について未作成！
                if yaku.agari_capable(OtherPlayer, sousa_hai, self.get_previous_sousa()):
                    capable_sousa_li.append([i_op, "ron", sousa_hai])
                
                if OtherPlayer.ifrichi(): continue # 立直していればロン判定のみで切り上げる
                
                # 立直してない場合
                # チー判定
                if i_op%4 == (self.whoturn+1)%4: # そもそも下家じゃないとチーできない
                    if len(sousa_hai) == 2: # 数牌判定
                        sh_mps, sh_n = sousa_hai[0], int(sousa_hai[1])
                        OPtm = OtherPlayer.tehai["menzen"]
                        if f"{sh_mps}{sh_n-2}" in OPtm and f"{sh_mps}{sh_n-1}" in OPtm:
                            capable_sousa_li.append([i_op, "chi", [sousa_hai, -2, -1]])
                        if f"{sh_mps}{sh_n-1}" in OPtm and f"{sh_mps}{sh_n+1}" in OPtm:
                            capable_sousa_li.append([i_op, "chi", [sousa_hai, -1, +1]])
                        if f"{sh_mps}{sh_n+1}" in OPtm and f"{sh_mps}{sh_n+2}" in OPtm:
                            capable_sousa_li.append([i_op, "chi", [sousa_hai, +1, +2]])

                           

                # ポン判定
                if OtherPlayer.tehai["menzen"].count(sousa_hai) >= 2: # 面前手牌に2個以上該当牌があったらポンできる
                    capable_sousa_li.append([i_op, "pon", sousa_hai])

                # カン判定
                if OtherPlayer.tehai["menzen"].count(sousa_hai) >= 3: # 面前手牌に3個以上該当牌があったらカンできる
                    capable_sousa_li.append([i_op, "daiminkan", sousa_hai])

            self.phase = "hai_kiru_before"

        capable_sousa_li.sort(key=lambda x: ["kiru", "richi", "tumo", "ankan", "kakan", "ron", "daiminkan", "pon", "chi"].index(x[1]))

        return capable_sousa_li

    def get_previous_sousa(self):
        if self.previous_cmd == None:
            return None
        else:
            return self.previous_cmd[0]
        
    def do_cmds(self, cmds): # ダブロン・トリロンに対応するためcmdはリストにしている
        print("do cmds:", cmds)
        
        if cmds == None: 
            self.previous_cmd = cmds # 直前に行われた操作を保存する
            return # 何もしない
        
        self.previous_cmd = cmds[0] # 直前に行われた操作を保存する
        
        for cmd in cmds:
            p_id = int(cmd[0])
            Player = self.players[p_id]
            sousa = cmd[1]
            sousa_hai = cmd[2]

            # 選択された操作に基づいて処理を行う
            if sousa in "ankan kakan richi tumo kiru".split():
                # 自分の手牌を編集する系のやつ

                if sousa == "ankan": # 暗槓
                    for i in range(4):  Player.kiru(sousa_hai)
                    Player.tehai["naki"].append([[sousa_hai, self.whoturn] for i in range(4)])
                    
                elif sousa == "kakan": # 明槓   
                    # 該当牌のインデックスの取得
                    for k_index, n in Player.naki:
                        if [nn[0] for nn in n] == [sousa_hai for i in range(3)]:
                            Player.tehai["naki"][k_index].append([sousa_hai, self.whoturn])

                elif sousa == "kiru": # 普通に切るとき
                    if Player.status == "tumo": # 鳴き後に切るときは手牌に牌を追加しない 
                        Player.tehai["menzen"].append(Player.tehai["tumo"]) # ここで一度14牌にし、ツモ切りにも対応する
                    Player.kiru(sousa_hai)
                    Player.kawa.append([sousa_hai, False])

                elif sousa == "richi": # 立直
                    Player.tehai["menzen"].append(Player.tehai["tumo"])
                    Player.kiru(sousa_hai)
                    Player.kawa.append([sousa_hai, True])
                
                elif sousa == "tumo": # ツモ和了
                    self.agari_data.append({
                        "whoagari": self.whoturn,
                        "whoagarare": None,
                        "tehai": Player.tehai,
                        "yaku":  yaku.best_yaku(Player, Player.tehai["tumo"], self.get_previous_sousa()), })
                    
                Player.status = "wait"
            else:
                # 他人の捨て牌を鳴く系のやつ

                if sousa == "pon": # ポンの場合
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
                    info.edit("kancount", info.read()["kancount"] + 1)

                elif sousa == "chi": # チーの場合
                    sh_mps, sh_n = sousa_hai[0][0], int(sousa_hai[0][1])
                    Player.kiru(f"{sh_mps}{sh_n+sousa_hai[1]}")
                    Player.kiru(f"{sh_mps}{sh_n+sousa_hai[2]}")
                    Player.tehai["naki"].append([
                        [f"{sh_mps}{sh_n+sousa_hai[1]}", p_id],
                        [f"{sh_mps}{sh_n+sousa_hai[2]}", p_id],
                        [sousa_hai[0], self.whoturn],])
                    
                elif sousa == "ron": # ロン和了
                    self.agari_data.append({
                        "whoagari": p_id,
                        "whoagarare": self.whoturn,
                        "tehai": Player.tehai,
                        "yaku":  yaku.best_yaku(Player, sousa_hai, sousa), })

                    
                Player.status = "naki"
                
        # 最後にプレイヤーのツモ牌をNoneにし、ステータスをwaitにし、誰のターンかを更新する
        # ロンの場合はここらへんがぐちゃぐちゃになってしまうので奇妙な対策をする
        if len(cmds) != 1:
            Player.tehai["tumo"] = None
            Player.status = "wait"
            self.whoturn = p_id


    def step(self):
        if self.previous_cmd == None:
            # 前の操作がなければ次のひとにツモらせる
            self.whoturn = (self.whoturn + 1) % 4 # 下家にターンをゆずる
            Player = self.players[self.whoturn]

            tumohai = random.choice(self.YAMA)
            self.YAMA.remove(tumohai)
            Player.tehai["tumo"] = tumohai
            Player.status = "tumo"
            for i in [0,1,2,3]:
                if i != self.whoturn:
                    self.players[i].status = "wait"
        
    def dbg(self):
        for P in self.players: printd(P.dbg())



# 半荘の開始
printd("HANCHAN STARTED")
# infoの初期化
info.edit("kyoku", "t1")
info.edit("hon", 0)

while True:
    # 局の初期化
    Game = Kyoku()
    Game.reset_kyoku()
    while True:
        # プレイヤーができる操作を取得する
        capable_sousa_li = Game.get_capable_sousa()
        
        if capable_sousa_li == []: # プレイヤーの選択余地がなかったら
            cmds = None
        else:
            # プレイヤーに選択させる
            Game.dbg()
            print("capable_sousa_li:", capable_sousa_li)
            
            cmds = [input("INPUT CMD [who, sousa, hai]: ").split()]
            if cmds == [""]: cmds = None

        # プレイヤーのコマンドを実行する
        Game.do_cmds(cmds)



        # 局が終わるかの判定をここで行う
        # 誰かがアガってたら終了
        if Game.agari_data != []: 
            printd(Game.agari_data)
            break
        # 残りのツモ牌がなかったら終了
        if Game.previous_cmd == None and len(Game.YAMA) <= 4:
            # 流し満貫の判定
            # 未作成！
            break

        # プレイヤーの操作が絡む場所までゲームをすすめる
        Game.step()
    
    printd(f"FINISH {info.read()["kyoku"].upper()}")

    # 点数計算・点棒のやりとり
    oyakeep = False
    # 流局かそうでないかで場合分け
    if len(Game.agari_data) == 0: 
        printd("RYUKYOKU(?)")
        # 流し満貫の判定
        # 未作成！！！
        if False:
            Game.agari_data.append(
                {
                    "hogehoge"
                }
            )
    if len(Game.agari_data) != 0:
        printd("AGARI")
        # 親がキープされるかの判定
        for agd in Game.agari_data:
            if agd["whoagari"] == info.getoya():
                oyakeep = True    
            # 点数計算・点棒移動の処理  
            # 未作成！！
    
    # 次局のためのinfo編集
    if oyakeep: # 親キープの場合
        info.edit("hon", info.read()["hon"] + 1)
    else: # 親が流れる場合
        kyoku_li = ["t1", "t2", "t3", "t4", "n1", "n2", "n3", "n4"]
        now_kyoku_index = kyoku_li.index(info.read()["kyoku"])
        if now_kyoku_index == 7: # 半荘消化終わり
            break
        else:
            info.edit("kyoku", kyoku_li[now_kyoku_index+1])
                        
    # 箱割れが発生したらbreak
    # 未作成！！！
    if False:
        break
printd("HANCHAN FINISHED")