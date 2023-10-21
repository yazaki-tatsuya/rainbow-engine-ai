import openai
from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import env
def main():
    # APIキーの設定
    openai.api_key = env.get_env_variable("OPEN_AI_KEY")
    # Modelの指定
    ft_model = 'ada:ft-personal-2023-10-21-04-42-54'
    # 入力(prompt)の指定
    sample_input="""Team White strikes first! Oliver Moore off a nice pass from Joe Palodichuk to get things started."""
    # APIコール
    res = openai.Completion.create(model=ft_model, prompt=sample_input + '\n\n###\n\n', max_tokens=1, temperature=0, logprobs=2)
    # 結果出力
    print(res['choices'][0]["text"])

if __name__ == "__main__":
     main()