import y_honroto
import y_junchan_2
import y_junchan_3
def y_chanta_1(PlayerInfo, menzen_pattern, agarihai):
    if y_honroto.y_honroto(PlayerInfo, menzen_pattern, agarihai) or y_junchan_2.y_junchan_2(PlayerInfo, menzen_pattern, agarihai) or y_junchan_3.y_junchan_3(PlayerInfo, menzen_pattern, agarihai):
        return False
    if not PlayerInfo.ifnaki():
        return False
    if len(menzen_pattern) == 7:
        return False
    naki = PlayerInfo.tehai["naki"]
    for menz in menzen_pattern:
        flag = True
        for item in menz:
            if len(item) == 2:
                i = int(item[1])
                if i == 1 or i == 9:
                    flag = False
            else:
                flag = False
        if flag:
            return False
    for naki_i in naki:
        flag = True
        for item in naki_i:
            if len(item[0]) == 2:
                i = int(item[0][1])
                if i == 1 or i == 9:
                    flag = False
            else: 
                flag = False
        if flag:
            return False
    return "混全帯么九_1"