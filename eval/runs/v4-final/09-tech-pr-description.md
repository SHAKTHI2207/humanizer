## Summary

Replaces the polling loop in the order-sync service with a webhook handler. This cuts vendor API calls sharply and lays groundwork for a more scalable design.

## Changes

- The webhook handler replaces the polling loop and reduces API calls to the vendor from ~40,000/day to ~1,200/day.
- Webhook signatures are verified with HMAC-SHA256.
- The legacy polling code stays available behind the `order_sync_polling` flag for one release as a fallback.
- Added tests for signature failures and duplicate events.
