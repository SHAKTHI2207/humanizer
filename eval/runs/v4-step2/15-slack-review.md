A longer timeout wouldn't cover the failure we're seeing. The upstream service sometimes drops connections outright, so with 60s the request would hang the full minute and then fail anyway. The retry (3 attempts with exponential backoff) handles those cases.

Fair point on the added complexity, though. I'll add a comment in the code explaining why we retry instead of raising the timeout.
