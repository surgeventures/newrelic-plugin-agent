#How to test it

1. Build docker image
`docker build . -t newrelic-agent`
2. Run it 
` docker run -d --net=host -v /var/run/docker.sock:/var/run/docker.sock:ro -v <backends-dir>/backends:/etc/newrelic/backends -e NEWRELIC_KEY="YOUR_KEY"  newrelic-plugin-agent`
