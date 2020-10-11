# comment

mysql db resist tweet

## use

```
docker run -it --rm \
    -e CONSUMER_KEY=x \
    -e CONSUMER_SECRET=x \
    -e ACCESS_TOKEN=x-x \
    -e ACCESS_TOKEN_SECRET=x \
    -p 80:80 \
    -e REQ_Q="test" \
    -e DB_HOST="0.0.0.0" \
    -e DB_USERNAME="root" \
    -e DB_PASSWORD="pass" \
    -e REQ_COUNT=50 \
    --network net  \
    hashito/tweetsearchapi:0.0.1
```


## build

```
docker build . -t hashito/tweetsearchapi:0.0.1
```