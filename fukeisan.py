import y_pinfu
import y_menzentumo
import info

def atama(PlayerInfo, menzen_pattern, agarihai):
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
    for menz in menzen_pattern:
        if len(menz) == 2:
            for ya in yakuhai:
                if menz[0] == ya:
                    return True
    return False

def kokushi(PlayerInfo, menzen_pattern, agarihai):
    yaochuhai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun".split()
    if menzen_pattern[0] == yaochuhai and menzen_pattern[1][0] in yaochuhai:
        return True
    return False

def haikei(s:str):#2~8のときTrue, それいがいFalse
    if len(s) != 2:
        return False
    if int(s[1]) == 1 and int(s[1]) == 9:
        return False
    return True

def ryanmen(PlayerInfo, menzen_pattern, agarihai):
    if len(agarihai) != 2:
        return False
    flag = False
    for menz in menzen_pattern:
        flag_1 = False
        for item in menz:
            if item == agarihai:
                flag_1 = True

def fukeisan(PlayerInfo, menzen_pattern, agarihai):
    if len(menzen_pattern) == 7:
        return 25
    if y_pinfu.y_pinfu(PlayerInfo, menzen_pattern, agarihai) and y_menzentumo.y_menzentumo(PlayerInfo, menzen_pattern, agarihai):
        return 20
    if kokushi(PlayerInfo, menzen_pattern, agarihai):#国士無双はよくわからんので適当に。
        return 20
    hai_count = 20
    for menz in menzen_pattern:
        if len(menz) == 2:#頭確定(激アツ)
            if atama(PlayerInfo, menzen_pattern, agarihai):
                hai_count += 2
        else:
            if menz[0] == menz[1] and menz[1] == menz[2]: #暗刻確定
                if haikei(menz[0]):
                    hai_count += 4
                else:
                    hai_count += 8
    
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        if len(menz) == 3: #明刻確定というわけでもない
            if menz[0][0] == menz[1][0] and menz[1][0] == menz[2][0]:
                if haikei(menz[0][0]):
                    hai_count += 2
                else:
                    hai_count += 4
        if menz[0][1] == menz[1][1] and menz[1][1] == menz[2][1] and menz[2][1] == menz[3][1]:#あんかん
            if haikei(menz[0][0]):
                hai_count += 16
            else:
                hai_count += 32
        else: #めいかん
            if haikei(menz[0][0]):
                hai_count += 8
            else:
                hai_count += 16
    #あとは両面とシャンポン待ちの判定をする。