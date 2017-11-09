# Example Prometheus Instrumentation for Python

This is a quick example of how to instrument your Flask-based Python app
with the Python Prometheus client.

This project is built with:

- Python 3.6.x

And is packaged as a Docker container. The two top level dependencies are:

- Flask==0.12.2
- prometheus-client==0.0.21

See the [requirements file](./requirements.txt) for more details.

## Prometheus

[Prometheus](https://prometheus.io/) is a
[Cloud Native](https://winderresearch.com/what-is-cloud-native/?utm_source=github&utm_medium=web&utm_content=link)
monitoring application.

To instrument our Python code we need to manipulate the metrics each
time a new HTTP request is received.

See [the application](./app.py) for more details.

## Building

This project is automatically built by Docker Automated Builds.

To build manually:

`docker build -t python-app .`

## Running

Simply open port 5000 when running as a container:

`docker run -p 5000:5000 --name python-app philwinder/prometheus-python`