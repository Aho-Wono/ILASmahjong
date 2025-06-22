def y_toitoiho(menzen_pattern, naki, tumo, kawa):
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    hantei = 0
    for i in tehaikari:
        if len(i) == 4:
            i.remove(i[0])
        if len(i) == 3:
            if i[0] ==i[1] and i[1] == i[2]:
                hantei += 1
    if hantei >= 4:
        return True
    else:
        return False