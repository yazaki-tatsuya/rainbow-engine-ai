import openai
from sklearn.datasets import fetch_20newsgroups
import pandas as pd

def main():

    #### データの取得 ####
    # scikit-learnのサンプルデータセットを取得
    categories = ['rec.sport.baseball', 'rec.sport.hockey']
    dataset = fetch_20newsgroups(subset='train', shuffle=True, random_state=42, categories=categories)
    # チェック
    # print(dataset)

    #### データの加工&JSONL出力 ####
    # 分離は「dataset['target']」に入っており、分類は「大分類.小分類」の様になってるため「split('.')[-1]」で.以降を取得する
    labels = [dataset.target_names[x].split('.')[-1] for x in dataset['target']]
    texts = [text.strip() for text in dataset['data']]
    # dataframe形式に変換
    df = pd.DataFrame(zip(texts, labels), columns = ['prompt','completion']) #[:300]
    # JSONL形式で出力
    df.to_json("test_sport.jsonl", orient='records', lines=True)
    # チェック
    print(df.head())

if __name__ == "__main__":
     main()