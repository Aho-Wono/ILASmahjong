def y_tuiso(PlayerInfo, menzen_pattern, agarihai):
    for menz in menzen_pattern:
        for item in menz:
            if len(item) == 2:
                return False
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        for item in menz:
            if len(item[0]) == 2:
                return False
    return "字一色"