import itertools

def y_ryanpeiko(menzen_pattern, naki, kawa, tumo, agarihai):
    if not naki:
        return False
    if len(menzen_pattern) != 4:
        return False
    for permu in itertools.permutations(menzen_pattern, 4):
        if permu[0] == permu[1] and permu[2] == permu[3]:
            return True
    return False