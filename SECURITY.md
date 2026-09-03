# Security policy

## Reporting a vulnerability

Do not open a public GitHub issue for a suspected vulnerability, leaked credential, merchant identifier, wallet configuration, transaction record, or other sensitive information.

Email **support@boltutil.com** with the subject `Security report`. Include:

- the affected feature or endpoint;
- the security impact;
- reproducible steps or a minimal proof of concept;
- whether any real account, order, wallet, or credential may be affected;
- a safe way to contact you for follow-up.

Redact API keys, Webhook secrets, authentication tokens, private keys, seed phrases, personal information, and unnecessary production data. BoltUtil never needs a wallet private key or seed phrase to investigate a report.

We will acknowledge actionable reports and coordinate remediation and disclosure when appropriate. Please allow a reasonable investigation period before publishing details.

## Integration safety

- Keep API keys and Webhook secrets on trusted servers.
- Verify Webhook signatures against the exact raw request body.
- Reject stale callback timestamps.
- Make order fulfillment idempotent.
- Never commit credentials or production payloads to this repository.
