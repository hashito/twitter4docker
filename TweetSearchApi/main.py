import os
import sys
import json
import time
import pytz

#from pytz import timezone
from requests_oauthlib import OAuth1Session,OAuth1
from datetime import datetime,timedelta,timezone
from flask import Flask

import requests
import mysql.connector as mydb

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

DB_HOST=os.environ["DB_HOST"]
DB_USERNAME=os.environ["DB_USERNAME"]
DB_PASSWORD=os.environ["DB_PASSWORD"]
DB_PORT=os.environ["DB_PORT"]
DB_DATABASE=os.environ["DB_DATABASE"]

CASH_FILE="/root/cash"
app = Flask(__name__)
JST = timezone(timedelta(hours=+9), 'JST')

def cash_read():
    try:
        with open(CASH_FILE,mode="r") as f:
            return json.loads(f.read())
    except:
        pass
    return False

def cash_write(data):
    with open(CASH_FILE,mode="w") as f:
        f.write(json.dumps(data,ensure_ascii=False))

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
            tweets.append(
                (line['id_str'],
                line['user']['id_str'],
                twdate2date(line['created_at']).strftime('%Y/%m/%d %H:%M:%S'),
                line['text'],
                line["favorite_count"],
                line["retweet_count"]
                )
            )
            print(json.dumps([line['id_str'],line['user']['id_str'],line["favorite_count"],line["retweet_count"]], ensure_ascii=False ))
            print("https://twitter.com/{}/status/{}".format(line['user']['id_str'],line['id_str']))
        return tweets
        
        for line in res["statuses"]:
            print(line["text"])
    else:
        print("Failed: %d" % req.status_code)
    return False


def resist_db(tweets):
    conn = mydb.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_DATABASE
    )
    conn.ping(reconnect=True)
    print(conn.is_connected())
    cur = conn.cursor()
    try:
        v=cur.executemany(
            "INSERT INTO tweets VALUES (%s,%s,%s,%s,%s,%s,0)", tweets)
        conn.commit()
    except Exception as e:
        print("err",e)
    cur.close()
    conn.close()


@app.route('/')
def tweet_get():
    if(not cash_read()):
        cash_write({"time":str(datetime.now(JST))})

    tweets = search_tweet()
    if(tweets):
        resist_db(tweets)
    return json.dumps(tweets, ensure_ascii=False),200

if(__name__ == '__main__'):
    app.run(debug=True,host="0.0.0.0",port=80)
