# QuickCache

QuickCache is a lightweight Python library that caches function results. Add a decorator and repeated calls return the stored result.

## Features

- You add a decorator. No configuration file is needed.
- Results are stored on disk in `~/.quickcache`, so the cache survives restarts.
- The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each key from the function name and its arguments, so every unique call is cached independently.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not currently support async functions. We are exploring support for them.
