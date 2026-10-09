A longer timeout wouldn't cover dropped connections. The upstream service sometimes drops them entirely, so the request would hang until the 60s limit and then fail anyway. The retry makes 3 attempts with exponential backoff, which handles those transient failures.

I agree it adds complexity, so I'll add a code comment explaining why we did it this way.
