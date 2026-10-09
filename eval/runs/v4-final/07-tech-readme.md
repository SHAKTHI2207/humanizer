# QuickCache

QuickCache is a lightweight Python library that caches function results.

## Features

Add a decorator to a function and QuickCache caches its results. You don't need a configuration file.

Results are stored on disk in `~/.quickcache`, so the cache survives restarts.

The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each cache key from the function name and its arguments, so each unique call is cached separately.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We're looking into adding support in a future release.
