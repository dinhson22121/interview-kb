@@@ sd-checklist | What is your framework for a 45-minute system design interview? | arch | system-design,framework | qa | System design
*Đây là khung dùng cho mọi bài system design; tập nói theo đúng thứ tự này.*

"1. **Clarify requirements, 5–10 minutes:** core features, what's out of scope, and non-functional needs: scale (daily active users, read/write ratio), latency, availability target, consistency needs.
2. **Estimate, about 5 minutes:** QPS at average and peak, storage per year, bandwidth. Rough orders of magnitude are enough; they drive later choices.
3. **High-level design, 10–15 minutes:** API, data model, main components and the request flow. Get something end to end on the board before optimizing.
4. **Deep dive, 15–20 minutes:** the bottleneck the interviewer cares about: database choice and schema, scaling and partitioning, caching, concurrency, failure handling and single points of failure.
5. **Wrap up, 2–3 minutes:** trade-offs I made, what I'd monitor, and what I'd improve with more time.

Throughout I say the trade-offs out loud and check in with the interviewer before going deep."

Tham khảo thêm: [System Design Interview - The Ultimate Checklist](https://minhnhat97kg.github.io/docsify/content/system-design-interview-the-ultimate-checklist/vi.md)

@@@ sd-cdn | How does a CDN work, and what can it do for an API? | arch | system-design,cdn,caching,performance | qa | System design
*Đây là chủ đề bạn chưa làm thực tế; trả lời ở mức nguyên lý và nói rõ điều đó nếu bị hỏi sâu.*

"A CDN caches content at edge locations close to users, so requests don't travel to the origin, which cuts latency and offloads the origin.

- **Static assets** such as images, JS and video are cached for a long time, with versioned file names (`app.3f9a.js`) so a deploy never needs invalidation.
- **Dynamic API responses** can be cached briefly when they're public, such as a product catalogue for 30 seconds, controlled by `Cache-Control: public, max-age=30, stale-while-revalidate=60`. Personalized responses get `private` or `no-store`. The cache key must include anything that changes the response, but not unnecessary cookies or query parameters, or the hit rate collapses.
- **Invalidation** is the hard part: prefer short TTLs or versioned URLs over purges.
- **Protection:** the edge absorbs DDoS traffic, and request collapsing stops a thundering herd when a popular object expires, by sending one request to the origin.
- **Edge computing** runs small functions at the edge for redirects, auth checks or A/B routing.

Even without a CDN in my past projects, the same reasoning applies to the API gateway and Redis caching I did use."

Tham khảo thêm: [System Design - CDN & Edge Computing](https://minhnhat97kg.github.io/docsify/content/system-design-cdn-edge-computing/vi.md)

@@@ sd-consistent-hashing | What is consistent hashing and why use it? | arch | system-design,distributed-systems,hashing | qa | System design
"With `hash(key) % N`, changing N from 4 to 5 moves almost every key, which empties a cache cluster. Consistent hashing places both nodes and keys on a ring; a key belongs to the first node clockwise. Adding or removing a node moves only about 1/N of the keys, those between it and its neighbour.

Plain rings distribute unevenly, so each physical node gets many **virtual nodes**, typically 100–200, which smooths the load and lets stronger machines take more. Lookup is a binary search over sorted ring positions: O(log V).

Replication: store each key on the next R distinct physical nodes clockwise. Used by Cassandra and DynamoDB-style stores, client-side memcached sharding, and load balancers that need session affinity. Redis Cluster instead uses 16,384 fixed hash slots, which is a related idea."

Tham khảo thêm: [System Design - Consistent Hashing](https://minhnhat97kg.github.io/docsify/content/system-design-consistent-hashing/vi.md)

@@@ sd-distributed-lock | How do you implement a distributed lock, and what can go wrong? | arch | system-design,distributed-systems,redis,lock | qa | System design
"Single Redis: `SET lock:key <random-token> NX PX 30000`. The random token lets me release safely with a Lua script that deletes only if the value is still mine, so I never delete a lock another client acquired after mine expired. The TTL prevents a crashed holder from blocking forever.

**Redlock** acquires the lock on a majority of independent Redis nodes within a time budget, to survive a node failure. It's debated because it depends on bounded clock drift and process pauses.

The fundamental problem: a holder can pause, for example in a long GC, past its TTL, and then write after someone else took the lock. The fix is a **fencing token**: an increasing number issued with each lock, which the storage layer checks and rejects if it's older than one it has seen.

So: Redis locks for efficiency, such as avoiding duplicate work. For correctness, I use ZooKeeper or etcd with fencing, or better, a database constraint or conditional update that makes the lock unnecessary."

Tham khảo thêm: [System Design - Distributed Locking (Redlock)](https://minhnhat97kg.github.io/docsify/content/system-design-distributed-locking-redlock/vi.md)

@@@ sd-eventual | What is eventual consistency, and when is it acceptable? | arch | system-design,consistency,distributed-systems | qa | System design
"If no new writes happen, all replicas eventually converge to the same value. It's the BASE side of the trade-off with ACID: basically available, soft state, eventually consistent.

Acceptable when a short delay doesn't break business rules: transaction history views, loyalty points, search indexes, like counters, notifications. Not acceptable for the balance check that decides whether a payment goes through; that stays strongly consistent in one database.

'How long is eventually' should be measured, through replication or consumer lag metrics, and bounded with alerts. Conflicts on concurrent writes are resolved by last-write-wins with timestamps (simple but lossy), version vectors, or CRDTs. Replicas repair through read repair and background anti-entropy. On the UX side: read-your-own-writes from the primary, or show a 'processing' state."

Tham khảo thêm: [System Design - Eventual Consistency](https://minhnhat97kg.github.io/docsify/content/system-design-eventual-consistency/vi.md)

@@@ sd-flash-sale | Design a flash sale: 1,000 items, one million users clicking at once. | arch | system-design,concurrency,redis | qa | System design
"**The two problems:** a thundering herd of traffic, and overselling.

**Absorb traffic:** static pages on a CDN, a countdown handled client-side, rate limiting and a virtual waiting room at the gateway, so only a manageable flow reaches the backend.

**No overselling:** keep the stock counter in Redis and decrement atomically, with a Lua script that checks `stock > 0` and decrements in one step, or `DECR` and roll back if the result is negative. Only requests that win a unit continue.

**Protect the database:** winners go onto a queue such as Kafka; consumers create orders at a pace the database handles, with a unique constraint on (user, sale) so each user buys once, and idempotent processing.

**Reservations:** a won unit is held for, say, 10 minutes awaiting payment; on timeout, a delayed job returns it to stock.

**Consistency:** Redis is the gatekeeper, the database is the source of truth; a reconciliation job compares them after the sale."

Tham khảo thêm: [Behavioral Interview (có phần thiết kế flash sale)](https://minhnhat97kg.github.io/docsify/content/behavioral-interview/vi.md)

@@@ sd-double-entry | How does double-entry bookkeeping work in a ledger? | arch | system-design,fintech,payments,ledger | qa | System design
"Money is never created or destroyed: every transaction has entries that sum to zero, for example debit Alice 100 and credit Bob 100.

Schema: `accounts`, `transactions` (one business event, with an idempotency key) and `entries` (transaction ID, account ID, signed amount). Entries are a separate table, not JSON, so they can be indexed, summed and constrained, and the database can enforce that each transaction balances.

The ledger is **immutable**: no updates or deletes. A mistake is fixed by a new reversing transaction, which keeps the audit trail.

Fees and external money flow through **system accounts**: a fee revenue account, a settlement account for each bank partner, a suspense account for unmatched items. So a 100 transfer with a 1 fee is three entries: Alice −101, Bob +100, fees +1.

Daily **reconciliation** checks that the entries sum to zero, that cached balances match the sum of entries, and that settlement accounts match bank statements."

Tham khảo thêm: [Double Entry Bookkeeping](https://minhnhat97kg.github.io/docsify/content/system-design-double-entry-bookkeeping/vi.md), [E-Wallet (High Consistency)](https://minhnhat97kg.github.io/docsify/content/system-design-e-wallet-high-consistency-reliability/vi.md)

@@@ sd-strangler | How do you migrate a monolith to microservices safely? | arch | system-design,migration,microservices | qa | Architecture
"Not with a big-bang rewrite: it freezes features for months and fails at cutover. I use the **Strangler Fig** pattern:

1. Put a facade, such as an API gateway or NGINX, in front of the monolith.
2. Pick one bounded context with clear edges and value, build it as a service, and route its endpoints there, gradually, by percentage or by user.
3. Repeat until the monolith is empty or small enough to keep.

Rollback is just switching the route back, which is why routing must be configurable without a deploy.

The database is the hardest part: start with the new service reading the shared database if needed, then give it its own store, synchronized by backfill plus change data capture (Debezium) or dual writes, verified by comparing results, before cutting over.

When not to use it: small systems where a rewrite is cheap, or when you can't intercept calls to the old system."

Tham khảo thêm: [Strangler Fig Pattern](https://minhnhat97kg.github.io/docsify/content/system-design-strangler-fig-pattern/vi.md)

@@@ arch-hexagonal | What is hexagonal (ports and adapters) architecture? | arch | architecture,clean-architecture,design | qa | Architecture
"The domain and use cases sit in the core with no dependencies on frameworks or databases. The core defines **ports**, interfaces such as `PaymentRepository` or `NotificationSender`. **Adapters** implement them on the outside: a Postgres repository, a Kafka publisher, an HTTP controller. Dependencies point inward only.

Benefits: business logic is testable with fakes in milliseconds, and infrastructure can change, such as swapping a database or adding a gRPC API, without touching the core.

A practical rule: don't use ORM entities as domain models, for example a GORM model or a JPA entity full of annotations and lazy-loading proxies leaking into business logic; map at the adapter boundary.

Costs: more files and mapping code. The performance overhead is negligible. I'd skip it for simple CRUD services or short-lived prototypes, and use it where business rules are rich and long-lived."

Tham khảo thêm: [Clean Architecture - Hexagonal, Ports & Adapters](https://minhnhat97kg.github.io/docsify/content/clean-architecture-hexagonal-ports-adapters/vi.md)

@@@ arch-principles | DRY, KISS, YAGNI: duplication or coupling? | arch | clean-code,principles,design | qa | Architecture
"- **DRY** is about knowledge, not identical-looking code. Two pieces of code that look the same but change for different reasons should stay separate; merging them couples unrelated features.
- **KISS:** the simplest design that works, readable by the next engineer.
- **YAGNI:** don't build for requirements that don't exist yet.
- **Rule of three:** abstract on the third occurrence, when the pattern is actually clear.
- **Law of Demeter:** talk to direct collaborators, not `a.getB().getC().doX()`.
- **Fail fast:** validate early and surface errors immediately.

Duplication or coupling? I usually prefer a little duplication over the wrong abstraction. Across microservices especially, sharing a domain library couples deployments; duplicating a small DTO is cheaper than a shared library every service must upgrade together."

Tham khảo thêm: [Software Principles](https://minhnhat97kg.github.io/docsify/content/software-principles/vi.md)

@@@ kafka-internals | Why is Kafka fast, and what are ISR and exactly-once? | arch | kafka,distributed-systems,performance | qa | Kafka và messaging
"**Why fast despite writing to disk:** it appends sequentially to a log, which disks do very fast; it relies on the OS page cache instead of its own cache; it uses zero-copy `sendfile` from page cache to the socket; and it batches and compresses records.

**ISR, in-sync replicas:** the followers that are caught up with the partition leader. With `acks=all` and `min.insync.replicas=2`, a write succeeds only when at least two replicas have it, so losing one broker loses no acknowledged data. Only ISR members can become leader, unless unclean leader election is enabled, which trades data loss for availability.

**Consumer crashes before processing:** if offsets are committed after processing, the message is redelivered: at-least-once.

**Exactly-once:** idempotent producers remove duplicates from retries, and transactions write output records and consumer offsets atomically for read-process-write within Kafka. Once a database or external API is involved, I still need idempotent consumers. Modern Kafka runs in KRaft mode, without ZooKeeper."

Tham khảo thêm: [Kafka - Basic Concepts](https://minhnhat97kg.github.io/docsify/content/kafka-basic/vi.md)
