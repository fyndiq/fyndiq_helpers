FROM fyndiq/python-alpine-kafka:python3.7.0-librdkafka0.11.5

ARG ENV=test
ENV CONFIG=$ENV

COPY requirements/* /tmp/
RUN pip install --process-dependency-links --no-cache-dir -r /tmp/$ENV.txt
