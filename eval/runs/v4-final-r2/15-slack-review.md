Good point, Ken, but a longer timeout wouldn't help here. The upstream service sometimes drops the connection entirely, so the request would just hang until it hit 60s and then fail anyway. The retry makes 3 attempts with exponential backoff, which handles those transient failures.

I get the concern about added complexity. I'm happy to add a code comment explaining the reasoning so future readers have the context.
