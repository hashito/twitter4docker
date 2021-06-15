FROM python:3

ENV TRANS_URL=https://script.google.com/macros/s/xxxx \
    SOURCE_TYPE=ja \
    TARGET_TYPE=en \
    TARGET_USER_ID=1176288952401059841 \
    SCREEN_NAME=hashito \
    TARGET_COUNT=10 \
    CONSUMER_KEY=x \
    CONSUMER_SECRET=x \
    ACCESS_TOKEN=x \
    ACCESS_TOKEN_SECRET=x \
    FIRST_TWEET_ID=1357840369602461696 \
    DOCUMENT_NAME=001 \
    COLLECTION_NAME=cash \
    GOOGLE_APPLICATION_CREDENTIALS=/firebase.json \
    FIREBASEKEY=xxxx \
    PORT=80 \
    TWEET_DELAY=150

COPY . /root/
RUN pip install -r /root/requirements.txt
RUN chmod a+x /root/run.sh
CMD ["/root/run.sh"]
