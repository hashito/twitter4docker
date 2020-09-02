# comment

Tweet read to trans Language.

## use
### trans sheets create

ref->https://support.google.com/docs/answer/183965?co=GENIE.Platform%3DDesktop&hl=en

copy and use
>trans.gas

###

```
docker run -it --rm \
    -e CONSUMER_KEY=x \
    -e CONSUMER_SECRET=x \
    -e ACCESS_TOKEN=x-x \
    -e ACCESS_TOKEN_SECRET=x \
    -v /Users/hashito/git/twitter4docker/TweetRSS/main.py:/root/main.py   \
    -v /Users/hashito/git/twitter4docker/TweetRSS/cash:/root/cash   \
    hashito/tweettrans
```


## build

```
docker build -t hashito/tweettrans .
```