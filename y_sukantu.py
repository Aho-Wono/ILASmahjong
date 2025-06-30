def y_sukantu(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    hantei = 0
    for i in tehaikari:
        if len(i) == 4:
            hantei += 1
    if hantei == 4:
        return "四槓子"
    else:
        return False