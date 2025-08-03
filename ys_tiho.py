import info
def ys_tiho(players, p_id, menzen_pattern, agarihai):
    kyoku = info.read()["kyoku"]
    oya_id = int(kyoku[1]) - 1
    kawakakunin = 0
    if players[p_id].tehai["tumo"] != agarihai:
        return False
    if p_id == oya_id:
        return False
    if p_id > oya_id:
        kawakakunin = 4
    for PlayerInfo in players:
        if PlayerInfo.ifnaki():
            return False
    for i in range(p_id , (oya_id + kawakakunin)):
        if players[i % 4].kawa:
            return False
    return "地和"