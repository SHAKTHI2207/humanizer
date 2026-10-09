# QuickCache

QuickCache is a lightweight Python library that caches function results, so repeated calls return without running the function again.

## Features

Add a decorator to a function and QuickCache caches its results. You do not need a configuration file.

QuickCache stores results on disk in `~/.quickcache`, so the cache survives restarts. Entries expire after 3600 seconds by default, and you can change the TTL.

## How it works

QuickCache builds each cache key from the function name and its arguments, so each unique call is cached separately.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We are exploring support for a future release.
