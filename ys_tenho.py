import info
def ys_tenho(players, p_id, menzen_pattern, agarihai):
    all_kawa = players[0].kawa + players[1].kawa + players[2].kawa + players[3].kawa
    kyoku = info.read()["kyoku"]
    oya_id = int(kyoku[1]) - 1
    if p_id != oya_id:
        return False
    if all_kawa:
        return False
    else:
        return "天和"
    