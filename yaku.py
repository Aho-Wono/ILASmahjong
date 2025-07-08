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

yaku_debug_mode = False

def yaku_printd(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    if yaku_debug_mode:
        print(*args, sep=sep, end=end, file=file, flush=flush)


# いろんなデータを渡して、役の組み合わせを出力する関数
def yaku(PlayerInfo, agarihai, sousa): # 引数は二つ、ロンでもツモでも槍槓でも対応できるようにPlayerInfoとアガる予定の牌の2つを渡す
    #debug.printd("[yaku fn roaded]")
    yaku_pattern_li = []
    
    playerid = PlayerInfo.playerid
    menzen = PlayerInfo.tehai["menzen"]
    naki = PlayerInfo.tehai["naki"]
    tumo = PlayerInfo.tehai["tumo"]
    kawa = PlayerInfo.kawa

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
    if not ifagari.ifagari(integrated_tehai):
        return yaku_pattern_li
    else: yaku_printd("ifagari is valuable.")

    # ありうる分割パターンぶんためす
    yaku_printd("try menzen_patterns;")
    for m in menzen_pattern_li: yaku_printd(m)
    for menzen_pattern in menzen_pattern_li:
        yaku_printd("=== menzen_pattern ", menzen_pattern)
        debug.printd("=== menzen_pattern ", menzen_pattern)
        yaku_pattern = []

        # 暗槓ロン判定（国士のみ）を行う
        # まず国士判定（あらゆる場合でアガれる）
        yaochuhai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun".split()
        if menzen_pattern[0] == yaochuhai and menzen_pattern[1][0] in yaochuhai:
            yaku_pattern.append("国士無双")

        # sousaが暗槓後で出アガリ形なら、国士を除いて門前払いする
        if sousa == "ankan" and tumo == None and yaku_pattern != ["国士無双"]: # 一応国士の場合でもドラの計上などを残す
            continue

        # 特別な役(ドラ、裏ドラ、槍槓、嶺上開花)の判定を行う    
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
            if hai in dora_omote_valid: yaku_pattern.append("ドラ")
            if hai in dora_ura_valid and (not PlayerInfo.ifnaki()):   yaku_pattern.append("裏ドラ")



        # それぞれの役モジュールをインポートして、成立する役のパターンを取得する
        dotpy_files = list(getdir.dir().glob('*.py'))
        for pyfilepath in dotpy_files:
            filename = Path(pyfilepath).stem
            if "y_" in filename: # ここでのファイル
                module = importlib.import_module(filename)   # ← ここがポイント
                fn = getattr(module, filename)
                try:
                    result = fn(PlayerInfo= PlayerInfo, menzen_pattern= menzen_pattern, agarihai= agarihai) # 役の名前もしくはFalseが返ってくる
                    yaku_printd(f"about: {filename} -> {result}")
                except Exception as e:
                    result = False
                    yaku_printd(f"about: {filename} -> ERROR: {e}")
                
                if result != False:
                    yaku_pattern.append(result)
        yaku_printd("yaku_pattern:", yaku_pattern)

        yaku_pattern_li.append(yaku_pattern)
        

    yaku_printd(f"yaku_pattern_li: {yaku_pattern_li}")
    return yaku_pattern_li

# PlayerInfoとアガリ牌を渡せば、それらの情報から和了系の役があるかどうかをTrue/Falseで返す
def agari_capable(PlayerInfo, agarihai, sousa):
    teyaku_li = [name for name, info in yaku_dic.items() if info["teyaku"]]

    ag_cp = False
    yaku_pattern_li = yaku(PlayerInfo, agarihai, sousa)
    for yaku_pattern in yaku_pattern_li:
        if any([(y in teyaku_li) for y in yaku_pattern]):
            ag_cp = True
    return ag_cp

# 役の組み合わせからどれが最も役数が高くなるか言ってくれるやつ～
def best_yaku(PlayerInfo, agarihai, sousa):
    yaku_pattern_li = yaku(PlayerInfo, agarihai, sousa)
    if len(yaku_pattern_li) == 0: return None # そもそも役がなければNoneを返す
    max_yp = None
    max_hansu = 0
    for yp in yaku_pattern_li:
        hansu = 0
        for y in yp:
            hansu += yaku_dic[y]["hansu"]
        if hansu >= max_hansu: max_yp = yp
    return max_yp
    # 未作成！

if False:

    class PlayerInfo:
        def __init__(self, playerid, tehai, kawa):  # コンストラクタ (初期化メソッド)
            self.playerid = playerid # プレイヤー名 
            self.tehai = tehai # 手牌の情報
            self.kawa = kawa # 河の情報
    TestPlayer = PlayerInfo(
        playerid= 0, # ← 0が親
        tehai= {"menzen": [],
                "naki": [],
                "tumo": None
                },
        kawa= []
        )

    debug_patterns = [
        #["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8 m9 m9 m9".split(), [], None, "m9"],  
        ["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8".split(), [[["ton", 0], ["ton", 0], ["ton", 1]]], None, "m9"], 
        ["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8".split(), [[["ton", 0], ["ton", 0], ["ton", 1], ["ton", 0]]], None, "m9"], 
        #["m1 m1 m1 m2 m3 p7 p8 p9 s9 s9 s9 sha sha".split(), [], "sha", "sha"],
        #["m1 m1 m1 m2 m3 m7 m8 m9 s7 s8 s9 p7 p8".split(), [], None, "p9"],    
        #["m2 m2 m3 m3 m4 m4 m5 m5 m6 m6 m7 m8 m8".split(), [], "m7", "m7"],    
    ]

    yaku_debug_mode = False

    for i, dp in enumerate(debug_patterns):
        TestPlayer.tehai["menzen"] = dp[0]
        TestPlayer.tehai["naki"] = dp[1]
        TestPlayer.tehai["tumo"] = dp[2]
        ag = dp[3]

        yaku_printd(f"[ {i+1} ]","="*100)

        yaku_printd(yaku(PlayerInfo= TestPlayer, agarihai=ag))