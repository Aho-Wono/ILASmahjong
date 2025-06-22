def tanyao(menzen_pattern, naki, tumo, kawa):
    tehaikari = menzen_pattern + naki
    tehai = []
    for i in tehaikari:
        tehai = tehai + i
    hantei = 1
    for j in tehai:
            if not j[1] in ("2" , "3" , "4" , "5" , "6" , "7" , "8"):
                hantei = 0
    return bool(hantei)
