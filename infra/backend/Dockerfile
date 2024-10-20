FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt .
COPY ./bbt_admin .
COPY ./infra/backend/entrypoint.sh /entrypoint.sh


RUN set -ex \
    && python3 -m pip install --upgrade pip \
    && pip3 install -r ./requirements.txt \
    && chmod u+x /entrypoint.sh 

ENTRYPOINT ["/entrypoint.sh"]



