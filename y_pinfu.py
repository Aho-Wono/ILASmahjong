def y_pinfu(PlayerInfo, menzen_pattern, agarihai):
    import info
    if PlayerInfo.ifnaki():
        return False
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    kyoku = info.read()["kyoku"]
    player = PlayerInfo.playerid
    kazehai = ["ton" , "nan" , "sha" , "pei"]
    yakuhai = ["haku" , "hatu" , "chun"]
    zyantou = []
    zikaze_keisan = (int(player)-(int(kyoku[1])-1))%4
    hantei = 0
    kensa = []
    kanchan_count = 0
    penchan_count = 0
    if kyoku[0] == "t":
        yakuhai.append(kazehai[0])
    elif kyoku[0] == "n":
        yakuhai.append(kazehai[1])
    elif kyoku[0] == "s":
        yakuhai.append(kazehai[2])
    elif kyoku[0] == "p":
        yakuhai.append(kazehai[3])
    yakuhai.append(kazehai[zikaze_keisan])
    if len(tehaikari) == 7:
        return False
    for i in tehaikari:
        if len(i) == 2:
            zyantou = i
            if i[0] in yakuhai:
                return False
        if len(i) == 3:
            if i[0] != i[1]:
                hantei += 1
                kensa = kensa + i
    if hantei == 4:
        tehaikari.remove(zyantou)
        for j in tehaikari:
            if j[1] == agarihai:
                kanchan_count += 1
            if j[0][1] == "1" and agarihai[1] == "3":
                penchan_count += 1
            if j[2][1] == "9" and agarihai[1] == "7":
                penchan_count += 1
        if kensa.count(agarihai) == (kanchan_count + penchan_count):
            return False
        else:
            return "平和"
    else:
        return False