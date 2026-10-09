## Summary

This PR replaces the polling loop in the order-sync service with a webhook handler. API calls to the vendor drop from about 40,000 a day to about 1,200.

## Changes

- Adds a webhook handler in place of the polling loop.
- Verifies webhook signatures with HMAC-SHA256.
- Keeps the old polling code behind the `order_sync_polling` flag for one release, as a fallback.
- Adds tests for signature failures and duplicate events.
