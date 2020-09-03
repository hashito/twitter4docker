import json
import os
import time
import datetime
import json
import requests
from requests_oauthlib import OAuth1Session

TRANS_URL=os.environ["TRANS_URL"]
SOURCE_TYPE=os.environ["SOURCE_TYPE"]
TARGET_TYPE=os.environ["TARGET_TYPE"]

TARGET_USER_ID=os.environ["TARGET_USER_ID"]
TARGET_COUNT=int(os.environ["TARGET_COUNT"])
SCREEN_NAME=os.environ["SCREEN_NAME"]

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

def cash_write(data):
    with open(CASH_FILE,mode="w") as f:
        f.write(json.dumps(data,ensure_ascii=False))

def read_tweet(since_id):
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params ={
            'count'      : TARGET_COUNT , 
            'user_id'    : TARGET_USER_ID ,
            'tweet_mode' : "extended"
            }
    if(since_id):
        params['since_id']=since_id
    
    req = twitter.get(url,params=params)
    if req.status_code == 200:
        res = json.loads(req.text)
        for line in res:
            print(line['user']['name']+'::'+line['full_text'])
            print(line['created_at'])
            print('*******************************************')
        return res
    else:
        print("Failed: %d" % req.status_code)
        return []
    
def send_tweet(text,tgurl,replyid=False):
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
    url = "https://api.twitter.com/1.1/statuses/update.json" 
    params = {
        "status" : text,
        "batch_mode":"first",
        "weighted_character_count":True,
        "attachment_url":tgurl
        }
    if(replyid):
        params["batch_mode"] ="subsequent"
        params["status"]     =f"@{SCREEN_NAME} " + params["status"]
        params["in_reply_to_status_id"] = replyid
    
    print(params)
    res = twitter.post(url, params = params) 
    if(res.status_code == 200):
        return json.loads(res.text)["id_str"]
    else:
        print(res.status_code,res.text)
        return False

def trans_tweet(text):
    params ={
            'text'   : text , 
            'source' : SOURCE_TYPE,
            'target' : TARGET_TYPE,
            }    
    print(TRANS_URL,params)
    req = requests.get(TRANS_URL,params=params)
    if req.status_code == 200:
        res = json.loads(req.text)
        print(res["text"])
        return res["text"]
    else:
        print("Failed: %d" % req.status_code)
        return []

#############################
#  @foxnews => [to:Fox News]
def mentions2name(tweet):
    text = tweet['full_text']
    if('entities' in tweet and 'user_mentions' in tweet['entities']):
        user_mentions = tweet['entities']['user_mentions']
        for u in user_mentions:
            text = text.replace(f"@{u['screen_name']}",f"[to:{u['name']}]")
        tweet["mentions2name"]={"text":text}
    return text


def tweetsplit(text,tweet_max=130):
    base_texts=text.split()
    ret=[]
    count=0
    tmp_text=[]
    for t in base_texts:
        if(len(t)>=tweet_max):
            ret.append(" ".join(tmp_text))
            ret.extend([t[i: i+tweet_max] for i in range(0,len(t),tweet_max)])
            count=0
            tmp_text=[]
        else:
            count=count+len(t)+1
            if(count>=tweet_max):
                ret.append(" ".join(tmp_text))
                count=len(t)
                tmp_text=[]
            tmp_text.append(t)
    if(not tmp_text==[]):
        ret.append(" ".join(tmp_text))
    return ret


if(__name__ == '__main__'):
    cash=cash_read()
    print("cash:",cash)
    while(1):
        tm=datetime.datetime.now().timestamp()
        tweets=read_tweet(cash["since_id"])
        for i in tweets:
            url=f"https://twitter.com/{i['user']['screen_name']}/status/{i['id_str']}"
            text  = mentions2name(i)
            text  = trans_tweet(text)
            texts = tweetsplit(text)
            replyid=False
            for t in texts:
                replyid=send_tweet(t,url,replyid)
                time.sleep(TWEET_DELAY)
            if(not cash["since_id"] or int(cash["since_id"])<int(i['id_str'])):
                cash["since_id"]=i['id_str']
            cash_write(cash)
        time.sleep(SCAN_SPAN)

#    # trans_tweet:test
#    trans_tweet("これはペンです")
#    # tes:tweetsplit
#    print(tweetsplit("1234567890",1))
#    print(tweetsplit("1 2 34 567 8 90",2))
#    print(tweetsplit("1 2 34 567 8 90",3))
#    print(tweetsplit("1 2 34 567 8 90",4))
#    print(tweetsplit("1 2 34 567 8 90",5))
#    print(tweetsplit("1 2 34 567 8 90",6))
#    print(tweetsplit("1 2 34 567 8 90",7))
#    print(tweetsplit("1 2 34 567 8 90",8))
#    print(tweetsplit("1 2 34 567 8 90",9))
#    print(tweetsplit("1 2 34 567 8 90",10))
#    print(tweetsplit("1 2 34 567 8 90",11))
#    print(tweetsplit("1 2 34 567 8 90",12))
#    print(tweetsplit("1 2 34 567 8 90",13))
#    print(tweetsplit("1 2 34 567 8 90",14))
#    print(tweetsplit("1 2 34 567 8 90",15))
#    print(tweetsplit("1 2 34 567 8 90",16))
#    print(tweetsplit("1 2 34 567 8 90",17))
#    print(tweetsplit("1 2 34 567 8 90",18))
#    print(tweetsplit("1 2 34 567 8 90",19))
#    print(tweetsplit("1 2 34 567 8 90",20))
#    print(tweetsplit("1 2 34 567 8 90",21))