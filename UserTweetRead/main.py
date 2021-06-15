import json
import os
import time
import datetime
import json
import requests
from requests_oauthlib import OAuth1Session
from flask import *
import time

app = Flask(__name__)

PORT = int(os.environ['PORT'])

TARGET_USER_ID=os.environ["TARGET_USER_ID"]
TARGET_COUNT=int(os.environ["TARGET_COUNT"])
SCREEN_NAME=os.environ["SCREEN_NAME"]


CONSUMER_KEY=os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]

TWEET_DELAY=int(os.environ["TWEET_DELAY"])
FIRST_TWEET_ID=os.environ['FIRST_TWEET_ID']


COLLECTION_NAME=os.environ['COLLECTION_NAME']
DOCUMENT_NAME=os.environ['DOCUMENT_NAME']

def cash_read():
    db=firestore.Client()
    try:
        ret = db.collection(COLLECTION_NAME).document(DOCUMENT_NAME).get().to_dict()
    except:
        pass 
    if(not ret):   
        ret = {"since_id":FIRST_TWEET_ID}
    return ret

def cash_write(data):
    db=firestore.Client()
    try:
        db.collection(COLLECTION_NAME).document(DOCUMENT_NAME).set(data)
    except:
        db.collection(COLLECTION_NAME).document(DOCUMENT_NAME).update(data)

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
    
    req = twitter.get(url,params=params,timeout=60.0)
    if req.status_code == 200:
        res = list(json.loads(req.text))
#        print(json.dumps(res))
        for line in res:
            print(line['user']['name']+'::'+line['full_text'])
            print(line['created_at'])
            print('*******************************************')
        return res
    else:
        print("Failed: %d" % req.status_code)
        return []
    
@app.route('/')
def doUpdate():
    cash=cash_read()
    print("cash:",cash)
    tm=datetime.datetime.now().timestamp()
    tweets=read_tweet(cash["since_id"])
    tweets.reverse()
    print(f"{tm}={cash['since_id']}," ,end="")
    
    for i in tweets:
        i['full_text'];
        if(not cash["since_id"] or int(cash["since_id"])<int(i['id_str'])):
            cash["since_id"]=i['id_str']
    cash_write(cash)
    with open(time.time(), mode='w') as f:
    f.write(s)
    return "ok",200

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=PORT)


