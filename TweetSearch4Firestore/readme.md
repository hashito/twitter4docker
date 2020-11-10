# comment

mysql db resist tweet

## use

```
docker run -it --rm \
    -e CONSUMER_KEY=x \
    -e CONSUMER_SECRET=x \
    -e ACCESS_TOKEN=x-x \
    -e ACCESS_TOKEN_SECRET=x \
    -e REQ_Q="test" \
    -e FIREBASE_STORE_COLLECTION="raw" \
    -v $(pwd)/.firebasekey.json:/root/.firebasekey.json \
    hashito/tweetsearch4firestore:0.0.1
```


## build

```
docker build . -t hashito/tweetsearch4firestore
```