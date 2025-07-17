import y_tinroto
def y_honroto(PlayerInfo, menzen_pattern, agarihai):
    if y_tinroto.y_tinroto(PlayerInfo, menzen_pattern, agarihai):
        return False
    flag = True
    for menz in menzen_pattern:
        for item in menz:
            if len(item) == 2:
                if int(item[1]) != 1 and int(item[1]) != 9:
                    flag = False
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        for item in menz:
            if len(item[0]) == 2:
                if int(item[0][1]) != 1 and int(item[0][1]) != 9:
                    flag = False
    if flag:
        return "混老頭"
    else:
        return False