import ifagari
import ripai
import info
from debug import printd
from debug import printc
import getdir
import glob
from pathlib import Path
import importlib
import mentsu_pattern

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

    # 二飜役
    "三色同順":     {"teyaku": True, "hansu": 2},
    "一気通貫":     {"teyaku": True, "hansu": 2},
    "混全帯么九":   {"teyaku": True, "hansu": 2},
    "七対子":       {"teyaku": True, "hansu": 2},
    "対々和":       {"teyaku": True, "hansu": 2},
    "三暗刻":       {"teyaku": True, "hansu": 2},
    "三槓子":       {"teyaku": True, "hansu": 2},
    "三色同刻":     {"teyaku": True, "hansu": 2},
    "混老頭":       {"teyaku": True, "hansu": 2},
    "小三元":       {"teyaku": True, "hansu": 2},
    "ダブル立直":   {"teyaku": True, "hansu": 2},

    # 三飜役
    "混一色":       {"teyaku": True, "hansu": 3},
    "純全帯么九":   {"teyaku": True, "hansu": 3},
    "二盃口":       {"teyaku": True, "hansu": 3},

    # 四飜役
    "流し満貫":     {"teyaku": True, "hansu": 4},

    # 六飜役
    "清一色":       {"teyaku": True, "hansu": 6},

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

# PlayerInfoとアガリ牌を渡せば、それらの情報から和了系の役があるかどうかをTrue/Falseで返す
def agari_capable(PlayerInfo, agarihai):
    teyaku_li = [name for name, info in yaku_dic.items() if info["teyaku"]]

    ag_cp = False
    yaku_pattern_li = yaku(PlayerInfo, agarihai)
    for yaku_pattern in yaku_pattern_li:
        if any([(y in teyaku_li) for y in yaku_pattern]):
            ag_cp = True
    return ag_cp

def yaku(PlayerInfo, agarihai): # 引数は二つ、ロンでもツモでも槍槓でも対応できるようにPlayerInfoとアガる予定の牌の2つを渡す
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
                integrated_tehai.append(n[0])
        elif len(n) == 4: # カンの場合
            integrated_tehai.extend([n[0], n[0], n[0]])
    integrated_tehai.append(agarihai)
    printd("integrated: ", integrated_tehai)
    if not ifagari.ifagari(integrated_tehai):
        return yaku_pattern_li
    else: printd("ifagari is valuable.")

    # ありうる分割パターンぶんためす
    printd("try menzen_patterns;")
    for m in menzen_pattern_li: printd(m)
    for menzen_pattern in menzen_pattern_li:
        printd("=== menzen_pattern ", menzen_pattern)
        yaku_pattern = []
        
        # 特別な役(ドラ、裏ドラ、槍槓をyaku_patternに追加する)
        



        # それぞれの役モジュールをインポートして、成立する役のパターンを取得する
        dotpy_files = list(getdir.dir().glob('*.py'))
        for pyfilepath in dotpy_files:
            filename = Path(pyfilepath).stem
            if "y_" in filename: # ここでのファイル
                module = importlib.import_module(filename)   # ← ここがポイント
                fn = getattr(module, filename)
                try:
                    result = fn(PlayerInfo= PlayerInfo, menzen_pattern= menzen_pattern, agarihai= agarihai) # 役の名前もしくはFalseが返ってくる
                    printd(f"about: {filename} -> {result}")
                except Exception as e:
                    result = False
                    printd(f"about: {filename} -> ERROR: {e}")
                
                if result != False:
                    yaku_pattern.append(result)
        printd("yaku_pattern:", yaku_pattern)

        yaku_pattern_li.append(yaku_pattern)
        

    printd(f"yaku_pattern_li: {yaku_pattern_li}")
    return yaku_pattern_li

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
    ["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8 m9 m9 m9".split(), [], None, "m9"],     # パターン: 1
    ["m1 m1 m1 m2 m3 m4 m5 m6 m7 m8 ton ton ton".split(), [], None, "m9"],  # パターン: 2
    ["m1 m1 m1 m2 m3 p7 p8 p9 s9 s9 s9 sha sha".split(), [], "sha", "sha"], # パターン: 3
    ["m1 m1 m1 m2 m3 m7 m8 m9 s7 s8 s9 p7 p8".split(), [], None, "p9"],     # パターン: 4
    ["m2 m2 m3 m3 m4 m4 m5 m5 m6 m6 m7 m8 m8".split(), [], "m7", "m7"],     # パターン: 5
]

for i, dp in enumerate(debug_patterns):
    TestPlayer.tehai["menzen"] = dp[0]
    TestPlayer.tehai["naki"] = dp[1]
    TestPlayer.tehai["tumo"] = dp[2]
    ag = dp[3]

    printd(f"[ {i+1} ]","="*100)

    print(yaku(PlayerInfo= TestPlayer, agarihai=ag))