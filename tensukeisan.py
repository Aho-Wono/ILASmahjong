import info
from yaku import yaku_dic
import fukeisan
from mahjong import Mahjong
from debug import printd

def yakuhai_count(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    kyoku = info.read()["kyoku"]
    player = PlayerInfo.playerid
    kazehai = ["ton" , "nan" , "sha" , "pei"]
    yakuhai = ["haku" , "hatu" , "chun"]
    zikaze_keisan = (int(player)-(int(kyoku[1])-1))%4
    if kyoku[0] == "t":
        yakuhai.append(kazehai[0])
    elif kyoku[0] == "n":
        yakuhai.append(kazehai[1])
    elif kyoku[0] == "s":
        yakuhai.append(kazehai[2])
    elif kyoku[0] == "p":
        yakuhai.append(kazehai[3])
    yakuhai.append(kazehai[zikaze_keisan])
    count = 0
    for menz in menzen_pattern:
        for ya in yakuhai:
            if menz[0] == ya:
                count += 1
    for menz in naki:
        for ya in yakuhai:
            if menz[0][0] == ya:
                count += 1
    return count

def tensukeisan(Game:Mahjong):
    agari_data = Game.agari_data
    # info.getoya() で親確認できる
    #"whoagari": p_id,
    #"whoagarare": self.whoturn,
    #"tehai": Player.tehai,
    #"yaku": by[1],
    #"mentu_pattern": by[0]})
    
    aga_per = agari_data["whoagari"]
    make_per = agari_data["whoagarare"]
    yaku_list = agari_data["yaku"]
    mentsu_pattern = agari_data["mentu_pattern"]
    agarihai = agari_data["agarihai"]


    fu = fukeisan.fukeisan(Game.players[aga_per],mentsu_pattern, agarihai)
    han = 0
    for yaku in yaku_list:
        if yaku == "役牌":
            continue
        han += yaku_dic[yaku]["hansu"]
    han += yakuhai_count(Game.players[aga_per], mentsu_pattern, agarihai)
    tensu_data = [0, 0, 0, 0] #各々のプレイヤーの得失をまとめる
    if make_per == None: #ツモのとき
        if aga_per == info.getoya(): #親があがったとき
            ten_ko = 0
            ten_aga = 0
            if (han == 4 and fu >= 40) or (han == 3 and fu >= 70) or han == 5:
                ten_oya = 12000
                ten_ko = 4000
            elif han == 6 or han == 7:
                ten_oya = 18000
                ten_ko = 6000
            elif han >= 8 and han <= 10:
                ten_oya = 24000
                ten_ko = 8000
            elif han >= 11 and han <= 12:
                ten_oya = 36000
                ten_ko = 12000
            elif han >= 13:
                ten_oya = 48000
                ten_ko = 16000
            else:
                ten_ko = fu * pow(2, han) * 4 * 2
                ten_aga = ten_ko * 3
                ten_ko = ((ten_ko + 99) // 100) * 100
                ten_aga = ((ten_aga + 99) // 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                else:
                    tensu_data[i] = -ten_ko
        else: #子があがったとき
            ten_ko = 0
            ten_aga = 0
            ten_oya = 0
            if (han == 4 and fu >= 40) or (han == 3 and fu >= 70) or han == 5:
                ten_aga = 8000
                ten_ko = 2000
                ten_oya = 4000
            elif han == 6 or han == 7:
                ten_aga = 12000
                ten_ko = 3000
                ten_oya = 6000
            elif han >= 8 and han <= 10:
                ten_aga = 16000
                ten_ko = 4000
                ten_oya = 8000
            elif han >= 11 and han <= 12:
                ten_aga = 24000
                ten_ko = 6000
                ten_oya = 12000
            elif han >= 13:
                ten_aga = 32000
                ten_ko = 8000
                ten_oya = 16000
            else:
                ten_ko = fu * pow(2, han) * 4
                ten_oya = ten_ko * 2
                ten_aga = ten_ko * 4
                ten_ko = ((ten_ko + 99) // 100) * 100
                ten_oya = ((ten_oya + 99) // 100) * 100
                ten_aga = ((ten_aga + 99) // 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == info.getoya():
                    tensu_data[i] = -ten_oya
                else:
                    tensu_data[i] = -ten_ko
    else: #ロンのとき
        if aga_per == info.getoya(): #親があがったとき
            ten_aga = 0
            if (han == 4 and fu >= 40) or (han == 3 and fu >= 70) or han == 5:
                ten_aga = 12000
            elif han == 6 or han == 7:
                ten_aga = 18000
            elif han >= 8 and han <= 10:
                ten_aga = 24000
            elif han >= 11 and han <= 12:
                ten_aga = 36000
            elif han >= 13:
                ten_aga = 48000
            else:
                ten_aga = fu * pow(2, han) * 4 * 2 * 3
                ten_aga = ((ten_aga + 99) // 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == make_per:
                    tensu_data[i] = -ten_aga
        else: #子があがったとき
            ten_aga = 0
            if (han == 4 and fu >= 40) or (han == 3 and fu >= 70) or han == 5:
                ten_aga = 8000
            elif han == 6 or han == 7:
                ten_aga = 12000
            elif han >= 8 and han <= 10:
                ten_aga = 16000
            elif han >= 11 and han <= 12:
                ten_aga = 24000
            elif han >= 13:
                ten_aga = 32000
            else:
                ten_aga = fu * pow(2, han) * 4 * 4
                ten_aga = ((ten_aga + 99) // 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == make_per:
                    tensu_data[i] = -ten_aga

    printd(han, "翻", fu, "符")
    printd(tensu_data, end=" → ")

    # 何本場の処理を追加（ゴリ押し）
    zero_count = tensu_data.count(0)
    if zero_count == 0: # ツモ
        for i, t in enumerate(tensu_data[:]):
            if t<0:   tensu_data[i] += info.read()["hon"]*100
            elif t>0: tensu_data[i] += info.read()["hon"]*300
    else: # ロン
        for i, t in enumerate(tensu_data[:]):
            if t<0:   tensu_data[i] += info.read()["hon"]*300
            elif t>0: tensu_data[i] += info.read()["hon"]*300

    printd(tensu_data)
    return [tensu_data, fu, han]