def y_suanko(PlayerInfo, menzen_pattern, agarihai):
    if PlayerInfo.tehai["tumo"] == None:
        if menzen_pattern[len(menzen_pattern)-1][0] != agarihai:
            return False
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
    if len(tehaikari) == 7:
        return False
    for i in tehaikari:
        if i[0] != i[1]:
            return False
    return "四暗刻"
