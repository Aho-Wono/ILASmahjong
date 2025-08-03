import y_doublerichi
def y_richi(PlayerInfo, menzen_pattern, agarihai):
    if y_doublerichi.y_doublerichi(PlayerInfo, menzen_pattern, agarihai):
        return False
    if PlayerInfo.ifrichi():
        return "立直"
    else:
        return False