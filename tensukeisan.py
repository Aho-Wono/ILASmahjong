import info
from yaku import yaku_dic
import fukeisan
from mahjong import Mahjong

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
        han += yaku_dic[yaku]["hansu"]
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
            if (han == 4 and fu >= 40) or han == 5:
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
            if (han == 4 and fu >= 40) or han == 5:
                ten_oya = 12000
            elif han == 6 or han == 7:
                ten_oya = 18000
            elif han >= 8 and han <= 10:
                ten_oya = 24000
            elif han >= 11 and han <= 12:
                ten_oya = 36000
            elif han >= 13:
                ten_oya = 48000
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
            if (han == 4 and fu >= 40) or han == 5:
                ten_oya = 8000
            elif han == 6 or han == 7:
                ten_oya = 12000
            elif han >= 8 and han <= 10:
                ten_oya = 16000
            elif han >= 11 and han <= 12:
                ten_oya = 24000
            elif han >= 13:
                ten_oya = 32000
            else:
                ten_aga = fu * pow(2, han) * 4 * 3
                ten_aga = ((ten_aga + 99) // 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == make_per:
                    tensu_data[i] = -ten_aga
    print(han, "翻", fu, "符")
    print(tensu_data)
    return [tensu_data, fu, han]