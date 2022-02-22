from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware


PROMETHEUS_METRICS_PORT = 8001

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', metrics)


@app.get('/')
def read_root():
    return {'Hello': 'World'}
