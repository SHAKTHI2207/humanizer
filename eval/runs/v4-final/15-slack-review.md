Good question. The problem is dropped connections as well as slow responses. The upstream service sometimes drops a connection entirely, and a longer timeout doesn't help there: the request just hangs until it hits 60s and then fails anyway. The retry makes 3 attempts with exponential backoff, which handles those transient failures.

I get the concern about added complexity. Happy to add a comment in the code explaining the reasoning so future readers have the context.
