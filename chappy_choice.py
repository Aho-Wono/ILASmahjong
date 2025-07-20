import os
import random
from dotenv import load_dotenv
import openai

def chappy_choice(situations , what_ai_can_do):
    load_dotenv(".env")
    chatgpt = openai.OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
    
    setting = "あなたはプロの雀士です。今から誰かの手牌と全員分の河と鳴きの様子を伝えます。" \
    "牌の表示は省略されていて、萬子、筒子、索子はそれぞれ一文字目にm、p、sで二文字目には1~9の数字で表されます。" \
    "字牌は、ton、nan、chunのようにローマ字で表されます。" \
    "その試合では、プレイヤーには0,1,2,3の番号が割り振られ、0,1,2,3,0,1...と番が回ってきます。" \
    "まず、誰の手牌であるかの情報がプレイヤーの番号で与えられます。" \
    "次に、手牌の情報が3つの要素で与えられます。手持ち牌と鳴き牌とツモ牌です。" \
    "手持ち牌はツモをする前まで持っていた鳴いていない牌です。鳴き牌は既に鳴いた牌です。" \
    "鳴き牌はリスト形式で与えられ、牌ごとに誰の牌であったかの番号が割り振られています。" \
    "ツモ牌は、その直前にツモした牌です。直前に鳴きを行って他家から牌をもらった場合はNoneになります。" \
    "河の情報はリスト形式で与えられ、その四つの中身は、最初から順番にプレイヤー0,1,2,3の河を示しています。" \
    "河の牌には牌の種類以外に別の情報が与えられます。牌の種類のすぐ次にあるTrueかFalseは、" \
    "Trueの場合にはそこでその河のプレイヤーが立直したことを示し、Falseはそうでないことを示します。その次にあるTrueかFalseは無視してください" \
    "鳴きの様子の情報はリスト形式で与えられ、その四つの中身は、最初から順番にプレイヤー0,1,2,3の鳴きの様子を示しています。" \
    "牌ごとに誰の牌であったかの番号が割り振られています。" \
    "また、あなたには現在可能な行動の選択肢が与えられます。" \
    "行動の選択肢はリスト形式で与えられ、最初の要素はそれを行うプレイヤー番号、二番目の要素は行動の具体的な内容、三番目の要素は使う牌を示します。四、五番目の要素がある場合は無視してください。" \
    "二番目の要素である行動の具体的な内容は、kiru(切る)やron(ロン)などローマ字で示されます。ignoreは何もしないことを表します。" \
    "あなたは、与えられた情報から、最も効果的と考えられる選択肢を選び、その選択肢の0ベースのインデックスの数字のみを出力してください。" \
    "解説などは不要なので数字のみを出力してください。"
    
    joukyou = {
        "プレイヤー番号" : situations["whoturn"],
        "手持ち牌" : situations["tehai"]["menzen"],
        "鳴き牌" : situations["tehai"]["naki"],
        "ツモ牌" : situations["tehai"]["tumo"],
        "河" : situations["kawa_li"],
        "鳴きの様子" : situations["naki"],
        "選択肢" : what_ai_can_do
    }

    response = chatgpt.chat.completions.create(
        model = "gpt-4-turbo", 
        messages = [{"role": "system", "content": setting} ,
                    {"role": "user", "content": str(joukyou)}
        ]
    )

    answer = response.choices[0].message.content
    try:
        selected_action = what_ai_can_do[int(answer)]
    except:
        print("chappy_choice error")
        selected_action = random.choice(what_ai_can_do)
    return selected_action