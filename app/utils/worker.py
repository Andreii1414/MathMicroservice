from concurrent.futures import ThreadPoolExecutor, Future


class AsyncWorker:
    """
    A simple asynchronous worker using ThreadPoolExecutor.
    """
    def __init__(self, max_workers: int = 1):
        """
        Initialize the AsyncWorker with a ThreadPoolExecutor.
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def run(self, func, *args, **kwargs) -> Future:
        """
        Submit a task to the thread pool for asynchronous execution.
        :param func: Function to run
        :param args: Positional arguments for the function
        :param kwargs: Keyword arguments for the function
        :return: Future object
        """
        return self.executor.submit(func, *args, **kwargs)

    def shutdown(self, wait=True):
        """
        Shutdown the executor gracefully.
        """
        self.executor.shutdown(wait=wait)
