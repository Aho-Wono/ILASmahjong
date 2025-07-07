def y_ikkitukan_1(PlayerInfo, menzen_pattern, agarihai):
    #食い下がりは後ほど→14行目以降でどちらも鳴いたやつを数えるが最初に.ifnakiで落とすため大丈夫　なはず
    if not PlayerInfo.ifnaki():
        return False
    if len(menzen_pattern) == 7:
        return False
    zi_num = [0, 0, 0] #萬子、筒子、索子の順
    for menz in menzen_pattern:
        for item in menz:
            if len(item) == 2:
                if item[0] == 'm':
                    zi_num[0] += 1
                elif item[0] == 'p':
                    zi_num[1] += 1
                else:
                    zi_num[2] += 1
    naki = PlayerInfo.tehai["naki"]
    for menz in naki:
        for item_i in naki:
            item = item_i[0]
            if len(item) == 2:
                if item[0] == 'm':
                    zi_num[0] += 1
                elif item[0] == 'p':
                    zi_num[1] += 1
                else: #item[0] == 's'という意味です
                    zi_num[2] += 1
    # これで数字の牌の個数をそれぞれカウントしたので、あとは各々やる(めんどすぎ)
    if zi_num[0] < 9 and zi_num[1] < 9 and zi_num[2] < 9:
        return False
    zi_str = 'x'
    if zi_num[0] >= 9:
        zi_str = 'm'
    if zi_num[1] >= 9:
        zi_str = 'p'
    if zi_num[2] >= 9:
        zi_str = 's'
    #menzen_patternとかで数牌がソートされていることを祈るが、一応されていないようにもつくる
    ans_ik = [False, False, False] #一気通貫判定
    for menz in menzen_pattern:
        if menz[0][0] != zi_str:
            continue
        n_ex = 1
        n_ad = 0
        for item in menz:
            if len(item) != 2:
                break
            n_ex *= int(item[1])
            n_ad += int(item[1])
        n_if = n_ex + n_ad #やってることはパリティビットのノリです　数牌の値の足し算と掛け算の和が(面子として揃う前提で)一意的なことを用いてます
        #1+2+3+1*2*3=12 実は1+1+5+1*1*5=12だけど面子として存在しないので無視できます
        if n_if == 12:
            ans_ik[0] = True
        #4+5+6+4*5*6=135
        if n_if == 135:
            ans_ik[1] = True
        #7+8+9+7*8*9=528
        if n_if == 528:
            ans_ik[2] = True
    for menz in naki:
        if menz[0][0][0] != zi_str:
            continue
        for item_i in naki:
            item = item_i[0]
            n_ex = 1
            n_ad = 0
            for item in menz:
                if len(item) != 2:
                    break
                n_ex *= int(item[1])
                n_ad += int(item[1])
            n_if = n_ex + n_ad 
            if n_if == 12:
                ans_ik[0] = True
            # 実は2+2+5+6+2*2*5*6=135ですが、上記のように無視できます
            if n_if == 135:
                ans_ik[1] = True
            if n_if == 528:
                ans_ik[2] = True
    if ans_ik[0] and ans_ik[1] and ans_ik[2]:
        return "一気通貫_1"
    else:
        return False