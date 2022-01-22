# comment

Firestore2Tweet

## use
```
docker run -it --rm -p 80:80 \
    -e SCAN_SPAN=60 \
    -e TWEET_DELAY=60 \
    -e FIREBASEKEY=xxxx \
    asia.gcr.io/active-landing-173201/firestore2tweet-server-v2:20210619
#    -e SCREEN_NAME=hasitozzz \
#    -e CONSUMER_KEY=x \
#    -e CONSUMER_SECRET=x \
#    -e ACCESS_TOKEN=x-x \
#    -e ACCESS_TOKEN_SECRET=x \
```

## build

```
docker build -t hashito/firestore2tweet .
docker build . -t asia.gcr.io/active-landing-173201/firestore2tweet-server-v2:20210619
```

## data

{
    "time":1611473233,
    "text":"test",
    "url":"https://httpbin"
}