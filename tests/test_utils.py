import time
from app.utils.cache import cache
from app import worker
from flask import Flask
from app.utils.worker import AsyncWorker


def test_memoize_cache():
    """
    Test the memoization cache functionality.
    This test checks that the cache stores results of function calls
    and returns cached results for subsequent calls with the same arguments.
    """
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
        assert slow_function(3) == 6
        assert calls == [2, 3]


def test_run_async_future():
    """
    Test the AsyncWorker's run method with a simple function.
    This test checks that the function can be executed asynchronously
    and that the result can be retrieved from the future.
    """
    def dummy(x): return x + 1

    future = worker.run(dummy, 5)
    result = future.result(timeout=1)
    assert result == 6


def cpu_heavy_task(x):
    """
    A CPU-heavy task that performs a large number of calculations.
    """
    total = 0
    for i in range(10_000_000):
        total += (i % x)
    return total


def test_async_worker_parallel_vs_serial():
    """
    Test the performance of AsyncWorker with parallel execution vs serial execution.
    This test checks that running tasks in parallel with multiple workers
    is faster than running them serially with a single worker.
    """
    inputs = [3, 5, 7, 9, 11]

    # serial: 1 worker
    worker_serial = AsyncWorker(max_workers=1)
    start_serial = time.perf_counter()
    futures_serial = [worker_serial.run(cpu_heavy_task, i) for i in inputs]
    results_serial = [f.result() for f in futures_serial]
    assert results_serial == [cpu_heavy_task(i) for i in inputs], \
        "Serial execution results do not match expected"
    time_serial = time.perf_counter() - start_serial
    worker_serial.shutdown()

    # parallel: 5 workers
    worker_parallel = AsyncWorker(max_workers=5)
    start_parallel = time.perf_counter()
    futures_parallel = [worker_parallel.run(cpu_heavy_task, i) for i in inputs]
    results_parallel = [f.result() for f in futures_parallel]
    assert results_parallel == [cpu_heavy_task(i) for i in inputs], \
        "Parallel execution results do not match expected"
    time_parallel = time.perf_counter() - start_parallel
    worker_parallel.shutdown()

    assert time_parallel < time_serial, \
        "Parallel execution should be faster than serial execution"
    print(f"Serial: {time_serial:.2f}s | Parallel: {time_parallel:.2f}s")
