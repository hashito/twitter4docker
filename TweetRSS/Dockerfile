FROM python:3


COPY . /root/

RUN pip install -r /root/requirements.txt

ENV RSS_URL=https://news.google.com/rss/search?hl=ja&gl=JP&ceid=JP:ja&q=twitter \
    CONSUMER_KEY=x \
    CONSUMER_SECRET=x \
    ACCESS_TOKEN=x \
    ACCESS_TOKEN_SECRET=x \
    CASH_FILE=/root/cash \
    ADD_TEXT="#rss2tweet" \
    SCAN_SPAN=600 \
    TWEET_DELAY=150

RUN chmod a+x /root/run.sh
CMD ["/root/run.sh"]