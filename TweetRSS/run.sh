#! /bin/bash
#mkdir -p $CASH_FILE

if [ ! -f $CASH_FILE ]; then
    echo "{}"> $CASH_FILE
fi

python3 /root/main.py