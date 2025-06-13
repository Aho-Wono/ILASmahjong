# by Chappy

import sys
import inspect
from pprint import pformat

debug_mode = True

def printd(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    """
    デバッグ用 print ラッパー。
    引数はすべてそのまま標準の print() に渡されます。
    """
    if debug_mode:
        print(*args, sep=sep, end=end, file=file, flush=flush)

def printc(obj, name=None, indent=0, visited=None):
    """
    オブジェクトの中身を再帰的に表示するデバッグ関数。
    リスト・タプル・セットはインライン表示し、縦にズラッと並ばないようにする。
    """

    if debug_mode:
        if visited is None:
            visited = set()
        prefix = ' ' * indent

        # 循環参照チェック
        obj_id = id(obj)
        if obj_id in visited:
            print(f"{prefix}{name or type(obj).__name__}: (循環参照)")
            return
        visited.add(obj_id)

        # プリミティブ型はそのまま表示
        if isinstance(obj, (int, float, str, bool, type(None))):
            print(f"{prefix}{name or type(obj).__name__}: {repr(obj)}")
            return

        # dict は再帰的に展開
        if isinstance(obj, dict):
            print(f"{prefix}{name or 'dict'} (dict) {{")
            for k, v in obj.items():
                printc(v, name=f"[{k!r}]", indent=indent+4, visited=visited)
            print(f"{prefix}}}")
            return

        # list, tuple, set はインライン表示
        if isinstance(obj, (list, tuple, set)):
            cls_name = type(obj).__name__
            print(f"{prefix}{name or cls_name} ({cls_name}): {repr(obj)}")
            return

        # カスタムオブジェクトは属性を展開
        cls = type(obj)
        print(f"{prefix}{name or cls.__name__} ({cls.__module__}.{cls.__name__}) {{")
        if hasattr(obj, '__dict__'):
            for attr, val in obj.__dict__.items():
                printc(val, name=attr, indent=indent+4, visited=visited)
        else:
            members = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
            for attr, val in members:
                if attr.startswith('__') and attr.endswith('__'):
                    continue
                printc(val, name=attr, indent=indent+4, visited=visited)
        print(f"{prefix}}}")