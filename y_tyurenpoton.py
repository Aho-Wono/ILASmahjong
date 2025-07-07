def y_tyurenpoton(PlayerInfo, menzen_pattern, agarihai):
    if not PlayerInfo.ifnaki():
        return False
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    kensa = []
    iro = tehaikari[0][0][0]
    for i in tehaikari:
        if len(i[0]) != 2:
            return False
        if i[0][0] != tehaikari[0][0][0]:
            return False
        kensa = kensa + i
    if kensa.count(iro + "1") >=3 and kensa.count(iro + "9") >=3:
        kensa = list(set((kensa)))
        if len(kensa) == 9:
            return "九蓮宝燈"
    return False