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

5. Why we need get_k8s_pod_suffix.py file

newrelic-plugin-agent uses newRelic plugin api which doesn't allow to distinquish more than 1 instance of the same plugin name.
So if we have pgbouncer in a high-availability mode we can't see detailed monitoring divided by instance.
To overcome this limitation we use script that connect to k8s api and check deployed pgbouncer pods. 
If there is more than one pod script sorts them in descending order and return pod index in the list. 
This suffix is added to PGBOUNCER_NAME so those two instances will be visible as two separated pgbouncer deployment in monitoring
We need to ensure that new pods are created in parallel. Thats why we modified rolling update maxSurge parameter in Chart to number of replicas deployed. 
So new pods are deployed first and script see them all and is able to count suffix correctly.
