#! /bin/bash
#mkdir -p $CASH_FILE

if [ ! -f $CASH_FILE ]; then
    echo '{"since_id":false}'> $CASH_FILE
fi

python3 /root/main.py