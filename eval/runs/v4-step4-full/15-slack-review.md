Fair question, Ken. A longer timeout wouldn't help here, because the upstream service sometimes drops connections entirely. The request would hang until the 60s limit and then fail anyway. The retry makes 3 attempts with exponential backoff, which covers those transient failures. It does add complexity, so I'll add a code comment explaining why. Let me know if that works.

Changes: cut the praise and the "not just X, it's Y" framing, removed "gracefully and robustly," and put the reason a timeout fails first.
