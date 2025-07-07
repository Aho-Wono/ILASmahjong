import itertools
import y_ryanpeiko
def y_ipeiko(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    if len(menzen_pattern) == 7:
        return False
    for naki_i in naki:
        flag = naki_i[0][1] #あんかんのとき鳴いたもののリストの誰のものか(2番目)がすべて一致するはずなので、違うときにFalse
        for item in naki_i:
            if item[1] != flag:
                return False
    for item in itertools.combinations(menzen_pattern, 2):
        if item[0] == item[1]:
            return "一盃口"
    return False 