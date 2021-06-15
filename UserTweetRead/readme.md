# comment

Tweet read to trans Language.

## use
### trans sheets create

ref->https://support.google.com/docs/answer/183965?co=GENIE.Platform%3DDesktop&hl=en

copy and use
>trans.gas

###

```
docker run -it --rm -p 80:80\
    -e TRANS_URL=xxx \
    -e SOURCE_TYPE=en \
    -e TARGET_TYPE=ja \
    -e TARGET_USER_ID=25073877 \
    -e SCREEN_NAME=xxx \
    -e TARGET_COUNT=30 \
    -e FIRST_TWEET_ID=xx \
    -e DOCUMENT_NAME=xx \
    -e CONSUMER_KEY=xxx \
    -e CONSUMER_SECRET=xx \
    -e ACCESS_TOKEN=xx-xx \
    -e ACCESS_TOKEN_SECRET=xxx \
    -e FIREBASEKEY=xxx \
    hashito/tweet-trans-server:20210206v1

```


## build

```
docker build -t hashito/tweet-trans-server:20210206v1 .
```