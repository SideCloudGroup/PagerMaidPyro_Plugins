FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY main.py requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

CMD python -u /app/main.py