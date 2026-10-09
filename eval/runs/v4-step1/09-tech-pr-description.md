## Summary

This PR replaces the polling loop in the order-sync service with a webhook handler. API calls to the vendor drop from about 40,000 a day to about 1,200.

## Changes

- The webhook handler replaces the polling loop.
- Webhook signatures are verified with HMAC-SHA256.
- The old polling code stays behind the `order_sync_polling` flag for one release, as a fallback.
- Tests cover signature failures and duplicate events.
