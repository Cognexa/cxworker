# CXWorker

Provides access to computation resources on a single machine.

## Development Guide

### Prerequisities

1. Install dependencies with `pip install -r requirements.txt`
2. Make sure you have Docker installed and that your user has permissions to use 
   it
3. If you intend to run computations on a GPU, install also `nvidia-docker2`

### Running Tests

The test suite can be run with `python setup.py test`.

### Launching the Worker

First, you need to have a Docker registry and a Minio server running. The 
easiest way to achieve this is to use the Docker Compose example:

```
docker-compose -f examples/docker/docker-compose-sandbox.yml up -d
```

Second, you need a configuration file. Again, examples found in the `examples/configs/` 
folder are a great starting point. Feel free to pick one of those and edit it to 
your needs.

Finally, you need to run the following command to start the worker:

```
cxworker -c examples/configs/cxworker-docker-cpu.yml
```

Be sure to adjust the command line parameters according to your needs (`-h` is 
your host address, `-p` is the port number where the worker API server listens 
and `-c` is the path to the configuration file).

After launching the worker, there will be an HTTP API available on the 
configured port that can be used to control the worker.

### Processing a Request Directly

To process a request for debugging purposes, you need to:

- choose a request id
- create a bucket on your Minio server with a name same as your request id
- put the payload (input for the model) in `<yourbucket>/inputs/input.json`
- invoke the `/start-job` API endpoint with your chosen request id
- after the job is processed, the result should be stored in Minio, in 
  `<yourbucket>/outputs.json`
