# comment

This is an image to get the twitter access token.

## use

```
docker run --rm -it -e "CONSUMER_KEY=xxx" -e "CONSUMER_SECRET=xxx" hashito/twitteraccesstoken
```

```
access >>  https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}
PIN? >> {input}
ACCESS TOKEN        = {ACCESS TOKEN}
ACCESS TOKEN SECRET = {ACCESS TOKEN SECRET}
```

## build

```
docker build  -t hashito/twitteraccesstoken .
```