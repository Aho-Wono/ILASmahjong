import json
from getdir import dir

# JSONファイルのパス
path = f"{dir()}/info.json"

# JSONファイルに書き込む
def write(data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("json written")

def read():
    # JSONファイルを読み込む
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)  
        print("[json readed]")
        return data