FROM python:3

ENV CONSUMER_KEY=x \
    CONSUMER_SECRET=x \
    ACCESS_TOKEN=x \
    ACCESS_TOKEN_SECRET=x \
    REQ_Q="hashito filter:images"  \
    REQ_LANG="ja"  \
    REQ_LOCALE="ja"  \
    REQ_POPULAR="recent"  \
    REQ_COUNT="10"  \
    REQ_INTERVAL="20"  \
    REQ_INCLUDE_ENTITIES="true"  \
    FIREBASEKEY="xxx" \
    PORT=80 \
    GOOGLE_APPLICATION_CREDENTIALS="/firebase.json" \
    FIRST_TIME=1612600205 \
    CASH_DOCUMENT_NAME="cash" \
    CASH_COLLECTION_NAME="cash" \
    SET_COLLECTION_NAME="raw"

COPY . /root/
RUN pip install -r /root/requirements.txt
RUN chmod a+x /root/run.sh
CMD ["/root/run.sh"]
