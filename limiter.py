import time
from collections import defaultdict, deque

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)
        self.stats = {"allowed": 0, "blocked": 0}

    def is_allowed(self, client_id: str) -> tuple[bool, int]:
        now = time.time()
        window_start = now - self.window_seconds
        client_history = self.requests[client_id]

        while client_history and client_history[0] <= window_start:
            client_history.popleft()

        if len(client_history) < self.max_requests:
            client_history.append(now)
            self.stats["allowed"] += 1
            return True, 0

        self.stats["blocked"] += 1
        retry_after = int(self.window_seconds - (now - client_history[0])) + 1
        return False, retry_after

    def reset(self, client_id: str = None):
        if client_id:
            self.requests.pop(client_id, None)
        else:
            self.requests.clear()
            self.stats = {"allowed": 0, "blocked": 0}
