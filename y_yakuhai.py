#仕様分からないのでとりあえずベースだけ作っておきます。
def y_bahuu(PlayerInfo, menzen_pattern, agarihai):
    for menz in menzen_pattern:
        if len(menz) != 3:
            continue
        if menz[0] == "ton": #ここら辺もおそらく変わるので今は東の時だけ実装
            return "場風"
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        if len(menz) != 3:
            continue
        if menz[0][0] == "ton":
            return "場風"
    return False
#あとはこれをうまく変更すれば作れると思います。