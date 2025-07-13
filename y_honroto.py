def y_honroto(PlayerInfo, menzen_pattern, agarihai):
    flag = True
    for menz in menzen_pattern:
        for item in menz:
            if len(item) != 2:
                flag = False
            elif int(item[1]) != 1 and int(item[1]) != 9:
                flag = False
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        for item in menz:
            if len(item[0]) != 2:
                flag = False
            elif int(item[0][1]) != 1 and int(item[0][1]) != 9:
                flag = False
    if flag:
        return "混老頭"
    else:
        return False