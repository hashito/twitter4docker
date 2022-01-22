FROM python:3

ENV TWEET_DELAY=20 \
    PORT=80 \
    FIREBASEKEY="xxxxx" \
    GOOGLE_APPLICATION_CREDENTIALS="/firebase.json" 

#    CONSUMER_KEY=x \
#    CONSUMER_SECRET=x \
#    ACCESS_TOKEN=x \
#    ACCESS_TOKEN_SECRET=x \
#    COLLECTION_NAME="tweet"\
    
COPY . /root/
RUN pip install -r /root/requirements.txt
RUN chmod a+x /root/run.sh
CMD ["/root/run.sh"]
