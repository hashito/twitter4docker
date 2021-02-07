import os
import sys
import json
import time
import pytz
import datetime

from requests_oauthlib import OAuth1Session,OAuth1
#from datetime import datetime,timedelta,timezone

import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import *

app = Flask(__name__)
PORT = int(os.environ['PORT'])
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
FIRST_TIME=os.environ["FIRST_TIME"]

GOOGLE_APPLICATION_CREDENTIALS=os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

SET_COLLECTION_NAME=os.environ["SET_COLLECTION_NAME"]
CASH_COLLECTION_NAME=os.environ["CASH_COLLECTION_NAME"]
CASH_DOCUMENT_NAME=os.environ["CASH_DOCUMENT_NAME"]

cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred)

CASH_FILE="/root/cash"
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


def cash_read():
    db=firestore.Client()
    try:
        ret = db.collection(CASH_COLLECTION_NAME).document(CASH_DOCUMENT_NAME).get().to_dict()
    except:
        pass 
    if(not ret):   
        ret = {"time":FIRST_TIME}
    return ret

def cash_write(data):
    db=firestore.Client()
    try:
        db.collection(CASH_COLLECTION_NAME).document(CASH_DOCUMENT_NAME).set(data)
    except:
        db.collection(CASH_COLLECTION_NAME).document(CASH_DOCUMENT_NAME).update(data)

def twdate2date(dt):
    r = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
    try:
        r = r.astimezone(pytz.timezone('Asia/Tokyo'))
    except:
        pass
    return r

def search_tweet():
    tm = datetime.datetime.fromtimestamp(int(cash_read()["time"]))
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    url  = "https://api.twitter.com/1.1/search/tweets.json"
    # Enedpointへ渡すパラメーター
    params ={
            'q'       : f"{REQ_Q} since:{tm.strftime('%Y-%m-%d_%H:%M:%S')}_JST",# サーチテキスト
            'lang'    : REQ_LANG        , # Language
            'locale'  : REQ_LOCALE      ,
            'popular' : REQ_POPULAR     , # type(最新のみ)
            'count'   : REQ_COUNT       , # count
            'include_entities' : REQ_INCLUDE_ENTITIES ,
            'tweet_mode' : "extended"
            }
    print(json.dumps(params, ensure_ascii=False ))
    req = requests.get(url, params = params,auth=auth)
    cash_write({"time":time.time()})

    if req.status_code == 200:
        tweets=[]
        res = json.loads(req.text)
        for line in res['statuses']:
            tmpdata={
                "id":line['id_str'],
                "uid":line['user']['id_str'],
                "time":twdate2date(line['created_at']).timestamp(),
                "text":line['full_text'],
                "favorite_count":line["favorite_count"],
                "retweet_count":line["retweet_count"]
# --debug--
#                ,
#                "d_time":twdate2date(line['created_at']).strftime('%Y/%m/%d %H:%M:%S'),
#                "d_debug":json.dumps(line,ensure_ascii=False ) #this is debug
            }
            try:
                tmpdata["url"]=line["entities"]["urls"][0]["expanded_url"]
            except:
                pass
            tweets.append(tmpdata)
            print(json.dumps(line,ensure_ascii=False ))
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
            db.collection(SET_COLLECTION_NAME).document(tweet["id"]).set(tweet)
        except Exception as e:
            print("resist_firestore",e)

@app.route('/')
def doUpdate():
    resist_firestore(search_tweet())
    return "ok",200

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=PORT)
