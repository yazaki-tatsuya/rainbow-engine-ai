import json
import openai
from datetime import datetime, timedelta
#---- 掲載時不要START ----#
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#---- 掲載時不要END ----#
import env
# 環境変数の設定を読み込み
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
        }
    ]
    
    # ユーザーからの質問（プロンプト）
    user_prompt = "次の羽田からニューヨークへのフライトはいつですか？"

    # GPTに問いかけを行い、返答を取得
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        # 関数の情報を渡す
        functions=function_descriptions,
        function_call="auto",
    )

    # プロンプトの内容に基づき、自動的に関数の要否を判断して、引数も埋めた状態で返却してくれる
    output = completion.choices[0].message
    print("=== LLMの出力："+str(output))

    # 出力から関数の引数を取得
    #   json.loads関数で文字列をPythonオブジェクトに変換
    departure = json.loads(output.function_call.arguments).get("departure")
    destination = json.loads(output.function_call.arguments).get("destination")
    params = json.loads(output.function_call.arguments)

    print("=== 出発地："+departure)
    print("=== 目的地："+destination)
    print("=== 引数："+str(params))

    # 取得した引数を与えて、関数を呼び出し
    chosen_function = eval(output.function_call.name)
    flight = chosen_function(**params)

    print("=== 実行する関数："+str(chosen_function))
    print("=== 実行結果："+flight)

if __name__ == '__main__':
    main()