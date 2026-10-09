Good question, Ken. The upstream service sometimes drops the connection entirely, and a longer timeout doesn't help there: the request just hangs until it hits 60s and fails anyway. The retry makes 3 attempts with exponential backoff, which covers those dropped connections.

Fair point on the added complexity, though. I'll add a comment in the code explaining why it's a retry. Does that work for you?
