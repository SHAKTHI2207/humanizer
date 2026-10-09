## Draft

## Incident summary

On March 14, our platform had a 47-minute outage. An expired TLS certificate on the internal API gateway caused it.

## Root cause

The certificate renewal job had been failing silently since February, and nobody noticed. We had no alerting on it.

## Impact

About 30% of checkout requests failed during the outage.

## Remediation

We now alert on certificates that expire within 14 days.

## Lessons learned

Monitor the renewal job as well as the certificate.

## Remaining patterns

- "Nobody noticed" and "no alerting" are inferred from the original's "went undetected" and "gap in our observability". They are not new facts.
- The original's "significantly impacted the customer experience" is dropped. The 30% checkout failure figure carries it.
- The last lesson is my restatement of "what you don't monitor, you can't fix", cut because it was an aphorism closer. Check it matches your intent.

## Final rewrite

## Incident summary

On March 14, our platform had a 47-minute outage caused by an expired TLS certificate on the internal API gateway.

## Root cause

The certificate renewal job had been failing silently since February, and nobody noticed. We had no alerting on it.

## Impact

About 30% of checkout requests failed during the outage.

## Remediation

We now alert on certificates that expire within 14 days.

## Lessons learned

The renewal job failed for weeks without anyone knowing. Monitor the job as well as the certificate.
