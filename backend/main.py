import random as rng

from fastapi import FastAPI
from prometheus_client import Counter, Gauge, Histogram
from starlette_prometheus import PrometheusMiddleware, metrics

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)


@app.get('/')
def read_root():
    return {'Hello': 'World'}


SIMPLE_COUNTER = Counter('simple_counter', 'A simple counter example')


@app.get('/counter/simple')
def counter_simple():
    SIMPLE_COUNTER.inc()
    print('Increasing SIMPLE_COUNTER by 1')
    return 'Increasing SIMPLE_COUNTER by 1'


LABELS = ['created_by', 'status']
CREATED_BY_VALUES = ['Sossai', 'Sancho']
STATUS_VALUES = ['200', '400']
COUNTER_WITH_LABELS = Counter('label_counter', 'A counter with labels', LABELS)


@app.get('/counter/labels')
def counter_labels():
    created_by = rng.choice(CREATED_BY_VALUES)
    status = rng.choice(STATUS_VALUES)
    COUNTER_WITH_LABELS.labels(
        created_by=created_by,
        status=status,
    ).inc()
    print('Increasing COUNTER_WITH_LABELS by 1')
    return f'Increasing COUNTER_WITH_LABELS {created_by} {status} by 1'


SIMPLE_GAUGE = Gauge(
    'simple_gauge', 'A simple gauge example that simulates temperature values'
)


@app.get('/gauge/simple')
def gauge_simple():
    temperature = rng.randint(1, 100)
    SIMPLE_GAUGE.set(temperature)
    print(f'Settings gauge temperature to {temperature}')
    return f'Settings gauge temperature to {temperature}'


SIMPLE_HISTOGRAM = Histogram(
    'simple_histogram',
    'A simple histogram example that simulates request time.',
)


@app.get('/histogram/simple')
def histogram_simple():
    request_time = rng.randint(1, 1000) / 100
    SIMPLE_HISTOGRAM.observe(request_time)
    print(f'Adding {request_time} to histogram')
    return f'Adding {request_time} to histogram'
