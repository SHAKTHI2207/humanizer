Good point, Ken. A longer timeout wouldn't help with dropped connections, though. The upstream service sometimes drops them entirely, so the request would hang until the 60s limit and then fail anyway. The retry makes 3 attempts with exponential backoff, which covers those transient failures.

I agree it adds complexity, so I'll add a comment in the code explaining why.
