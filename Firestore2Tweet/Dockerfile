FROM python:3

ENV CONSUMER_KEY=x \
    CONSUMER_SECRET=x \
    ACCESS_TOKEN=x \
    ACCESS_TOKEN_SECRET=x \
    TWEET_DELAY=20 \
    SCAN_SPAN=60 \
    COLLECTION_NAME="tweet"\
    FIREBASEKEY="xxxxx" \
    GOOGLE_APPLICATION_CREDENTIALS="/firebase.json" 

COPY . /root/
RUN pip install -r /root/requirements.txt
RUN chmod a+x /root/run.sh
CMD ["/root/run.sh"]
