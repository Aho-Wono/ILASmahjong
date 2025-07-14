import y_sukantu
def y_sankantu(PlayerInfo, menzen_pattern, agarihai):
    if y_sukantu.y_sukantu(PlayerInfo, menzen_pattern, agarihai):
        return False
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    tehaikari = menzen_pattern + nakiseiri
    hantei = 0
    for i in tehaikari:
        if len(i) == 4:
            hantei += 1
    if hantei == 3:
        return "三槓子"
    else:
        return False