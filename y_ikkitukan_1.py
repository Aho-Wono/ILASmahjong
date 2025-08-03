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
    ans_ik = [False, False, False] #一気通貫判定, 最初が1,4,7であることを確認
    for menz in menzen_pattern:
        if menz[0][0] != zi_str:
            continue
        if len(menz) != 3:
            continue
        if menz[0] == menz[1] and menz[1] == menz[2]:
            continue
        if menz[0][1] == '1':
            ans_ik[0] = True
        if menz[0][1] == '4':
            ans_ik[1] = True
        if menz[0][1] == '7':
            ans_ik[2] = True
    for menz in naki:
        if menz[0][0][0] != zi_str:
            continue
        if len(menz) != 3:
            continue
        if menz[0][0] == menz[1][0] and menz[1][0] == menz[2][0]:
            continue
        if menz[0][0][1] == '1':
            ans_ik[0] = True
        if menz[0][0][1] == '4':
            ans_ik[1] = True
        if menz[0][0][1] == '7':
            ans_ik[2] = True
    # これで一気通貫の判定は完了
    if not (ans_ik[0] and ans_ik[1] and ans_ik[2]):
        return False
    return "一気通貫_1"