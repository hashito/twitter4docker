import json
import os
import time
import datetime
import json
import requests
from flask import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from requests_oauthlib import OAuth1Session
app = Flask(__name__)

PORT = int(os.environ['PORT'])
# CONSUMER_KEY=os.environ["CONSUMER_KEY"]
# CONSUMER_SECRET=os.environ["CONSUMER_SECRET"]
# ACCESS_TOKEN=os.environ["ACCESS_TOKEN"]
# ACCESS_TOKEN_SECRET=os.environ["ACCESS_TOKEN_SECRET"]
# COLLECTION_NAME=os.environ['COLLECTION_NAME']

TWEET_DELAY=int(os.environ["TWEET_DELAY"])

GOOGLE_APPLICATION_CREDENTIALS=os.environ['GOOGLE_APPLICATION_CREDENTIALS']
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(cred)
db=firestore.Client()
    
def send_tweet(text,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
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
    return ret

@app.route('/')
def doUpdate():
    #CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    consumerkey       = request.args.get("consumerkey")
    consumersecret    = request.args.get("consumersecret")
    accesstoken       = request.args.get("accesstoken")
    accesstokensecret = request.args.get("accesstokensecret")
    collection        = request.args.get("collection")
    tm=datetime.datetime.now().timestamp()
    print(request.args)
    print("tm:",tm)
    docs = db.collection(collection).where(u'time', u'<', tm).stream()
    first_flag=True
    for doc in docs:
        if(not first_flag):
            time.sleep(TWEET_DELAY)
        first_flag=False
        
        d = doc.to_dict()
        send_tweet(d["text"],consumerkey,consumersecret,accesstoken,accesstokensecret)
        db.collection(collection).document(doc.id).delete()
        print("delete",doc.id)
    return "ok",200

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=PORT)