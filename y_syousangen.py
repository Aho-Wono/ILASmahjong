def y_syousangen(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    tehaikari = menzen_pattern + nakiseiri
    kensa = []
    zyantouhantei = 0
    for i in tehaikari:
        if len(i) == 4:
            i.remove(i[0])
        if len(i) == 3 and len(i[0]) != 2:
            if i[0] == i[1] and not i[0] in ("ton" , "nan" , "sha" , "pei"):
                kensa.append(i)
        if len(i) == 2 and len(i[0]) != 2 and not i[0] in ("ton" , "nan" , "sha" , "pei"):
                kensa.append(i)
                zyantouhantei += 1
    if len(kensa) == 3 and zyantouhantei == 1:
        return "小三元"
    else:
        return False