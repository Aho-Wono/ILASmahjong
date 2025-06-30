def y_tintumo(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    if naki:
        return True
    for naki_i in naki:
        flag = naki_i[0][1]
        for item in naki_i:
            if flag != item[1]:
                return False
    return True #あってるんか？→あってるよ