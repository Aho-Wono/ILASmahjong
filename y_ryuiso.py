def y_ryuiso(PlayerInfo, menzen_pattern, agarihai):
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
        kensa = kensa + i
    for j in kensa:
        if not j in ("s2" , "s3" , "s4" , "s6" , "s8" , "hatu"):
            return False
    return "緑一色"