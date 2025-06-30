def y_sansyokudouko(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    kensa = []
    kazukensa = []
    hantei = 0
    for i in tehaikari:
        if len(i) == 4:
            i.remove(i[0])
        if len(i) == 3 and len(i[0]) == 2:
            if i[0] == i[1] and i[1] == i[2]:
                kensa.append(i)
    if len(kensa) < 3:
        return False
    else:
        for k in kensa:
            for l in range(3):
                k[l] = k[l][1]
                kazukensa.append(k[l])
        for kazu in kazukensa:
            if kazu == kazukensa[0]:
                hantei += 1
        if hantei >= 9:
            return "三色同刻"
        else:
            return False