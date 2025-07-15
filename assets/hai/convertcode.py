from pathlib import Path
from PIL import Image
import sys
import getdir

# 収縮率（0.9 = 90 %）
SCALE = 0.9

# ---------- 設定 ----------
# 1 番目の引数にディレクトリを渡す（省略時はカレント）
src_dir = getdir.dir()
# ---------------------------

for png in src_dir.glob('*.png'):
    # 画像を RGBA で開く（αチャネルが無い場合も強制付与）
    im = Image.open(png).convert('RGBA')
    w, h = im.size

    # 内容を 0.9 倍でリサイズ
    new_w, new_h = int(w * SCALE), int(h * SCALE)
    im_scaled = im.resize((new_w, new_h), resample=Image.LANCZOS)

    # 元と同じサイズの透明キャンバスを作成し、中心に貼り付け
    canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    offset = ((w - new_w) // 2, (h - new_h) // 2)  # 左上オフセット
    canvas.paste(im_scaled, offset, im_scaled)      # α を使って合成

    # 保存（例: src/画像.png -> src/scaled/画像.png）
    canvas.save(f"{src_dir}/edited/{png.name}")

print(f'完了: {len(list(src_dir.glob("*.png")))} 枚処理しました → {src_dir}')
