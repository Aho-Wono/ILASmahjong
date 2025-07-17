import info
from yaku import yaku_dic
import fukeisan

def tensukeisan(agari_data):
    # info.getoya() で親確認できる
    #"whoagari": p_id,
    #"whoagarare": self.whoturn,
    #"tehai": Player.tehai,
    #"yaku": by[1],
    #"mentu_pattern": by[0]})
    aga_per = agari_data["whoagari"]
    make_per = agari_data["whoagarare"]
    yaku_list = agari_data["yaku"]
    fu = fukeisan.fukeisan(PlayerInfo, menzen_pattern, agarihai)
    han = 0
    for yaku in yaku_list:
        han += yaku_dic[yaku]["hansu"]
    tensu_data = [0, 0, 0, 0] #各々のプレイヤーの得失をまとめる
    if make_per == None: #ツモのとき
        if aga_per == info.getoya(): #親があがったとき
            ten_ko = fu * pow(2, han) * 4 * 2
            ten_aga = ten_ko * 3
            ten_ko = ((ten_ko + 99) % 100) * 100
            ten_aga = ((ten_aga + 99) % 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                else:
                    tensu_data[i] = -ten_ko
        else: #子があがったとき
            ten_ko = fu * pow(2, han) * 4
            ten_oya = ten_ko * 2
            ten_aga = ten_ko * 4
            ten_ko = ((ten_ko + 99) % 100) * 100
            ten_oya = ((ten_oya + 99) % 100) * 100
            ten_aga = ((ten_aga + 99) % 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == info.getoya():
                    tensu_data[i] = -ten_oya
                else:
                    tensu_data[i] = -ten_ko
    else: #ロンのとき
        if aga_per == info.getoya(): #親があがったとき
            ten_aga = fu * pow(2, han) * 4 * 2 * 3
            ten_aga = ((ten_aga + 99) % 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == make_per:
                    tensu_data[i] = -ten_aga
        else: #子があがったとき
            ten_aga = fu * pow(2, han) * 4 * 3
            ten_aga = ((ten_aga + 99) % 100) * 100
            for i in range(4):
                if i == aga_per:
                    tensu_data[i] = ten_aga
                elif i == make_per:
                    tensu_data[i] = -ten_aga
    print(han, "翻", fu, "符")
    print(tensu_data)
    return tensu_data