# QuickCache

QuickCache is a lightweight Python library that caches function results, so your code runs faster with little effort.

## Features

- Add a decorator. You do not need a configuration file.
- Results are stored on disk in `~/.quickcache`, so the cache survives restarts.
- The default TTL is 3600 seconds, and you can change it.

## How it works

QuickCache builds each key from the function name and its arguments, so every unique call is cached independently.

## Installation

```bash
pip install quickcache
```

## Limitations

QuickCache does not support async functions yet. We are looking into adding that in a future release.


Changes: removed emojis, bold labels, the sales adjectives and the "at its core" opener, and dropped the dash.
