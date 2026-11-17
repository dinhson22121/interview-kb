@@@ sec-jwt | How does JWT work, and how do you revoke one? | security | security,jwt,authentication | qa | Authentication
"A JWT is three base64url parts: a header with the algorithm, a payload of claims such as `sub`, `exp`, `aud`, and a signature. The server verifies the signature and the claims without a database lookup, which is why it scales. The payload is only encoded, not encrypted, so it must not contain secrets; JWE is the encrypted variant.

HS256 uses one shared secret, so every verifier could also issue tokens. RS256 or ES256 sign with a private key and verify with a public key, which is what I use between services, with keys published via JWKS.

Revocation is the weak point. Options: short-lived access tokens, around 5–15 minutes, plus refresh tokens that can be revoked; a deny list of token IDs in Redis kept until expiry; or a per-user token version checked on each request. Checklist: always validate `alg`, `exp`, `iss` and `aud`; reject `alg: none`; keep tokens small because they travel with every request."

Tham khảo thêm: [Security - JWT](https://minhnhat97kg.github.io/docsify/content/security-jwt-json-web-tokens/vi.md)

@@@ sec-oauth | Explain OAuth 2.0 and OpenID Connect. Which flow would you use? | security | security,oauth2,oidc,authentication | qa | Authentication
"OAuth 2.0 is about **authorization**: a client gets an access token to call an API on a user's behalf. OpenID Connect adds **authentication** on top: an ID token that says who the user is.

Roles: resource owner (user), client (app), authorization server (Keycloak, Auth0, Cognito), and resource server (API).

Flows:

- **Authorization Code with PKCE** for web and mobile apps: the browser gets a one-time code, the client exchanges it with a code verifier, so an intercepted code is useless.
- **Client Credentials** for service-to-service calls with no user.
- Implicit and password grants are deprecated.

The API validates the access token's signature, expiry, audience and scopes; the ID token is for the client only and shouldn't be sent to APIs. In the browser I keep tokens out of localStorage, which XSS can read, using a backend-for-frontend with HttpOnly cookies. Refresh tokens should be rotated on each use so reuse can be detected."

Tham khảo thêm: [Security - OAuth 2.0 & OIDC](https://minhnhat97kg.github.io/docsify/content/security-oauth-20-oidc-modern-authentication/vi.md)

@@@ sec-password | How should passwords be stored? | security | security,hashing,authentication | qa | Cryptography
"Hash, never encrypt: we never need the original password back. And not with SHA-256 or MD5, which are designed to be fast, so GPUs can try billions of guesses per second.

Use a slow, salted password hashing algorithm: **Argon2id** for new systems, or **bcrypt**, which is still fine. The salt is random per user and stored with the hash; it defeats rainbow tables and makes identical passwords hash differently. The work factor, such as bcrypt cost or Argon2 memory and iterations, is tuned so one hash takes roughly 100–300 ms, and raised over time, rehashing on the user's next login.

A pepper is an extra secret kept outside the database, for example in a KMS, so a stolen database alone isn't enough. On top of hashing: rate limiting and lockout on login, checking new passwords against breached-password lists, and MFA."

Tham khảo thêm: [Security - Password Hashing](https://minhnhat97kg.github.io/docsify/content/security-password-hashing/vi.md)

@@@ sec-crypto | Hashing vs encryption, and how do you manage keys? | security | security,cryptography,encryption,kms | qa | Cryptography
"Hashing is one-way and used for integrity and passwords. Encryption is reversible with a key and used for confidentiality.

For symmetric encryption I use **AES-GCM**, which provides both confidentiality and integrity; never ECB, which leaks patterns, and never reuse a nonce with the same key. AES-128 is already secure; AES-256 is chosen for compliance or long-term margins at a small cost.

The hard part is **key management**: keys don't belong in code, config files or environment variables in images. They live in a KMS or Vault, access is controlled by IAM, use is audited, and keys rotate. A secret, such as a key or password, is different from configuration such as a URL: secrets need access control, auditing and rotation."

Tham khảo thêm: [Security - Cryptography](https://minhnhat97kg.github.io/docsify/content/security-cryptography/vi.md)

@@@ sec-pii | How do you protect PII at rest, and still search it? | security | security,pii,encryption,kms | qa | Cryptography
"There are three layers. Disk or volume encryption protects against stolen disks. Database TDE protects files and backups. **Application-level encryption** protects against anyone with database access, including DBAs and SQL injection, so for sensitive fields such as ID numbers or phone numbers I encrypt in the application with AES-GCM.

Keys use **envelope encryption**: a data key encrypts the data, a master key in KMS encrypts the data key, and only the encrypted data key is stored next to the data. Rotating the master key doesn't require re-encrypting all data.

Searching: encrypted values can't be compared, so I add a **blind index**, an HMAC of the normalized value with a separate key, stored in its own column for exact-match lookups. Masking (showing `****1234`) is a display control, not protection. Plus: collect less PII, define retention, and keep PII out of logs."

Tham khảo thêm: [Security - PII Data Protection](https://minhnhat97kg.github.io/docsify/content/security-pii-data-protection-encryption-at-rest/vi.md)

@@@ sec-owasp-api | What are the most important OWASP API security risks? | security | security,owasp,api | qa | Application security
"From the OWASP API Security Top 10 (2023), the ones I see most:

- **BOLA, broken object-level authorization:** `GET /accounts/123` returns account 123 to any logged-in user. Fix: check ownership on every object access, ideally in a shared layer, and prefer non-guessable IDs as defense in depth.
- **Broken authentication:** weak token validation, no rate limit on login.
- **BOPLA, broken object property-level authorization:** returning internal fields (excessive data exposure) or accepting fields the user shouldn't set, such as `role` (mass assignment). Fix: explicit request and response DTOs, never binding requests straight to entities.
- **Unrestricted resource consumption:** no rate limits, pagination caps or payload size limits.
- **Unrestricted access to sensitive business flows:** bots abusing sign-up or checkout.

BOLA is about which object; BOPLA is about which fields of an object."

Tham khảo thêm: [Security - OWASP Top 10 API Security](https://minhnhat97kg.github.io/docsify/content/security-owasp-top-10-api-security/vi.md)

@@@ sec-sqli | How do you prevent SQL injection? | security | security,sql,owasp | qa | Application security
"Use parameterized queries everywhere, so input is always sent as data and never parsed as SQL. ORMs such as JPA and GORM do this for normal methods, but not for raw or string-built queries such as `createNativeQuery` with concatenation or GORM's `Raw` with `fmt.Sprintf`.

Places parameters can't help: identifiers such as column names in `ORDER BY` or table names. There I map user input to an allow-list of known columns.

Regex sanitization isn't a defense: there are too many encodings and edge cases. Stored procedures are only safe if they don't build dynamic SQL internally. For `LIKE`, pass the pattern as a parameter and escape `%` and `_` in user input. Defense in depth: the application's database user has least privilege, and errors don't leak SQL details."

Tham khảo thêm: [Security - SQL Injection Prevention](https://minhnhat97kg.github.io/docsify/content/security-sql-injection-prevention/vi.md)

@@@ sec-xss-csrf | XSS vs CSRF: what are they and how do you defend? | security | security,xss,csrf,web | qa | Application security
"**XSS**: an attacker's script runs in the victim's page and can do anything the user can. Defense: context-aware output encoding (frameworks do it by default; avoid raw HTML injection), a strict Content-Security-Policy, and HttpOnly cookies. HttpOnly doesn't stop XSS; it only stops scripts from reading the cookie.

**CSRF**: another site makes the victim's browser send an authenticated request, because cookies are attached automatically. Defense: `SameSite=Lax` or `Strict` cookies, anti-CSRF tokens for state-changing requests, and never changing state on `GET`.

If the API uses a bearer token from JavaScript instead of cookies, CSRF doesn't apply, but the token is then exposed to XSS. Postman isn't blocked by CORS or CSRF protections because those are browser mechanisms. Also send `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, and frame protection headers."

Tham khảo thêm: [Security - CSRF & XSS](https://minhnhat97kg.github.io/docsify/content/security-csrf-xss-the-twin-killers/vi.md)

@@@ sec-mtls | What is mTLS and when do you use it? | security | security,mtls,zero-trust,microservices | qa | Infrastructure security
"In normal TLS only the server presents a certificate. In mutual TLS the client also presents one, so both sides prove their identity cryptographically, and traffic is encrypted.

I use it for service-to-service traffic, usually through a service mesh such as Istio or Linkerd, whose sidecars issue short-lived certificates automatically and rotate them. That's much stronger than IP allow-lists, because IPs in Kubernetes change and can be spoofed inside a network.

It doesn't replace JWT or OAuth: mTLS proves which **service** is calling; a token says which **user** and what they may do. The cost is the handshake, which connection reuse amortizes, plus certificate management. The hard parts are rotation and protecting the CA: if the CA key leaks, every certificate is untrustworthy, so it lives in an HSM or KMS."

Tham khảo thêm: [Security - mTLS](https://minhnhat97kg.github.io/docsify/content/security-mtls/vi.md)

@@@ sec-rbac-abac | RBAC vs ABAC: how do you design authorization? | security | security,authorization,rbac,abac | qa | Authorization
"**RBAC** grants permissions to roles and roles to users. It's simple to reason about and audit. Tables: `users`, `roles`, `permissions`, and join tables `user_roles` and `role_permissions`, with permissions cached per user.

It breaks down with **role explosion**: 'manager of branch A for loans under 1 billion' becomes a new role. That's when I move to **ABAC**: policies evaluated against attributes of the user, the resource and the context, such as department, owner, amount or time. Tools such as OPA or Cedar keep policies as code, separate from business logic.

A common hybrid: roles for coarse access, attributes for fine-grained rules. For relationship-heavy cases, like 'can edit documents in folders shared with my team', Google's Zanzibar model (relationship-based access, as in OpenFGA or SpiceDB) fits best. Performance: evaluate close to the service and cache decisions briefly."

Tham khảo thêm: [Security - RBAC & ABAC](https://minhnhat97kg.github.io/docsify/content/security-rbac-abac/vi.md)

@@@ sec-zero-trust | What is Zero Trust? | security | security,zero-trust | qa | Infrastructure security
"'Never trust, always verify': no request is trusted because of where it comes from on the network. Every request is authenticated and authorized based on identity, device posture and context, with least privilege.

Components: a strong identity provider with MFA, device checks, a policy engine and enforcement points (an identity-aware proxy or service mesh), mTLS between services, micro-segmentation, and continuous logging.

A traditional VPN isn't Zero Trust: once inside, a user often reaches the whole network, which enables **lateral movement**, an attacker hopping from one compromised machine to others. Zero Trust limits each identity to the specific resources it needs. Legacy apps that can't do modern auth are put behind an identity-aware proxy. The trade-offs are latency from extra checks and operational complexity, so it's rolled out incrementally, starting with the most sensitive systems."

Tham khảo thêm: [Security - Zero Trust](https://minhnhat97kg.github.io/docsify/content/security-zero-trust/vi.md)

@@@ sec-stride | How do you threat-model a feature? Explain STRIDE. | security | security,threat-modeling,stride | qa | Secure design
"I threat-model during design, on a data-flow diagram showing trust boundaries, and go through STRIDE for each element:

- **Spoofing** identity → authentication.
- **Tampering** with data → integrity, signatures, validation.
- **Repudiation**, denying an action → audit logs that can't be altered, which matters a lot for payments.
- **Information disclosure** → encryption, access control.
- **Denial of service** → rate limits, quotas.
- **Elevation of privilege** → authorization checks, least privilege.

Spoofing is pretending to be someone else; elevation is gaining rights you shouldn't have even as yourself.

Each threat gets a risk rating and a mitigation or an explicit accepted risk. If the business won't fund a fix, I document the risk with its impact and get an owner to sign off, rather than silently dropping it. Keep it lightweight and repeat it when the design changes, otherwise it becomes shelfware."

Tham khảo thêm: [Security - Threat Modeling & STRIDE](https://minhnhat97kg.github.io/docsify/content/security-threat-modeling-mo-hinh-hoa-moi-đe-doa-va-bo-khung-stride/vi.md)
