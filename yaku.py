import ifagari
import ripai
import info
import debug
import getdir
import glob
from pathlib import Path
import importlib
import mentsu_pattern
import sys
import ys_haiteimoyue
import ys_hoteiraoyui
import ys_tenho
import ys_tiho

ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()

# PlayerInfoのクラスが渡されたら、info.jsonなどの総合的な情報から成立する役を返す関数yaku(Player)を作ろうと思います
# それが手役かどうかはmainの中で判定します

# ILAS麻雀で扱う役はこのWikipediaの記事に載ってる役のうち、「主な役」と「流し満貫」のみに限定するつもりです
# https://ja.wikipedia.org/wiki/%E9%BA%BB%E9%9B%80%E3%81%AE%E5%BD%B9%E4%B8%80%E8%A6%A7
# プログラム上での役の扱いは、バグが怖いですが表記ゆれを防ぐためすべて漢字の文字列で扱いたいと思います

# いちいち参照するのめんどくさいと思うので辞書形式にしました
yaku_dic = {
    # 一飜役
    "立直":         {"teyaku": True, "hansu": 1},
    "一発":         {"teyaku": False, "hansu": 1},
    "門前清自摸和": {"teyaku": True, "hansu": 1},
    "断么九":       {"teyaku": True, "hansu": 1},
    "平和":         {"teyaku": True, "hansu": 1},
    "一盃口":       {"teyaku": True, "hansu": 1},
    "役牌":         {"teyaku": True, "hansu": 1},  # 白 發 中・自風・場風
    "嶺上開花":     {"teyaku": True, "hansu": 1},
    "槍槓":         {"teyaku": True, "hansu": 1},
    "海底摸月":     {"teyaku": True, "hansu": 1},
    "河底撈魚":     {"teyaku": True, "hansu": 1},
    "ドラ":         {"teyaku": False, "hansu": 1},
    "裏ドラ":       {"teyaku": False, "hansu": 1},

        "混全帯么九_1":   {"teyaku": True, "hansu": 1},
        "一気通貫_1":     {"teyaku": True, "hansu": 1},
        "三色同順_1":     {"teyaku": True, "hansu": 1},

        

    # 二飜役
    "七対子":       {"teyaku": True, "hansu": 2},
    "対々和":       {"teyaku": True, "hansu": 2},
    "三暗刻":       {"teyaku": True, "hansu": 2},
    "三槓子":       {"teyaku": True, "hansu": 2},
    "三色同刻":     {"teyaku": True, "hansu": 2},
    "混老頭":       {"teyaku": True, "hansu": 2},
    "小三元":       {"teyaku": True, "hansu": 2},
    "ダブル立直":   {"teyaku": True, "hansu": 2},

    
        "三色同順_2":     {"teyaku": True, "hansu": 2},
        "一気通貫_2":     {"teyaku": True, "hansu": 2},
        "混全帯么九_2":   {"teyaku": True, "hansu": 2},
        
        "純全帯么九_2":   {"teyaku": True, "hansu": 2},
        "混一色_2":       {"teyaku": True, "hansu": 2},

    # 三飜役
    "二盃口":       {"teyaku": True, "hansu": 3},
    
        "純全帯么九_3":   {"teyaku": True, "hansu": 3},
        "混一色_3":       {"teyaku": True, "hansu": 3},

    # 四飜役
    "流し満貫":     {"teyaku": True, "hansu": 4},

    # 五飜役
        "清一色_5":       {"teyaku": True, "hansu": 5},
        
    # 六飜役
        "清一色_6":       {"teyaku": True, "hansu": 6},

    # 役満（13飜相当）
    "国士無双":     {"teyaku": True, "hansu": 13},
    "四暗刻":       {"teyaku": True, "hansu": 13},
    "大三元":       {"teyaku": True, "hansu": 13},
    "小四喜":       {"teyaku": True, "hansu": 13},
    "大四喜":       {"teyaku": True, "hansu": 13},
    "字一色":       {"teyaku": True, "hansu": 13},
    "緑一色":       {"teyaku": True, "hansu": 13},
    "清老頭":       {"teyaku": True, "hansu": 13},
    "四槓子":       {"teyaku": True, "hansu": 13},
    "九蓮宝燈":     {"teyaku": True, "hansu": 13},
    "天和":         {"teyaku": True, "hansu": 13},
    "地和":         {"teyaku": True, "hansu": 13},
}

def teyaku_li():
    tyk_li = []
    for yaku in list(yaku_dic):
        if yaku_dic[yaku]["teyaku"]: tyk_li.append(yaku)
    return tyk_li

def yakuman():
    ykm_li = []
    for yaku in list(yaku_dic):
        if yaku_dic[yaku]["hansu"] == 13: ykm_li.append(yaku)
    return ykm_li

# デバッグ用print関数
def yaku_printd(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    if False:
        print(*args, sep=sep, end=end, file=file, flush=flush)


# いろんなデータを渡して、役の組み合わせを出力する関数
def yaku(players, p_id, agarihai, sousa=None, mpmode= False): # 引数は二つ、ロンでもツモでも槍槓でも対応できるようにPlayerInfoとアガる予定の牌の2つを渡す
    #debug.printd("[yaku fn roaded]")
    #debug.printd(PlayerInfo.dbg(), agarihai, sousa)
    
    yaku_pattern_li = []
    
    playerid = players[p_id].playerid
    menzen = players[p_id].tehai["menzen"]
    naki = players[p_id].tehai["naki"]
    tumo = players[p_id].tehai["tumo"]
    kawa = players[p_id].kawa
    
    menzen_pattern_li = mentsu_pattern.mentsu_pattern(menzen + [agarihai])
    
    # アガリ系じゃなかったら空のyaku_pattern_liを返す
    integrated_tehai = menzen[:] # いっかいキレイな形の手牌を作成してifagariに渡す
    for n in naki:
        if len(n) == 3: # カン以外の場合
            for nn in n:
                integrated_tehai.append(nn[0])
        elif len(n) == 4: # カンの場合
            integrated_tehai.extend([n[0][0], n[0][0], n[0][0]])
    integrated_tehai.append(agarihai)
    yaku_printd("integrated: ", integrated_tehai)
    if not ifagari.ifagari(integrated_tehai): # そもそも渡されたデータがアガリ形やなかった場合
        return yaku_pattern_li
    else: yaku_printd("ifagari is valuable.")

    # ありうる分割パターンぶんためす
    yaku_printd("try menzen_patterns;")
    for m in menzen_pattern_li: yaku_printd(m)
    for menzen_pattern in menzen_pattern_li:
        yaku_printd("=== menzen_pattern ", menzen_pattern)
        yaku_pattern = []

        # 暗槓ロン判定（国士のみ）を行う
        # まず国士判定（あらゆる場合でアガれる）
        yaochuhai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun".split()
        if menzen_pattern[0] == yaochuhai and menzen_pattern[1][0] in yaochuhai:
            yaku_pattern.append("国士無双")

        # sousaが暗槓後で出アガリ形なら、国士を除いて門前払いする
        if sousa == "ankan" and tumo == None and yaku_pattern != ["国士無双"]: # 一応国士の場合でもドラの計上などを残す
            continue

        # 特別な役(ドラ、裏ドラ、槍槓、嶺上開花、一発)の判定を行う    
        # 嶺上開花
        if sousa in ["ankan", "kakan", "daiminkan"] and tumo != None:
            yaku_pattern.append("嶺上開花")
        # 槍槓
        if sousa == "daiminkan" and tumo == None:
            yaku_pattern.append("槍槓")
        # ドラ
        dorasu = info.read()["kancount"] + 1
        dora_omote_valid = info.read()["dora_omote"][:dorasu]
        dora_ura_valid = info.read()["dora_ura"][:dorasu]
        saladbowl = menzen[:] # 手牌を物理的にぶち込んだリストを作る
        for n in naki:
                for nn in n:
                    saladbowl.append(nn[0])
        saladbowl.append(agarihai)
        for hai in saladbowl:
            hai_mae = ALL_HAI[ALL_HAI.index(hai)-1] # 一個前の牌を取得
            if hai_mae in dora_omote_valid: yaku_pattern.append("ドラ")
            if hai_mae in dora_ura_valid and players[p_id].ifrichi():   yaku_pattern.append("裏ドラ")
        
        
        #天和地和など特殊な情報が必要な役を判定
        if ys_haiteimoyue.ys_haiteimoyue(players, p_id, menzen_pattern, agarihai):
            yaku_pattern.append(ys_haiteimoyue.ys_haiteimoyue(players, p_id, menzen_pattern, agarihai))
        if ys_hoteiraoyui.ys_hoteiraoyui(players, p_id, menzen_pattern, agarihai):
            yaku_pattern.append(ys_hoteiraoyui.ys_hoteiraoyui(players, p_id, menzen_pattern, agarihai))
        if ys_tenho.ys_tenho(players, p_id, menzen_pattern, agarihai):
            yaku_pattern.append(ys_tenho.ys_tenho(players, p_id, menzen_pattern, agarihai))
        if ys_tiho.ys_tiho(players, p_id, menzen_pattern, agarihai):
            yaku_pattern.append(ys_tiho.ys_tiho(players, p_id, menzen_pattern, agarihai))


        # それぞれの役モジュールをインポートして、成立する役のパターンを取得する
        dotpy_files = list(getdir.dir().glob('*.py'))
        for pyfilepath in dotpy_files:
            filename = Path(pyfilepath).stem
            if "y_" in filename: # ここでのファイル
                module = importlib.import_module(filename)   # ← ここがポイント
                fn = getattr(module, filename)
                try:
                    result = fn(PlayerInfo= players[p_id], menzen_pattern= menzen_pattern, agarihai= agarihai) # 役の名前もしくはFalseが返ってくる
                    yaku_printd(f"about: {filename} -> {result}")
                except Exception as e:
                    result = False
                    yaku_printd(f"about: {filename} -> ERROR: {e}")
                
                if result != False:
                    yaku_pattern.append(result)
        yaku_printd("yaku_pattern:", yaku_pattern)

        if mpmode:
            yaku_pattern_li.append([menzen_pattern, yaku_pattern])
        else:
            yaku_pattern_li.append(yaku_pattern)    

    yaku_printd(f"yaku_pattern_li: {yaku_pattern_li}")
    return yaku_pattern_li

# PlayerInfoとアガリ牌を渡せば、それらの情報から和了系の役があるかどうかをTrue/Falseで返す
def agari_capable(players, p_id, agarihai, sousa):
    teyaku_li = [name for name, info in yaku_dic.items() if info["teyaku"]]

    ag_cp = False
    yaku_pattern_li = yaku(players, p_id, agarihai, sousa)
    for yaku_pattern in yaku_pattern_li:
        if any([(y in teyaku_li) for y in yaku_pattern]):
            ag_cp = True
    return ag_cp

# 役の組み合わせからどれが最も役数が高くなるか言ってくれるやつ～（点数処理の関係でベスト時のmenzen_patternも返すような関数にします）
def best_yaku(players, p_id, agarihai, sousa):
    yaku_pattern_li_and_mentsu_pattern = yaku(players, agarihai, sousa, mpmode=True)
    
    if len(yaku_pattern_li_and_mentsu_pattern) == 0: return None # そもそも役がなければNoneを返す
    max_yp_mp = None
    max_hansu = 0
    for yplamp in yaku_pattern_li_and_mentsu_pattern:
        yp = yplamp[1]
        hansu = 0
        for y in yp:
            hansu += yaku_dic[y]["hansu"]
        if hansu >= max_hansu: 
            max_yp_mp = yplamp
    return max_yp_mp
    # 未作成！


if __name__ == "__main__":
    from mahjong import PlayerInfo

    TestPlayer = [PlayerInfo(
        playerid= i, # ← 0が親
        tehai= {"menzen": [],
                "naki": [],
                "tumo": None
                },
        kawa= []
        ) for i in [0,1,2,3]]

    debug_patterns = [
        #["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8 m9 m9 m9".split(), [], None, "m9"],  
        ["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8".split(), [[["ton", 0], ["ton", 0], ["ton", 1]]], None, "m9"], 
        #["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8".split(), [[["ton", 0], ["ton", 0], ["ton", 1], ["ton", 0]]], None, "m9"], 
        #["m1 m1 m1 m2 m3 p7 p8 p9 s9 s9 s9 sha sha".split(), [], "sha", "sha"],
        #["m1 m1 m1 m2 m3 m7 m8 m9 s7 s8 s9 p7 p8".split(), [], None, "p9"],    
        #["m2 m2 m3 m3 m4 m4 m5 m5 m6 m6 m7 m8 m8".split(), [], "m7", "m7"],    
    ]

    debug.printd(debug_patterns)
    for i, dp in enumerate(debug_patterns):
        TestPlayer[0].tehai["menzen"] = dp[0]
        TestPlayer[0].tehai["naki"] = dp[1]
        TestPlayer[0].tehai["tumo"] = dp[2]
        ag = dp[3]
        TestPlayer[0].kawa = []

        debug.printd(f"[ {i+1} ]","="*100)
        debug.printd(yaku(players= TestPlayer, p_id=0, agarihai=ag))
