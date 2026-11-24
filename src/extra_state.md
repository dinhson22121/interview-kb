@@@ sd-stateless-stateful | Stateless và stateful khác nhau thế nào? Cho ví dụ ở từng tầng của hệ thống. / What's the difference between stateless and stateful? Give examples at each layer of a system. | arch | stateless,stateful,scalability | qa | Nền tảng scale
### Tiếng Việt

**Định nghĩa:**
- **Stateless (phi trạng thái):** server **không giữ thông tin gì về các request trước** của client. Mỗi request mang **đủ thông tin** để được xử lý độc lập, nên **bất kỳ instance nào** cũng xử lý được.
- **Stateful (có trạng thái):** server **nhớ trạng thái** giữa các request (session, kết nối, dữ liệu trong bộ nhớ). Request sau phụ thuộc vào request trước, nên thường phải quay về **đúng instance** đang giữ trạng thái đó.

**Lưu ý quan trọng:** hệ thống nào cũng có trạng thái (giỏ hàng, đơn hàng, số dư). "Stateless service" nghĩa là **trạng thái được đẩy ra ngoài** (database, Redis, token phía client), chứ không phải không có trạng thái.

| | Stateless | Stateful |
|---|---|---|
| Trạng thái nằm ở | Ngoài process: DB, Redis, S3, token của client | Trong bộ nhớ hoặc đĩa của chính instance |
| Scale ngang | **Dễ**: thêm instance, load balancer chia đều | Khó: cần sticky session, chia dữ liệu, đồng bộ trạng thái |
| Instance chết | Không mất gì, request sau sang instance khác | **Mất trạng thái** (session, kết nối) nếu không có bản sao |
| Deploy, restart | Dễ, rolling update thoải mái | Phải drain, chuyển hoặc khôi phục trạng thái |
| Hiệu năng | Có thể chậm hơn vì mỗi request phải đọc trạng thái từ ngoài | Nhanh vì dữ liệu sẵn trong bộ nhớ |
| Độ phức tạp | Thấp ở tầng app | Cao hơn |

**Ví dụ ở từng tầng:**

| Tầng | Stateless | Stateful |
|---|---|---|
| **Giao thức** | HTTP: mỗi request độc lập | TCP (kết nối có trạng thái), **WebSocket**, gRPC streaming, FTP |
| **Xác thực** | **JWT**: token chứa thông tin user và chữ ký, server chỉ cần kiểm tra chữ ký | **Session**: server lưu session, client giữ `JSESSIONID` cookie |
| **Service** | REST API Spring Boot, mọi dữ liệu nằm ở DB hoặc Redis | Game server, chat server giữ kết nối WebSocket, service có cache cục bộ quan trọng |
| **Lưu trữ** | | Database, Kafka broker, Redis, Elasticsearch: **bản chất là stateful** |
| **Kubernetes** | **Deployment**: pod giống nhau, tên ngẫu nhiên, thay thế tùy ý | **StatefulSet**: pod có tên cố định (`db-0`, `db-1`), ổ đĩa riêng gắn theo pod, khởi động theo thứ tự |
| **Firewall** | Stateless firewall: xét từng gói tin riêng lẻ | Stateful firewall: nhớ kết nối, tự cho gói trả lời đi qua (AWS Security Group là stateful, Network ACL là stateless) |
| **Xử lý stream** | Lọc, biến đổi từng message | Đếm, cộng dồn theo cửa sổ thời gian, join stream (Kafka Streams, Flink lưu state store) |

**Session và JWT, chi tiết hơn:**

| | Session (stateful) | JWT (stateless) |
|---|---|---|
| Lưu ở đâu | Server (bộ nhớ, hoặc Redis qua Spring Session) | Client giữ token |
| Thu hồi ngay (logout, khóa tài khoản) | **Dễ**: xóa session | **Khó**: token còn hiệu lực tới khi hết hạn; cần TTL ngắn + refresh token, hoặc danh sách chặn (lại thành có trạng thái) |
| Scale | Cần session dùng chung (Redis) hoặc sticky session | Dễ, instance nào cũng kiểm tra được |
| Kích thước | Cookie nhỏ | Token lớn hơn, gửi kèm mỗi request |
| Hợp với | Web app truyền thống, cần thu hồi ngay | API, mobile, microservices, gọi giữa các service |

Thực tế hay kết hợp: **access token JWT sống ngắn (5–15 phút) + refresh token lưu ở server** để thu hồi được.

**Câu trả lời mẫu:** *"Stateless nghĩa là server không nhớ gì giữa các request, nên instance nào cũng phục vụ được và scale ngang dễ. Tôi giữ tầng ứng dụng stateless bằng cách đưa trạng thái ra ngoài: session vào Redis hoặc dùng JWT, file vào S3, cache dùng chung vào Redis. Những thành phần vốn stateful như database, Kafka hay WebSocket server thì tôi xử lý riêng: replication, StatefulSet, hoặc định tuyến về đúng node."*

### English

**Definitions:**
- **Stateless:** the server **keeps nothing about a client's previous requests**. Each request carries **all the information** needed to process it independently, so **any instance** can handle it.
- **Stateful:** the server **remembers state** between requests (sessions, connections, in-memory data). Later requests depend on earlier ones, so they often have to return to **the same instance** that holds the state.

**An important point:** every system has state (carts, orders, balances). A "stateless service" means **the state has been pushed out** (to a database, Redis, or a client-side token), not that there is no state.

| | Stateless | Stateful |
|---|---|---|
| Where the state lives | Outside the process: DB, Redis, S3, the client's token | In the instance's own memory or disk |
| Horizontal scaling | **Easy**: add instances and let the load balancer spread traffic | Hard: needs sticky sessions, data partitioning, state synchronization |
| An instance dies | Nothing is lost; the next request goes elsewhere | **State is lost** (sessions, connections) unless replicated |
| Deploys, restarts | Easy; rolling updates freely | State must be drained, moved or restored |
| Performance | Can be slower, since each request reads state from outside | Fast, since the data is already in memory |
| Complexity | Low at the application tier | Higher |

**Examples at each layer:**

| Layer | Stateless | Stateful |
|---|---|---|
| **Protocols** | HTTP: each request is independent | TCP (stateful connections), **WebSocket**, gRPC streaming, FTP |
| **Authentication** | **JWT**: the token holds user info and a signature; the server only verifies the signature | **Sessions**: the server stores the session; the client holds a `JSESSIONID` cookie |
| **Services** | A Spring Boot REST API with all data in the DB or Redis | Game servers, chat servers holding WebSocket connections, services with an important local cache |
| **Storage** | | Databases, Kafka brokers, Redis, Elasticsearch: **stateful by nature** |
| **Kubernetes** | **Deployment**: identical pods with random names, replaceable at will | **StatefulSet**: stable pod names (`db-0`, `db-1`), a dedicated volume per pod, ordered startup |
| **Firewalls** | Stateless firewalls: judge each packet on its own | Stateful firewalls: track connections and let reply packets through automatically (AWS Security Groups are stateful; Network ACLs are stateless) |
| **Stream processing** | Filtering or transforming each message | Counting, aggregating over time windows, joining streams (Kafka Streams and Flink keep state stores) |

**Sessions vs JWT in more detail:**

| | Sessions (stateful) | JWT (stateless) |
|---|---|---|
| Stored where | On the server (in memory, or in Redis via Spring Session) | The client holds the token |
| Immediate revocation (logout, account lock) | **Easy**: delete the session | **Hard**: the token stays valid until it expires; you need short TTLs + refresh tokens, or a denylist (which brings state back) |
| Scaling | Needs a shared session store (Redis) or sticky sessions | Easy; any instance can verify |
| Size | A small cookie | A larger token sent with every request |
| Fits | Traditional web apps needing immediate revocation | APIs, mobile, microservices, service-to-service calls |

In practice they're often combined: **a short-lived JWT access token (5–15 minutes) + a refresh token stored on the server** so access can be revoked.

**A model answer:** *"Stateless means the server remembers nothing between requests, so any instance can serve them and horizontal scaling is easy. I keep the application tier stateless by pushing state out: sessions into Redis or JWTs, files into S3, shared caches into Redis. Components that are stateful by nature, like databases, Kafka or WebSocket servers, I handle separately: replication, StatefulSets, or routing to the right node."*

@@@ sd-stateful-scaling | Làm sao scale và vận hành thành phần stateful (WebSocket, database, StatefulSet)? Chuyển một service stateful sang stateless thế nào? / How do you scale and operate stateful components (WebSocket, databases, StatefulSets), and how do you turn a stateful service into a stateless one? | arch | stateful,scalability,kubernetes,websocket | qa | Nền tảng scale
### Tiếng Việt

**1. Chuyển service stateful sang stateless (checklist hay gặp khi lên Kubernetes):**

| Trạng thái đang nằm trong instance | Đưa ra ngoài bằng |
|---|---|
| `HttpSession` trong bộ nhớ | **Spring Session + Redis**, hoặc chuyển sang JWT |
| File upload ghi ra ổ local | **S3** / object storage |
| Cache cục bộ cần nhất quán | Redis, hoặc chấp nhận lệch với TTL ngắn + broadcast invalidation |
| Job `@Scheduled` chạy trên mọi instance | **ShedLock** (khóa qua DB/Redis), hoặc tách thành job riêng (Kubernetes CronJob) |
| Bộ đếm, rate limit trong bộ nhớ | Redis (`INCR`, sorted set) |
| Khóa `synchronized` để chống trùng | Khóa phân tán, hoặc **ràng buộc unique / optimistic locking trong DB** |
| Workflow nhiều bước giữ trong RAM | Lưu trạng thái vào DB (state machine), xử lý qua hàng đợi |

**2. Sticky session:** load balancer gắn user vào một instance (theo cookie). Là cách **chữa cháy** khi chưa đưa được trạng thái ra ngoài: tải lệch, instance chết thì user mất session, scale down hay deploy làm đứt phiên.

**3. Scale WebSocket (kết nối là trạng thái không tránh được):**
- Mỗi client giữ kết nối lâu dài tới **một** instance. Khi user A (ở instance 1) gửi tin cho user B (ở instance 3), instance 1 không có kết nối của B.
- Giải pháp: **pub/sub giữa các instance** (Redis pub/sub, Kafka, hoặc message broker STOMP như RabbitMQ). Instance 1 phát tin, instance đang giữ kết nối của B nhận và đẩy xuống. Hoặc lưu **registry user → instance** trong Redis để gửi thẳng.
- Load balancer phải hỗ trợ kết nối lâu (timeout idle lớn, ALB hỗ trợ WebSocket); dùng heartbeat để phát hiện kết nối chết.
- Khi deploy hoặc instance chết, client **tự kết nối lại** (có backoff) và lấy lại tin nhắn bị lỡ từ DB theo id tin cuối đã nhận.
- Giới hạn: mỗi instance giữ được bao nhiêu kết nối (file descriptor, RAM); scale theo số kết nối, không theo CPU.

**4. Database và thành phần lưu trữ (stateful thật sự):**
- **Scale đọc** bằng read replica; **scale ghi** bằng sharding (chia dữ liệu theo key).
- **HA** bằng replication + failover tự động (Patroni, RDS Multi-AZ).
- Thường dùng **dịch vụ quản lý** (RDS, ElastiCache, MSK) thay vì tự chạy, vì vận hành stateful khó hơn nhiều.

**5. StatefulSet trong Kubernetes** (khi tự chạy Kafka, PostgreSQL, Elasticsearch, Zookeeper...):
- **Tên và DNS ổn định:** `kafka-0.kafka.svc`, pod tạo lại vẫn giữ tên, nên các node nhận ra nhau.
- **Mỗi pod một PersistentVolume riêng** (`volumeClaimTemplates`); pod tạo lại trên node khác vẫn gắn lại đúng ổ của mình.
- **Thứ tự:** tạo `0, 1, 2` tuần tự, xóa ngược lại; rolling update từng pod một.
- Cần **headless Service** cho DNS từng pod; `PodDisruptionBudget` để không mất quá nhiều node cùng lúc.
- Vẫn phải tự lo replication, backup, nâng cấp: thường dùng **Operator** (Strimzi cho Kafka, CloudNativePG / Zalando cho PostgreSQL).

**6. Partition trạng thái theo key** (cách scale stateful phổ biến): định tuyến mọi request của cùng một key về cùng một node bằng **consistent hashing** hoặc partition (Kafka consumer theo partition, Kafka Streams state store, actor model như Akka). Mỗi node giữ trạng thái của một phần key, thêm node thì chuyển một phần key.

**Câu trả lời mẫu:** *"Tôi giữ service nghiệp vụ stateless và đẩy trạng thái ra DB, Redis, S3. Với thứ vốn stateful như WebSocket, tôi chấp nhận kết nối gắn với một instance nhưng dùng Redis pub/sub để định tuyến tin giữa các instance và cho client tự kết nối lại. Database thì dùng dịch vụ quản lý có replication; nếu phải tự chạy trên Kubernetes thì dùng StatefulSet kèm Operator."*

### English

**1. Turning a stateful service into a stateless one (a common checklist when moving to Kubernetes):**

| State currently inside the instance | Move it out with |
|---|---|
| In-memory `HttpSession` | **Spring Session + Redis**, or switch to JWTs |
| File uploads written to local disk | **S3** / object storage |
| Local caches that must be consistent | Redis, or accept divergence with short TTLs + broadcast invalidation |
| `@Scheduled` jobs running on every instance | **ShedLock** (a lock in the DB/Redis), or a separate job (a Kubernetes CronJob) |
| In-memory counters, rate limits | Redis (`INCR`, sorted sets) |
| `synchronized` locks to prevent duplicates | Distributed locks, or **unique constraints / optimistic locking in the DB** |
| Multi-step workflows held in RAM | Persist the state in the DB (a state machine) and process via a queue |

**2. Sticky sessions:** the load balancer pins a user to one instance (by cookie). It's a **stopgap** for when state hasn't been moved out yet: load becomes uneven, users lose their session when an instance dies, and scale-downs or deploys cut sessions.

**3. Scaling WebSockets (the connection is unavoidable state):**
- Each client holds a long-lived connection to **one** instance. When user A (on instance 1) messages user B (on instance 3), instance 1 doesn't hold B's connection.
- The fix: **pub/sub between instances** (Redis pub/sub, Kafka, or a STOMP broker such as RabbitMQ). Instance 1 publishes, and the instance holding B's connection receives it and pushes it down. Or keep a **user → instance registry** in Redis to send directly.
- The load balancer must support long-lived connections (a large idle timeout; ALB supports WebSockets); use heartbeats to detect dead connections.
- On deploys or instance failures, clients **reconnect automatically** (with backoff) and fetch missed messages from the DB using the last received message id.
- Limits: how many connections one instance can hold (file descriptors, RAM); scale on connection count, not CPU.

**4. Databases and storage (truly stateful):**
- **Scale reads** with read replicas; **scale writes** with sharding (partitioning data by key).
- **HA** through replication + automatic failover (Patroni, RDS Multi-AZ).
- Often use **managed services** (RDS, ElastiCache, MSK) instead of running them yourself, because operating stateful systems is much harder.

**5. StatefulSets in Kubernetes** (when you run Kafka, PostgreSQL, Elasticsearch, ZooKeeper... yourself):
- **Stable names and DNS:** `kafka-0.kafka.svc`; a recreated pod keeps its name, so nodes recognize each other.
- **One PersistentVolume per pod** (`volumeClaimTemplates`); a pod recreated on another node reattaches its own volume.
- **Ordering:** pods are created `0, 1, 2` in sequence and deleted in reverse; rolling updates go one pod at a time.
- You need a **headless Service** for per-pod DNS, and a `PodDisruptionBudget` so too many nodes aren't lost at once.
- You still handle replication, backups and upgrades yourself, usually through an **Operator** (Strimzi for Kafka, CloudNativePG / Zalando for PostgreSQL).

**6. Partitioning state by key** (a common way to scale stateful work): route every request for the same key to the same node using **consistent hashing** or partitions (Kafka consumers per partition, Kafka Streams state stores, actor models like Akka). Each node holds the state for a share of the keys, and adding a node moves some keys over.

**A model answer:** *"I keep business services stateless and push state out to the DB, Redis and S3. For things that are inherently stateful, like WebSockets, I accept that a connection is tied to one instance but use Redis pub/sub to route messages between instances and let clients reconnect automatically. For databases I use managed services with replication; if I have to run them on Kubernetes myself, I use a StatefulSet with an Operator."*
