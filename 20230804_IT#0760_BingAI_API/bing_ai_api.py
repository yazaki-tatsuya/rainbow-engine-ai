import requests
#---- 掲載時不要START ----#
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#---- 掲載時不要END ----#
import env
# 環境変数の設定を読み込み
bing_subscription_key = env.get_env_variable('BING_AI_API_KEY')

def bing_web_search(subscription_key, query):
    # set parameters
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": query,
        "textDecorations": True,
        "textFormat": "HTML"}
    # get response
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def main():
    result = bing_web_search(
        bing_subscription_key,
        "SUUMOで次の条件に合致する中古マンションのURLを教えて。①JR藤沢駅、②3LDK、徒歩5分以内、③築年数15年以内、④4000万円以内"
    )
    print(result['webPages']['value'][0]['url'])

if __name__ == "__main__":
    main()