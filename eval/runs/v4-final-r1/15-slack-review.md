Fair question. The upstream service sometimes drops connections entirely, and a longer timeout doesn't help with those: the request just hangs until it hits 60s and then fails anyway. The retry makes 3 attempts with exponential backoff, so it recovers from those transient failures.

I get the worry about the extra complexity, so I'll add a code comment explaining the reasoning for future readers.
