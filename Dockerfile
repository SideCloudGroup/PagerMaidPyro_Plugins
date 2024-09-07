FROM python:3.12-alpine

WORKDIR /app
ADD main.py /app
ADD requirements.txt /app

RUN pip install -r requirements.txt
RUN rm requirements.txt

CMD python -u /app/main.py