def ys_hoteiraoyui(players, p_id, menzen_pattern, agarihai):
    naki = players[0].tehai["naki"] + players[1].tehai["naki"] + players[2].tehai["naki"] + players[3].tehai["naki"]
    nakiseiri = []
    for k in naki:
        nakikari = []
        for l in range(len(k)):
            nakikari.append(k[l][0])
        nakiseiri.append(nakikari)
    temoto = players[0].tehai["menzen"] + players[1].tehai["menzen"] + players[2].tehai["menzen"] + players[3].tehai["menzen"]
    temoto.append(agarihai)
    for j in nakiseiri:
        temoto = temoto + j
    for k in range(4):
        for hai in players[k].kawa:
            temoto.append(hai[0])
    if (players[p_id].tehai["tumo"] != agarihai) and len(temoto) == 122:
        return "河底撈魚"
    else:
        return False