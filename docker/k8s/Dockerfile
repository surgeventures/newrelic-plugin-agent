FROM alpine:latest

MAINTAINER sre@shedul.com
ENV ROOT_DIR docker/k8s

COPY ./ src
WORKDIR /src

RUN apk add --update python python-dev py-pip build-base postgresql-dev && \
		pip install pyyaml psycopg2 && \
		python setup.py install && \
		rm -rf /var/cache/apk/*

RUN mkdir -p /etc/newrelic /var/log/newrelic /var/run/newrelic
ADD $ROOT_DIR/newrelic-plugin-agent.cfg /etc/newrelic/newrelic-plugin-agent.cfg
ADD $ROOT_DIR/bin/newrelic-plugin-agent.sh /newrelic-plugin-agent.sh

ENTRYPOINT ["/newrelic-plugin-agent.sh"]
