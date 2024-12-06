from threading import Lock
from time import sleep, time
from .z3950 import AlephZ3950Session


class NkpZ3950Session(AlephZ3950Session):
    def __init__(self, z3950_host, z3950_port, rate_limit_ms=1000):
        super().__init__(z3950_host, z3950_port)
        self._rate_limit = rate_limit_ms / 1000
        self._lock = Lock()
        self._last_request_time = 0

    def _wait_for_rate_limit(self):
        with self._lock:
            current_time = time()
            time_since_last_request = current_time - self._last_request_time

            if time_since_last_request < self._rate_limit:
                sleep_time = self._rate_limit - time_since_last_request
                print(
                    "Rate limit reached. "
                    f"Sleeping for {sleep_time:.3f} seconds..."
                )
                sleep(sleep_time)

            self._last_request_time = time()

    def search(self, base: str, query: str):
        self._wait_for_rate_limit()
        return super().search(base, query)
