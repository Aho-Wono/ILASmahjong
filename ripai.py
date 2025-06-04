import random

#リストで与えられた牌をソートして返す
def ripai(hai_li):
	suhai_li = []
	jihai_li = []
	jihai_li_new = []

	for hai in hai_li:
		if len(hai) == 2: suhai_li.append(hai)
		else            : jihai_li.append(hai)

	for jihai in ["ton", "nan", "sha", "pei", "haku", "hatu", "chun"]:
		
		while True:
			if jihai in jihai_li:
				jihai_li_new.append(jihai)
				jihai_li.remove(jihai)
			else: break

	return sorted(suhai_li) + jihai_li_new

#↓こんな感じで牌を定義してほしい
haipai = ["m1", "m9", "p1", "p9", "s1", "s9", "ton", "nan", "sha", "pei", "haku", "hatu", "chun"]
random.shuffle(haipai)
print("理牌前：", haipai)

#理牌関数に通した後
print("理牌後：", ripai(haipai))