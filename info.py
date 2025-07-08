import json
from getdir import dir
from debug import printd

# JSONファイルのパス
path = f"{dir()}/info.json"

# JSONファイルに生データを書き込む
def write(data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    #printd("[json written]")

# JSONファイルを読み込む
def read():
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)  
        #printd("[json readed]")
        return data

# JSONファイルの辞書を書き換える
def edit(key, value):
    data = read()
    data[key] = value
    write(data= data)

def getoya():
    return 0 + int(read()["kyoku"][1]) - 1