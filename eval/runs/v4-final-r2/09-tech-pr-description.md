## Summary

This PR replaces the polling loop in the order-sync service with a webhook handler. It cuts API calls to the vendor and sets the service up to scale more easily.

## Changes

- The webhook handler replaces the polling loop and reduces API calls to the vendor from ~40,000/day to ~1,200/day.
- The handler verifies webhook signatures with HMAC-SHA256.
- The legacy polling code stays available behind the `order_sync_polling` flag for one release as a fallback.
- New tests cover signature failures and duplicate events.
