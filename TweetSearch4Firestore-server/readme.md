# comment

mysql db resist tweet

## use

```
 docker run -it --rm   \
    -p 80:80 \
    -e CONSUMER_KEY=xx \
    -e CONSUMER_SECRET=xxx \
    -e ACCESS_TOKEN=117102281-xxx \
    -e ACCESS_TOKEN_SECRET=xxx \
    -e REQ_Q="xxx" \
    -e REQ_COUNT=10 \
    -e CASH_DOCUMENT_NAME=amazonprm \
    -e SET_COLLECTION_NAME=test \
    -e FIRST_TIME=1612600205 \
    -e FIREBASEKEY=xxx \
    --name amazonprm \
    hashito/tweetsearch-4-firestore-server:20210207v1 
```


## build

```
docker build . -t hashito/tweetsearch-4-firestore-server:20210207v1 
```