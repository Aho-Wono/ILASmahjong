def y_menzentumo(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    tumo = PlayerInfo.tehai["tumo"]
    
    result = True

    for n in naki: # 誰かからひとつでも鳴いてたらFalse
        fromwho_li = [nn[1] for nn in n]
        for f in fromwho_li:
            if f != fromwho_li: result = False

    if tumo == None: result = False # ツモってなかったらFalse

    if result:
        return "門前清自摸和"
    else: return False

    # 動作確認済 by 小野