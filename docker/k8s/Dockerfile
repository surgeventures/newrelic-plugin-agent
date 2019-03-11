FROM alpine:latest

MAINTAINER sre@shedul.com

RUN apk add --update python python-dev py-pip build-base postgresql-dev git && pip install pyyaml psycopg2 && rm -rf /var/cache/apk/*
RUN git clone https://github.com/surgeventures/newrelic-plugin-agent.git src

WORKDIR /src
RUN python setup.py install && rm -rf /src

WORKDIR /
RUN mkdir -p /etc/newrelic /var/log/newrelic /var/run/newrelic
ADD newrelic-plugin-agent.cfg /etc/newrelic/newrelic-plugin-agent.cfg
ADD bin/newrelic-plugin-agent.sh newrelic-plugin-agent.sh

ENTRYPOINT ["/newrelic-plugin-agent.sh"]
