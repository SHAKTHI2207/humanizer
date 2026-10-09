## Incident summary

On March 14, our platform was down for 47 minutes, which hurt the customer experience.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and nobody noticed. We had a gap in observability.

## Impact

About 30% of checkout requests failed during the incident window.

## Remediation

We now alert on certificates that expire within 14 days, so similar problems get caught before they cause an outage.

## Lessons learned

What you don't monitor, you can't fix.


Changes: cut the "crucial reminder", "not just X" contrast and "underscoring" riders, and the "fundamental truth" staging, and sentence-cased the headings.
