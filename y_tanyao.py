def y_tanyao(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    tehai = []
    for i in tehaikari:
        tehai = tehai + i
    hantei = 1
    for j in tehai:
            if not j[1] in ("2" , "3" , "4" , "5" , "6" , "7" , "8"):
                hantei = 0
    if hantei == 1:
        return "断么九"
    else:
        return False
