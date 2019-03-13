#!/bin/sh

sed -i "s/NEWRELIC_KEY/${NEWRELIC_KEY}/g" /etc/newrelic/newrelic-plugin-agent.cfg
sed -i "s/PGBOUNCER_STATS_USER/${PGBOUNCER_STATS_USER}/g" /etc/newrelic/newrelic-plugin-agent.cfg
sed -i "s/PGBOUNCER_STATS_PASSWORD/${PGBOUNCER_STATS_PASSWORD}/g" /etc/newrelic/newrelic-plugin-agent.cfg
sed -i "s/PGBOUNCER_NAME/${PGBOUNCER_NAME}/g" /etc/newrelic/newrelic-plugin-agent.cfg
sed -i "s/PGBOUNCER_HOST/${PGBOUNCER_HOST:=127.0.0.1}/g" /etc/newrelic/newrelic-plugin-agent.cfg
sed -i "s/PGBOUNCER_PORT/${PGBOUNCER_PORT:=6432}/g" /etc/newrelic/newrelic-plugin-agent.cfg
sed -i "s/WAKE_INTERVAL/${WAKE_INTERVAL:=30}/g" /etc/newrelic/newrelic-plugin-agent.cfg
exec newrelic-plugin-agent -f -c /etc/newrelic/newrelic-plugin-agent.cfg
