def y_honitu(PlayerInfo, menzen_pattern, agarihai):
    naki = PlayerInfo.tehai["naki"]
    m_char = 'x'
    for menz in menzen_pattern:
        for item in menz:
            if len(item) == 2:
                if m_char == 'x':
                    m_char = item[0]
                else:
                    if m_char != item[0]:
                        return False
    for menz in naki:
        for item in menz:
            if len(item[0]) == 2:
                if m_char == 'x':
                    m_char = item[0][0]
                else:
                    if m_char != item[0][0]:
                        return False
    return "混一色_3"