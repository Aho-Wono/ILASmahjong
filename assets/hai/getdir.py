# 以下チャッピーに作ってもらった、.pyのファイルでも.exeされたあとでも使える親ディレクトリの取得関数です
# 使用する.pyファイルと同じディレクトリ下に置いてね
# そのときは from getdir import dir とすればdir()がいつでも使えます

import sys
from pathlib import Path

def dir():
    """
    実行中のファイル（または exe） が置かれているディレクトリを返す。
    - 通常の .py 実行時： __file__ を使って取得
    - PyInstaller などで exe 化（frozen）されている場合： sys.executable のディレクトリを取得
    - zipapp 形式で圧縮している場合： __file__ を使って取得（zip 内ファイルのパスになるが、多くはこちらで事足りる）
    """
    # まず「frozen（exe 化）かどうか」を判定
    if getattr(sys, 'frozen', False):
        # PyInstaller などで exe 化された場合は、sys.executable が実行ファイルのパスになる
        base_path = Path(sys.executable).parent
    else:
        # 通常のスクリプトや zipapp 圧縮時は __file__ が使える
        # resolve() でシンボリックリンクも解決しつつ絶対パスに
        base_path = Path(__file__).resolve().parent

    return base_path

#他の.pyファイルからモジュールとしてインポートされたときには、以下のコードは実行されない
if __name__ == '__main__':
    current_dir = dir()
    print(f"このプログラムが置かれているディレクトリ: {current_dir}")
