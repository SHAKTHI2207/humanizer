# QuickCache

QuickCache is a lightweight Python library that caches function results, so your application skips repeated work.

## Features

- Add a decorator and you are done. You do not need a configuration file.
- Results are stored on disk in `~/.quickcache`, so the cache survives restarts.
- The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each cache key from the function name and its arguments, so every unique call is cached separately.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not currently support async functions. We are exploring support for them.
