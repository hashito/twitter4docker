# comment

Firestore2Tweet

## use
```
docker run -it --rm \
    -e CONSUMER_KEY=x \
    -e CONSUMER_SECRET=x \
    -e ACCESS_TOKEN=x-x \
    -e ACCESS_TOKEN_SECRET=x \
    -e SCAN_SPAN=60 \
    -e TWEET_DELAY=60 \
    -e SCREEN_NAME=hasitozzz \
    hashito/firestore2tweet
```

## build

```
docker build -t hashito/firestore2tweet .
```

## data

{
    "time":1611473233,
    "text":"test",
    "url":"https://httpbin"
}