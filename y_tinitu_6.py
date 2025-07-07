def y_tinitu_6(PlayerInfo, menzen_pattern, agarihai):
    if not PlayerInfo.ifnaki():
        return False
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    for i in tehaikari:
        if len(i[0]) != 2:
            return False
        if i[0][0] != tehaikari[0][0][0]:
            return False
    return "清一色_6"