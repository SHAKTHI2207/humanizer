---
type: report
facts:
  - support tickets increased by 10% in Q2
  - some customers reported slower load times after the March release
  - one possible explanation is the new image pipeline, not confirmed
  - churn may rise if the issue persists
  - in Brazil response times doubled; elsewhere they were flat
keep:
  - "10\\s?%|10 percent"
  - "\\bsome\\b"
  - "possible|may|might|could|perhaps"
  - "not (?:yet |been |been yet )?confirmed|unconfirmed|haven'?t confirmed|not verified|unverified"
  - "Brazil"
  - "doubled|twice"
  - "flat|unchanged|did not change|didn'?t change|held steady|steady"
forbid:
  - "\\bsurg|\\bspik|\\bsoar|\\bskyrocket|\\bjump"
  - "\\b(?:most|many|all) (?:customers|users)"
  - "\\bwill (?:rise|increase|go up)"
  - "\\bthe (?:cause|reason|culprit)\\b|\\bcaused by\\b"
  - "(?:across|in) (?:all|every) region"
---
## Q2 Support Overview

In Q2, support tickets increased by 10%, underscoring the critical importance of proactive customer experience management. Notably, some customers reported slower load times following the March release — a development that warrants careful attention.

One possible explanation is the new image pipeline, although this has not yet been confirmed. Should the issue persist, churn may rise, potentially impacting our growth trajectory.

Regional performance paints a nuanced picture: in Brazil, response times doubled, while elsewhere they remained flat. Moving forward, a comprehensive, data-driven, and customer-centric approach will be essential to navigating these challenges.
