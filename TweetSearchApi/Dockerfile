FROM python:3

COPY . /root/
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
    REQ_INCLUDE_ENTITIES="true"  \
    DB_HOST="localhost"  \
    DB_USERNAME="root"  \
    DB_PASSWORD="pass"  \
    DB_PORT="3306"  \
    DB_DATABASE="tw"

CMD ["python","/root/main.py"]