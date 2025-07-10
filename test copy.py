import threading, queue, random, asyncio, pygame, aiohttp
from mahjong import Mahjong

# Pygame 初期化 -------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock  = pygame.time.Clock()

# ゲームロジック
Game     = Mahjong()
MY_PID   = 0
AI_PIDS  = {1, 2, 3}
AI_DONE  = pygame.USEREVENT + 1       # カスタムイベント ID

# スレッド間キュー（AI→Pygame）
ai_q: queue.Queue = queue.Queue()

# ----------------- ① asyncio イベントループを別スレッドで回す ---------------
loop = asyncio.new_event_loop()       # 個別ループ生成
def loop_runner(loop):
    asyncio.set_event_loop(loop)      # スレッド内でこのループをデフォルトに
    loop.run_forever()                # 無限に回し続ける

threading.Thread(target=loop_runner, args=(loop,), daemon=True).start()

# ----------------- ② AI 推論コルーチン ------------------------------------
async def ai_think(pid: int):
    await asyncio.sleep(0.8)          # 疑似思考ウェイト

    # --- 行動候補を取得 ---
    acts = Game.get_capable_sousa()
    if not acts:
        ai_q.put(None)                # 何も出来ない
    else:
        cmd = random.choice(acts)     # とりあえずランダム
        ai_q.put(cmd)

    # --- メインへ「出来たよ」通知 ---
    pygame.event.post(pygame.event.Event(AI_DONE))

def launch_ai(pid: int):
    """メインスレッドから AI コルーチンを発火"""
    asyncio.run_coroutine_threadsafe(ai_think(pid), loop)

# ----------------- ③ メインループ -----------------------------------------
waiting_ai = False                    # いま AI 思考中か？
running = True
while running:
    cmd = None

    # 入力イベント処理
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if Game.wait_p_id == MY_PID:
                acts = Game.get_capable_sousa()
                cmd  = acts[0] if acts else None
        elif ev.type == AI_DONE:      # ← コルーチン完了通知
            cmd = ai_q.get()
            waiting_ai = False        # 思考完了

    # AI が入力待ちになった瞬間にコルーチンを発火
    if Game.wait_p_id in AI_PIDS and not waiting_ai:
        launch_ai(Game.wait_p_id)
        waiting_ai = True

    # ゲームを 1 フレーム進行
    Game.step(cmd)

    # 簡易描画
    screen.fill((0, 96, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
