Humanize the text below using the skill in your instructions.

<text>
# QuickCache 🚀

QuickCache is a powerful, lightweight, and intuitive Python library that seamlessly caches function results — empowering developers to build faster applications with minimal effort.

## Key Features

- **Simple:** Just add a decorator. No configuration file needed.
- **Persistent:** Results are stored on disk in `~/.quickcache`, ensuring your cache survives restarts.
- **Flexible:** The default TTL of 3600 seconds can be easily customized to suit your needs.

## How It Works

At its core, QuickCache leverages a robust key-generation strategy. Keys are built from the function name and arguments, ensuring that each unique call is cached independently.

## Installation

```bash
pip install quickcache
```

## Limitations

It's worth noting that QuickCache does not currently support async functions. We're actively exploring this feature and look forward to delivering it in a future release!

Happy caching! 🎉
</text>

Follow the skill's full process, then put only the final rewrite between <final> and </final>.