import time
from app.utils.cache import cache
from app import worker
from flask import Flask


def test_memoize_cache():
    app = Flask(__name__)
    calls = []
    app.config['CACHE_TYPE'] = 'SimpleCache'
    cache.init_app(app)

    with app.app_context():
        @cache.memoize()
        def slow_function(x):
            time.sleep(0.1)
            calls.append(x)
            return x * 2

        assert slow_function(2) == 4
        assert slow_function(2) == 4
        assert slow_function(3) == 6
        assert len(calls) == 2


def test_run_async_future():
    def dummy(x): return x + 1

    future = worker.run(dummy, 5)
    result = future.result(timeout=1)
    assert result == 6
