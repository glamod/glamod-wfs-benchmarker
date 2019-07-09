# glamod-wfs-benchmarker

Benchmarking for Web Feature Service

## Basic usage

Command-line will find `locustfile.py` and use it to configure tests. Run with:

```
locust --no-web -c 5 -r 1 --run-time 10s
```

Where `-c` is number of locusts to spawn and `-r` is hatch rate.

## Modifying behaviour of locust

### Setting the `wait_function`

If we set the `TaskSet.wait_function` to return 20000 (milliseconds), then the 
initial number of concurrent locusts will spawn at the start but no more will 
appear until 20 seconds have elapsed, regardless of whether they complete.

Can test this with:

```
locust --no-web -c 4 --run-time 30s
``` 

### Adding a logger

I have added a global logger called `log` that we can use to log to the screen
to test out different modifications.


