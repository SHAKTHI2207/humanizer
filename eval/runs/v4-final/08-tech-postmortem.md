## Incident summary

On March 14, the platform had a 47-minute outage that significantly affected customers.

## Root cause

The TLS certificate on the internal API gateway expired. The certificate renewal job had been failing silently since February, and our monitoring did not detect it.

## Impact

About 30% of checkout requests failed during the outage.

## Remediation

We added alerts for certificates that expire within 14 days.

## Lessons learned

We can't fix failures we aren't monitoring for.
