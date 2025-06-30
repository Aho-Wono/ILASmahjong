def y_tintumo(menzen_pattern, naki, tumo, kawa):
    if naki:
        return True
    for naki_i in naki:
        flag = naki_i[0][1]
        for item in naki_i:
            if flag != item[1]:
                return False
    return True #あってるんか？→あってるよ