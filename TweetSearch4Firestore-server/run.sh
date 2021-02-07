#! /bin/bash
echo $FIREBASEKEY | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
python3 /root/main.py
