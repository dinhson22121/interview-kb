# Backend Interview KB

Nov 17, 2026 · @Dinh Son

## Cách dùng tài liệu

Kho kiến thức gom câu hỏi và câu trả lời mẫu cho phỏng vấn Senior Backend (Java/Go), dùng chung cho nhiều công ty: HR screening, technical (Java, Spring, database, microservices, system design, CI/CD, coding) và behavioral. Quy trình và trọng tâm riêng của từng công ty nằm ở mục Công ty. Câu hỏi và câu trả lời viết bằng tiếng Anh vì bạn sẽ phải nói bằng tiếng Anh; ghi chú viết bằng tiếng Việt.

- **Trước mỗi cuộc phỏng vấn:** đọc trang của công ty đó để biết vòng nào nặng (coding, system design hay kiến thức Java) rồi ôn theo tag tương ứng.
- **Chỗ trong ngoặc vuông `[...]`** là thông tin chỉ bạn biết (số liệu, tên công cụ, sự cố thật). Hãy điền bằng sự thật, đừng dùng nguyên câu mẫu.
- **Cách luyện:** che câu trả lời, nói to trong 60–90 giây, ghi âm, rồi so lại. Câu mẫu là khung ý, không phải để học thuộc.
- **Khi bị hỏi vặn:** nêu trade-off và ví dụ từ dự án thật (Opswat, DXC) thay vì lặp lại định nghĩa.

## HR screening

Vòng này kiểm tra tiếng Anh, độ khớp với vị trí và kỳ vọng lương; trả lời ngắn, rõ, không đi sâu kỹ thuật.

**Q1. Tell me about yourself.**

"I'm a backend engineer with about five years of experience, mainly in Java and Spring Boot, plus two years of Go. I spent three years at DXC Technology building life insurance platforms for clients such as Shinhan Life, MapLife and MetLife. Then I moved to Opswat, where I worked on an endpoint management platform in the cybersecurity domain. My strengths are API design, microservices and working directly with international stakeholders. I'm now looking for a senior role where I can own larger parts of a system and mentor others."

*Ghi chú: giữ dưới 90 giây, kết thúc bằng lý do hợp với công ty đang phỏng vấn. Với công ty product (Grab, Axon) nhấn vào ownership và quy mô; với công ty dịch vụ (EPAM, mgm) nhấn vào kinh nghiệm làm với khách hàng nước ngoài.*

**Q2. Why did you leave your last company?**

"I left Opswat in August 2026 because \[lý do thật, nói trung tính: muốn phạm vi lớn hơn / thay đổi tổ chức / ...\]. I used the time since then to \[việc đã làm: ôn system design, luyện tiếng Anh, làm side project\]. I'm now ready to commit to a long-term role."

*Ghi chú: không chê công ty cũ. Chuẩn bị sẵn câu giải thích khoảng trống từ tháng 8 đến nay, vì gần như chắc chắn sẽ bị hỏi.*

**Q3. Why do you want to join our company?**

"Three reasons. First, \[điều cụ thể về sản phẩm hoặc khách hàng của công ty\], which matches what I want to work on. Second, my background fits: \[kinh nghiệm liên quan nhất\]. Third, \[văn hóa kỹ thuật / lộ trình phát triển / quy mô hệ thống\], which matters to me at the senior level."

*Ghi chú theo công ty:*

- *EPAM, mgm: dự án cho khách hàng toàn cầu, đa domain; bạn có 3 năm làm outsourcing cho khách hàng nước ngoài ở DXC.*
- *Grab: hệ thống quy mô Đông Nam Á, ownership end-to-end; bạn đã dùng Go và Java ở môi trường production.*
- *Axon: sản phẩm có sứ mệnh rõ (an toàn công cộng), domain bảo mật; bạn có kinh nghiệm nền tảng cybersecurity ở Opswat.*

**Q4. What are you looking for in your next role?**

"A senior backend role where I own features end to end, take part in design decisions, and help less experienced engineers. I'd like to stay hands-on with Java and cloud-native systems."

**Q5. What is your experience working with international clients or teams?**

"At DXC I worked on projects for Korean and international insurers. I joined requirement clarification calls, wrote technical documentation in English and handled production support with client teams. At Opswat the engineering organization was international, so English was the working language for \[design reviews / tickets / stand-ups\]."

**Q6. What is your salary expectation?**

"Based on my experience and the senior level of this role, I'm expecting around \[con số hoặc khoảng của bạn\] gross per month. I'm open to discussing the whole package."

*Ghi chú: tra mức lương thị trường trước và nêu một khoảng, cận dưới là mức bạn chấp nhận được.*

**Q7. When can you start? Are you interviewing elsewhere?**

"I can start \[ngay / trong vòng X tuần\]. I'm in discussions with a few other companies, but this role is one of my top choices because of \[lý do cụ thể\]."

**Q8. Are you open to working on a project chosen after you join, or in a different time zone?**

"Yes. I'm flexible about the domain. For time zones, I can overlap with \[EU/US\] hours for meetings as long as it's planned. I'd like to know the expected overlap for the project."

**Q9. What is your strongest technology, and your weakest?**

"My strongest area is Java with Spring Boot and relational databases. An area I'm actively improving is CI/CD: I've used pipelines daily, and recently I built a full pipeline myself with GitHub Actions, Docker and Kubernetes to understand each stage."

*Ghi chú: chỉ nói câu cuối sau khi bạn đã thực sự dựng pipeline đó.*

## Technical: Java core, JVM, concurrency

Đây là nhóm câu hỏi xuất hiện nhiều nhất; người hỏi thường đi từ định nghĩa sang "bên trong hoạt động thế nào" và "bạn đã gặp ở đâu".

### Collections và ngôn ngữ

**Q1. How does HashMap work internally?**

"It's an array of buckets. The key's `hashCode()` is spread by XOR-ing the high 16 bits into the low ones, and the index is `(n - 1) & hash`. Collisions are stored as a linked list, which turns into a red-black tree when a bucket reaches 8 entries and the table has at least 64 buckets, so worst-case lookup is O(log n). The default load factor is 0.75; when exceeded, the table doubles and entries are redistributed. It allows one null key and is not thread-safe."

**Q2. HashMap vs ConcurrentHashMap vs Collections.synchronizedMap?**

"`synchronizedMap` locks the whole map for every operation. `ConcurrentHashMap` since Java 8 uses CAS to insert into an empty bucket and `synchronized` on the bucket's first node otherwise, so writers on different buckets don't block each other and reads are lock-free. It doesn't allow null keys or values. Its iterators are weakly consistent, and compound actions should use `compute`, `merge` or `putIfAbsent` to stay atomic."

**Q3. What is the contract between equals() and hashCode()?**

"Equal objects must have equal hash codes; the reverse isn't required. If I override `equals` without `hashCode`, two equal keys can land in different buckets, so a `HashMap` lookup or `HashSet` de-duplication fails. Keys should also be immutable, because changing a field used in the hash after insertion makes the entry unreachable."

**Q4. Why is String immutable?**

"Four reasons: the string pool can share instances safely, strings are thread-safe without locking, the hash code can be cached which makes them good map keys, and security, since class names, file paths and connection strings can't be changed after validation."

**Q5. ArrayList vs LinkedList? StringBuilder vs StringBuffer?**

"`ArrayList` is backed by an array: O(1) random access, amortized O(1) append, O(n) insert in the middle. `LinkedList` has O(1) insert at a known node but O(n) access and poor cache locality, so in practice `ArrayList` or `ArrayDeque` is almost always faster. `StringBuffer` is synchronized; `StringBuilder` is not and is the default choice."

**Q6. Checked vs unchecked exceptions, and how do you design error handling in a service?**

"Checked exceptions must be declared or handled; unchecked ones extend `RuntimeException`. In services I use unchecked domain exceptions, translate them in one place with `@RestControllerAdvice` into a consistent error body with an error code, log once at the boundary, and never swallow exceptions or use them for normal control flow."

### Java 8 đến 21

**Q7. Explain the Stream API. What is the difference between map and flatMap?**

"A stream is a lazy pipeline: intermediate operations such as `filter` and `map` only run when a terminal operation such as `collect` is called. `map` transforms each element one to one; `flatMap` maps each element to a stream and flattens the results. I avoid parallel streams for I/O or small collections, because they share the common ForkJoinPool and the overhead often outweighs the gain."

**Q8. What newer Java features have you used?**

"Records for immutable DTOs, sealed interfaces to model a closed set of types, pattern matching for `instanceof` and `switch`, text blocks, and `var` for local variables. In Java 21, virtual threads and sequenced collections. Records with sealed types and `switch` let the compiler check that every case is handled."

**Q9. What is Optional for, and how is it misused?**

"It's a return type that makes 'no result' explicit. Misuses are calling `get()` without checking, using it for fields or method parameters, and wrapping collections, where an empty collection is better. I prefer `map`, `orElseGet` and `orElseThrow`."

### JVM và bộ nhớ

**Q10. Describe the JVM memory areas.**

"The heap holds objects and is split into a young generation, with Eden and survivor spaces, and an old generation. Metaspace holds class metadata in native memory. Each thread has its own stack for frames and local variables. There is also the code cache for JIT-compiled code. `StackOverflowError` comes from deep recursion; `OutOfMemoryError` can come from heap, metaspace or direct memory."

**Q11. Which garbage collectors do you know, and how do you choose?**

"G1 is the default: region-based, aims for a pause-time target, good for most services. ZGC does almost all work concurrently, with pauses typically under a millisecond even on large heaps, and has been generational since Java 21; I'd pick it for latency-sensitive services. Parallel GC maximizes throughput for batch jobs. I start with the default, set heap size, enable GC logs, and tune only after measuring."

**Q12. How do you find a memory leak?**

"I confirm it first: old generation usage keeps growing after full GCs. Then I take a heap dump, with `jcmd` or `-XX:+HeapDumpOnOutOfMemoryError`, and open it in Eclipse MAT to look at the dominator tree and the path to GC roots. Typical causes are static or unbounded caches, `ThreadLocal` values in pooled threads, listeners never removed, and unclosed resources. At \[Opswat/DXC\] I found \[sự cố thật nếu có\]."

**Q13. How do class loaders work?**

"There are three built-in loaders: bootstrap, platform and application. They follow parent delegation: a loader asks its parent first and loads the class itself only if the parent can't, which prevents core classes from being replaced. A class is identified by its name plus its loader, which is why the same class loaded twice causes `ClassCastException` in app servers."

### Concurrency

**Q14. volatile vs synchronized vs Atomic classes?**

"`volatile` guarantees visibility and ordering for a single variable but not atomicity of compound actions such as `count++`. `synchronized` gives mutual exclusion and visibility. Atomic classes use CAS for lock-free atomic updates of one variable; `LongAdder` is better under high contention. For anything involving several variables I use a lock or an immutable snapshot."

**Q15. How does ThreadPoolExecutor decide when to create threads?**

"It creates threads up to the core size, then puts tasks in the queue, and only when the queue is full creates threads up to the maximum. After that the rejection policy applies. So with an unbounded queue the maximum size is never used and memory can grow without limit. I size bounded queues deliberately, use `CallerRunsPolicy` for back-pressure, and keep separate pools for CPU-bound and blocking work."

**Q16. What are virtual threads and when would you use them?**

"They're lightweight threads scheduled by the JVM onto a small set of carrier threads. When a virtual thread blocks on I/O it unmounts, so the carrier is free. That makes thread-per-request code scale to many thousands of concurrent blocking calls. They don't help CPU-bound work, they shouldn't be pooled, and concurrency to a limited resource should be capped with a semaphore. Before JDK 24, blocking inside `synchronized` pinned the carrier thread."

**Q17. What is a deadlock and how do you prevent and diagnose it?**

"Two or more threads each hold a lock the other needs. I prevent it by acquiring locks in a fixed global order, keeping critical sections small, using `tryLock` with a timeout, and preferring concurrent collections or message passing. To diagnose I take a thread dump with `jstack` or `jcmd Thread.print`, which reports the deadlock cycle."

**Q18. How do you run several remote calls in parallel and combine the results?**

"With `CompletableFuture.supplyAsync` on a dedicated executor, then `thenCombine` or `allOf`, with `orTimeout` and `exceptionally` for failures. I never use the common pool for blocking calls. On Java 21, starting one virtual thread per call is simpler and reads like sequential code."

## Technical: Spring, database, JPA

Người hỏi muốn thấy bạn hiểu Spring hoạt động bên trong, không chỉ dùng annotation; phần database xoay quanh index, transaction và các bẫy của Hibernate.

### Spring và Spring Boot

**Q1. What are IoC and dependency injection? Which injection type do you prefer?**

"Inversion of control means the container creates objects and wires their dependencies instead of the objects doing it themselves. I prefer constructor injection: dependencies are explicit and can be `final`, the object is never half-initialized, circular dependencies fail at startup, and unit tests need no Spring context."

**Q2. Describe the bean lifecycle and scopes.**

"Spring reads bean definitions, instantiates the bean, injects dependencies, calls aware callbacks, runs `BeanPostProcessor`s before initialization, then `@PostConstruct` or `afterPropertiesSet`, then post-processors after initialization, which is where AOP proxies are created. On shutdown it calls `@PreDestroy`. Scopes are singleton by default, prototype, and the web scopes request and session. Injecting a prototype into a singleton gives one instance unless I use `ObjectProvider` or a scoped proxy."

**Q3. How does @Transactional work, and when does it silently not work?**

"Spring wraps the bean in a proxy that opens a transaction before the method and commits or rolls back after it. It fails in three common cases: self-invocation, because a call from another method of the same class bypasses the proxy; non-public methods with the default proxy mode; and checked exceptions, which don't trigger rollback unless I set `rollbackFor`. Catching the exception inside the method also prevents rollback."

**Q4. Explain propagation and isolation.**

"Propagation defines how a method joins transactions: `REQUIRED` joins or creates one, `REQUIRES_NEW` suspends the current one and starts an independent one, for example for audit logs, and `NESTED` uses a savepoint. Isolation controls what concurrent transactions see: read committed prevents dirty reads, repeatable read also prevents non-repeatable reads, serializable prevents phantoms. MySQL InnoDB defaults to repeatable read; PostgreSQL defaults to read committed."

**Q5. How does Spring Boot auto-configuration work?**

"`@SpringBootApplication` enables auto-configuration. Boot loads the configuration classes listed in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` and applies each only if its conditions match, such as `@ConditionalOnClass`, `@ConditionalOnMissingBean` and `@ConditionalOnProperty`. So if I define my own `DataSource` bean, the default one backs off. I use the `--debug` conditions report to see why something was or wasn't configured."

**Q6. How does Spring AOP work, and what are its limits?**

"It's proxy-based: a JDK dynamic proxy for interfaces, or a CGLIB subclass otherwise. Advice runs around calls that go through the proxy. So it only intercepts external calls to public methods of Spring beans, not internal calls, private methods or final classes."

**Q7. How does Spring Security process a request? How did authentication work in your last system?**

"A request passes through a filter chain. An authentication filter extracts credentials, such as a JWT from the `Authorization` header, validates them and stores an `Authentication` in the `SecurityContext`. Authorization is then checked by URL rules or method security such as `@PreAuthorize`. At Opswat we used forward auth: the gateway called an auth service that validated the token and added identity headers, so downstream services trusted those headers and didn't re-authenticate. The trade-off is that services must only be reachable through the gateway."

**Q8. How do you design and version a REST API?**

"Resource-oriented URLs with plural nouns, correct HTTP methods and status codes, pagination and filtering on collections, a consistent error format, and idempotency: `PUT` and `DELETE` are idempotent by definition, and for `POST` I accept an idempotency key. I version in the path, such as `/v1`, make only backward-compatible changes within a version, and document with OpenAPI."

**Q9. Which design patterns have you actually used? Explain SOLID briefly.**

"Strategy for interchangeable business rules, for example \[tính phí bảo hiểm theo sản phẩm ở DXC\]; Factory to choose an implementation; Builder for complex objects; Template Method and Proxy inside Spring itself; Observer through application events. SOLID: single responsibility, open for extension but closed for modification, subtypes must be substitutable, small specific interfaces, and depend on abstractions rather than concrete classes."

**Q10. How do you test a Spring Boot service?**

"Mostly unit tests with JUnit 5 and Mockito, without a Spring context. Slice tests such as `@WebMvcTest` and `@DataJpaTest` for the web and persistence layers. A smaller number of integration tests with `@SpringBootTest` and Testcontainers, so they run against a real database and broker. I test behaviour, not implementation, and I don't chase a coverage number."

### Database

**Q11. How do indexes work, and when does an index not get used?**

"Most are B+ trees, which keep keys sorted, so they serve equality, range and prefix lookups in O(log n). A composite index follows the leftmost-prefix rule. An index is skipped when I apply a function or implicit type conversion to the column, use a leading wildcard in `LIKE`, when selectivity is low, or when the leading column isn't in the predicate. Indexes cost write time and storage, so I add them based on real queries."

**Q12. What is a covering index? Clustered vs non-clustered?**

"A covering index contains every column the query needs, so the engine doesn't read the table row. In InnoDB the primary key is the clustered index and the rows live in it; secondary indexes store the primary key and need a second lookup unless they cover the query."

**Q13. A query is slow in production. What do you do?**

"I find it in the slow query log or APM, run `EXPLAIN ANALYZE`, and look for full scans, wrong join order, filesort or temporary tables. Then I fix the cause: add or adjust an index, rewrite the query, fetch fewer columns, or paginate with keyset pagination instead of a large `OFFSET`. I verify with the plan and with production-like data volume. At \[công ty\] I reduced \[query\] from \[X\] to \[Y\]."

**Q14. Optimistic vs pessimistic locking?**

"Optimistic locking uses a version column: the update succeeds only if the version is unchanged, otherwise I retry or report a conflict. It suits low contention. Pessimistic locking uses `SELECT ... FOR UPDATE` to block others; it suits high contention on the same rows, such as balance updates, but needs short transactions and consistent lock order to avoid deadlocks."

**Q15. What is ACID? When would you choose NoSQL?**

"Atomicity, consistency, isolation, durability. I default to a relational database for transactional data with relationships. I'd choose a document or key-value store for flexible schemas, very high write volume or simple access by key, and Redis for caching, rate limiting and short-lived data."

### JPA và Hibernate

**Q16. What is the N+1 problem and how do you fix it?**

"Loading N parent entities and then touching a lazy association triggers one extra query per parent. I fix it with `JOIN FETCH` or an `@EntityGraph`, with batch fetching through `@BatchSize`, or with a DTO projection when I only need a few fields. I detect it by logging SQL or asserting query counts in tests."

**Q17. Lazy vs eager loading? What is LazyInitializationException?**

"Lazy loads the association on first access; eager loads it with the parent. I keep everything lazy and fetch explicitly per use case, because eager loading can't be turned off per query. The exception happens when a lazy association is accessed after the session is closed. The fix is to fetch what I need inside the transaction and return DTOs, not to enable open-session-in-view."

**Q18. Explain entity states and the first- and second-level cache.**

"Entities are transient, managed, detached or removed. Managed entities are tracked by the persistence context, which is the first-level cache: it's per session, guarantees one instance per row, and flushes changes automatically through dirty checking. The second-level cache is shared across sessions, optional, and useful for read-mostly reference data; it needs an invalidation strategy."

**Q19. How do you handle large batch inserts or updates with JPA?**

"Enable JDBC batching with `hibernate.jdbc.batch_size`, order inserts and updates, flush and clear the persistence context every batch to keep memory flat, and avoid `IDENTITY` generation because it disables insert batching. For very large volumes I use plain JDBC or a bulk statement."

## Technical: microservices, Kafka, system design

Ở mức senior, điểm được chấm là trade-off: mỗi câu trả lời nên có "khi nào dùng, khi nào không, và cái giá phải trả".

### Microservices

**Q1. Monolith vs microservices: when would you choose each?**

"Microservices give independent deployment, scaling and team ownership, but add network failures, distributed data, and operational cost. I'd start with a well-modularized monolith for a small team or an unclear domain, and split out services when there is a clear bounded context with different scaling or release needs. A distributed monolith, where services must be deployed together, is the worst of both."

**Q2. How do services communicate, and how do you choose sync vs async?**

"Synchronous REST or gRPC when the caller needs the answer now. Asynchronous messaging when the work can complete later, when I want to decouple availability, or when several consumers react to one event. Sync chains multiply latency and failure probability, so I keep them short and use events for everything else."

**Q3. How do you keep data consistent across services?**

"Each service owns its database, so I don't use distributed transactions. I use the saga pattern: a sequence of local transactions, each publishing an event, with compensating actions on failure. Choreography suits simple flows; an orchestrator suits long flows that need visibility. The result is eventual consistency, so the UI and APIs must tolerate intermediate states."

**Q4. What is the outbox pattern?**

"It solves the dual-write problem: updating the database and publishing a message can't be atomic. I write the business change and an outbox row in the same local transaction; a relay, by polling or change data capture such as Debezium, publishes the row to the broker. Delivery is at least once, so consumers must be idempotent."

**Q5. How do you make an operation idempotent?**

"The client sends an idempotency key, or I derive one from the message ID. I store processed keys with a unique constraint, in the same transaction as the business change, and return the stored result on a repeat. For updates I prefer absolute values or version checks over increments."

**Q6. How do you make calls between services resilient?**

"Timeouts on every call, retries with exponential backoff and jitter only for idempotent operations, a circuit breaker to stop calling a failing dependency, bulkheads to isolate thread pools, and a fallback where one makes sense. In Java I use Resilience4j. Retries without timeouts or limits cause retry storms."

**Q7. What does an API gateway do? How is authentication handled across services?**

"It's the single entry point: routing, TLS termination, authentication, rate limiting and request logging. At Opswat the gateway used forward auth to an auth service, which validated the token and passed identity as headers. The alternative is each service validating a JWT itself, which removes the trust assumption but duplicates logic. Between services I'd use mTLS or short-lived service tokens."

**Q8. How do you observe and debug a distributed system?**

"Three signals: structured logs with a correlation or trace ID, metrics such as rate, errors and latency percentiles, and distributed tracing with OpenTelemetry. I alert on symptoms users feel, such as error rate and p99 latency, and use traces to find which hop is slow."

**Q9. Explain the CAP theorem in practical terms.**

"During a network partition a system must choose between consistency and availability. So the real question per feature is: should it reject requests or serve possibly stale data? Payments choose consistency; a product catalogue chooses availability."

### Kafka và messaging

**Q10. Explain topics, partitions, offsets and consumer groups.**

"A topic is split into partitions, each an ordered, append-only log. Each record has an offset. Within a consumer group each partition is read by exactly one consumer, so partitions are the unit of parallelism; adding consumers beyond the partition count gives no benefit. Different groups each receive all records."

**Q11. What is a message key and why use it?**

"The key determines the partition, by hash. Records with the same key go to the same partition and keep their order. So I key by the entity ID, such as order ID, when order per entity matters. A poorly distributed key creates hot partitions."

**Q12. What delivery guarantees does Kafka offer?**

"At most once if I commit offsets before processing; at least once if I commit after, which is the usual choice and requires idempotent consumers. Exactly once is available within Kafka through idempotent producers and transactions, but as soon as a database or external call is involved I still need idempotency on my side."

**Q13. What is a dead letter queue? What happens after a message lands there?**

"It's a separate topic for messages that fail after the configured retries, so one poison message doesn't block the partition. I include the error and original metadata in headers, alert on DLQ volume, and have a process: inspect, fix the cause, then replay to the main topic or discard. A DLQ nobody monitors is just data loss with extra steps."

**Q14. What is a rebalance, and what is consumer lag?**

"A rebalance reassigns partitions when consumers join, leave or exceed `max.poll.interval.ms`. During it consumption pauses and uncommitted work can be reprocessed. Lag is the gap between the latest offset and the group's committed offset; growing lag means consumers are too slow, so I scale consumers up to the partition count or speed up processing."

**Q15. Kafka vs RabbitMQ?**

"Kafka is a durable distributed log: high throughput, replay, ordering per partition, many independent consumers. RabbitMQ is a broker with flexible routing, per-message acknowledgement and priorities, good for task queues. I pick Kafka for event streams and RabbitMQ for work distribution with complex routing."

### System design

*Khung trả lời cho mọi bài: làm rõ yêu cầu chức năng và phi chức năng → ước lượng tải → API → data model → kiến trúc tổng thể → đi sâu điểm nghẽn → lỗi và vận hành. Luôn hỏi lại trước khi vẽ.*

**Q16. Describe the architecture of your last project.**

"It was an endpoint management platform. \[Số lượng\] services in Go and Java behind an API gateway with forward auth. Agents on endpoints reported \[dữ liệu gì\] through \[giao thức\]; services communicated by \[REST/gRPC/message broker\]; data was stored in \[database\]. I owned \[service/module\]. The main challenges were \[quy mô, độ trễ, multi-tenant...\], which we handled by \[giải pháp\]."

*Ghi chú: câu này gần như chắc chắn được hỏi. Vẽ sẵn sơ đồ và tập nói trong 3 phút, kèm 2–3 quyết định thiết kế bạn bảo vệ được.*

**Q17. Design a URL shortener.**

"Requirements: create a short link, redirect fast, read-heavy. API: `POST /links` and `GET /{code}`. I generate the code by base62-encoding a unique ID from a sequence or ID generator, which avoids collisions. Storage is a key-value lookup from code to URL. Redirects are served from a cache such as Redis in front of the database, with a CDN for popular links. I'd add rate limiting on creation, expiry, and async click analytics through a queue."

**Q18. Design a rate limiter.**

"I'd use a token bucket per client key: it allows short bursts and is cheap. State lives in Redis so all instances share it, updated atomically with a Lua script. It sits in the gateway, returns 429 with `Retry-After`, and fails open if Redis is unavailable unless the endpoint is security-sensitive. A sliding window counter is the alternative when I need smoother limits."

**Q19. How do you use caching, and what can go wrong?**

"Cache-aside: read from cache, on miss read the database and populate with a TTL; on write, update the database and invalidate the key. Risks are stale data, a stampede when a hot key expires, which I handle with a lock or jittered TTLs, and cache penetration for missing keys, handled by caching negative results. A CDN applies the same idea at the edge for static and cacheable responses."

*Ghi chú: bạn chưa làm thực tế với CDN, nên nếu bị hỏi sâu hãy nói thẳng là bạn hiểu nguyên lý (edge cache, TTL, cache key, invalidation) nhưng chưa vận hành.*

**Q20. How do you scale a database?**

"In order: optimize queries and indexes, add caching, scale vertically, add read replicas for read-heavy load while accepting replication lag, then partition tables, and only last shard by a key such as tenant ID, because sharding complicates joins, transactions and rebalancing."

## Technical: CI/CD, cloud, DevOps

Đây là điểm yếu bạn tự nhận, và cách vá nhanh nhất là tự dựng một pipeline thật trong 2–3 ngày rồi trả lời bằng kinh nghiệm đó. Developer senior chỉ cần hiểu và đã từng làm, không cần sâu như DevOps engineer.

### Bài thực hành: dựng pipeline cho một Spring Boot service (8–10 giờ)

1. **CI cơ bản:** GitHub Actions chạy build và unit test trên mọi push và pull request; bật branch protection để test fail thì không merge được.
2. **Quality gate:** thêm Checkstyle hoặc SonarCloud, coverage bằng JaCoCo, và dependency scan.
3. **Đóng gói:** Dockerfile multi-stage, tag image theo commit SHA, push lên GitHub Container Registry.
4. **CD:** deploy lên Kubernetes local (`kind`) hoặc một dịch vụ cloud free tier; thêm manual approval trước production.
5. **Vận hành:** readiness và liveness probe, rollback về image trước, secrets lấy từ GitHub Secrets.

Workflow tối thiểu để bắt đầu (kiểm tra lại phiên bản action mới nhất khi dùng):

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven
      - run: mvn -B verify
      - uses: docker/login-action@v3
        if: github.ref == 'refs/heads/main'
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        if: github.ref == 'refs/heads/main'
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### CI/CD

**Q1. What is the difference between CI, continuous delivery and continuous deployment?**

"Continuous integration means everyone merges small changes often and each change is built and tested automatically. Continuous delivery means every change that passes the pipeline is releasable, and the production release is a manual decision. Continuous deployment removes that manual step: every passing change goes to production automatically."

**Q2. Walk me through the pipeline of your last project.**

"At \[Opswat/DXC\] we used \[Jenkins/GitLab CI/...\]. A merge request triggered compile, unit tests, static analysis and \[scan\]. After merge, the pipeline built a Docker image, pushed it to \[registry\] and deployed to \[dev/staging\] automatically. Production releases needed \[approval của ai\] and ran \[tần suất\]. I didn't own the pipeline, so I rebuilt an equivalent one myself with GitHub Actions, Docker and Kubernetes to understand each stage."

*Ghi chú: câu cuối biến điểm yếu thành bằng chứng chủ động học; chỉ nói khi đã làm xong bài thực hành.*

**Q3. What stages should a good pipeline have, and in what order?**

"Fast checks first: compile, unit tests, lint and static analysis. Then security scans for dependencies and secrets, then build the artifact once, run integration tests against it, publish it, deploy to a test environment, run smoke or end-to-end tests, and finally promote to production with an approval or automatically. The principle is fail fast and build once."

**Q4. What does 'build once, deploy many' mean?**

"The same immutable artifact, identified by commit SHA or version, is promoted through dev, staging and production. Only configuration changes per environment, injected through environment variables, config maps or a secret manager. Rebuilding per environment means production runs something that was never tested."

**Q5. Compare rolling, blue-green and canary deployments.**

"Rolling replaces instances gradually: no extra infrastructure, but two versions run together and rollback is slower. Blue-green runs the new version in a parallel environment and switches traffic at once: instant rollback, double the resources. Canary sends a small percentage of traffic to the new version and increases it while watching metrics: lowest risk, needs good monitoring and traffic control. All three require backward-compatible changes."

**Q6. How do you deploy database changes without downtime?**

"Schema changes are versioned with Flyway or Liquibase and run in the pipeline. I use expand and contract: first add the new column or table in a backward-compatible way, deploy code that writes both and reads the new one, backfill, then remove the old column in a later release. That way the old and new application versions can both run during a rolling deployment, and I can roll the code back."

**Q7. How do you roll back a bad release?**

"Redeploy the previous image tag, which is quick because artifacts are immutable; in Kubernetes that's `kubectl rollout undo`. Feature flags let me switch off a feature without redeploying. Database changes are the hard part, which is why migrations must be backward compatible. Afterwards I'd write up the cause and add a test or check so the pipeline catches it next time."

**Q8. Trunk-based development vs GitFlow?**

"Trunk-based uses short-lived branches merged to main at least daily, with feature flags hiding unfinished work; it suits continuous delivery and reduces merge conflicts. GitFlow uses long-lived develop and release branches; it suits scheduled releases and supporting several versions, at the cost of slower integration. I prefer trunk-based when the test suite is trustworthy."

**Q9. How do you manage secrets in a pipeline?**

"Never in the repository or image. They live in the CI system's secret store or a manager such as Vault or AWS Secrets Manager, are injected at runtime, masked in logs, scoped per environment and rotated. I prefer short-lived credentials through OIDC over long-lived keys, and I run secret scanning on commits."

**Q10. The pipeline takes 40 minutes. How do you speed it up?**

"Measure which stage is slow first. Then cache dependencies and Docker layers, run independent jobs in parallel, split or shard the test suite, move slow end-to-end tests to a later stage or nightly run, build only affected modules, and fix flaky tests that cause reruns."

**Q11. What quality gates do you put in a pipeline?**

"Tests must pass, static analysis with no new critical issues, coverage on new code above an agreed threshold, no known critical vulnerabilities in dependencies or the image, and at least one approving code review. Gates should be fast and trusted; a gate people routinely bypass is worse than none."

### Docker và Kubernetes

**Q12. Image vs container? How do you write a good Dockerfile for a Java service?**

"An image is an immutable, layered template; a container is a running instance of it. For Java I use a multi-stage build: compile with a JDK image, run on a slim JRE image. I order instructions so dependencies are cached before source code, run as a non-root user, pin base image versions, and let the JVM size the heap from the container limit with `-XX:MaxRAMPercentage`."

**Q13. Explain Pod, Deployment, Service, Ingress, ConfigMap and Secret.**

"A Pod is one or more containers sharing network and storage. A Deployment manages replicas and rolling updates. A Service gives a stable address and load-balances across pods. An Ingress routes external HTTP traffic to services. ConfigMaps and Secrets hold configuration and sensitive values outside the image."

**Q14. Liveness vs readiness probes?**

"Readiness says whether the pod can receive traffic; failing it removes the pod from the Service but doesn't restart it. Liveness says whether the process is stuck; failing it restarts the container. Liveness shouldn't check dependencies such as the database, otherwise a database outage restarts every pod. Spring Boot Actuator exposes both. With graceful shutdown they give zero-downtime rollouts."

**Q15. How do you set resources and scale?**

"Requests are what the scheduler reserves; limits are the cap. Exceeding the memory limit gets the container killed, and exceeding the CPU limit throttles it. The Horizontal Pod Autoscaler adds replicas based on CPU or custom metrics such as queue lag. The service has to be stateless for this to work."

### Cloud

**Q16. Which cloud services have you used?**

"\[Trả lời thật.\] On \[AWS/Azure/GCP\] I've worked with \[compute\], \[database\] and \[storage/queue\]. In AWS terms I know the building blocks: EC2 or ECS/EKS for compute, RDS for relational data, S3 for objects, SQS and SNS for messaging, IAM for access, and CloudWatch for logs and metrics."

*Ghi chú: nếu kinh nghiệm cloud còn mỏng, nói rõ phần nào đã làm thật, phần nào mới tự học. Người phỏng vấn senior nhận ra ngay câu trả lời thuộc lòng.*

**Q17. What is infrastructure as code, and why use it?**

"Infrastructure is defined in versioned files, with Terraform or CloudFormation, and applied automatically. It makes environments reproducible, changes reviewable and auditable, and recovery faster than clicking in a console."

**Q18. What are the twelve-factor principles you apply most?**

"Configuration in the environment, stateless processes, logs as event streams written to stdout, backing services as attached resources, fast startup and graceful shutdown, and keeping dev, staging and production as similar as possible."

## Technical: coding và SQL

Bài code ở vòng này thường ở mức easy đến medium; điểm nằm ở cách bạn nói ra suy nghĩ và phân tích độ phức tạp, không chỉ ở đáp án.

*Cách làm mỗi bài: nhắc lại đề và hỏi ràng buộc (input rỗng, ký tự gì, kích thước) → nêu cách brute force và độ phức tạp → nêu cách tối ưu → code → chạy tay một ví dụ → nói time và space complexity.*

### Coding

**Q1. Find the length of the longest substring without repeating characters.**

Sliding window: giữ vị trí gần nhất của mỗi ký tự, khi gặp lại thì dời mép trái. Time O(n), space O(k) với k là số ký tự khác nhau.

```java
int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> last = new HashMap<>();
    int best = 0, left = 0;
    for (int right = 0; right < s.length(); right++) {
        Integer prev = last.put(s.charAt(right), right);
        if (prev != null && prev >= left) {
            left = prev + 1;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

**Q2. Given an int array, group the numbers into ranges 0–9, 10–19, and so on, using Java 8.**

Group theo `n / 10`; dùng `TreeMap` để các khoảng được sắp xếp. Giả định số không âm; hãy hỏi lại điều này.

```java
Map<String, List<Integer>> groupByRange(int[] nums) {
    Map<Integer, List<Integer>> byBucket = Arrays.stream(nums).boxed()
        .collect(Collectors.groupingBy(n -> n / 10, TreeMap::new, Collectors.toList()));
    Map<String, List<Integer>> result = new LinkedHashMap<>();
    byBucket.forEach((b, list) -> result.put(b * 10 + "-" + (b * 10 + 9), list));
    return result;
}
```

**Q3. Two Sum: return the indices of two numbers that add up to a target.**

Một lượt duyệt với map từ giá trị sang chỉ số. Time O(n), space O(n); brute force là O(n²).

```java
int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        Integer j = seen.get(target - nums[i]);
        if (j != null) {
            return new int[] {j, i};
        }
        seen.put(nums[i], i);
    }
    return new int[0];
}
```

**Q4. Find the first non-repeated character in a string, using streams.**

`LinkedHashMap` giữ thứ tự xuất hiện. Time O(n).

```java
Character firstUnique(String s) {
    return s.chars().mapToObj(c -> (char) c)
        .collect(Collectors.groupingBy(Function.identity(), LinkedHashMap::new, Collectors.counting()))
        .entrySet().stream()
        .filter(e -> e.getValue() == 1)
        .map(Map.Entry::getKey)
        .findFirst()
        .orElse(null);
}
```

**Q5. Check whether a string of brackets is valid.**

Dùng stack: gặp ngoặc mở thì push ngoặc đóng tương ứng, gặp ngoặc đóng thì pop và so sánh. Time O(n), space O(n).

```java
boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        switch (c) {
            case '(' -> stack.push(')');
            case '[' -> stack.push(']');
            case '{' -> stack.push('}');
            default -> {
                if (stack.isEmpty() || stack.pop() != c) {
                    return false;
                }
            }
        }
    }
    return stack.isEmpty();
}
```

**Q6. Given a list of employees, find the highest-paid employee in each department and the average salary per department.**

```java
Map<String, Optional<Employee>> topByDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::department,
        Collectors.maxBy(Comparator.comparingDouble(Employee::salary))));

Map<String, Double> avgByDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::department,
        Collectors.averagingDouble(Employee::salary)));
```

*Các dạng nên luyện thêm: đảo chuỗi và palindrome, anagram, merge hai mảng đã sắp xếp, binary search, tìm phần tử trùng, LRU cache bằng `LinkedHashMap`, duyệt cây BFS/DFS.*

### SQL

**Q7. Find the second highest salary.**

```sql
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

"It returns NULL when there is no second value. For the Nth highest I'd use `DENSE_RANK()`."

**Q8. Find the top 3 salaries in each department.**

```sql
SELECT department_id, name, salary
FROM (
    SELECT e.*,
           DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
    FROM employees e
) ranked
WHERE rnk <= 3;
```

"`ROW_NUMBER` gives exactly three rows per department; `RANK` leaves gaps after ties; `DENSE_RANK` doesn't."

**Q9. Find duplicate emails, and customers who have never placed an order.**

```sql
SELECT email, COUNT(*) AS cnt
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

SELECT c.id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

**Q10. WHERE vs HAVING? INNER vs LEFT JOIN? UNION vs UNION ALL?**

"`WHERE` filters rows before grouping; `HAVING` filters groups after aggregation. An inner join returns only matching rows; a left join keeps every row from the left table with NULLs where there is no match. `UNION` removes duplicates, which costs a sort or hash; `UNION ALL` keeps them and is faster."

## Behavioral và manager interview

Vòng này đánh giá bạn có làm việc được với khách hàng và team hay không; mọi câu trả lời nên là một câu chuyện thật theo STAR, dài khoảng 2 phút.

*STAR: Situation (bối cảnh, 1–2 câu) → Task (trách nhiệm của bạn) → Action (bạn đã làm gì, dùng "I" chứ không phải "we") → Result (con số hoặc kết quả cụ thể, và bài học). Các câu mẫu dưới đây là khung; phần trong ngoặc vuông phải là chuyện thật của bạn. Chuẩn bị 6–8 câu chuyện là đủ dùng cho hầu hết câu hỏi.*

### Behavioral

**Q1. Tell me about the most challenging project you've worked on.**

"At \[Opswat/DXC\] we had to \[mục tiêu\] under \[ràng buộc: deadline, quy mô, hệ thống cũ\]. I was responsible for \[phần của bạn\]. The hard part was \[vấn đề kỹ thuật cụ thể\]. I \[các bước: đo đạc, đề xuất phương án, thử nghiệm, triển khai\]. As a result \[kết quả có số liệu\]. I learned \[bài học\]."

**Q2. Describe a production incident you handled.**

"\[Thời điểm\], \[triệu chứng\] affected \[ai, bao nhiêu\]. I first mitigated by \[rollback / tắt feature / scale\], then found the root cause through \[log, metric, trace\]: \[nguyên nhân\]. I fixed it with \[giải pháp\] and added \[test, alert, runbook\] so it can't recur silently. I kept stakeholders updated every \[X\] minutes."

*Ghi chú: thứ tự "giảm thiệt hại trước, tìm nguyên nhân sau, rồi ngăn tái diễn" là thứ người phỏng vấn muốn nghe.*

**Q3. Tell me about a disagreement with a teammate or lead.**

"We disagreed on \[quyết định kỹ thuật\]. I thought \[quan điểm của bạn\]; they preferred \[quan điểm kia\]. I asked for their reasoning, wrote down the trade-offs of both options, and proposed \[prototype / benchmark / ý kiến bên thứ ba\]. We went with \[kết quả\]. Whether or not my option won, I committed to the decision. The relationship stayed \[tốt / tốt hơn\]."

**Q4. How do you handle unclear or changing requirements from a client?**

"On the insurance projects at DXC, requirements from \[khách hàng\] often \[thay đổi như thế nào\]. I clarified by restating the requirement in writing with concrete examples and edge cases, and confirmed it before estimating. When a change arrived mid-sprint, I explained the impact on scope and timeline and offered options, rather than just saying yes or no. That reduced \[rework / bug\] by \[kết quả\]."

**Q5. Tell me about a time you had to push back on a client or say no.**

"The client asked for \[yêu cầu\] by \[deadline\]. It wasn't feasible without \[rủi ro\]. I explained the risk with data, proposed \[phương án thay thế: chia giai đoạn, giảm phạm vi\], and we agreed on \[kết quả\]. The key was offering an alternative instead of only refusing."

**Q6. Tell me about a deadline you were at risk of missing.**

"We were \[X ngày\] from the release of \[tính năng\] when \[vấn đề\]. I flagged it early to \[lead/PM\] instead of hoping to catch up, split the work into must-have and can-wait, and \[hành động\]. We delivered \[phạm vi\] on time and \[phần còn lại\] in the next release."

**Q7. Have you mentored or led other engineers?**

"I \[onboard / review code / hướng dẫn\] \[số người\] engineers at \[công ty\]. My approach is to explain the reasoning in code reviews, pair on the first task in a new area, and give them ownership of something small but complete. One example: \[người đó tiến bộ thế nào\]."

*Ghi chú: nếu chưa từng lead chính thức, nói thật và dùng ví dụ mentoring không chính thức.*

**Q8. Tell me about a mistake you made.**

"I \[lỗi thật, có hậu quả vừa phải\]. I noticed it when \[cách phát hiện\], told the team immediately, and fixed it by \[hành động\]. Since then I \[thay đổi trong cách làm việc\]."

*Ghi chú: chọn lỗi thật, không chọn "lỗi" kiểu "tôi làm việc quá chăm".*

**Q9. How do you do code review, and how do you handle technical debt?**

"In reviews I look at correctness, readability, tests and design, in that order of risk; I ask questions rather than give orders, and separate blocking issues from suggestions. For technical debt I make it visible as tickets with the cost it causes, fix small items as part of related work, and negotiate time for larger ones with a clear benefit, such as fewer incidents or faster delivery."

**Q10. How do you estimate work and work in Scrum?**

"I break a story into tasks, identify unknowns, and spike the risky ones before committing. I estimate relatively in story points with the team and include testing, review and deployment. I raise blockers in the daily stand-up, and use retrospectives to change one concrete thing per sprint."

**Q11. How do you learn a new domain or technology quickly?**

"I moved from life insurance at DXC to cybersecurity at Opswat, and from Java to also writing Go. I start with the official docs and the existing codebase, build something small end to end, and ask domain experts focused questions. Within \[thời gian\] I was \[đóng góp gì\]."

**Q12. Where do you see yourself in three years?**

"As a strong senior or lead engineer who owns the design of a system and helps a team deliver. I want to deepen system design and cloud skills, and \[công ty\] is a good place for that."

### AI-assisted development

Câu hỏi về công cụ AI khi lập trình đang xuất hiện ngày càng nhiều; ví dụ một báo cáo phỏng vấn EPAM tháng 7/2026 ghi câu hỏi về Claude Code, prompt và token usage ([Glassdoor](https://www.glassdoor.com.hk/Interview/EPAM-Systems-Interview-E15544-RVW85790472.htm)).

**Q13. How do you use AI coding tools in your work?**

"I use \[công cụ bạn dùng thật\] for exploring unfamiliar code, generating tests and boilerplate, refactoring, and drafting documentation. I stay responsible for the result: I review every change, run the tests, and don't accept code I can't explain. I don't paste secrets or client data, and I follow the client's policy on AI tools."

**Q14. How do you write an effective prompt for a coding task?**

"I give context, the goal, constraints and the expected output: which files matter, what done looks like, what must not change, and how to verify, for example which tests to run. I split large tasks into small steps, ask for a plan before code on anything non-trivial, and provide examples of the existing style."

**Q15. What are tokens, and how do you control token usage and cost?**

"Models read and write text as tokens, and both cost and the context window are measured in them. Usage grows with everything in the context: the conversation history, files read and tool output. To control it I keep tasks focused, start a fresh session for a new task, point the tool at specific files instead of the whole repository, keep project instructions short, and use a smaller model for simple work. Long sessions also lose accuracy as the context fills, so this is about quality as well as cost."

## Câu hỏi cho interviewer và checklist

Luôn hỏi lại 2–3 câu ở cuối mỗi vòng; không hỏi gì bị xem là thiếu quan tâm.

### Câu hỏi nên hỏi

**Vòng HR**

- "What does the rest of the interview process look like, and what is the timeline?"
- "Is this position for a specific project, or will I be assigned after joining?"
- "What does the career path from Senior to Lead look like here?"

**Vòng technical**

- "What does the tech stack and architecture of the project look like?"
- "How does the team handle code review, testing and releases? How often do you deploy?"
- "What is the biggest technical challenge the team is facing now?"

**Vòng manager/client**

- "What would you expect me to achieve in the first three months?"
- "How is the team structured, and how much overlap with the client's time zone is expected?"
- "How do you measure success for this role?"

### Checklist trước ngày phỏng vấn

- [ ] Self-introduction 90 giây, đã ghi âm và nghe lại
- [ ] Câu trả lời về lý do rời Opswat và khoảng trống từ tháng 8
- [ ] Sơ đồ kiến trúc dự án Opswat và một dự án DXC, nói được trong 3 phút mỗi cái
- [ ] 6–8 câu chuyện STAR đã điền đủ phần trong ngoặc vuông
- [ ] Pipeline CI/CD tự dựng đã chạy được, repo sẵn sàng để chia sẻ
- [ ] Mọi công nghệ ghi trong CV đều trả lời được câu "bạn đã dùng nó như thế nào"
- [ ] Hai buổi mock bằng tiếng Anh đã xong, ba điểm yếu nhất đã vá
- [ ] Mức lương kỳ vọng và ngày có thể bắt đầu
- [ ] Kiểm tra camera, micro, mạng và IDE cho phần live coding
