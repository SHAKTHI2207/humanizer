## Incident summary

On March 14, our platform had a 47-minute outage that significantly affected customers.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and none of our monitoring caught it.

## Impact

About 30% of checkout requests failed during the incident.

## Remediation

We added alerts for certificates that expire within 14 days, so we can catch similar problems before they cause an outage.

## Lessons learned

We can't fix failures we aren't monitoring for. The renewal job failed for weeks before anyone knew.
