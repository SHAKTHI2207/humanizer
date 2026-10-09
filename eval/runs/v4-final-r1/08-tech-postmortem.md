## Incident summary

On March 14, our platform had a 47-minute outage that significantly affected customers.

## Root cause

The TLS certificate on the internal API gateway expired. The certificate renewal job had been failing silently since February, and no monitoring caught it.

## Impact

About 30% of checkout requests failed during the outage.

## Remediation

We added alerts for certificates that expire within 14 days, so we can catch and fix a failed renewal before it causes an outage.

## Lessons learned

We could not fix a failure we were not monitoring.
