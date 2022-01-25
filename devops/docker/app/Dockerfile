FROM ubuntu:18.04

RUN set -ex \
    \
    && apt-get update \
    && apt-get install postgis -y --no-install-recommends \
    && apt-get install gdal-bin -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl netbase wget \
        git openssh-client \
        libcurl4-openssl-dev libpq-dev libjpeg-dev libpng-dev libsqlite3-dev libxml2-dev libyaml-dev \
        libtool libssl-dev build-essential \
        python3.8 python3.8-dev python3-virtualenv python3-cffi python3-pip libcairo2 \
        libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev \
        shared-mime-info

ENV VIRTUAL_ENV /app/venv

RUN python3 -m virtualenv --python=/usr/bin/python3.8 $VIRTUAL_ENV

ENV PATH $VIRTUAL_ENV/bin:$PATH

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app/

WORKDIR /app

COPY ./devops/docker/app/gunicorn.conf.py /app/gunicorn.conf.py
COPY ./devops/docker/app/entrypoint.sh /app/entrypoint.sh

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD gunicorn -c /app/gunicorn.conf.py --log-level=${DJANGO_LOGLEVEL} --name ${SERVICE_VARIANT} --max-requests=1000 --access-logfile - --error-logfile - --bind=0.0.0.0:8000 core.${WSGI_NAME}:application

