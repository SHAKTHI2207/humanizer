## Summary

This PR replaces the legacy polling loop in the order-sync service with a webhook handler.

## Changes

- The webhook handler replaces the polling loop. API calls to the vendor drop from about 40,000 a day to about 1,200.
- Webhook signatures are verified with HMAC-SHA256.
- The legacy polling code stays behind the `order_sync_polling` flag for one release, so we can fall back to it.
- New tests cover signature failures and duplicate events.

## Why

Polling makes tens of thousands of vendor calls a day, and a webhook handler needs only a small fraction of them.
