import itertools

def ipeiko(menzen_pattern, naki, kawa, tumo, agarihai):
    if not naki:
        return False
    for item in itertools.combinations(menzen_pattern, 2):
        if item[0] == item[1]:
            return True
    return False