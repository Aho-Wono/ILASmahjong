import ifagari
import ripai
import info
import debug
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

def yaku(PlayerInfo, agarihai): # 引数は二つ、ロンでもツモでも槍槓でも対応できるようにPlayerInfoとアガる予定の牌の2つを渡す
    yaku_pattern_li = []
    
    menzen = PlayerInfo.tehai["menzen"]
    naki = PlayerInfo.tehai["naki"]
    tumo = PlayerInfo.tehai["tumo"]
    kawa = PlayerInfo.kawa
    menzen_pattern_li = mentsu_pattern(menzen)

    for menzen_pattern in menzen_pattern_li:
        yaku_pattern = []

        # それぞれの役モジュールをインポートして、成立する役のパターンを取得する
        dotpy_files = list(getdir.dir().glob('*.py'))
        for pyfilepath in dotpy_files:
            filename = Path(pyfilepath).stem
            if "y_" in filename: # ここでのファイル
                module = importlib.import_module(filename)   # ← ここがポイント
                fn = getattr(module, filename)
                result = fn(menzen_pattern, naki, kawa, agarihai)
                
                if result != False:
                    yaku_pattern.append(result)
        
        yaku_pattern_li.append(yaku_pattern)
        

    debug.printd(f"yaku_pattern_li: {yaku_pattern_li}")
    return yaku_pattern_li

