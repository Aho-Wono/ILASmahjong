import info
def y_yakuhai(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    tehaikari = menzen_pattern + nakiseiri
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
    for i in tehaikari:
        if i[0] in yakuhai:
            return "役牌"
    return False
    
    
    
    
    
    
    
    
    
