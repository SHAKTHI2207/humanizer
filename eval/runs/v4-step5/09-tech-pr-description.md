## Summary

This PR replaces the polling loop in the order-sync service with a webhook handler.

## Changes

- The webhook handler replaces the polling loop and cuts API calls to the vendor from ~40,000/day to ~1,200/day.
- Webhook signatures are verified with HMAC-SHA256.
- The legacy polling code stays available behind the `order_sync_polling` flag for one release, as a fallback.
- Added tests for signature failures and duplicate events.
