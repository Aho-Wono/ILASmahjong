import mentsu_pattern

tehais = [
    "m1 m1 m1 m2 m2 m2 m3 m3 m3 p1 p2 p3 s9 s9 ".split(),
    "m2 m2 m3 m3 m4 m4 m5 m5 m6 m6 m7 m7 m8 m8 ".split(),
    "m1 m1 m1 m1 m2 m2 m2 m2 m3 m3 m3 m3 m4 m4 ".split()
]

for t in tehais:
    print(f"\n===== {t} ===== ")
    li = mentsu_pattern.mentsu_pattern(tehai= t)
    for l in li: print(l)