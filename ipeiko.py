import itertools

def ipeiko(naki, tumo, kawa, menzen_pattern):
    flag = False
    for item in itertools.combinations(menzen_pattern, 2):
        if item[0] == item[1]:
            flag = False
    return flag