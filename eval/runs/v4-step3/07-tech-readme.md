# QuickCache

QuickCache is a lightweight Python library that caches function results, so you can speed up an application with little effort.

## Features

- Add a decorator to a function and it is cached. You do not need a configuration file.
- Results are stored on disk in `~/.quickcache`, so the cache survives restarts.
- The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each key from the function name and its arguments, so every distinct call is cached on its own.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We are looking at adding support in a future release.
