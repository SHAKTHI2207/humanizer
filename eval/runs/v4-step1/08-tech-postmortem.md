## Incident summary

On March 14, our platform had a 47-minute outage that affected customers.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and nobody noticed. We had no monitoring that would have caught it.

## Impact

About 30% of checkout requests failed during the incident window.

## Remediation

We added alerting for certificates that expire within 14 days.

## Lessons learned

A failing job we do not monitor stays broken until it causes an outage.
