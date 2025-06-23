import info


print(info.read())

dic = info.read()
dic["hon"] += 1

info.write(dic)

print(info.read())