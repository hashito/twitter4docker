FROM python:3


COPY . /root/

RUN pip install -r /root/requirements.txt

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
    CASH_FILE=/root/cash \
    SCAN_SPAN=60 \
    TWEET_DELAY=150

RUN chmod a+x /root/run.sh
CMD ["/root/run.sh"]
