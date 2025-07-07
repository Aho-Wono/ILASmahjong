import itertools

def y_ryanpeiko(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    if len(menzen_pattern) == 7:
        return False
    # for naki_i in naki:
    #    flag = naki_i[0][1] #あんかんのとき鳴いたもののリストの誰のものか(2番目)がすべて一致するはずなので、違うときにFalse
    #    for item in naki_i:
    #        if item[1] != flag:
    #            return False
    if len(menzen_pattern) != 4:
        return False
    for permu in itertools.permutations(menzen_pattern, 4):
        if permu[0] == permu[1] and permu[2] == permu[3] and permu[1] != permu[2]:
            return "二盃口"
    return False
    # あんかんがあった時点でりゃんぺは成立しないので、コメントアウトした5行がおそらくいらない