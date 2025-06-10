import random
import itertools
import ripai
from debug import printd
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


def ifagari(tehai=None):
    agari = False

    tehai = ripai.ripai(tehai)
    printd(f"=== {tehai} ===")

    for 普通系の判定 in [1]:
        # 雀頭候補を見つける
        janto_koho = []
        for hai in tehai:
            if tehai.count(hai) >= 2 and hai not in janto_koho:
                janto_koho.append(hai)
        printd(f"janto_koho: {janto_koho}")



        # 雀頭候補を外した上でアガリ系になっているか判定する
        janto_hantei = False
        for janto in janto_koho: #雀頭候補ぶん外しながら試す
            printd(f"---janto: {janto}")
            tehai_without_janto = tehai[:] # リストをコピー（ここでそのまま=としてしまうと同じ値を参照してしまう）
            for i in range(2): tehai_without_janto.remove(janto)
            printd(f"without janto: {tehai_without_janto}")

            # 萬子・筒子・索子・字牌に分ける
            m_li = tehai_split(tehai_without_janto, "m")
            p_li = tehai_split(tehai_without_janto, "p")
            s_li = tehai_split(tehai_without_janto, "s")
            j_li = tehai_split(tehai_without_janto, "j")
            
            # それぞれの数牌に対し、先に刻子を除去して、残りで順子ができているかどうかを全パターン試す
            mpsj_hantei = 0 # 最後まで0を保持していたらアガリ

            # 萬子・筒子・索子の判定
            for mps_li in [m_li, p_li, s_li]: 
                # まず文字列のリストから数字のリストへと変換する
                suhai_li = [int(i[1]) for i in mps_li]
                printd(f"{mps_li} >>> {suhai_li}")

                if len(suhai_li) == 0: # そもそも構成牌が無ければそのまま通過させる
                    mpsj_hantei += 1
                    printd("nai")
                else:
                    # 刻子の候補を出す
                    kotu_koho = []
                    for hai in suhai_li:
                        if suhai_li.count(hai) >= 3 and hai not in kotu_koho:
                            kotu_koho.append(hai)
                    printd(f"kotu_koho: {kotu_koho}")

                    # 除去する刻子の組み合わせ(Σ[k=1..n]k!)を作る（対々和系でも多くて33通りなので処理的には問題ない）
                    kotu_del_li = []
                    for i in range(len(kotu_koho)):
                        kotu_del_li.extend(list(itertools.combinations(kotu_koho, i+1)))
                    printd(f"kot_del_li: {kotu_del_li}")

                    only_shuntu_li = []
                    only_shuntu_li.append(suhai_li)

                    # 刻子のパターンを実際にすべて試す
                    for kotu_del in kotu_del_li:
                        suhai_li_copied = suhai_li[:]
                        # 刻子の削除
                        for i in kotu_del:
                            for ii in range(3): suhai_li_copied.remove(i)
                        only_shuntu_li.append(suhai_li_copied)

                    printd(f"only_shuntu_li: {only_shuntu_li}")

                    kotu_hantei = 0
                    for only_shuntu in only_shuntu_li:
                        # 順子を削除していく
                        while True:
                            if len(only_shuntu) == 0: # エラー処理外でリストの個数が0になってたら成功
                                kotu_hantei += 1
                                break

                            try:
                                min_hai = min(only_shuntu)
                                for i in range(3):
                                    only_shuntu.remove(min_hai+i) # 小さい順に順子の削除
                            except Exception: # うまく削除できなかった場合
                                break
                            
                    
                    # 刻子パターンで成立するものがあれば
                    if kotu_hantei >= 1: 
                        mpsj_hantei += 1
            
            # 字牌の判定
            j_hantei = True
            for j in "ton nan sha pei haku hatu chun".split(): 
                if j_li.count(j) not in [0, 3]: j_hantei = False
            if j_hantei: mpsj_hantei += 1
                    

            printd(f"mpsj: {mpsj_hantei}")
            if mpsj_hantei == 4: # 萬子・筒子・索子・字牌すべてについてキレイな形になっていれば
                janto_hantei = True
            printd(janto_hantei)
        
        if janto_hantei: agari = True
    for 七対子の判定 in [1]:
        hai_count_li = [] # 各牌の数を格納するリスト
        for hai in tehai:
            hai_count_li.append(tehai.count(hai))
        if [max(hai_count_li), min(hai_count_li)] == [2, 2]: # すべてが2つずつならTrue
            agari = True 
    for 国士無双の判定 in [1]:
        ikj_li = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun".split()
        for ikj in ikj_li:
            try:
                tehai_copied = tehai[:]
                tehai_copied.remove(ikj)
                if ripai.ripai(tehai_copied) == ripai.ripai(ikj_li):
                    agari = True
            except Exception: continue
    
    return agari



#以下、デバッグ用
if False:
        
    tehai = random.choices(ALL_HAI, k=14)
    tehai = 'm1 m1 m1 p2 p3 p4 s5 s6 s7 ton ton ton pei pei'.split()
    tehai = "m1 m9 p1 p9 s1 s9 ton nan sha pei haku hatu chun chun".split()
    tehai = "m1 m1 s2 s2 s3 s3 s4 s4 s5 s5 ton ton sha sha".split()
    tehai = 'm1 m2 m3 s2 s3 s4 s4 s4 s5 s5 s6 s6 pei pei'.split()

    printd(ifagari(tehai=tehai))


    whiling = False

    count = 0
    while whiling:
        count += 1
        tehai = random.choices(ALL_HAI, k=14)
        
        if count%10000 == 0: printd(count)

        if ifagari(tehai=tehai):
            printd(f"\n和了 count={count}")
            printd(tehai)
            break


