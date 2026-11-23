@@@ microservices-2 | Các service giao tiếp với nhau thế nào? Khi nào dùng đồng bộ (sync), khi nào bất đồng bộ (async)? / How do services communicate, and when do you use synchronous vs asynchronous communication? | arch | | override
### Tiếng Việt

**Đồng bộ (sync):** bên gọi gửi request rồi **chờ** response mới làm tiếp. Ví dụ REST qua HTTP, gRPC, GraphQL.

**Bất đồng bộ (async):** bên gửi đẩy message hoặc sự kiện vào broker rồi **làm tiếp ngay**, không chờ người nhận xử lý xong. Ví dụ Kafka, RabbitMQ, SQS. Người nhận xử lý khi sẵn sàng.

| | Đồng bộ (REST, gRPC) | Bất đồng bộ (Kafka, RabbitMQ) |
|---|---|---|
| Bên gọi có kết quả ngay | **Có** | Không (chỉ biết message đã được nhận vào broker) |
| Phụ thuộc lúc chạy | Bên nhận **phải đang sống** | Bên nhận chết thì message nằm chờ trong broker |
| Độ trễ đầu cuối | Thấp, nhưng **cộng dồn** theo chuỗi gọi | Cao hơn, có độ trễ của hàng đợi |
| Lỗi lan truyền | Dễ **sập dây chuyền** | Được cô lập, có retry và DLQ |
| Chịu tải đột biến | Bên nhận phải chịu ngay | Hàng đợi hấp thụ, xử lý dần |
| Nhất quán | Dễ hiểu, gần với nhất quán mạnh | **Eventual consistency**, phải xử lý trùng lặp và sai thứ tự |
| Debug | Dễ, theo một luồng | Khó hơn, cần trace id xuyên qua message |
| Thêm người nhận mới | Phải sửa bên gọi | Chỉ cần subscribe thêm, bên gửi không đổi |

**Khi nào dùng đồng bộ:**
- Người dùng **cần câu trả lời ngay** để làm bước tiếp: đăng nhập, kiểm tra tồn kho trước khi đặt hàng, lấy giá, truy vấn để hiển thị.
- **Truy vấn (query)** dữ liệu của service khác.
- REST cho API công khai và frontend; **gRPC** cho gọi nội bộ cần nhanh (HTTP/2, protobuf nhị phân, có hợp đồng chặt, hỗ trợ streaming).

**Khi nào dùng bất đồng bộ:**
- Việc **có thể làm sau**: gửi email, thông báo, tạo báo cáo, đồng bộ sang search hoặc data warehouse.
- **Một sự kiện, nhiều service phản ứng**: `OrderPlaced` thì Payment, Inventory, Notification, Analytics cùng xử lý.
- Muốn **tách availability**: Notification chết thì đặt hàng vẫn chạy.
- Việc **chạy lâu** (xử lý video, import file lớn), hoặc cần **san phẳng tải**.
- Giao dịch nhiều bước giữa các service (saga).

**Quy tắc thực tế:**
1. **Giữ chuỗi gọi đồng bộ ngắn** (lý tưởng ≤ 2–3 bước). Gọi nối tiếp 5 service, mỗi cái 99,9% availability và 50 ms, thì chỉ còn khoảng 99,5% và ít nhất 250 ms.
2. Mọi lời gọi đồng bộ phải có **timeout, retry có giới hạn (chỉ với thao tác idempotent), và circuit breaker**.
3. **Lệnh (command)** cần kết quả thì gọi đồng bộ; **sự kiện (event)**, tức thông báo "việc này đã xảy ra", thì phát bất đồng bộ.
4. Phát sự kiện phải tin cậy: dùng [outbox pattern](#microservices-4); consumer phải [idempotent](#microservices-5).
5. Mô hình lai hay gặp: API nhận request đồng bộ, kiểm tra nhanh, lưu trạng thái `PENDING`, **trả 202 kèm id**, phần còn lại chạy bất đồng bộ; client hỏi lại trạng thái hoặc nhận webhook.

**Câu trả lời mẫu:** *"Tôi dùng đồng bộ khi bên gọi cần kết quả ngay, chủ yếu là truy vấn, và giữ chuỗi gọi ngắn, có timeout và circuit breaker. Mọi thứ còn lại, đặc biệt khi một sự kiện có nhiều service quan tâm, tôi phát qua Kafka bằng outbox, chấp nhận eventual consistency và làm consumer idempotent. Ở [Opswat], [ví dụ thật của bạn]."*

### English

**Synchronous:** the caller sends a request and **waits** for the response before continuing. Examples: REST over HTTP, gRPC, GraphQL.

**Asynchronous:** the sender pushes a message or event to a broker and **continues immediately**, without waiting for the receiver to finish processing. Examples: Kafka, RabbitMQ, SQS. The receiver processes it when ready.

| | Synchronous (REST, gRPC) | Asynchronous (Kafka, RabbitMQ) |
|---|---|---|
| Caller gets the result immediately | **Yes** | No (it only knows the broker accepted the message) |
| Runtime dependency | The receiver **must be up** | If the receiver is down, the message waits in the broker |
| End-to-end latency | Low, but it **adds up** along the call chain | Higher, including queueing delay |
| Failure propagation | Prone to **cascading failures** | Isolated, with retries and DLQs |
| Handling spikes | The receiver must absorb them immediately | The queue absorbs them and work drains gradually |
| Consistency | Easy to reason about, close to strong consistency | **Eventual consistency**; duplicates and reordering must be handled |
| Debugging | Easy, one flow | Harder; trace ids must travel through messages |
| Adding a new receiver | The caller must change | Just add a subscriber; the sender stays the same |

**When to use synchronous:**
- The user **needs the answer now** to take the next step: login, checking stock before ordering, getting a price, queries for display.
- **Querying** another service's data.
- REST for public APIs and frontends; **gRPC** for fast internal calls (HTTP/2, binary protobuf, strict contracts, streaming support).

**When to use asynchronous:**
- Work that **can happen later**: emails, notifications, reports, syncing to search or a data warehouse.
- **One event, many reacting services**: on `OrderPlaced`, Payment, Inventory, Notification and Analytics all react.
- To **decouple availability**: if Notification is down, ordering still works.
- **Long-running** work (video processing, large file imports), or when you need **load leveling**.
- Multi-step transactions across services (sagas).

**Practical rules:**
1. **Keep synchronous chains short** (ideally ≤ 2–3 hops). Calling 5 services in series, each at 99.9% availability and 50 ms, leaves only about 99.5% and at least 250 ms.
2. Every synchronous call needs a **timeout, bounded retries (for idempotent operations only), and a circuit breaker**.
3. **Commands** that need a result are synchronous; **events**, meaning notices that "this has happened", are published asynchronously.
4. Publish events reliably with the [outbox pattern](#microservices-4), and make consumers [idempotent](#microservices-5).
5. A common hybrid: the API accepts the request synchronously, validates quickly, stores a `PENDING` state, **returns 202 with an id**, and the rest runs asynchronously; the client polls the status or receives a webhook.

**A model answer:** *"I use synchronous calls when the caller needs the result right away, mostly queries, and I keep the chain short with timeouts and circuit breakers. Everything else, especially when several services care about one event, I publish through Kafka with an outbox, accepting eventual consistency and making consumers idempotent. At [Opswat], [your real example]."*

@@@ sync-async-code | Trong một service, xử lý đồng bộ và bất đồng bộ khác nhau thế nào? @Async, CompletableFuture, reactive, virtual threads? / Within one service, how do synchronous and asynchronous processing differ? @Async, CompletableFuture, reactive, virtual threads? | arch | async,concurrency,spring | qa | Request flow & sync/async
### Tiếng Việt

Câu này hỏi về **cách code xử lý bên trong một service**, khác với giao tiếp giữa các service.

**Hai khái niệm hay bị nhầm:**
- **Blocking và non-blocking:** thread có bị **đứng chờ** I/O (DB, HTTP) hay không.
- **Đồng bộ và bất đồng bộ:** bên gọi có **chờ kết quả** rồi mới làm tiếp hay không.

| Cách | Mô hình | Ví dụ | Ưu | Nhược |
|---|---|---|---|---|
| **Blocking thông thường** (Spring MVC) | Mỗi request một thread, thread chờ I/O | `repo.findById()`, `restClient.get()` | Đơn giản, dễ debug, stack trace rõ | Mỗi request giữ một thread khi chờ; số thread giới hạn throughput |
| **`@Async`** | Đẩy việc sang thread pool khác, trả về ngay | Gửi email sau khi đăng ký | Response nhanh hơn | **Mất việc nếu app chết** (chỉ nằm trong RAM); lỗi dễ bị nuốt; gọi trong cùng class thì không chạy bất đồng bộ (proxy) |
| **`CompletableFuture`** | Chạy song song nhiều việc rồi gộp kết quả | Gọi 3 service cùng lúc | Giảm độ trễ: tổng thời gian bằng việc **lâu nhất** thay vì tổng các việc | Code khó đọc hơn; phải tự cấp executor và xử lý timeout |
| **Reactive** (WebFlux, Reactor) | Non-blocking hoàn toàn, vài thread phục vụ rất nhiều request | `Mono`, `Flux`, `WebClient`, R2DBC | Throughput cao, có backpressure | **Khó học, khó debug**; mọi thư viện phải non-blocking (JDBC thì không); một lời gọi blocking làm hỏng cả hệ thống |
| **Virtual threads** (Java 21+) | Code blocking bình thường, JVM tự gỡ thread khi chờ I/O | Spring MVC + `spring.threads.virtual.enabled=true` | Throughput gần reactive mà code vẫn đơn giản | Cần để ý pinning (Java 21–23), vẫn phải giới hạn tài nguyên phía sau |
| **Message queue** | Ghi vào Kafka hoặc RabbitMQ, worker xử lý | Tạo báo cáo, thông báo | **Bền vững**: không mất việc khi app chết, có retry | Hạ tầng phức tạp hơn, eventual consistency |

```java
// Gọi song song bằng CompletableFuture, có timeout
var executor = Executors.newVirtualThreadPerTaskExecutor();
CompletableFuture<User>  u = CompletableFuture.supplyAsync(() -> userClient.get(id), executor);
CompletableFuture<List<Order>> o = CompletableFuture.supplyAsync(() -> orderClient.list(id), executor);
Profile p = u.thenCombine(o, Profile::new)
             .orTimeout(2, TimeUnit.SECONDS)
             .join();            // tổng thời gian ≈ max(user, order), không phải user + order
```

**`@Async` dùng đúng cách:**
- Cấu hình **executor riêng** có giới hạn (`ThreadPoolTaskExecutor` với queue capacity), đừng dùng mặc định.
- Bắt lỗi bằng `AsyncUncaughtExceptionHandler`, hoặc trả về `CompletableFuture` để bên gọi xử lý.
- Gọi từ **bean khác**, không gọi `this.method()`.
- Việc **không được mất** (thanh toán, email quan trọng) thì dùng outbox và message queue, **không dùng `@Async`**.

**Chọn cách nào:**
- Service CRUD và nghiệp vụ thông thường: **Spring MVC + virtual threads**.
- Cần gọi song song nhiều nguồn: `CompletableFuture` hoặc structured concurrency.
- Streaming, rất nhiều kết nối lâu (WebSocket, SSE, gateway): **reactive** đáng để đầu tư.
- Việc chạy nền cần bền vững: **message queue**.

### English

This question is about **how code is processed inside one service**, which is different from communication between services.

**Two concepts that often get mixed up:**
- **Blocking vs non-blocking:** whether a thread **sits waiting** on I/O (DB, HTTP).
- **Synchronous vs asynchronous:** whether the caller **waits for the result** before continuing.

| Approach | Model | Example | Pros | Cons |
|---|---|---|---|---|
| **Plain blocking** (Spring MVC) | One thread per request; the thread waits on I/O | `repo.findById()`, `restClient.get()` | Simple, easy to debug, clear stack traces | Each request holds a thread while waiting; the thread count caps throughput |
| **`@Async`** | Hands work to another thread pool and returns immediately | Sending an email after sign-up | Faster responses | **Work is lost if the app dies** (it lives only in memory); errors are easily swallowed; calls within the same class don't run asynchronously (proxies) |
| **`CompletableFuture`** | Runs several tasks in parallel and combines the results | Calling 3 services at once | Lower latency: total time equals the **slowest** task instead of the sum | Harder to read; you must supply the executor and handle timeouts |
| **Reactive** (WebFlux, Reactor) | Fully non-blocking; a few threads serve very many requests | `Mono`, `Flux`, `WebClient`, R2DBC | High throughput, built-in backpressure | **Hard to learn and debug**; every library must be non-blocking (JDBC isn't); one blocking call breaks the whole system |
| **Virtual threads** (Java 21+) | Ordinary blocking code; the JVM unmounts threads while they wait on I/O | Spring MVC + `spring.threads.virtual.enabled=true` | Throughput close to reactive with simple code | Watch for pinning (Java 21–23); downstream resources still need limits |
| **Message queues** | Write to Kafka or RabbitMQ; workers process it | Report generation, notifications | **Durable**: work isn't lost if the app dies, with retries | More infrastructure, eventual consistency |

```java
// Parallel calls with CompletableFuture, with a timeout
var executor = Executors.newVirtualThreadPerTaskExecutor();
CompletableFuture<User>  u = CompletableFuture.supplyAsync(() -> userClient.get(id), executor);
CompletableFuture<List<Order>> o = CompletableFuture.supplyAsync(() -> orderClient.list(id), executor);
Profile p = u.thenCombine(o, Profile::new)
             .orTimeout(2, TimeUnit.SECONDS)
             .join();            // total time ≈ max(user, order), not user + order
```

**Using `@Async` correctly:**
- Configure a **dedicated, bounded executor** (`ThreadPoolTaskExecutor` with a queue capacity); don't rely on the default.
- Catch errors with an `AsyncUncaughtExceptionHandler`, or return a `CompletableFuture` so the caller handles them.
- Call it from **another bean**, not via `this.method()`.
- For work that **must not be lost** (payments, important emails), use an outbox and a message queue, **not `@Async`**.

**Which to choose:**
- Ordinary CRUD and business services: **Spring MVC + virtual threads**.
- Calling several sources in parallel: `CompletableFuture` or structured concurrency.
- Streaming, or very many long-lived connections (WebSocket, SSE, gateways): **reactive** is worth the investment.
- Durable background work: **message queues**.

@@@ request-flow | Mô tả toàn bộ hành trình của một request từ lúc client gửi đến khi nhận response. / Walk through the full journey of a request from the client sending it to receiving the response. | arch | request-flow,networking,spring | qa | Request flow & sync/async
### Tiếng Việt

**Ví dụ:** app mobile gọi `POST https://api.shop.vn/api/orders` để đặt hàng. Backend là Spring Boot trên Kubernetes (AWS), dùng PostgreSQL, Redis và Kafka.

```
Client ─► DNS ─► TCP + TLS ─► CDN/WAF ─► Load balancer (ALB) ─► Ingress / API gateway
       ─► Kubernetes Service ─► Pod: Tomcat ─► Filter chain (Security) ─► DispatcherServlet
       ─► Controller ─► Service (@Transactional) ─► Redis / DB / service khác ─► Outbox
       ◄─ JSON response ◄──────────────────────────────────────────────────── (ngược lại)
                       └─► (sau commit) Relay ─► Kafka ─► Payment, Inventory, Notification
```

**Phần 1: Mạng, trước khi đến backend**

1. **DNS:** client hỏi IP của `api.shop.vn` (cache của máy, resolver, rồi Route 53). Có thể là GeoDNS trả về region gần nhất.
2. **Kết nối TCP:** bắt tay 3 bước (SYN, SYN-ACK, ACK).
3. **TLS handshake:** thỏa thuận mã hóa, server gửi chứng chỉ, client kiểm tra. TLS 1.3 mất 1 round trip. Các request sau **tái sử dụng kết nối** (keep-alive, HTTP/2) nên bỏ qua bước 1–3.
4. **CDN / WAF** (CloudFront, Cloudflare): chặn tấn công (SQL injection, bot), rate limit thô. API `POST` không cache, nên được chuyển tiếp về origin.
5. **Load balancer** (AWS ALB, L7): thường **kết thúc TLS** ở đây, chọn một node hoặc target khỏe mạnh qua health check, thêm header `X-Forwarded-For`, `X-Forwarded-Proto`.
6. **Ingress / API gateway** (Nginx Ingress, Kong, Spring Cloud Gateway): định tuyến theo path `/api/orders` sang `order-service`; có thể **xác thực JWT** một lần, rate limit theo user, gắn `X-Request-Id`/trace id. (Ở Opswat: forward auth, auth service kiểm tra token rồi gắn header `X-User-Id` để service phía sau không phải xác thực lại.)
7. **Kubernetes Service:** chọn một pod đang **Ready** (kube-proxy, iptables/IPVS).

**Phần 2: Bên trong service Spring Boot**

8. **Tomcat** nhận kết nối, lấy **một thread** từ pool (mặc định tối đa 200, hoặc một virtual thread nếu bật), parse HTTP.
9. **Servlet filter chain:**
   - Filter tracing/logging: đọc trace id, đưa vào MDC để mọi dòng log có trace id.
   - **Spring Security filter chain:** `BearerTokenAuthenticationFilter` kiểm tra chữ ký và hạn của JWT, tạo `Authentication` và lưu trong `SecurityContextHolder`; kiểm tra quyền. Lỗi thì trả **401/403**, request không đi tiếp.
   - CORS, nén...
10. **`DispatcherServlet`:** `HandlerMapping` tìm method khớp `POST /api/orders`, chạy interceptor `preHandle`, rồi `HandlerAdapter` gọi method.
11. **Chuyển body thành object:** `HttpMessageConverter` (Jackson) đọc JSON thành `CreateOrderRequest`; **`@Valid`** kiểm tra; sai thì `MethodArgumentNotValidException` trả **400**.
12. **Controller** gọi **service**. Proxy `@Transactional` **mở transaction**: lấy một kết nối từ **HikariCP** (hết kết nối thì chờ, quá `connectionTimeout` thì lỗi).
13. **Logic nghiệp vụ:**
    - Kiểm tra **idempotency key** (header `Idempotency-Key`), trùng thì trả lại kết quả cũ.
    - Đọc giá sản phẩm từ **Redis** (cache-aside; miss thì đọc DB).
    - Gọi **đồng bộ** Inventory service để giữ hàng, có timeout và circuit breaker. *Không nên gọi HTTP khi đang giữ transaction DB lâu; tốt hơn là gọi trước khi mở transaction, hoặc chuyển sang saga.*
    - **Hibernate** sinh SQL `INSERT INTO orders ...`, chạy trên PostgreSQL (ghi **WAL**, cập nhật index, MVCC).
    - **Ghi dòng outbox** `OrderCreated` trong cùng transaction.
14. **Commit:** Hibernate flush, PostgreSQL commit (WAL được fsync, nên dữ liệu bền vững), kết nối trả về pool.
15. **Response:** controller trả `OrderResponse` với status **201 Created** và header `Location`; Jackson ghi thành JSON; filter ghi log access (method, path, status, thời gian). Lỗi ở bất kỳ đâu sẽ đi qua `@ControllerAdvice` và được trả theo dạng `ProblemDetail`.
16. Thread trả về pool. Response đi ngược lại qua LB, CDN, rồi tới client.

**Phần 3: Phần bất đồng bộ sau khi trả response**

17. **Relay outbox** (Debezium hoặc polling) đọc `OrderCreated` rồi phát lên Kafka, key là `orderId`.
18. **Payment, Inventory, Notification** consume sự kiện, mỗi service xử lý **idempotent**, rồi phát tiếp sự kiện của mình (`PaymentCompleted`...). Đó là saga.
19. Client nhận trạng thái cuối qua **polling** (`GET /api/orders/{id}`), **WebSocket/SSE**, hoặc **push notification**.

**Phần 4: Quan sát xuyên suốt**
- **Trace id** đi qua header HTTP và header Kafka, nên Jaeger hoặc Tempo vẽ được toàn bộ hành trình.
- Metrics: số request, tỷ lệ lỗi, p99 latency (Micrometer, Prometheus); log JSON có trace id (ELK, Loki).

**Những câu interviewer hay hỏi tiếp:**

| Câu hỏi | Ý chính để trả lời |
|---|---|
| "Chỗ nào có thể chậm?" | DNS/TLS ở lần đầu, hết connection pool, query thiếu index, gọi đồng bộ tới service chậm, GC pause |
| "Pod chết giữa chừng thì sao?" | Trước commit: transaction rollback, client nhận lỗi rồi retry với cùng idempotency key. Sau commit: dữ liệu và outbox đã lưu, relay vẫn phát sự kiện |
| "Client retry thì có tạo trùng đơn không?" | Không, nhờ **idempotency key** lưu cùng đơn hàng (unique constraint) |
| "Xác thực ở đâu?" | Gateway kiểm tra token; service vẫn kiểm tra **quyền** trên tài nguyên (user chỉ xem được đơn của mình) |
| "Vì sao trả 201 mà thanh toán chưa xong?" | Đơn ở trạng thái `PENDING_PAYMENT`; phần còn lại là bất đồng bộ (saga), client theo dõi trạng thái |

### English

**Example:** a mobile app calls `POST https://api.shop.vn/api/orders` to place an order. The backend is Spring Boot on Kubernetes (AWS), with PostgreSQL, Redis and Kafka.

```
Client ─► DNS ─► TCP + TLS ─► CDN/WAF ─► Load balancer (ALB) ─► Ingress / API gateway
       ─► Kubernetes Service ─► Pod: Tomcat ─► Filter chain (Security) ─► DispatcherServlet
       ─► Controller ─► Service (@Transactional) ─► Redis / DB / other services ─► Outbox
       ◄─ JSON response ◄───────────────────────────────────────────────────── (way back)
                       └─► (after commit) Relay ─► Kafka ─► Payment, Inventory, Notification
```

**Part 1: The network, before reaching the backend**

1. **DNS:** the client resolves `api.shop.vn` to an IP (local cache, resolver, then Route 53). GeoDNS may return the nearest region.
2. **TCP connection:** the three-way handshake (SYN, SYN-ACK, ACK).
3. **TLS handshake:** cipher negotiation; the server sends its certificate and the client verifies it. TLS 1.3 takes 1 round trip. Later requests **reuse the connection** (keep-alive, HTTP/2), skipping steps 1–3.
4. **CDN / WAF** (CloudFront, Cloudflare): blocks attacks (SQL injection, bots) and does coarse rate limiting. A `POST` API call isn't cached, so it's forwarded to the origin.
5. **Load balancer** (AWS ALB, L7): usually **terminates TLS** here, picks a healthy node or target via health checks, and adds `X-Forwarded-For` and `X-Forwarded-Proto` headers.
6. **Ingress / API gateway** (Nginx Ingress, Kong, Spring Cloud Gateway): routes the `/api/orders` path to `order-service`; may **validate the JWT** once, rate limit per user, and attach an `X-Request-Id`/trace id. (At Opswat: forward auth, where an auth service validates the token and sets an `X-User-Id` header so downstream services don't re-authenticate.)
7. **Kubernetes Service:** picks a pod that is **Ready** (kube-proxy, iptables/IPVS).

**Part 2: Inside the Spring Boot service**

8. **Tomcat** accepts the connection, takes **one thread** from its pool (200 max by default, or a virtual thread if enabled), and parses the HTTP.
9. **Servlet filter chain:**
   - Tracing/logging filters: read the trace id and put it in the MDC so every log line carries it.
   - **Spring Security's filter chain:** `BearerTokenAuthenticationFilter` checks the JWT's signature and expiry, builds an `Authentication` stored in the `SecurityContextHolder`, and checks permissions. On failure it returns **401/403** and the request goes no further.
   - CORS, compression, and so on.
10. **`DispatcherServlet`:** the `HandlerMapping` finds the method matching `POST /api/orders`, interceptors' `preHandle` run, then a `HandlerAdapter` invokes the method.
11. **Turning the body into an object:** an `HttpMessageConverter` (Jackson) reads the JSON into a `CreateOrderRequest`; **`@Valid`** validates it; failures raise `MethodArgumentNotValidException` and return **400**.
12. The **controller** calls the **service**. The `@Transactional` proxy **opens a transaction**: it takes a connection from **HikariCP** (if none are free it waits, and errors after `connectionTimeout`).
13. **Business logic:**
    - Check the **idempotency key** (the `Idempotency-Key` header); on a duplicate, return the previous result.
    - Read product prices from **Redis** (cache-aside; on a miss, read the DB).
    - Call the Inventory service **synchronously** to reserve stock, with a timeout and circuit breaker. *Avoid HTTP calls while holding a DB transaction open for long; better to call before opening the transaction, or move to a saga.*
    - **Hibernate** generates `INSERT INTO orders ...`, which runs on PostgreSQL (writes the **WAL**, updates indexes, MVCC).
    - **Write the outbox row** `OrderCreated` in the same transaction.
14. **Commit:** Hibernate flushes, PostgreSQL commits (the WAL is fsynced, so the data is durable), and the connection goes back to the pool.
15. **Response:** the controller returns an `OrderResponse` with status **201 Created** and a `Location` header; Jackson writes it as JSON; a filter writes the access log (method, path, status, duration). Errors anywhere go through `@ControllerAdvice` and come back as a `ProblemDetail`.
16. The thread returns to the pool. The response travels back through the LB and CDN to the client.

**Part 3: The asynchronous part after the response**

17. The **outbox relay** (Debezium or polling) reads `OrderCreated` and publishes it to Kafka, keyed by `orderId`.
18. **Payment, Inventory and Notification** consume the event, each processing it **idempotently**, and publish their own events (`PaymentCompleted`, ...). That's the saga.
19. The client gets the final status by **polling** (`GET /api/orders/{id}`), via **WebSocket/SSE**, or through a **push notification**.

**Part 4: Observability end to end**
- The **trace id** travels in HTTP headers and Kafka headers, so Jaeger or Tempo can draw the whole journey.
- Metrics: request count, error rate, p99 latency (Micrometer, Prometheus); JSON logs with the trace id (ELK, Loki).

**Common follow-up questions:**

| Question | Key points to answer |
|---|---|
| "Where can it be slow?" | DNS/TLS on the first request, an exhausted connection pool, queries missing indexes, synchronous calls to slow services, GC pauses |
| "What if the pod dies midway?" | Before commit: the transaction rolls back, the client gets an error and retries with the same idempotency key. After commit: the data and outbox are saved, and the relay still publishes the event |
| "Can a client retry create duplicate orders?" | No, thanks to the **idempotency key** stored with the order (a unique constraint) |
| "Where does authentication happen?" | The gateway validates the token; the service still checks **authorization** on the resource (users can only see their own orders) |
| "Why return 201 when payment isn't done?" | The order is in `PENDING_PAYMENT`; the rest is asynchronous (a saga), and the client tracks the status |
