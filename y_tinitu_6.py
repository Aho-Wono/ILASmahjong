def y_tinitu_6(PlayerInfo, menzen_pattern, agarihai):
    if PlayerInfo.ifnaki():
        return False
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    tehaikari = menzen_pattern + nakiseiri
    for i in tehaikari:
        if len(i[0]) != 2:
            return False
        if i[0][0] != tehaikari[0][0][0]:
            return False
    return "清一色_6"