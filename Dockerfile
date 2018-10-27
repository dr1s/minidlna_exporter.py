FROM alpine:3.8

RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip setuptools && \
    pip3 install pipenv

WORKDIR /exporter

COPY minidlna_exporter/minidlna_exporter.py minidlna_exporter.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system

EXPOSE EXPOSE 9312

ENTRYPOINT python3 minidlna_exporter.py
