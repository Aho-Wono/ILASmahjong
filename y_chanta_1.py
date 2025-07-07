def y_chanta_1(PlayerInfo, menzen_pattern, agarihai):
    if not PlayerInfo.ifnaki():
        return False
    if len(menzen_pattern) == 7:
        return False
    naki = PlayerInfo.tehai["naki"]
    for menz in menzen_pattern:
        flag = True
        for item in menz:
            try:
                if (len(item) == 2):
                    i = int(item[1])
                    if i == 1 or i == 9:
                        flag = False
                else:
                    flag = False
            except Exception as e:
                print(e)
        if flag:
            return False
    for naki_i in naki:
        flag = True
        for item in naki_i:
            if(len(item[0]) == 2):
                i = int(item[1])
                if i == 1 or i == 9:
                    flag = False
            else: 
                flag = False
        if flag:
            return False
    return "混全帯么九_1"