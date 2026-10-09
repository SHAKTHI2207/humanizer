## Incident summary

On March 14, our platform had a 47-minute outage that hurt the customer experience.

## Root cause

An expired TLS certificate on the internal API gateway caused the outage. The certificate renewal job had been failing silently since February, and nobody noticed. We had no monitoring on the job, so the failure went unseen until the certificate expired.

## Impact

About 30% of checkout requests failed during the incident.

## Remediation

We added alerting for certificates that expire within 14 days, so a failing renewal gets caught well before an outage.

## Lessons learned

A failure we do not monitor is a failure we cannot fix. The renewal job needed an alert from the start.
