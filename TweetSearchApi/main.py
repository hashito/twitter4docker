import os
import sys
import json
import time

from pytz import timezone
from requests_oauthlib import OAuth1Session,OAuth1
from datetime import datetime,timedelta
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

def cash_read():
    with open(CASH_FILE) as f:
        return json.loads(f.read())

def cash_wite(data):
    with open(CASH_FILE,"w") as f:
        f.wite(json.dumps(data),ensure_ascii=False)

def twdate2date(dt):
    r = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
    try:
        r = r.astimezone(timezone('Asia/Tokyo'))
    except:
        pass
    return r

def search_tweet():
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    url = "https://api.twitter.com/1.1/search/tweets.json"

    # Enedpointへ渡すパラメーター
    params ={
            'q'       : REQ_Q           , # サーチテキスト
            'lang'    : REQ_LANG        , # Language
            'locale'  : REQ_LOCALE      ,
            'popular' : REQ_POPULAR     , # type(最新のみ)
            'count'   : REQ_COUNT       , # count
            'include_entities' : REQ_INCLUDE_ENTITIES 
            }

    req = requests.get(url, params = params,auth=auth)

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
#            print(line['user']['name']+'::'+line['text'])
#            print(line['created_at'])
#            print('*******************************************')
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
def hello():
    tweets = search_tweet()
    if(tweets):
        resist_db(tweets)
    return json.dumps(tweets, ensure_ascii=False),200

if(__name__ == '__main__'):
    app.run(debug=True,host="0.0.0.0",port=80)


#def send_tweet(text):
#    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) #認証処理
#    url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント
#    params = {"status" : text}
#    res = twitter.post(url, params = params) #post送信
#    return res.status_code == 200

#def tweets_serch(event, context):
#    try:
#        timespan  = int(os.environ.get('TIMESPAN',"600"))
#        # Twitter
#        CK        = os.environ.get('CONSUMER_KEY',None)
#        CS        = os.environ.get('CONSUMER_SECRET',None)
#        AT        = os.environ.get('ACCESS_TOKEN',None)
#        ATS       = os.environ.get('ACCESS_TOKEN_SECRET',None)
#        read_time = (datetime.now(timezone('Asia/Tokyo'))-timedelta(seconds=timespan)).strftime('%Y-%m-%d_%H:%M:%S_JST')
#
#        print("tw keys",CK, CS, AT, ATS)
#
#        def twdate2date(dt):
#            r = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')
#            try:
#                r = r.astimezone(timezone('Asia/Tokyo'))
#            except:
#                pass
#            return r
#
#        twitter = OAuth1Session(CK, CS, AT, ATS)
#        url = 'https://api.twitter.com/1.1/search/tweets.json'
#        tparams = {}
#        tparams["q"]          = os.environ.get('TWSEARCH_q',None)
#        tparams["geocode"]    = os.environ.get('TWSEARCH_geocode',None)
#        tparams["lang"]       = os.environ.get('TWSEARCH_lang',None)
#        tparams["locale"]     = os.environ.get('TWSEARCH_locale',None)
#        tparams["result_type"]= os.environ.get('TWSEARCH_result_type',None)
#        tparams["count"]      = os.environ.get('TWSEARCH_count',None)
#        tparams["until"]      = os.environ.get('TWSEARCH_until',None)
#        tparams["since_id"]   = os.environ.get('TWSEARCH_since_id',None)
#        tparams["since"]      = os.environ.get('TWSEARCH_since',read_time)
#        tparams["max_id"]     = os.environ.get('TWSEARCH_max_id',None)
#        tparams["include_entities"]= os.environ.get('TWSEARCH_include_entities',None)
#        params={}
#        for k in tparams:
#            if(not (tparams[k]==None)):
#                params[k]=tparams[k]
#
#        print(params)
#        req = twitter.get(url, params = params)
#        tweets=[]
#        if req.status_code == 200:
#            res = json.loads(req.text)
#            for line in res['statuses']:
#                tweets.append(
#                    (line['id_str'],
#                    line['user']['id_str'],
#                    twdate2date(line['created_at']).strftime('%Y/%m/%d %H:%M:%S'),
#                    line['text'],
#                    line["favorite_count"],
#                    line["retweet_count"]
#                    )
#                )
#                print(json.dumps([line['id_str'],line['user']['id_str'],line["favorite_count"],line["retweet_count"]] ))
#                print("https://twitter.com/{}/status/{}".format(line['user']['id_str'],line['id_str']))
#        else:
#            print("Failed: %d" % req.status_code)
#        print(json.dumps(tweets))
#
#        db_params={}
#        db_params["host"]          = os.environ.get('DB_host',"localhost")
#        db_params["user"]          = os.environ.get('DB_user',"root")
#        db_params["password"]      = os.environ.get('DB_password',"")
#        db_params["port"]          = os.environ.get('DB_port',"3306")
#        db_params["database"]      = os.environ.get('DB_database',"tw")
##        db_params["unix_socket"]   = "/cloudsql/{}".format(os.environ.get('DB_host',""))
#        
#
#
#        conn = mydb.connect(**db_params)
#        conn.ping(reconnect=True)
#        print(conn.is_connected())
#        cur = conn.cursor()
#        try:
#            v=cur.executemany(
#                "INSERT INTO tweets VALUES (%s,%s,%s,%s,%s,%s,0)", tweets)
#            conn.commit()
#        except Exception as e:
#            print("err",e)
#        cur.close()
#        conn.close()
#        return f'okey!'
#    except Exception as e:
#        return json.dumps(e)
#