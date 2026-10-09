## Incident summary

On March 14, our platform had a 47-minute outage that affected customers. Better monitoring would have caught the cause earlier.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and nobody noticed.

## Impact

About 30% of checkout requests failed during the incident window.

## Remediation

We now have alerting for certificates that expire within 14 days, so a failed renewal gets noticed before it causes an outage.

## Lessons learned

What you don't monitor, you can't fix.
