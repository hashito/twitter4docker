import os
import sys
import json
import time
import pytz

#from pytz import timezone
from requests_oauthlib import OAuth1Session,OAuth1
from datetime import datetime,timedelta,timezone

import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

CONSUMER_KEY=os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]

REQ_Q=os.environ["REQ_Q"]
REQ_LANG=os.environ["REQ_LANG"]
REQ_LOCALE=os.environ["REQ_LOCALE"]
REQ_POPULAR=os.environ["REQ_POPULAR"]
REQ_COUNT=int(os.environ["REQ_COUNT"])
REQ_INCLUDE_ENTITIES=os.environ["REQ_INCLUDE_ENTITIES"]
REQ_INTERVAL=int(os.environ["REQ_INTERVAL"])

FIREBASE_KEY_FILE=os.environ["FIREBASE_KEY_FILE"]
FIREBASE_STORE_COLLECTION=os.environ["FIREBASE_STORE_COLLECTION"]

cred = credentials.Certificate(FIREBASE_KEY_FILE)
firebase_admin.initialize_app(cred)

CASH_FILE="/root/cash"
JST = timezone(timedelta(hours=+9), 'JST')

def cash_read():
    try:
        with open(CASH_FILE,mode="r") as f:
            return json.loads(f.read())
    except:
        # deflute
        return cash_write({"time":str(datetime.now(JST))})
    return False

def cash_write(data):
    with open(CASH_FILE,mode="w") as f:
        f.write(json.dumps(data,ensure_ascii=False))
    return data

def twdate2date(dt):
    r = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
    try:
        r = r.astimezone(pytz.timezone('Asia/Tokyo'))
    except:
        pass
    return r

def search_tweet():
    time = datetime.fromisoformat(cash_read()["time"])
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    url  = "https://api.twitter.com/1.1/search/tweets.json"
    # Enedpointへ渡すパラメーター
    params ={
            'q'       : f"{REQ_Q} since:{time.strftime('%Y-%m-%d_%H:%M:%S')}_JST",# サーチテキスト
            'lang'    : REQ_LANG        , # Language
            'locale'  : REQ_LOCALE      ,
            'popular' : REQ_POPULAR     , # type(最新のみ)
            'count'   : REQ_COUNT       , # count
            'include_entities' : REQ_INCLUDE_ENTITIES 
            }
    print(json.dumps(params, ensure_ascii=False ))
    req = requests.get(url, params = params,auth=auth)
    cash_write({"time":str(datetime.now(JST))})

    if req.status_code == 200:
        tweets=[]
        res = json.loads(req.text)
        for line in res['statuses']:
            tmpdata={
                "id":line['id_str'],
                "uid":line['user']['id_str'],
                "time":twdate2date(line['created_at']).strftime('%Y/%m/%d %H:%M:%S'),
                "text":line['text'],
                "favorite_count":line["favorite_count"],
                "retweet_count":line["retweet_count"]
            }
            try:
                tmpdata["url"]=line["entities"]["urls"][0]["expanded_url"]
            except:
                pass
            tweets.append(tmpdata)
            print(json.dumps([line['id_str'],line['user']['id_str'],line["favorite_count"],line["retweet_count"]], ensure_ascii=False ))
            print("https://twitter.com/{}/status/{}".format(line['user']['id_str'],line['id_str']))
        return tweets
        
        for line in res["statuses"]:
            print(line["text"])
    else:
        print("Failed: %d" % req.status_code)
    return False

def resist_firestore(tweets):
    db = firestore.client()
    for tweet in tweets:
        try:
            db.collection(FIREBASE_STORE_COLLECTION).document(tweet["id"]).set(tweet)
        except Exception as e:
            print("resist_firestore",e)

if(__name__ == '__main__'):
    while(True):
        resist_firestore(search_tweet())
        time.sleep(REQ_INTERVAL)

