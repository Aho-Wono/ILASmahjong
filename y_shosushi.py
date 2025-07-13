def ifzihai(s):
    if s == "ton" or s == "nan" or s == "sha" or s == "pei":
        return True
    else:
        return False

def y_shosushi(PlayerInfo, menzen_pattern, agarihai):
    if len(menzen_pattern) == 7:
        return False
    cnt = 0
    for menz in menzen_pattern:
        if ifzihai(menz[0]):
            cnt += 1
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        if ifzihai(menz[0][0]):
            cnt += 1
    if cnt == 3:
        return "小四喜"
    return False