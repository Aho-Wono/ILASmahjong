def y_sansyokudouzyun(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    nakiseiri = []
    for k in naki:
        for l in range(len(k)):
            k[l] = k[l][0]
        nakiseiri.append(k)
    tehaikari = menzen_pattern + nakiseiri
    kensa = []
    hantei1 = 0
    hantei2 = 0
    for i in tehaikari:
        if len(i) == 3:
            if i[0] != i[1]:
                kensa.append(i)  #kensaに入るのを順子に限定
    
    manzu = 0
    pinzu = 0
    souzu = 0
    for m in kensa:
        if m[0][0] == "m":
            manzu = 1
        elif m[0][0] == "p":
            pinzu = 1
        elif m[0][0] == "s":
            souzu = 1
    if manzu * pinzu * souzu == 0:    #萬子、筒子、索子が揃っているか確認
        return False
    
    for n in kensa:
        if kensa.count(n) > 1:
            kensa.remove(n)      #被りがあるとカウントしづらいので消す  面子は四つまでなので一回で十分
    
    for l in kensa:      #面子四つの場合を考慮して二回判定
        if l[0][1] == kensa[0][0][1]:
            hantei1 += 1
        if l[0][1] == kensa[1][0][1]:
            hantei2 += 1
    if hantei1 >= 3 or hantei2 >= 3:
        return "三色同順"
    else:
        return False