## Incident summary

On March 14, our platform had a 47-minute outage that affected customers. Better monitoring would have caught the cause.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and nobody noticed. We had no alerting on certificate expiry.

## Impact

About 30% of checkout requests failed during the incident window.

## Remediation

We now alert on certificates that expire within 14 days, so a failing renewal gets noticed well before it causes an outage.

## Lessons learned

We can't fix what we don't monitor.
