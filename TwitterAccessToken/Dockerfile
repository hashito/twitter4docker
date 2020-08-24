FROM python:3

ADD ./main.py /root/
ADD ./requirements.txt /root/

RUN pip install -r /root/requirements.txt

ENV CONSUMER_KEY="xxxx" \
    CONSUMER_SECRET="xxxx"

CMD [ "python","/root/main.py" ]