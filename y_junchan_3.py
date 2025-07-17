def y_junchan_3(PlayerInfo, menzen_pattern, agarihai):
    if PlayerInfo.ifnaki():
        return False
    if len(menzen_pattern) == 7:
        return False
    for menz in menzen_pattern:
        flag = True
        for item in menz:
            if len(item) == 2:
                if item[1] == '1' or item[1] == '9':
                    flag = False
        if flag:
            return False
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        flag = True
        for item in menz:
            if len(item[0]) == 2:
                if item[0][1] == '1' or item[0][1] == '9':
                    flag = False
        if flag:
            return False
    return "純全帯么九_3"