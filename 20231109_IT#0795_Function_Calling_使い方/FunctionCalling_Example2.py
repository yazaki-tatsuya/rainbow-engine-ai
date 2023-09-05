import json
import openai
from datetime import datetime, timedelta
#---- 掲載時不要START ----#
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#---- 掲載時不要END ----#
# 環境変数の設定を読み込み
import env
openai.api_key = env.get_env_variable('OPEN_AI_KEY')


# 出発地と目的地を引数としてフライト情報を取得する関数
def get_flight_info(departure, destination):
    """
    出発地と目的地の間のフライト情報を取得する関数
    """
    # デモのためのダミーのフライト情報（本来はDBやAPI経由で取得する）
    flight_info = {
        "departure": departure,
        "destination": destination,
        "datetime": str(datetime.now() + timedelta(hours=2)),
        "airline": "JAL",
        "flight": "JL0006",
    }
    # フライト情報をJSON形式で返す
    return json.dumps(flight_info)

def main():

    # GPTに渡す関数の説明
    function_descriptions = [
        {
            "name": "get_flight_info",
            "description": "出発地と目的地の2つの情報からフライト情報を取得する",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure": {
                        "type": "string",
                        "description": "出発地の空港。(例) HND",
                    },
                    "destination": {
                        "type": "string",
                        "description": "目的地の空港。(例) CDG",
                    },
                },
                "required": ["departure", "destination"],
            },
        },
        {
            "name": "book_flight",
            "description": "フライト情報を基に、フライトを予約する",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure": {
                        "type": "string",
                        "description": "出発地の空港。(例) HND",
                    },
                    "destination": {
                        "type": "string",
                        "description": "目的地の空港。(例) CDG",
                    },
                    "datetime": {
                        "type": "string",
                        "description": "フライトの日時。(例) 2023-01-01 01:01",
                    },
                    "airline": {
                        "type": "string",
                        "description": "航空会社の名前。(例) Japan Airline",
                    },
                },
                "required": ["departure", "destination", "datetime", "airline"],
            },
        },
        {
            "name": "inquiry",
            "description": "お客様のお問い合わせ窓口から、問い合わせを行う。",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "顧客名。(例) 山田 太郎",
                    },
                    "email": {
                        "type": "string",
                        "description": "顧客メールアドレス。(例) taro.yamada@rainbow.com",
                    },
                    "text": {
                        "type": "string",
                        "description": "お問い合わせの内容",
                    },
                },
                "required": ["name", "email", "text"],
            },
        },
    ]

    # -----------------------------------------------------
    # ステップ1：フライト情報をチェックする
    # -----------------------------------------------------
    user_prompt = "次の羽田からニューヨークへのフライトはいつですか？"
    
    # GPTに問いかけを行い、返答を取得
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user","content": user_prompt}],
        # 関数の情報を渡す
        functions=function_descriptions,
        function_call="auto",
    )

    # プロンプトの内容に基づき、自動的に正しい関数を判断して、引数も埋めた状態で返却してくれる
    output = completion.choices[0].message
    print("=== ステップ1 - LLMの出力："+str(output))

    # 出力から関数の引数を取得
    #   json.loads関数で文字列をPythonオブジェクトに変換
    origin = json.loads(output.function_call.arguments).get("departure")
    destination = json.loads(output.function_call.arguments).get("destination")

    # 取得した引数を与えて、関数を呼び出し
    chosen_function = eval(output.function_call.name)
    flight = chosen_function(origin, destination)

    print("=== ステップ1 - 出発地："+origin)
    print("=== ステップ1 - 目的地："+destination)
    print("=== ステップ1 - フライト情報："+flight)

    # 結果から、次のフライト予約に必要な情報を抽出
    flight_datetime = json.loads(flight).get("datetime")
    flight_airline = json.loads(flight).get("airline")

    print("=== ステップ1 - フライト日時："+flight_datetime)
    print("=== ステップ1 - 航空会社："+flight_airline)

    # -----------------------------------------------------
    # ステップ2：フライト情報を予約する
    # -----------------------------------------------------

    user_prompt2 = f"私は {flight_airline}の {origin} から {destination} への {flight_datetime} のフライトを、予約したいです。"
    
    # GPTに問いかけを行い、返答を取得
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user","content": user_prompt2}],
        # 関数の情報を渡す
        functions=function_descriptions,
        function_call="auto",
    )

    # プロンプトの内容に基づき、自動的に正しい関数を判断して、引数も埋めた状態で返却してくれる
    output = completion.choices[0].message
    print("=== ステップ2 - LLMの出力："+str(output))

    # -----------------------------------------------------
    # ステップ3：お問い合わせする
    # -----------------------------------------------------
    user_prompt3 = "AAA BBBです。xxx空港に落とし物が届いていないか確認させてください。落としたのは眼鏡です。"

    # GPTに問いかけを行い、返答を取得
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user","content": user_prompt3}],
        # 関数の情報を渡す
        functions=function_descriptions,
        function_call="auto",
    )

    # プロンプトの内容に基づき、自動的に正しい関数を判断して、引数も埋めた状態で返却してくれる
    output = completion.choices[0].message
    print("=== ステップ3 - LLMの出力："+str(output))

if __name__ == '__main__':
    main()