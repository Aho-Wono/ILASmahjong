def y_tinitu_5(PlayerInfo, menzen_pattern, agarihai):
    if not PlayerInfo.ifnaki():
        return False
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    tehaikari = menzen_pattern + nakiseiri
    if len(tehaikari) == 7:
        return False
    for i in tehaikari:
        if len(i[0]) != 2:
            return False
        if i[0][0] != tehaikari[0][0][0]:
            return False
    return "清一色_5"