## Summary

This PR replaces the polling loop in the order-sync service with a webhook handler. That cuts API calls to the vendor from about 40,000 a day to about 1,200 a day.

## Changes

- The webhook handler replaces the polling loop.
- Webhook signatures are verified with HMAC-SHA256.
- The old polling code stays behind the `order_sync_polling` flag for one release, as a fallback.
- New tests cover signature failures and duplicate events.

## Why

Polling is no longer sufficient for this service, and the webhook handler fits how the vendor delivers events.
