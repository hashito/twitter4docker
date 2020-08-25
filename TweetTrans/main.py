import feedparser
import json
import os
import time
import datetime
import json
from requests_oauthlib import OAuth1Session

TRANS_URL=os.environ["TRANS_URL"]
SOURCE_TYPE=os.environ["SOURCE_TYPE"]
TARGET_TYPE=os.environ["TARGET_TYPE"]
TARGET_USER=os.environ["TARGET_USER"]

CONSUMER_KEY=os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]

CASH_FILE=os.environ["CASH_FILE"]
SCAN_SPAN=int(os.environ["SCAN_SPAN"])
TWEET_DELAY=int(os.environ["TWEET_DELAY"])


def cash_read():
    with open(CASH_FILE) as f:
        return json.loads(f.read())

def cash_wite(data):
    with open(CASH_FILE,"w") as f:
        f.wite(json.dumps(data),ensure_ascii=False)

def read_tweet():
    # Twitter Endpoint(ユーザータイムラインを取得する)
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    # Enedpointへ渡すパラメーター
    params ={
            'count'       : 5,             # 取得するtweet数
            'screen_name' : 'mos_burger',  # twitterアカウント名
            }

    req = twitter.get(url, params = params)

    if req.status_code == 200:
        res = json.loads(req.text)
        for line in res:
            print(line['user']['name']+'::'+line['text'])
            print(line['created_at'])
            print('*******************************************')
    else:
        print("Failed: %d" % req.status_code)
    
def send_tweet(text):
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) #認証処理
    url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント
    params = {"status" : text}
    res = twitter.post(url, params = params) #post送信
    return res.status_code == 200

if(__name__ == '__main__'):
    cash=cash_read()
    print("cash:",cash)
    while(1):
        tm=datetime.datetime.now().timestamp()
        rss=read_rss()
        for i in rss["entries"]:
            if(not i["id"] in cash):
                print("tweet:",f"{i['title']} {i['link']} {ADD_TEXT}")
                send_tweet(f"{i['title']} {i['link']} {ADD_TEXT}")
                time.sleep(TWEET_DELAY)
            cash["id"]=tm
        for k in cash.keys():
            if((cash[k]+60)<tm):
                print("delete:",k,cash[k],tm)
                cash.pop(k)
        time.sleep(SCAN_SPAN)
# update