FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache jpeg-dev zlib-dev && \
  apk add --no-cache --virtual .build-deps build-base linux-headers gcc musl-dev postgresql-dev && \
  # apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  python3 --version && pip --version && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps
COPY . /code/