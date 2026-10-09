## Summary

Replaces the polling loop in the order-sync service with a webhook handler. This cuts vendor API calls sharply and should make the service easier to scale.

## Changes

- The webhook handler replaces the polling loop and reduces API calls to the vendor from ~40,000/day to ~1,200/day.
- Webhook signatures are verified with HMAC-SHA256 to confirm each event is authentic and unmodified.
- The legacy polling code stays available behind the `order_sync_polling` flag for one release as a fallback.
- New tests cover signature failures and duplicate events.
