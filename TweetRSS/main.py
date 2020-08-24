import feedparser
import json
import os
import time
import datetime
import json
from requests_oauthlib import OAuth1Session

RSS_URL=os.environ["RSS_URL"]
CONSUMER_KEY=os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]

CASH_FILE=os.environ["CASH_FILE"]
ADD_TEXT=os.environ["ADD_TEXT"]
SCAN_SPAN=int(os.environ["SCAN_SPAN"])
TWEET_DELAY=int(os.environ["TWEET_DELAY"])


def cash_read():
    with open(CASH_FILE) as f:
        return json.loads(f.read())

def cash_wite(data):
    with open(CASH_FILE,"w") as f:
        f.wite(json.dumps(data),ensure_ascii=False)

def read_rss():
    return feedparser.parse(RSS_URL)
    
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
            cash_wite(cash)
        for k in cash.keys():
            if((cash[k]+60)<tm):
                print("delete:",k,cash[k],tm)
                cash.pop(k)
        time.sleep(SCAN_SPAN)