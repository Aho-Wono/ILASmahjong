def y_daisangen(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    tehaikari = menzen_pattern + nakiseiri
    kensa = []
    for i in tehaikari:
        if len(i) == 4:
            i.remove(i[0])
        if len(i) == 3 and len(i[0]) != 2:
            if i[0] == i[1] and not i[0] in ("ton" , "nan" , "sha" , "pei"):
                kensa.append(i)
    if len(kensa) == 3:
        return "大三元"
    else:
        return False