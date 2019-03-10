from threading import Thread


class DataDispatcher(Thread):
    def __init__(self, data_queue, dispatch_data_func):
        super().__init__()
        self._run = True
        self._data_queue = data_queue
        self._dispatch_data = dispatch_data_func

    def run(self):
        while self._run:
            data = self._data_queue.get()
            if data is not None:
                self._dispatch_data(data)

    def stop(self, timeout=10):
        self._run = False
        self.join(timeout)
