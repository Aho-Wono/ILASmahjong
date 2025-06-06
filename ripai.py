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
