import random
import itertools
import ripai
import debug
ALL_HAI = "m1 m2 m3 m4 m5 m6 m7 m8 m9 p1 p2 p3 p4 p5 p6 p7 p8 p9 s1 s2 s3 s4 s5 s6 s7 s8 s9 ton nan sha pei haku hatu chun".split()


# "m","p","s","j"を引数として対象の種類だけを返してくる関数
def tehai_split(tehai=None, kind=None): 
    splited_tehai = []
    for hai in tehai:
        if kind == "j":
            if hai in "ton nan sha pei haku hatu chun".split():
                splited_tehai.append(hai)
        else:
            if len(hai)==2 and hai[0] == kind:
                splited_tehai.append(hai)
    
    return splited_tehai

def printd_ifagari(text): # デバッグモードのさらにデバッグモード的なもの
    if False:
        debug.printd(text)

def mentsu_pattern(tehai=None):
    mentsu_patterns = []
    agari = False

    tehai = ripai.ripai(tehai)
    printd_ifagari(f"=== {tehai} ===")

    for 普通系の判定 in [1]:
        # 雀頭候補を見つける
        janto_koho = []
        for hai in tehai:
            if tehai.count(hai) >= 2 and hai not in janto_koho:
                janto_koho.append(hai)
        printd_ifagari(f"janto_koho: {janto_koho}")



        # 雀頭候補を外した上でアガリ系になっているか判定する
        janto_hantei = False
        for janto in janto_koho: #雀頭候補ぶん外しながら試す
            printd_ifagari(f"< ---janto: {janto}--- >")
            tehai_without_janto = tehai[:] # リストをコピー（ここでそのまま=としてしまうと同じ値を参照してしまう）
            for i in range(2): tehai_without_janto.remove(janto)
            printd_ifagari(f"without janto: {tehai_without_janto}")

            # 萬子・筒子・索子・字牌に分ける
            m_li = tehai_split(tehai_without_janto, "m")
            p_li = tehai_split(tehai_without_janto, "p")
            s_li = tehai_split(tehai_without_janto, "s")
            j_li = tehai_split(tehai_without_janto, "j")
            
            # それぞれの数牌に対し、先に刻子を除去して、残りで順子ができているかどうかを全パターン試す
            mpsj_hantei = 0 # 最後まで0を保持していたらアガリ

            mpsj_patterns = [[], [], [], []]

            # 萬子・筒子・索子の判定
            for mps, mps_li in enumerate([m_li, p_li, s_li]):
                mps_kind = ["m", "p", "s"][mps] 
                # まず文字列のリストから数字のリストへと変換する
                suhai_li = [int(i[1]) for i in mps_li]
                printd_ifagari(f"{mps_li} >>> {suhai_li}")

                if len(suhai_li) == 0: # そもそも構成牌が無ければそのまま通過させる
                    mpsj_hantei += 1
                    printd_ifagari("nai")
                else:
                    # 刻子の候補を出す
                    kotu_koho = []
                    for hai in suhai_li:
                        if suhai_li.count(hai) >= 3 and hai not in kotu_koho:
                            kotu_koho.append(hai)
                    printd_ifagari(f"kotu_koho: {kotu_koho}")

                    # 除去する刻子の組み合わせ(Σ[k=1..n]k!)を作る（対々和系でも多くて33通りなので処理的には問題ない）
                    kotu_del_li = [[]] # 何にも削除せず
                    for i in range(len(kotu_koho)):
                        kotu_del_li.extend(list(itertools.combinations(kotu_koho, i+1)))
                    printd_ifagari(f"kot_del_li: {kotu_del_li}")

                    only_shuntu_li = []
                    kotu_hantei = 0

                    # 刻子のパターンを実際にすべて試す
                    for kotu_del in kotu_del_li:
                        suhai_li_copied = suhai_li[:]
                        kotu_shuntu_pattern = [] # 刻子・順子としてそれぞれが成立するパターンのリスト

                        # 刻子の削除
                        for i in kotu_del:
                            for ii in range(3): suhai_li_copied.remove(i)
                            kotu_shuntu_pattern.append([f"{mps_kind}{i}" for iii in range(3)])
                        only_shuntu_li = suhai_li_copied[:]
                        printd_ifagari(f"only_shuntu_li: {only_shuntu_li}")
                        
                        shuntu_koho = []
                        # 順子を削除していく
                        while True:
                            if len(only_shuntu_li) == 0: # エラー処理外でリストの個数が0になってたら成功
                                kotu_hantei += 1
                                kotu_shuntu_pattern.extend(shuntu_koho)
                                mpsj_patterns[mps].append(kotu_shuntu_pattern)
                                break

                            try:
                                min_hai = min(only_shuntu_li)
                                for i in range(3):
                                    only_shuntu_li.remove(min_hai+i) # 小さい順に順子の削除
                                shuntu_koho.append([f"{mps_kind}{min_hai+ii}" for ii in range(3)])
                                
                            except Exception: # うまく削除できなかった場合
                                break
                    
                    # 刻子パターンで成立するものがあれば
                    if kotu_hantei >= 1: 
                        mpsj_hantei += 1
            
            # 字牌の判定
            j_hantei = True
            j_kind = []
            for j in "ton nan sha pei haku hatu chun".split(): 
                if j_li.count(j) not in [0, 3]: j_hantei = False
                if j_li.count(j) == 3:
                    j_kind.append(j)
            if j_hantei: 
                j_pattern = []
                for jh in j_kind:
                    j_pattern.append([jh, jh, jh])
                mpsj_patterns[3].append(j_pattern)
                mpsj_hantei += 1
                    

            printd_ifagari(f"mpsj: {mpsj_hantei}")
            if mpsj_hantei == 4: # 萬子・筒子・索子・字牌すべてについてキレイな形になっていれば
                # ここでmentsu_patternに実際に成立するパターンを追加していく
                janto_hantei = True
                # やっとパターンを追加できるぜ　やったぜ。　気持ちが良い！
                
                mpsj_patterns_copied = []
                for mpsj_p in mpsj_patterns:
                    printd_ifagari(mpsj_p)
                    if mpsj_p == []: mpsj_patterns_copied.append([[]])
                    else: mpsj_patterns_copied.append(mpsj_p)
                mpsj_patterns = mpsj_patterns_copied[:]

                printd_ifagari(f"mpsj_patterns: {mpsj_patterns}")

                for i in mpsj_patterns[0]:
                    for ii in mpsj_patterns[1]:
                        for iii in mpsj_patterns[2]:
                            for iiii in mpsj_patterns[3]:
                                mentsu_patterns.append(i + ii + iii + iiii + [[janto, janto]])

        if janto_hantei: agari = True
    for 七対子の判定 in [1]:
        hai_count_li = [] # 各牌の数を格納するリスト
        hai_li = []
        for hai in tehai:
            hai_count_li.append(tehai.count(hai))
            if hai not in hai_li: hai_li.append(hai)
        if ([max(hai_count_li), min(hai_count_li)] == [2, 2]) and len(tehai) == 14: # すべてが2つずつかつ14個ずつならTrue
            agari = True 
            mentsu_patterns.append([[hai, hai] for hai in hai_li]) # 面子パターンに追加
    for 国士無双の判定 in [1]:
        ikj_li = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun".split()
        for ikj in ikj_li:
            try:
                tehai_copied = tehai[:]
                tehai_copied.remove(ikj)
                if ripai.ripai(tehai_copied) == ripai.ripai(ikj_li):
                    agari = True
                    mentsu_patterns.append([ikj_li, [ikj]])
            except Exception: continue
    
    return mentsu_patterns



#以下、デバッグ用
if True:
        
    tehai = random.choices(ALL_HAI, k=14)
    tehai = 'm1 m1 m1 p2 p3 p4 s5 s6 s7 ton ton ton pei pei'.split()
    tehai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun chun".split()
    tehai = "m1 m1 s2 s2 s3 s3 s4 s4 s5 s5 ton ton sha sha".split()
    tehai = 'm1 m2 m3 s2 s3 s4 s4 s4 s5 s5 s6 s6 pei pei'.split()
    tehai = "m1 m1 m3 m3 ton ton".split()
    tehai = "m1 m1".split()
    tehai = "m1 m1 m1 m2 m2 m2 m3 m3 m3 ton ton s1 s2 s3".split()
    tehai = "m1 m1 m2 m2 m3 m3 m4 m4 m5 m5 m6 m6 m7 m7".split()
    tehai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun chun".split()
    tehai = 'm1 m1 m1 p2 p3 p4 s5 s6 s7 ton ton ton pei pei'.split()

    tehai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun ton".split()
    debug.printd(f"mentsu_patterns: {mentsu_pattern(tehai=tehai)}")



    count = 0
    while False:
        count += 1
        tehai = random.choices(ALL_HAI, k=14)
        
        if count%10000 == 0: printd_ifagari(count)

        if ifagari(tehai=tehai):
            printd_ifagari(f"\n和了 count={count}")
            printd_ifagari(tehai)
            break


