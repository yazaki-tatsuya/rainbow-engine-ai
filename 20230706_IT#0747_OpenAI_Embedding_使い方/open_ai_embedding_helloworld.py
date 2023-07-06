import openai
import pandas as pd
import numpy as np
#---- 掲載時不要START ----#
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#---- 掲載時不要END ----#
# 環境変数の設定を読み込み
import env
openai.api_key = env.get_env_variable('OPEN_AI_KEY')
# Modelの指定
model = env.get_env_variable('MODEL_EMBEDDINGS')

def get_embedding(text, model=model):
    text = text.replace("\n", " ")
    result = openai.Embedding.create(
        engine=model,
        input = [text]
    )
    return result['data'][0]['embedding']

def main():
    ##################### 追記START #####################
    # 入力(prompt)のデータ(PandasのDataFrame)の生成
    question_1 = 'マウスの動作がカクカクする際の対処方法を教えてください'
    answer_1 = 'マウスの動作がカクカクする場合は、マウスのドライバーを再インストールしてみてください'
    answer_2 = 'Windowsの更新プログラムをインストールした後は、PCを再起動してみてください'
    df = pd.DataFrame({'value': [question_1, answer_1]},index=['1', '2'])

    # APIコールし、ベクトルを取得
    df["embedding_vector"] = df["value"].apply(lambda x : get_embedding(x))
    # question_1のベクトル、answer_nのベクトル値を抽出
    embedding_a = df["embedding_vector"][0]
    embedding_b = df["embedding_vector"][1]
    # 内積を取得
    similarity_score = np.dot(embedding_a, embedding_b)
    print(similarity_score)
    ##################### 追記END #####################

if __name__ == "__main__":
    main()