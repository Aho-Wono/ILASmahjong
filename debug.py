import sys

debug_mode = True

def printd(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    """
    デバッグ用 print ラッパー。
    引数はすべてそのまま標準の print() に渡されます。
    """
    if debug_mode:
        print(*args, sep=sep, end=end, file=file, flush=flush)

# by Chappy