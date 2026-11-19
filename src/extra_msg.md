@@@ kafka-15 | Kafka và RabbitMQ khác nhau thế nào? Khi nào chọn cái nào? / Kafka vs RabbitMQ: how do they differ and when do you choose each? | messaging | | override
### Tiếng Việt

**Khác biệt cốt lõi:** Kafka là **log phân tán**: message được ghi nối tiếp và **giữ lại** theo thời gian cấu hình, consumer tự quản lý vị trí đọc (offset) và đọc lại được. RabbitMQ là **message broker**: message được định tuyến vào queue và **bị xóa khi consumer ack**.

| | Kafka | RabbitMQ |
|---|---|---|
| Mô hình | Log bất biến, chia partition | Exchange định tuyến vào queue |
| Sau khi đọc | Message **vẫn còn** tới khi hết retention | Message **bị xóa** sau khi ack |
| Đọc lại (replay) | Có, tua offset về trước | Không (trừ RabbitMQ Streams) |
| Nhiều nhóm consumer cùng đọc | Tự nhiên: mỗi consumer group có offset riêng | Phải tạo queue riêng cho từng nhóm (fanout) |
| Thứ tự | Đảm bảo **trong một partition** | Trong một queue với một consumer |
| Định tuyến | Đơn giản: topic + key → partition | **Linh hoạt**: direct, topic (wildcard), fanout, headers |
| Thông lượng | Rất cao (hàng trăm nghìn tới hàng triệu msg/s) | Cao, thường thấp hơn Kafka |
| Ack | Theo offset (commit vị trí) | Theo **từng message**, có nack và requeue |
| Ưu tiên, delay | Không có sẵn | Có priority queue, TTL, delay qua plugin hoặc DLX |

**Chọn Kafka khi:**
- Cần **event streaming**: nhiều service cùng phản ứng với một sự kiện (order created → kho, thanh toán, analytics).
- Cần **đọc lại** dữ liệu cũ, ví dụ để rebuild read model hoặc xử lý lại sau khi sửa bug.
- Thông lượng lớn: log, tracking, CDC (Debezium), metrics.
- Cần **thứ tự theo entity** (dùng key = orderId).

**Chọn RabbitMQ khi:**
- Cần **phân phối công việc** (task queue): gửi email, resize ảnh, mỗi job chỉ một worker xử lý.
- Cần **định tuyến phức tạp** theo routing key hoặc header.
- Cần ack, retry, hoặc ưu tiên **theo từng message**, hoặc message có độ trễ.
- Hệ thống nhỏ hơn, muốn vận hành đơn giản.

**Câu chốt:** *"Kafka cho luồng sự kiện cần lưu lại và nhiều bên đọc; RabbitMQ cho hàng đợi công việc cần định tuyến linh hoạt và ack từng message."*

### English

**Core difference:** Kafka is a **distributed log**: messages are appended and **retained** for a configured period, consumers track their own position (offset) and can re-read. RabbitMQ is a **message broker**: messages are routed into queues and **deleted once a consumer acks them**.

| | Kafka | RabbitMQ |
|---|---|---|
| Model | Immutable log, split into partitions | Exchanges route into queues |
| After consumption | Message **stays** until retention expires | Message is **deleted** after ack |
| Replay | Yes, rewind the offset | No (except RabbitMQ Streams) |
| Several consumer groups reading | Natural: each consumer group has its own offset | Needs a separate queue per group (fanout) |
| Ordering | Guaranteed **within one partition** | Within one queue with a single consumer |
| Routing | Simple: topic + key → partition | **Flexible**: direct, topic (wildcards), fanout, headers |
| Throughput | Very high (hundreds of thousands to millions of msg/s) | High, usually lower than Kafka |
| Acknowledgement | By offset (commit a position) | **Per message**, with nack and requeue |
| Priority, delay | Not built in | Priority queues, TTL, delays via plugin or DLX |

**Choose Kafka when:**
- You need **event streaming**: several services react to the same event (order created → inventory, payment, analytics).
- You need to **replay** old data, for example to rebuild a read model or reprocess after fixing a bug.
- Throughput is high: logs, tracking, CDC (Debezium), metrics.
- You need **ordering per entity** (key = orderId).

**Choose RabbitMQ when:**
- You need **work distribution** (a task queue): sending emails, resizing images, each job handled by exactly one worker.
- You need **complex routing** by routing key or headers.
- You need **per-message** ack, retry or priority, or delayed messages.
- The system is smaller and you want simpler operations.

**Closing line:** *"Kafka for event streams that must be retained and read by many parties; RabbitMQ for work queues that need flexible routing and per-message acknowledgement."*

@@@ rabbitmq-basics | RabbitMQ hoạt động thế nào? Exchange có những loại nào? / How does RabbitMQ work, and what types of exchange are there? | messaging | rabbitmq,messaging | qa | RabbitMQ
### Tiếng Việt

**Luồng cơ bản:** Producer **không gửi thẳng vào queue**. Producer gửi message vào **exchange**, kèm một **routing key**. Exchange dựa vào các **binding** (quy tắc nối exchange với queue) để quyết định đưa message vào queue nào. Consumer đọc từ queue.

```
Producer → Exchange --(binding)--> Queue → Consumer
```

**4 loại exchange:**

| Loại | Cách định tuyến | Ví dụ dùng |
|---|---|---|
| **direct** | Routing key phải **khớp chính xác** binding key | `payment.failed` chỉ vào queue xử lý lỗi thanh toán |
| **topic** | Khớp theo **mẫu**: `*` thay đúng một từ, `#` thay 0 hoặc nhiều từ | `order.*.vn` nhận `order.created.vn`; `order.#` nhận mọi sự kiện order |
| **fanout** | Gửi tới **mọi queue** được bind, bỏ qua routing key | Broadcast: một sự kiện cho nhiều service |
| **headers** | Khớp theo **header** của message thay vì routing key | Định tuyến theo nhiều thuộc tính (`region=vn`, `type=pdf`) |

Ngoài ra có **default exchange** (tên rỗng): kiểu direct, mọi queue tự bind với routing key bằng chính tên queue. Đây là lý do có thể "gửi thẳng vào queue theo tên".

**Mô hình consumer:**
- **Work queue (competing consumers):** nhiều consumer cùng đọc một queue, mỗi message chỉ tới **một** consumer, chia đều kiểu round-robin. Dùng để scale xử lý.
- **Pub/sub:** fanout exchange, mỗi service có queue riêng, nên mỗi service đều nhận được bản sao của message.

**Prefetch (`basic.qos`):** giới hạn số message chưa ack mà một consumer được giữ cùng lúc. Prefetch = 1 chia việc công bằng khi job nặng nhẹ khác nhau; prefetch lớn hơn (10–100) cho thông lượng cao hơn với job nhẹ.

### English

**Basic flow:** a producer **doesn't publish directly to a queue**. It publishes to an **exchange**, with a **routing key**. The exchange uses **bindings** (rules linking an exchange to queues) to decide which queues get the message. Consumers read from queues.

```
Producer → Exchange --(binding)--> Queue → Consumer
```

**The four exchange types:**

| Type | Routing rule | Example use |
|---|---|---|
| **direct** | Routing key must **match exactly** the binding key | `payment.failed` goes only to the payment-failure queue |
| **topic** | Matches by **pattern**: `*` stands for exactly one word, `#` for zero or more words | `order.*.vn` receives `order.created.vn`; `order.#` receives every order event |
| **fanout** | Delivers to **every bound queue**, ignoring the routing key | Broadcast: one event to many services |
| **headers** | Matches on message **headers** instead of the routing key | Routing on several attributes (`region=vn`, `type=pdf`) |

There's also the **default exchange** (empty name): a direct exchange to which every queue is automatically bound with its own name as the routing key. That's why you can "publish to a queue by name".

**Consumer models:**
- **Work queue (competing consumers):** several consumers read one queue, each message goes to **one** consumer, distributed round-robin. Used to scale processing.
- **Pub/sub:** a fanout exchange with one queue per service, so every service gets its own copy of the message.

**Prefetch (`basic.qos`):** limits how many unacknowledged messages a consumer may hold at once. Prefetch = 1 spreads work fairly when jobs vary in cost; a larger prefetch (10–100) gives higher throughput for light jobs.

@@@ rabbitmq-reliability | Làm sao để RabbitMQ không mất message? Retry và dead letter làm thế nào? / How do you make RabbitMQ not lose messages, and how do you handle retries and dead letters? | messaging | rabbitmq,reliability,dlq | qa | RabbitMQ
### Tiếng Việt

Message có thể mất ở **3 chỗ**, mỗi chỗ có một cách chống:

1. **Producer → broker:** mạng lỗi hoặc broker sập trước khi nhận xong.
   → Bật **publisher confirms**: broker xác nhận đã nhận (và đã ghi đĩa với message persistent). Không nhận được confirm thì gửi lại, nên consumer phải idempotent. Dùng thêm flag `mandatory` để biết message không vào được queue nào.
2. **Trong broker:** broker restart.
   → Queue khai báo **durable**, message gửi với **delivery mode persistent**. Để chịu lỗi node, dùng **quorum queue** (nhân bản bằng Raft). Classic mirrored queue đã bị loại bỏ ở RabbitMQ 4.0.
3. **Broker → consumer:** consumer nhận rồi chết giữa chừng.
   → Dùng **manual ack**, chỉ ack **sau khi** xử lý xong. Consumer chết khi chưa ack thì message được giao lại cho consumer khác. Không dùng auto-ack cho việc quan trọng.

**Retry và dead letter:**
- Xử lý lỗi: `basic.nack` hoặc `basic.reject`. Nếu `requeue=true`, message quay lại queue ngay; với lỗi không tự hết, việc này gây **vòng lặp vô hạn** (poison message).
- Cách đúng: cấu hình **Dead Letter Exchange (DLX)** cho queue (`x-dead-letter-exchange`). Message bị reject (`requeue=false`), hết TTL, hoặc vượt giới hạn độ dài queue sẽ được chuyển sang DLX.
- **Retry có độ trễ:** queue `retry.5s` có `x-message-ttl=5000` và DLX trỏ ngược về exchange chính. Hết TTL thì message quay lại xử lý. Đếm số lần retry qua header `x-death`; quá N lần thì chuyển vào queue **parking lot** để người xem xét.
- Quorum queue có sẵn `x-delivery-limit` để giới hạn số lần giao lại.

**Luôn kèm:** consumer **idempotent**, vì cả publisher confirm lẫn redelivery đều có thể tạo trùng lặp; và **alert** khi DLQ có message.

### English

Messages can be lost in **three places**, each with its own defense:

1. **Producer → broker:** the network fails or the broker crashes before it has the message.
   → Enable **publisher confirms**: the broker acknowledges receipt (and, for persistent messages, that it's on disk). Without a confirm, resend, which means consumers must be idempotent. Use the `mandatory` flag to learn when a message couldn't be routed to any queue.
2. **Inside the broker:** the broker restarts.
   → Declare queues as **durable** and publish with **persistent delivery mode**. To survive node failures, use **quorum queues** (replicated with Raft). Classic mirrored queues were removed in RabbitMQ 4.0.
3. **Broker → consumer:** the consumer receives a message and dies mid-processing.
   → Use **manual ack** and ack only **after** processing finishes. If the consumer dies before acking, the message is redelivered to another consumer. Don't use auto-ack for important work.

**Retries and dead letters:**
- On failure: `basic.nack` or `basic.reject`. With `requeue=true` the message goes straight back to the queue; for errors that don't go away, that causes an **infinite loop** (a poison message).
- The right way: configure a **Dead Letter Exchange (DLX)** on the queue (`x-dead-letter-exchange`). Messages that are rejected (`requeue=false`), expire their TTL, or exceed the queue length limit are moved to the DLX.
- **Delayed retry:** a `retry.5s` queue with `x-message-ttl=5000` whose DLX points back to the main exchange. When the TTL expires, the message returns for processing. Count attempts with the `x-death` header; after N attempts, move it to a **parking-lot** queue for a human to review.
- Quorum queues have a built-in `x-delivery-limit` to cap redeliveries.

**Always add:** **idempotent** consumers, because both publisher confirms and redelivery can create duplicates; and an **alert** when the DLQ has messages.

@@@ kafka-ordering-retry | Kafka đảm bảo thứ tự thế nào? Retry khi xử lý lỗi mà không làm hỏng thứ tự? / How does Kafka guarantee ordering, and how do you retry failures without breaking it? | messaging | kafka,ordering,retry | qa | Kafka và messaging
### Tiếng Việt

**Thứ tự chỉ được đảm bảo trong một partition.** Message cùng **key** luôn vào cùng partition (theo hash của key), nên muốn mọi sự kiện của một đơn hàng theo đúng thứ tự thì dùng `key = orderId`.

**Những chỗ làm mất thứ tự:**
1. **Phía producer khi retry:** gửi batch 1 lỗi, batch 2 thành công, batch 1 gửi lại thì nằm sau batch 2. Cách chống: bật `enable.idempotence=true` (mặc định từ Kafka 3.0), khi đó vẫn giữ được thứ tự với `max.in.flight.requests.per.connection` tối đa 5.
2. **Đổi số partition:** tăng partition làm key được hash sang partition khác, nên thứ tự giữa dữ liệu cũ và mới không còn đảm bảo. Hãy chọn đủ số partition ngay từ đầu.
3. **Phía consumer xử lý song song:** nếu một consumer chia message của cùng một partition cho nhiều thread, thứ tự bị phá. Cách làm đúng: song song hóa **theo key** (cùng key vào cùng thread), ví dụ dùng thư viện Confluent Parallel Consumer.

**Retry khi xử lý lỗi, hai lựa chọn với đánh đổi khác nhau:**

| | Blocking retry | Non-blocking retry (retry topic) |
|---|---|---|
| Cách làm | Retry ngay trong consumer với backoff, không commit offset | Đẩy message lỗi sang `orders.retry.1m`, `orders.retry.10m`, rồi `orders.dlt` |
| Thứ tự | **Giữ nguyên** | **Mất thứ tự** với các message sau |
| Nhược điểm | Một message lỗi **chặn cả partition**, lag tăng | Phải chấp nhận xử lý không theo thứ tự |
| Hợp với | Sự kiện cần đúng thứ tự (trạng thái đơn hàng, số dư) | Sự kiện độc lập (gửi email, thông báo) |

Spring Kafka hỗ trợ cả hai: `DefaultErrorHandler` với `BackOff` cho blocking retry, `@RetryableTopic` cho retry topic.

**Kết hợp hay dùng:** blocking retry vài lần cho lỗi tạm thời (timeout, DB bận), rồi đưa vào DLT. Nếu cần giữ thứ tự theo key, ghi nhận key đang có message lỗi và **tạm dừng các message sau của cùng key**, cho tới khi message lỗi được xử lý.

### English

**Ordering is guaranteed only within a partition.** Messages with the same **key** always go to the same partition (by hashing the key), so to keep every event of one order in sequence, use `key = orderId`.

**What breaks ordering:**
1. **Producer retries:** batch 1 fails, batch 2 succeeds, batch 1 is resent and lands after batch 2. The fix: `enable.idempotence=true` (the default since Kafka 3.0), which preserves ordering with up to 5 `max.in.flight.requests.per.connection`.
2. **Changing the partition count:** adding partitions makes keys hash to different partitions, so ordering between old and new data is no longer guaranteed. Pick enough partitions up front.
3. **Parallel processing in the consumer:** if one consumer hands messages from the same partition to several threads, ordering breaks. The right way is to parallelize **by key** (same key, same thread), for example with the Confluent Parallel Consumer library.

**Retrying failed processing: two options with different trade-offs:**

| | Blocking retry | Non-blocking retry (retry topics) |
|---|---|---|
| How | Retry inside the consumer with backoff, without committing the offset | Send the failed message to `orders.retry.1m`, `orders.retry.10m`, then `orders.dlt` |
| Ordering | **Preserved** | **Lost** relative to later messages |
| Downside | One failing message **blocks the whole partition**, lag grows | You must accept out-of-order processing |
| Fits | Events that must stay ordered (order status, balances) | Independent events (emails, notifications) |

Spring Kafka supports both: `DefaultErrorHandler` with a `BackOff` for blocking retries, and `@RetryableTopic` for retry topics.

**A common combination:** a few blocking retries for transient errors (timeouts, a busy database), then the DLT. If per-key ordering matters, record which keys have a failed message and **hold back later messages for the same key** until the failed one is resolved.

@@@ kafka-retention | Kafka giữ dữ liệu bao lâu? Log compaction là gì? / How long does Kafka keep data, and what is log compaction? | messaging | kafka,retention,compaction | qa | Kafka và messaging
### Tiếng Việt

Mỗi partition được lưu thành nhiều **segment** (file). Kafka xóa dữ liệu theo **segment**, không theo từng message, dựa trên `cleanup.policy`:

**1. `delete` (mặc định): xóa theo thời gian hoặc dung lượng.**
- `retention.ms`: mặc định **7 ngày**. Segment cũ hơn mức này bị xóa.
- `retention.bytes`: giới hạn dung lượng mỗi partition (mặc định không giới hạn).
- Consumer đọc chậm hơn retention sẽ **mất dữ liệu**: offset của nó không còn tồn tại, và nó nhảy tới vị trí theo `auto.offset.reset` (`earliest` hoặc `latest`).

**2. `compact`: chỉ giữ giá trị mới nhất cho mỗi key.**
- Kafka giữ lại **bản ghi cuối cùng của mỗi key**, xóa các bản cũ hơn của cùng key.
- Gửi message với value `null` (**tombstone**) để xóa hẳn một key; tombstone bị dọn sau `delete.retention.ms`.
- Topic khi đó giống một **bảng key-value có thể đọc lại từ đầu**.
- Dùng cho: trạng thái hiện tại (giá sản phẩm, profile người dùng, cấu hình), changelog của Kafka Streams, và topic nội bộ `__consumer_offsets` của chính Kafka.

**3. `compact,delete`:** vừa compact vừa xóa theo thời gian.

**Ví dụ:**

```
Topic user-profile (compact), key = userId
offset 0: u1 → {name: "An"}
offset 1: u2 → {name: "Bình"}
offset 2: u1 → {name: "An Nguyễn"}   ← sau compaction chỉ còn bản ghi này cho u1
offset 3: u2 → null                   ← tombstone: u2 bị xóa
```

**Câu hỏi phụ: "Có thể dùng Kafka làm database không?"** Có thể dùng làm nguồn sự kiện (event sourcing) và compacted topic làm trạng thái, nhưng Kafka không có truy vấn tùy ý, index phụ hay transaction như database. Thường kết hợp Kafka với database hoặc state store.

### English

Each partition is stored as several **segments** (files). Kafka deletes data **by segment**, not message by message, according to `cleanup.policy`:

**1. `delete` (default): delete by time or size.**
- `retention.ms`: **7 days** by default. Segments older than that are deleted.
- `retention.bytes`: a size cap per partition (unlimited by default).
- A consumer that falls behind retention **loses data**: its offset no longer exists, and it jumps to the position given by `auto.offset.reset` (`earliest` or `latest`).

**2. `compact`: keep only the latest value for each key.**
- Kafka keeps **the last record of each key** and removes older records with the same key.
- Send a message with a `null` value (a **tombstone**) to delete a key entirely; tombstones are cleaned up after `delete.retention.ms`.
- The topic then behaves like a **key-value table you can replay from the beginning**.
- Used for current state (product prices, user profiles, configuration), Kafka Streams changelogs, and Kafka's own internal `__consumer_offsets` topic.

**3. `compact,delete`:** compaction plus time-based deletion.

**Example:**

```
Topic user-profile (compact), key = userId
offset 0: u1 → {name: "An"}
offset 1: u2 → {name: "Binh"}
offset 2: u1 → {name: "An Nguyen"}   ← after compaction only this record remains for u1
offset 3: u2 → null                   ← tombstone: u2 is deleted
```

**Follow-up: "Can Kafka be used as a database?"** It can serve as an event source (event sourcing), with compacted topics holding state, but it has no ad-hoc queries, secondary indexes or transactions like a database. It's usually combined with a database or a state store.

@@@ microservices-3 | Làm sao giữ dữ liệu nhất quán giữa các service? Saga pattern là gì? / How do you keep data consistent across services? What is the saga pattern? | messaging | | override
### Tiếng Việt

Mỗi service sở hữu database riêng, nên **không có transaction chung** giữa các service. Distributed transaction kiểu 2PC chặn tài nguyên và không hợp microservices. Cách phổ biến là **Saga**.

**Saga** là chuỗi **transaction cục bộ**: mỗi bước commit trong database của service đó rồi phát sự kiện hoặc lệnh cho bước tiếp theo. Nếu một bước thất bại, các bước **đã commit** được hoàn tác bằng **transaction bù (compensating transaction)**.

**Ví dụ đặt hàng:**

```
1. Order Service:     tạo đơn PENDING
2. Payment Service:   trừ tiền            (bù: hoàn tiền)
3. Inventory Service: giữ hàng            (bù: trả hàng về kho)
4. Order Service:     chuyển đơn CONFIRMED
Nếu bước 3 hết hàng → chạy bù bước 2 (hoàn tiền) → đơn CANCELLED
```

**Hai cách triển khai:**

| | Choreography | Orchestration |
|---|---|---|
| Cách làm | Mỗi service nghe sự kiện và tự quyết bước tiếp | Một **orchestrator** ra lệnh cho từng service theo kịch bản |
| Ưu | Đơn giản, ít phụ thuộc trung tâm | **Dễ nhìn toàn bộ luồng**, dễ debug, timeout, retry |
| Nhược | Luồng dài thì khó theo dõi, dễ phụ thuộc vòng | Thêm một thành phần phải vận hành |
| Hợp với | 2–4 bước đơn giản | Luồng dài, nghiệp vụ phức tạp (thanh toán, đặt vé) |

Orchestrator có thể tự viết (state machine lưu trong DB) hoặc dùng **Temporal**, Camunda, AWS Step Functions.

**Những điểm bắt buộc:**
- Mỗi bước phát sự kiện bằng **outbox pattern**, để commit DB và gửi message không bị lệch nhau.
- Mọi bước và mọi bước bù phải **idempotent**, vì message có thể giao lại.
- Bước bù phải **luôn thành công được**: retry tới khi xong; nếu nghiệp vụ không hoàn tác được (email đã gửi) thì bù bằng hành động khác (gửi email đính chính).
- **Thiếu isolation:** trong lúc saga chạy, service khác có thể thấy trạng thái trung gian. Giảm thiểu bằng trạng thái `PENDING` (semantic lock), hoặc sắp xếp bước có rủi ro thất bại cao lên trước bước khó bù.

**Kết quả:** **eventual consistency**: hệ thống nhất quán sau khi saga hoàn tất hoặc đã bù xong. UI và API phải hiển thị được trạng thái trung gian ("Đang xử lý").

### English

Each service owns its database, so there's **no shared transaction** across services. Distributed transactions like 2PC lock resources and don't fit microservices. The common approach is a **saga**.

A **saga** is a sequence of **local transactions**: each step commits in its own service's database and then publishes an event or command for the next step. If a step fails, the steps **already committed** are undone with **compensating transactions**.

**Order example:**

```
1. Order Service:     create order as PENDING
2. Payment Service:   charge the customer     (compensation: refund)
3. Inventory Service: reserve the items       (compensation: release stock)
4. Order Service:     mark order CONFIRMED
If step 3 is out of stock → run step 2's compensation (refund) → order CANCELLED
```

**Two implementation styles:**

| | Choreography | Orchestration |
|---|---|---|
| How | Each service listens to events and decides the next step itself | An **orchestrator** commands each service according to a workflow |
| Pros | Simple, no central component | **Whole flow visible in one place**, easier debugging, timeouts and retries |
| Cons | Long flows are hard to follow, risk of cyclic dependencies | One more component to operate |
| Fits | 2–4 simple steps | Long flows, complex business logic (payments, bookings) |

The orchestrator can be hand-written (a state machine persisted in the database) or a tool such as **Temporal**, Camunda or AWS Step Functions.

**Non-negotiables:**
- Each step publishes its events with the **outbox pattern**, so the database commit and the message can't diverge.
- Every step and every compensation must be **idempotent**, because messages can be redelivered.
- Compensations must **always be able to succeed**: retry until they do; if an action can't be undone (an email was sent), compensate with another action (a correction email).
- **No isolation:** while a saga runs, other services can see intermediate state. Mitigate with a `PENDING` state (a semantic lock), or order the steps so those most likely to fail run before those that are hard to compensate.

**The result is eventual consistency:** the system is consistent once the saga completes or finishes compensating. UIs and APIs must be able to show intermediate states ("Processing").

@@@ dt-2pc | Two-phase commit (2PC) là gì? Vì sao microservices ít dùng? / What is two-phase commit (2PC), and why do microservices rarely use it? | messaging | distributed-transaction,2pc | qa | Distributed transactions
### Tiếng Việt

**2PC** giúp nhiều tài nguyên (nhiều database, hoặc database và message broker) cùng commit hoặc cùng rollback, có một **coordinator** điều phối:

1. **Phase 1, Prepare (vote):** coordinator hỏi từng participant *"Bạn commit được không?"*. Mỗi participant ghi dữ liệu vào log, **giữ khóa**, rồi trả lời YES hoặc NO.
2. **Phase 2, Commit hoặc Abort:** tất cả YES thì coordinator gửi COMMIT; có một NO hoặc timeout thì gửi ABORT. Participant thực hiện rồi nhả khóa.

Trong Java, đây là **XA transaction** qua JTA (Atomikos, Narayana), ví dụ một transaction trải trên hai database.

**Vấn đề:**
- **Blocking:** nếu coordinator chết sau khi participant đã YES, participant **phải giữ khóa và chờ**, không dám tự commit hay rollback. Tài nguyên bị khóa có thể rất lâu.
- **Độ trễ và thông lượng:** nhiều vòng mạng, khóa giữ suốt hai phase, làm hệ thống chậm và khó scale.
- **Khả dụng:** mọi participant phải sống thì transaction mới hoàn tất, nên một service chết kéo theo cả luồng.
- **Không được hỗ trợ rộng:** Kafka, nhiều NoSQL và REST API của bên thứ ba không tham gia XA được.
- **3PC** thêm một phase để giảm blocking nhưng vẫn không chịu được phân vùng mạng, nên hầu như không dùng trong thực tế.

**Vì vậy microservices dùng:** Saga cùng outbox và consumer idempotent, chấp nhận eventual consistency.

**Khi nào 2PC vẫn hợp lý:** trong một hệ thống nhỏ, ít tài nguyên, cùng mạng nội bộ, cần nhất quán tức thì và chấp nhận chi phí hiệu năng. Bên trong một số database phân tán như Spanner hay CockroachDB cũng dùng 2PC kết hợp đồng thuận (Paxos/Raft), nhưng phần đó được ẩn khỏi lập trình viên.

### English

**2PC** makes several resources (several databases, or a database and a message broker) commit or roll back together, coordinated by a **coordinator**:

1. **Phase 1, Prepare (vote):** the coordinator asks each participant *"Can you commit?"*. Each participant writes its changes to a log, **holds its locks**, and answers YES or NO.
2. **Phase 2, Commit or Abort:** if everyone said YES, the coordinator sends COMMIT; if anyone said NO or timed out, it sends ABORT. Participants apply the decision and release their locks.

In Java this is an **XA transaction** via JTA (Atomikos, Narayana), for example one transaction spanning two databases.

**Problems:**
- **Blocking:** if the coordinator dies after participants voted YES, they **must hold their locks and wait**; they can't safely commit or roll back on their own. Resources can stay locked for a long time.
- **Latency and throughput:** several network round trips, with locks held across both phases, make the system slow and hard to scale.
- **Availability:** every participant must be up for a transaction to complete, so one dead service stalls the whole flow.
- **Limited support:** Kafka, many NoSQL stores and third-party REST APIs can't take part in XA.
- **3PC** adds a phase to reduce blocking but still can't tolerate network partitions, so it's almost never used in practice.

**So microservices use** sagas with an outbox and idempotent consumers, accepting eventual consistency.

**When 2PC is still reasonable:** a small system with few resources on the same internal network, where immediate consistency is required and the performance cost is acceptable. Some distributed databases such as Spanner or CockroachDB also use 2PC combined with consensus (Paxos/Raft) internally, but that's hidden from developers.

@@@ dt-tcc | TCC (Try-Confirm-Cancel) là gì? Khác Saga thế nào? / What is TCC (Try-Confirm-Cancel), and how does it differ from a saga? | messaging | distributed-transaction,tcc | qa | Distributed transactions
### Tiếng Việt

**TCC** chia mỗi thao tác nghiệp vụ thành 3 API:

1. **Try:** kiểm tra và **giữ chỗ tài nguyên** nhưng chưa dùng thật. Ví dụ: chuyển 100k từ "số dư khả dụng" sang "số dư tạm giữ".
2. **Confirm:** dùng phần đã giữ, hoàn tất giao dịch. Ví dụ: trừ hẳn 100k khỏi số dư tạm giữ.
3. **Cancel:** trả lại phần đã giữ. Ví dụ: chuyển 100k từ tạm giữ về khả dụng.

Coordinator gọi Try ở mọi service; tất cả thành công thì gọi Confirm ở tất cả, có một lỗi thì gọi Cancel ở những service đã Try.

**Ví dụ đặt vé máy bay và khách sạn:**

```
Try:     giữ ghế 15 phút   |  giữ phòng 15 phút
Confirm: xuất vé           |  xác nhận phòng
Cancel:  nhả ghế           |  nhả phòng
```

**So sánh với Saga:**

| | Saga | TCC |
|---|---|---|
| Bước đầu | Commit thật ngay | Chỉ **giữ chỗ** (Try) |
| Hoàn tác | Transaction bù (hoàn tiền sau khi đã trừ) | Cancel phần đã giữ, **chưa ai thấy kết quả** |
| Isolation | Kém: người khác thấy trạng thái trung gian | **Tốt hơn**: tài nguyên bị khóa ở mức nghiệp vụ |
| Công sức | Mỗi bước thêm 1 hành động bù | Mỗi service phải viết **3 API** và quản lý trạng thái giữ chỗ |
| Hợp với | Đa số luồng nghiệp vụ | Tài nguyên khan hiếm cần giữ chỗ: ghế, phòng, tồn kho, hạn mức tiền |

**Các bẫy phải xử lý:**
- **Idempotent:** Confirm hoặc Cancel có thể bị gọi lại nhiều lần.
- **Empty rollback:** Cancel tới trước khi Try kịp chạy (Try bị timeout); Cancel phải xử lý được trường hợp chưa có gì để hủy.
- **Suspension:** Try tới **sau** Cancel; phải ghi nhận đã Cancel để từ chối Try đến muộn, nếu không tài nguyên bị giữ mãi.
- Phần giữ chỗ cần **TTL** để tự nhả khi coordinator chết.

Framework hỗ trợ: Apache Seata (chế độ TCC).

### English

**TCC** splits each business operation into three APIs:

1. **Try:** validate and **reserve the resource** without consuming it. Example: move 100k from "available balance" to "held balance".
2. **Confirm:** consume the reservation and complete the transaction. Example: deduct the 100k from the held balance for good.
3. **Cancel:** release the reservation. Example: move the 100k from held back to available.

The coordinator calls Try on every service; if all succeed it calls Confirm on all of them, and if any fails it calls Cancel on those that ran Try.

**Example: booking a flight and a hotel:**

```
Try:     hold the seat 15 minutes   |  hold the room 15 minutes
Confirm: issue the ticket           |  confirm the room
Cancel:  release the seat           |  release the room
```

**Compared with a saga:**

| | Saga | TCC |
|---|---|---|
| First step | Commits for real immediately | Only **reserves** (Try) |
| Undo | A compensating transaction (refund after charging) | Cancel the reservation, **nobody has seen the result yet** |
| Isolation | Weak: others see intermediate state | **Better**: resources are locked at the business level |
| Effort | One compensating action per step | Each service writes **3 APIs** and manages reservation state |
| Fits | Most business flows | Scarce resources that need holding: seats, rooms, stock, credit limits |

**Traps you must handle:**
- **Idempotency:** Confirm or Cancel may be called several times.
- **Empty rollback:** Cancel arrives before Try ever ran (Try timed out); Cancel must cope with nothing to cancel.
- **Suspension:** Try arrives **after** Cancel; you must record the cancellation and reject the late Try, otherwise the resource stays held forever.
- Reservations need a **TTL** so they're released automatically if the coordinator dies.

Framework support: Apache Seata (TCC mode).

@@@ dt-compare | So sánh các cách xử lý giao dịch phân tán: 2PC, Saga, TCC, Outbox. / Compare the approaches to distributed transactions: 2PC, saga, TCC, outbox. | messaging | distributed-transaction | qa | Distributed transactions
### Tiếng Việt

| | 2PC / XA | Saga | TCC | Outbox (+ consumer idempotent) |
|---|---|---|---|---|
| Nhất quán | Mạnh, tức thì | Eventual | Eventual, isolation tốt hơn Saga | Eventual |
| Khóa tài nguyên | Khóa DB suốt hai phase | Không | Giữ chỗ ở mức nghiệp vụ | Không |
| Độ phức tạp | Thấp với dev, cao khi vận hành | Trung bình (viết bước bù) | **Cao** (3 API mỗi service) | Thấp |
| Hiệu năng | Kém | Tốt | Tốt | Tốt |
| Giải quyết vấn đề | Commit nhiều tài nguyên cùng lúc | Luồng nghiệp vụ nhiều service | Giữ tài nguyên khan hiếm | **Ghi DB và gửi message** không lệch nhau |

**Chúng không loại trừ nhau.** Outbox là **nền tảng** để Saga hoặc TCC gửi sự kiện tin cậy; idempotency là bắt buộc ở mọi cách.

**Cây quyết định khi trả lời phỏng vấn:**
1. Có thể **gom dữ liệu về một service hoặc một database** không? Nếu được thì dùng transaction cục bộ: đơn giản nhất. Ranh giới service sai thường là nguồn gốc của nhu cầu distributed transaction.
2. Chỉ cần "cập nhật DB **và** phát sự kiện"? Dùng **outbox**.
3. Luồng nhiều service, chấp nhận trạng thái trung gian? Dùng **Saga**: orchestration nếu luồng dài, choreography nếu ngắn.
4. Cần giữ chỗ tài nguyên khan hiếm, không muốn người khác thấy trạng thái trung gian? Dùng **TCC**.
5. Bắt buộc nhất quán tức thì, ít tài nguyên, cùng mạng? Cân nhắc **2PC**, chấp nhận chi phí.

**Kinh nghiệm thực tế để kể:** *"Ở [Opswat/DXC], [luồng X] đi qua [N] service; chúng tôi dùng [outbox/saga/...] và xử lý trùng lặp bằng [idempotency key]..."* (điền chuyện thật).

### English

| | 2PC / XA | Saga | TCC | Outbox (+ idempotent consumers) |
|---|---|---|---|---|
| Consistency | Strong, immediate | Eventual | Eventual, better isolation than a saga | Eventual |
| Resource locking | Database locks across both phases | None | Business-level reservations | None |
| Complexity | Low for developers, high to operate | Medium (write compensations) | **High** (3 APIs per service) | Low |
| Performance | Poor | Good | Good | Good |
| Problem it solves | Committing several resources at once | Business flows spanning services | Reserving scarce resources | **Writing to the DB and publishing a message** without divergence |

**They're not mutually exclusive.** The outbox is the **foundation** that lets sagas or TCC publish events reliably, and idempotency is mandatory in every approach.

**A decision tree for interviews:**
1. Can the data **live in one service or one database**? If so, use a local transaction: simplest. Wrong service boundaries are often what creates the need for distributed transactions.
2. Do you only need to "update the DB **and** publish an event"? Use an **outbox**.
3. A flow across several services where intermediate states are acceptable? Use a **saga**: orchestration for long flows, choreography for short ones.
4. Need to reserve scarce resources without others seeing intermediate state? Use **TCC**.
5. Immediate consistency is mandatory, with few resources on the same network? Consider **2PC** and accept the cost.

**A real story to tell:** *"At [Opswat/DXC], [flow X] spanned [N] services; we used [outbox/saga/...] and handled duplicates with [idempotency keys]..."* (fill in your real story).
