# QuickCache

QuickCache is a lightweight Python library that caches function results, so you can speed up an application by adding a decorator.

## Features

- Add a decorator to a function to cache it. You do not need a configuration file.
- QuickCache stores results on disk in `~/.quickcache`, so the cache survives restarts.
- The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each cache key from the function name and its arguments, so each unique call is cached separately.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We're looking into adding support in a future release.
