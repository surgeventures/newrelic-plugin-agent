##How to build and test newrelic-plugin-agent

1. Build docker image
```
docker build ../../ -f Dockerfile -t newrelic-plugin-agent
```
2. Run it 
```
docker run --net=host  -e PGBOUNCER_NAME="test-namespace" -e NEWRELIC_KEY="dd" -e PGBOUNCER_STATS_USER="aa" -e PGBOUNCER_STATS_PASSWORD="xx" newrelic-plugin-agent
```
3. If you want to test pgbouncer config ensure it is running in separate docker image and it exposes port and ip adddress exactly how your plugin config looks:
```
 #pgbouncer dir contains base pgbouncer configuration
 docker run -d --dns-opt randomize-case:0 -v  /pgbouncer:/etc/pgbouncer/ -p 6432:6432 --rm   officialsurgeventures/pgbouncer:1.9.0```
```
4. Tag build and push to registry
```
docker build ../../ -f Dockerfile . -t newrelic-plugin-agent:1.0 -t 514443763038.dkr.ecr.us-east-1.amazonaws.com/newrelic-plugin-agent:1.0 
docker push 514443763038.dkr.ecr.us-east-1.amazonaws.com/newrelic-plugin-agent:1.0
```
