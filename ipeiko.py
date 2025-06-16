import itertools

def ipeiko(naki, tumo, kawa, menzen_pattern):
    if not naki:
        return False
    for item in itertools.combinations(menzen_pattern, 2):
        if item[0] == item[1]:
            return True
    return False