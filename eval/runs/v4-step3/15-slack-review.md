Thanks, Ken. A longer timeout wouldn't help here, because the upstream service sometimes drops connections outright. The request would hang until it hit 60s and then fail anyway. The retry makes 3 attempts with exponential backoff, which covers those drops.

Fair point on the added complexity. I'll add a comment in the code explaining why.
