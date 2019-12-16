FROM dr1s/pipenv-alpine:3.8-python3.7

COPY minidlna_exporter/minidlna_exporter.py minidlna_exporter.py

EXPOSE 9312

ENTRYPOINT ["python3", "minidlna_exporter.py"]
