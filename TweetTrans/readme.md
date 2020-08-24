# comment

Read RSS regularly and Tweet

## use

```
docker run -it --rm \
    -e CONSUMER_KEY=x \
    -e CONSUMER_SECRET=x \
    -e ACCESS_TOKEN=x-x \
    -e ACCESS_TOKEN_SECRET=x \
    -v /Users/hashito/git/twitter4docker/TweetRSS/main.py:/root/main.py   \
    -v /Users/hashito/git/twitter4docker/TweetRSS/cash:/root/cash   \
    hashito/tweetrss
```


## build

```
docker build -t hashito/tweetrss .
```