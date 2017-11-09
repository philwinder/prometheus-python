import random
import time

from flask import Flask, render_template_string
from prometheus_client import generate_latest, REGISTRY, Counter, Gauge, Histogram

app = Flask(__name__)

# A counter to count the total number of HTTP requests
REQUESTS = Counter('http_request_total', 'Total HTTP Requests (count)', ['method', 'endpoint'])

# A gauge (i.e. goes up and down) to monitor the total number of in progress requests
IN_PROGRESS = Gauge('http_request_inprogress', 'Number of in progress HTTP requests')

# A histogram to measure the latency of the HTTP requests
TIMINGS = Histogram('http_request_duration_seconds', 'HTTP request latency (seconds)')


# Standard Flask route stuff.
@app.route('/')
# Helper annotation to measure how long a method takes and save as a histogram metric.
@TIMINGS.time()
# Helper annotation to increment a gauge when entering the method and decrementing when leaving.
@IN_PROGRESS.track_inprogress()
def hello_world():
    REQUESTS.labels(method='GET', endpoint="/").inc()  # Increment the counter
    return 'Hello, World!'


@app.route('/slow')
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def slow_request():
    REQUESTS.labels(method='GET', endpoint="/slow").inc()
    v = random.random()
    time.sleep(v)
    return render_template_string('<h1>Wow, that took {{v}} s!</h1>', v=v)


@app.route('/hello/<name>')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def index(name):
    REQUESTS.labels(method='GET', endpoint="/hello/<name>").inc()
    return render_template_string('<b>Hello {{name}}</b>!', name=name)


@app.route('/metrics')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def metrics():
    REQUESTS.labels(method='GET', endpoint="/metrics").inc()
    return generate_latest(REGISTRY)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
