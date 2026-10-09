---
type: technical
facts:
  - PR replaces the polling loop in order-sync with a webhook handler
  - reduces API calls to the vendor from about 40,000 a day to about 1,200
  - webhook signatures are verified with HMAC-SHA256
  - old polling code stays behind a feature flag named order_sync_polling for one release
  - tests added for signature failure and duplicate events
---
## Summary

This PR introduces a transformative improvement to the order-sync service by replacing the legacy polling loop with a modern webhook handler. This change not only enhances efficiency but also lays the groundwork for a more scalable architecture.

## Key Changes

- 🔄 **Webhook Handler:** Replaces the polling loop, reducing API calls to the vendor from ~40,000/day to ~1,200/day — a dramatic improvement!
- 🔐 **Security:** Webhook signatures are verified using HMAC-SHA256, ensuring the integrity and authenticity of incoming events.
- 🚩 **Feature Flag:** The legacy polling code remains available behind the `order_sync_polling` flag for one release, providing a seamless fallback.
- ✅ **Testing:** Comprehensive tests have been added for signature failures and duplicate events.

## Why This Matters

In today's event-driven landscape, polling is no longer sufficient. This change aligns our architecture with industry best practices and positions us for future growth.

Let me know if you have any questions or feedback! 🙌
