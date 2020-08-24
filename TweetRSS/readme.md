# comment

Read RSS regularly and Tweet

## use

```
docker run -it --rm \
    -e RSS_URL=https://news.google.com/rss/search?hl=ja&gl=JP&ceid=JP:ja&q=twitter \
    -e CONSUMER_KEY=x \
    -e CONSUMER_SECRET=x \
    -e ACCESS_TOKEN=x \
    -e ACCESS_TOKEN_SECRET=x \
    hashito/tweetrss
```


## build

```
docker build -t hashito/tweetrss .
```