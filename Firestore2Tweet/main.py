import json
import os
import time
import datetime
import json
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from requests_oauthlib import OAuth1Session

CONSUMER_KEY=os.environ["CONSUMER_KEY"]
CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]

SCAN_SPAN=int(os.environ["SCAN_SPAN"])
TWEET_DELAY=int(os.environ["TWEET_DELAY"])

COLLECTION_NAME=os.environ['COLLECTION_NAME']
GOOGLE_APPLICATION_CREDENTIALS=os.environ['GOOGLE_APPLICATION_CREDENTIALS']
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred)
db=firestore.Client()
    
def send_tweet(text):
    ret     = False
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
    url     = "https://api.twitter.com/1.1/statuses/update.json" 
    params = {
            "status" : text,
            "batch_mode":"first",
            "weighted_character_count":True,
        }
    print(params)
    res = twitter.post(url, params = params,timeout=60.0) 
    if(res.status_code == 200):
        ret = json.loads(res.text)["id_str"]
    else:
        print("[err]",res.status_code,res.text)
    time.sleep(TWEET_DELAY)
    return ret

if(__name__ == '__main__'):
    while(1):
        tm=datetime.datetime.now().timestamp()
        docs = db.collection(COLLECTION_NAME).where(u'time', u'<', tm).stream()
        for doc in docs:
            d = doc.to_dict()
            send_tweet(d["text"])
            db.collection(COLLECTION_NAME).document(doc.id).delete()
            print("delete",doc.id)
            
        time.sleep(SCAN_SPAN)