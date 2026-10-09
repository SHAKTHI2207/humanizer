## Incident summary

On March 14, our platform had a 47-minute outage that affected customers.

## Root cause

The TLS certificate on the internal API gateway expired. The certificate renewal job had been failing silently since February, and nothing alerted us to it.

## Impact

About 30% of checkout requests failed during the outage.

## Remediation

We now alert on any certificate that expires within 14 days.

## Lessons learned

We weren't monitoring the renewal job, so its failure went unnoticed until the certificate expired and took down checkout.
