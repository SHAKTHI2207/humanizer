## Summary

This PR replaces the legacy polling loop in the order-sync service with a webhook handler.

## Changes

- The webhook handler cuts API calls to the vendor from about 40,000 a day to about 1,200.
- Webhook signatures are verified with HMAC-SHA256.
- The old polling code stays behind the `order_sync_polling` flag for one release as a fallback.
- New tests cover signature failures and duplicate events.


Changes: removed emojis, bold labels, "transformative" and the architecture-and-future-growth claims, and the closing offer to answer questions.
