FROM python:3

COPY ./python/ /root/
RUN pip install -r /root/requirements.txt
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
    FIREBASE_KEY_FILE="/root/.firebasekey.json" \
    FIREBASE_STORE_COLLECTION="raw"

CMD ["python","/root/main.py"]