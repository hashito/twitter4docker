#! /bin/bash
echo $FIREBASEKEY | base64 -d > /firebase.json
python3 /root/main.py