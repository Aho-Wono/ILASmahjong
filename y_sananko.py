def y_sananko(PlayerInfo, menzen_pattern, agarihai):
    ank_n = 0
    for menz in menzen_pattern:
        if menz.count(menz[0]) == 3:
            ank_n += 1
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        fl = menz[0][1], an = True
        for item in menz:
            if fl != item[1]:
                an = False
        if an:
            ank_n += 1
    if ank_n >= 3:
        return "三暗刻"
    return False