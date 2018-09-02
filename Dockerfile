FROM alpine:3.8
MAINTAINER dr1s

RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip setuptools && \
    pip3 install virtualenv

WORKDIR /minidlna_exporter

COPY . /minidlna_exporter

RUN virtualenv -p python3 /env && \
    /env/bin/python3 setup.py install && \
    rm -rf /minidlna_exporter

EXPOSE 9312

ENTRYPOINT ["/env/bin/minidlna_exporter"]
