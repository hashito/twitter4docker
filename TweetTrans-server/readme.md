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
    -e TRANS_URL="https://script.google.com/macros/s/x/exec" \
    -e TARGET_USER_ID=1176288952401059841 \
    -e TARGET_COUNT=10 \
    -e SCAN_SPAN=60 \
    -e TWEET_DELAY=60 \
    -e SCREEN_NAME=hasitozzz \
    hashito/tweettrans

```


## build

```
docker build -t hashito/tweettrans .
```