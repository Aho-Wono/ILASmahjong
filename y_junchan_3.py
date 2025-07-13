def y_junchan_3(PlayerInfo, menzen_pattern, agarihai):
    if PlayerInfo.ifnaki():
        return False
    if len(menzen_pattern) == 7:
        return False
    flag = True
    for menz in menzen_pattern:
        flag_1 = False
        for item in menz:
            if len(item) == 2:
                if item[1] == '1' or item[1] == '9':
                    flag_1 = True
        flag = flag_1
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        flag_1 = False
        for item in menz:
            if len(item[0]) == 2:
                if item[0][1] == '1' or item[0][1] == '9':
                    flag_1 = True
        flag = flag_1
    if flag:
        return "純全帯么九_3"
    else:
        return False