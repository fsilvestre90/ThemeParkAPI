FROM frolvlad/alpine-python3

ENV API_SERVER_HOME=/opt/www
WORKDIR $API_SERVER_HOME
ENV PYTHONUNBUFFERED 0

RUN apk update && \
    apk upgrade && \
    apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
     build-base \
     python3-dev \
     gdal \
     geos \
     libffi-dev \
     libpq \
     musl-dev \
     proj4-dev \
     postgresql-dev \
     zlib-dev && \
    rm -rf /var/cache/apk/*
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt \
    && rm -rf ~/.cache/pip

COPY . .

RUN pip install --editable .

CMD [ 'gunicorn -c gunicorn.py --reload "app:create_app()"' ]
