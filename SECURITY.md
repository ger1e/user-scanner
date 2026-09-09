# Security policy

This repository is a hardened fork of [`kaifcodec/user-scanner`](https://github.com/kaifcodec/user-scanner). Security-sensitive changes in this fork focus on network boundaries, request and proxy handling, media fetching, report generation, MCP input validation, scan orchestration, and CI controls.

Report vulnerabilities privately through GitHub private vulnerability reporting when it is available for this repository. Do not place credentials, access tokens, private OSINT targets, personal data, breach material, customer information, or live sensitive infrastructure in public issues or pull requests.

For vulnerabilities that also affect unchanged upstream code, coordinate disclosure with the upstream project as appropriate. This fork may intentionally diverge from upstream and may not contain the newest upstream scan modules or release number.

Use this software only for authorized research and investigation. Scanner output is an investigative indicator, not proof that two accounts belong to the same person or that a target performed any activity.

## Inherited embedded client material

Some unchanged upstream scan adapters contain client identifiers, API-key-shaped strings, or token-shaped request fields copied from public web/mobile clients. This fork does **not** assert that those values are secret, safe, valid, unrestricted, or authorized for reuse. It does not perform live credential validation during CI.

`security/embedded-client-material.json` is the value-free review inventory. It stores only source paths, conservative classifications, provenance labels, and SHA-256 fingerprints. `scripts/audit_embedded_client_material.py` fails CI when a credential-shaped literal is added, changed, moved, or removed without an explicit manifest review, and never prints the underlying value.

New adapters should not embed private credentials. Owners of inherited upstream client material remain responsible for restriction, rotation, revocation, and terms-of-service review. A matching inventory fingerprint means only “known to this fork”; it is not a security approval.
