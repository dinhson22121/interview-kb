@@@ sd-scale-up-out | Scale dọc (vertical) và scale ngang (horizontal) khác nhau thế nào? Khi nào chọn cái nào? / Vertical vs horizontal scaling: how do they differ, and when do you choose each? | arch | scalability,system-design | qa | Nền tảng scale
### Tiếng Việt

**Scale dọc (vertical, scale up):** nâng cấp **một máy** mạnh hơn: thêm CPU, RAM, ổ nhanh hơn. Ví dụ đổi RDS từ `db.r6g.large` (2 vCPU, 16 GB) lên `db.r6g.4xlarge` (16 vCPU, 128 GB).

**Scale ngang (horizontal, scale out):** thêm **nhiều máy** chạy cùng một việc, đặt sau load balancer. Ví dụ tăng từ 3 lên 10 pod của order service.

| | Scale dọc | Scale ngang |
|---|---|---|
| Cách làm | Máy to hơn | Thêm máy |
| Sửa code | **Không cần** | Ứng dụng phải **stateless** (hoặc dữ liệu phải được chia) |
| Giới hạn | Có trần cứng: máy lớn nhất có hạn, và giá tăng **nhanh hơn tuyến tính** | Gần như không giới hạn với tầng stateless |
| Chịu lỗi | Vẫn là **một điểm hỏng duy nhất** (SPOF) | Một máy chết, các máy khác gánh |
| Downtime khi nâng | Thường phải restart, failover | Thêm hoặc bớt node không cần dừng |
| Độ phức tạp | Thấp | Cao hơn: load balancer, phân tán dữ liệu, nhất quán, deploy, quan sát |
| Hợp với | Database quan hệ (một primary), giai đoạn đầu, tải tăng vừa phải | Tầng ứng dụng web và API, cache cluster, Kafka, Cassandra |

**Điều kiện để scale ngang tầng ứng dụng: stateless.** Mọi request phải xử lý được ở **bất kỳ instance nào**. Trạng thái phải đưa ra ngoài:
- **Session:** dùng JWT, hoặc lưu session trong Redis (Spring Session), thay vì lưu trong bộ nhớ instance.
- **File upload:** đưa lên S3 hoặc object storage, không ghi ổ đĩa local.
- **Cache local:** chấp nhận lệch giữa các instance, hoặc dùng Redis.
- **Job định kỳ:** chỉ một instance được chạy, dùng khóa phân tán (ShedLock) hoặc tách ra thành job riêng.
- **Sticky session** (load balancer gắn user vào một instance) là cách chữa cháy: tải không đều, và instance chết thì mất session.

**Database khó scale ngang hơn**, vì dữ liệu có trạng thái. Thứ tự thường làm:
1. Tối ưu query và index.
2. **Scale dọc** primary.
3. Thêm **cache**.
4. **Read replica** cho truy vấn đọc.
5. **Partitioning** trong một máy.
6. Cuối cùng mới **sharding**, vì nó làm mọi thứ phức tạp hơn (JOIN và transaction xuyên shard, rebalance).

Xem thêm [How do you scale a database?](#system-design-20) và [Replication & sharding](#db-replication-sharding).

**Câu trả lời mẫu:** *"Tôi scale ngang tầng ứng dụng vì nó rẻ và chịu lỗi tốt, với điều kiện service stateless: session ở Redis hoặc JWT, file ở S3. Với database, tôi scale dọc và thêm read replica trước, chỉ sharding khi một primary thật sự không chịu nổi lượng ghi, vì sharding tốn chi phí vận hành lớn."*

### English

**Vertical scaling (scale up):** make **one machine** more powerful: more CPU, more RAM, faster disks. For example, moving RDS from `db.r6g.large` (2 vCPU, 16 GB) to `db.r6g.4xlarge` (16 vCPU, 128 GB).

**Horizontal scaling (scale out):** add **more machines** doing the same job behind a load balancer. For example, going from 3 to 10 pods of the order service.

| | Vertical | Horizontal |
|---|---|---|
| How | A bigger machine | More machines |
| Code changes | **None needed** | The application must be **stateless** (or the data must be partitioned) |
| Limits | A hard ceiling: the biggest machine is finite, and price grows **faster than linearly** | Practically unlimited for stateless tiers |
| Fault tolerance | Still a **single point of failure** (SPOF) | If one machine dies, the others take over |
| Downtime when upgrading | Usually a restart or failover | Adding or removing nodes needs no downtime |
| Complexity | Low | Higher: load balancers, data distribution, consistency, deployment, observability |
| Fits | Relational databases (a single primary), early stages, moderate growth | Web and API tiers, cache clusters, Kafka, Cassandra |

**The prerequisite for scaling the application tier horizontally: statelessness.** Every request must be servable by **any instance**. State has to move out:
- **Sessions:** use JWTs, or store sessions in Redis (Spring Session), instead of in instance memory.
- **File uploads:** put them in S3 or object storage, not on the local disk.
- **Local caches:** accept divergence between instances, or use Redis.
- **Scheduled jobs:** only one instance may run them, using a distributed lock (ShedLock) or a separate job.
- **Sticky sessions** (the load balancer pins a user to one instance) are a stopgap: load becomes uneven, and if the instance dies the session is lost.

**Databases are harder to scale horizontally**, because they hold state. The usual order:
1. Optimize queries and indexes.
2. **Scale up** the primary.
3. Add a **cache**.
4. **Read replicas** for read queries.
5. **Partitioning** within one machine.
6. Only then **sharding**, because it complicates everything (cross-shard JOINs and transactions, rebalancing).

See also [How do you scale a database?](#system-design-20) and [Replication & sharding](#db-replication-sharding).

**A model answer:** *"I scale the application tier horizontally because it's cheap and fault tolerant, as long as services are stateless: sessions in Redis or JWTs, files in S3. For the database I scale up and add read replicas first, and only shard when a single primary truly can't handle the write load, because sharding carries a large operational cost."*

@@@ sd-load-balancer | Load balancer hoạt động thế nào? L4 và L7 khác gì? Có những thuật toán nào? / How does a load balancer work? How do L4 and L7 differ, and what algorithms exist? | arch | scalability,load-balancer | qa | Nền tảng scale
### Tiếng Việt

**Load balancer (LB)** nhận request rồi phân phối cho nhiều instance phía sau, đồng thời **loại instance hỏng** ra khỏi vòng quay nhờ health check.

**L4 và L7:**

| | L4 (transport, TCP/UDP) | L7 (application, HTTP) |
|---|---|---|
| Nhìn thấy gì | IP và port | URL, header, cookie, method, body |
| Định tuyến | Chỉ theo kết nối | Theo nội dung: `/api/orders` sang order service, `/api/users` sang user service |
| Tốc độ | Rất nhanh, ít tốn CPU | Chậm hơn một chút vì phải đọc HTTP |
| Làm được thêm | | Kết thúc TLS, nén, rewrite, rate limit, xác thực, canary theo header |
| Ví dụ | AWS NLB, LVS | AWS ALB, Nginx, Envoy, HAProxy (mode http), Kubernetes Ingress |

**Thuật toán phân phối:**

| Thuật toán | Cách làm | Hợp khi |
|---|---|---|
| Round robin | Lần lượt từng instance | Instance giống nhau, request tốn công như nhau |
| Weighted round robin | Instance mạnh nhận nhiều hơn | Máy có cấu hình khác nhau, canary 5% |
| **Least connections / least outstanding requests** | Chọn instance đang bận ít nhất | Request có thời gian xử lý chênh lệch nhiều |
| IP hash / consistent hashing | Cùng client hoặc key luôn vào cùng instance | Cần cache cục bộ theo key, sticky session |
| Power of two choices | Chọn ngẫu nhiên 2 instance, lấy cái ít tải hơn | Cụm lớn, cân bằng tốt mà rẻ |

**Health check:**
- **Liveness:** process còn sống không. **Readiness:** đã sẵn sàng nhận request chưa (đã nối DB, đã warm cache).
- Instance lỗi liên tục N lần thì bị loại, hồi phục thì được đưa lại.
- **Connection draining:** khi deploy hoặc scale down, LB ngừng gửi request mới nhưng để request đang chạy xử lý xong.

**Chính LB có phải là điểm hỏng duy nhất không?** Có, nếu chỉ có một. Cách xử lý: LB được quản lý (ALB tự chạy ở nhiều AZ), hoặc cặp LB active-passive dùng chung virtual IP (keepalived), hoặc DNS trỏ tới nhiều LB.

**Các tầng phân phối trong thực tế:**
```
DNS (GeoDNS, Route 53) → CDN → L4/L7 LB (ALB) → Ingress hoặc API gateway → service (Kubernetes Service, client-side LB)
```

**Bên trong hệ thống microservices:** Kubernetes Service phân phối ở L4 (kube-proxy). Khi gọi gRPC, kết nối HTTP/2 tồn tại lâu nên L4 dồn hết request vào một pod: cần **LB ở L7** (Envoy, service mesh) hoặc client-side load balancing.

### English

A **load balancer (LB)** receives requests and distributes them across many instances behind it, and it **removes unhealthy instances** from rotation using health checks.

**L4 vs L7:**

| | L4 (transport, TCP/UDP) | L7 (application, HTTP) |
|---|---|---|
| What it sees | IPs and ports | URL, headers, cookies, method, body |
| Routing | By connection only | By content: `/api/orders` to the order service, `/api/users` to the user service |
| Speed | Very fast, cheap on CPU | Slightly slower because it parses HTTP |
| Extras | | TLS termination, compression, rewrites, rate limiting, authentication, header-based canaries |
| Examples | AWS NLB, LVS | AWS ALB, Nginx, Envoy, HAProxy (http mode), Kubernetes Ingress |

**Distribution algorithms:**

| Algorithm | How | Fits when |
|---|---|---|
| Round robin | Each instance in turn | Identical instances and equally expensive requests |
| Weighted round robin | Stronger instances get more | Mixed machine sizes, a 5% canary |
| **Least connections / least outstanding requests** | Picks the least busy instance | Request durations vary a lot |
| IP hash / consistent hashing | The same client or key always goes to the same instance | Per-key local caches, sticky sessions |
| Power of two choices | Pick 2 instances at random, use the less loaded one | Large clusters; good balance at low cost |

**Health checks:**
- **Liveness:** is the process alive? **Readiness:** is it ready to take requests (DB connected, cache warmed)?
- An instance failing N times in a row is removed, and added back when it recovers.
- **Connection draining:** during deploys or scale-down, the LB stops sending new requests but lets in-flight ones finish.

**Isn't the LB itself a single point of failure?** Yes, if there's only one. Fixes: a managed LB (ALB runs across several AZs automatically), an active-passive LB pair sharing a virtual IP (keepalived), or DNS pointing at several LBs.

**Distribution layers in practice:**
```
DNS (GeoDNS, Route 53) → CDN → L4/L7 LB (ALB) → Ingress or API gateway → service (Kubernetes Service, client-side LB)
```

**Inside a microservices system:** a Kubernetes Service balances at L4 (kube-proxy). With gRPC, long-lived HTTP/2 connections mean L4 sends every request to one pod: you need **L7 balancing** (Envoy, a service mesh) or client-side load balancing.

@@@ sd-availability | High availability là gì? 99,9% và 99,99% khác nhau bao nhiêu? Thiết kế thế nào để không có điểm hỏng duy nhất? / What is high availability? How different are 99.9% and 99.99%, and how do you design out single points of failure? | arch | availability,reliability | qa | Nền tảng scale
### Tiếng Việt

**Availability** là tỷ lệ thời gian hệ thống phục vụ được.

| Mức | Downtime mỗi năm | Mỗi tháng |
|---|---|---|
| 99% | khoảng 3,65 ngày | khoảng 7,3 giờ |
| 99,9% ("ba số 9") | khoảng 8,76 giờ | khoảng 43,8 phút |
| 99,99% | khoảng 52,6 phút | khoảng 4,4 phút |
| 99,999% | khoảng 5,3 phút | khoảng 26 giây |

Mỗi số 9 thêm vào **đắt hơn nhiều**: ở 99,99% thì không còn thời gian cho con người phản ứng, mọi thứ phải tự động failover.

**SLA, SLO, SLI:**
- **SLI:** chỉ số đo được, ví dụ tỷ lệ request thành công, p99 latency.
- **SLO:** mục tiêu nội bộ, ví dụ 99,9% request thành công trong 30 ngày.
- **SLA:** cam kết với khách hàng, có phạt; thường thấp hơn SLO.
- **Error budget** = 100% − SLO. Còn budget thì được deploy nhanh; hết budget thì dừng tính năng mới để tập trung vào độ ổn định.

**Availability của chuỗi phụ thuộc:** gọi nối tiếp 3 service, mỗi cái 99,9%, thì tổng chỉ còn khoảng 0,999³ ≈ **99,7%**. Muốn hệ thống đạt 99,9% thì từng thành phần phải tốt hơn, hoặc phải có fallback.

**Có dự phòng thì tăng:** hai instance độc lập, mỗi cái 99%, thì xác suất cả hai cùng chết là 0,01 × 0,01, nên tổng khoảng 99,99%. Điều kiện là chúng **hỏng độc lập**: khác máy, khác AZ, không chung một phụ thuộc.

**Cách loại bỏ điểm hỏng duy nhất (SPOF):**

| Tầng | Cách làm |
|---|---|
| Ứng dụng | ≥ 2 instance trải trên **nhiều AZ**, có health check và tự thay thế (Kubernetes, auto scaling group) |
| Load balancer | LB được quản lý chạy nhiều AZ |
| Database | Primary và standby **đồng bộ** ở AZ khác, tự failover (RDS Multi-AZ, Patroni); backup và **thử restore** định kỳ |
| Cache, broker | Redis Sentinel hoặc Cluster; Kafka `replication.factor=3`, `min.insync.replicas=2` |
| Phụ thuộc ngoài | Timeout, retry, circuit breaker, **fallback** (dữ liệu cache cũ, degrade tính năng) |
| Con người, quy trình | Deploy dần (canary, blue-green), rollback nhanh, feature flag, runbook, alert theo SLO |

**Active-passive và active-active:**
- **Active-passive:** một bên phục vụ, một bên chờ. Đơn giản, nhưng tốn tài nguyên chờ và failover mất thời gian.
- **Active-active:** mọi bên cùng phục vụ. Tận dụng tài nguyên, failover gần như tức thì, nhưng **ghi ở nhiều nơi** gây xung đột dữ liệu.

**Multi-region:** chỉ cần khi SLO rất cao hoặc yêu cầu khôi phục sau thảm họa. Phải xác định **RPO** (chấp nhận mất bao nhiêu dữ liệu) và **RTO** (mất bao lâu để khôi phục).

**Câu trả lời mẫu:** *"Tôi bắt đầu từ SLO, ví dụ 99,9%, rồi tìm từng điểm hỏng duy nhất theo đường đi của request: ít nhất 2 instance trên nhiều AZ, database có standby tự failover, Kafka replication 3. Với phụ thuộc ngoài, tôi dùng timeout, circuit breaker và fallback, vì availability của chuỗi phụ thuộc là tích của từng phần."*

### English

**Availability** is the fraction of time the system can serve requests.

| Level | Downtime per year | Per month |
|---|---|---|
| 99% | about 3.65 days | about 7.3 hours |
| 99.9% ("three nines") | about 8.76 hours | about 43.8 minutes |
| 99.99% | about 52.6 minutes | about 4.4 minutes |
| 99.999% | about 5.3 minutes | about 26 seconds |

Each extra nine **costs much more**: at 99.99% there's no time for humans to react, so everything must fail over automatically.

**SLA, SLO, SLI:**
- **SLI:** a measured indicator, for example the success rate or p99 latency.
- **SLO:** an internal target, for example 99.9% of requests succeed over 30 days.
- **SLA:** a commitment to customers, with penalties; usually lower than the SLO.
- **Error budget** = 100% − SLO. With budget left you can ship fast; when it's spent, you stop new features and focus on stability.

**Availability of a dependency chain:** calling 3 services in series, each at 99.9%, gives only about 0.999³ ≈ **99.7%** overall. For the system to reach 99.9%, each component must do better, or there must be fallbacks.

**Redundancy raises it:** two independent instances at 99% each fail together with probability 0.01 × 0.01, so together they give about 99.99%. The condition is that they **fail independently**: different machines, different AZs, no shared dependency.

**Removing single points of failure (SPOFs):**

| Tier | How |
|---|---|
| Application | ≥ 2 instances across **several AZs**, with health checks and automatic replacement (Kubernetes, auto scaling groups) |
| Load balancer | A managed LB spanning several AZs |
| Database | A **synchronous** standby in another AZ with automatic failover (RDS Multi-AZ, Patroni); backups, plus **regular restore tests** |
| Cache, broker | Redis Sentinel or Cluster; Kafka `replication.factor=3`, `min.insync.replicas=2` |
| External dependencies | Timeouts, retries, circuit breakers, **fallbacks** (stale cached data, degraded features) |
| People and process | Gradual deploys (canary, blue-green), fast rollback, feature flags, runbooks, SLO-based alerts |

**Active-passive vs active-active:**
- **Active-passive:** one side serves while the other waits. Simple, but the standby resources sit idle and failover takes time.
- **Active-active:** every side serves. Better resource use and near-instant failover, but **writes in several places** cause data conflicts.

**Multi-region:** only needed for very high SLOs or disaster-recovery requirements. You must define **RPO** (how much data loss is acceptable) and **RTO** (how long recovery may take).

**A model answer:** *"I start from the SLO, say 99.9%, and then find each single point of failure along the request path: at least 2 instances across several AZs, a database with an automatically failing-over standby, and Kafka replication of 3. For external dependencies I use timeouts, circuit breakers and fallbacks, because a chain's availability is the product of its parts."*

@@@ sd-estimation | Ước lượng dung lượng (back-of-the-envelope) làm thế nào? Những con số nào cần nhớ? / How do you do back-of-the-envelope capacity estimation, and which numbers should you remember? | arch | system-design,capacity | qa | Nền tảng scale
### Tiếng Việt

Ở phút thứ 5–10 của buổi system design, interviewer muốn thấy bạn **ước lượng được quy mô** để chọn kiến trúc. Không cần chính xác, chỉ cần đúng **bậc độ lớn**.

**Con số cần nhớ:**
- **1 ngày ≈ 86.400 giây ≈ 10⁵ giây** (làm tròn để tính nhẩm).
- **1 triệu request/ngày ≈ 12 request/giây.** 100 triệu/ngày ≈ 1.200 QPS.
- **Peak** thường gấp 2–5 lần trung bình (flash sale có thể gấp 10–100 lần).
- Độ trễ, theo bậc:

| Thao tác | Thời gian xấp xỉ |
|---|---|
| Đọc RAM | khoảng 100 ns |
| Đọc ngẫu nhiên SSD | khoảng 100 µs |
| Gọi trong cùng data center (round trip) | khoảng 0,5 ms |
| Lệnh Redis | khoảng 0,1–1 ms |
| Query DB có index | khoảng 1–10 ms |
| Round trip giữa hai châu lục | khoảng 100–150 ms |

- Năng lực tham khảo, rất phụ thuộc phần cứng và workload: một instance API Java khoảng 1.000–5.000 req/s cho request đơn giản; PostgreSQL một node khoảng vài nghìn đến hàng chục nghìn truy vấn đơn giản mỗi giây; Redis khoảng 100.000 lệnh/giây mỗi node; một partition Kafka khoảng 10 MB/s.

**Ví dụ: URL shortener, 100 triệu URL mới mỗi tháng, tỷ lệ đọc:ghi là 100:1.**

| Bước | Tính | Kết quả |
|---|---|---|
| Ghi/giây | 100M / (30 × 10⁵) | khoảng **40 ghi/s**, peak khoảng 200 |
| Đọc/giây | 40 × 100 | khoảng **4.000 đọc/s**, peak khoảng 20.000 |
| Dung lượng mỗi bản ghi | URL khoảng 500 byte + metadata | khoảng 1 KB |
| Lưu trữ 5 năm | 100M × 12 × 5 × 1 KB | khoảng **6 TB** |
| Cache 20% URL nóng của một ngày | 4.000 × 10⁵ × 20% × 1 KB | khoảng **80 GB** RAM |

**Rút ra kết luận kiến trúc** (đây mới là phần ghi điểm):
- 40 ghi/s rất nhỏ: một PostgreSQL primary là đủ, **không cần sharding**.
- 20.000 đọc/s lúc peak: cần **cache Redis** phía trước, cộng vài instance API scale ngang.
- 6 TB trong 5 năm: một node lưu được, nhưng nên partition theo thời gian hoặc tính trước việc chia sau này.
- Mã ngắn: 62⁷ ≈ 3,5 nghìn tỷ tổ hợp, dư cho 6 tỷ URL.

**Mẹo:** nói to giả định ("tôi giả sử..."), làm tròn mạnh tay, và **luôn kết thúc bằng một quyết định thiết kế** rút ra từ con số.

### English

Around minutes 5–10 of a system design interview, the interviewer wants to see that you can **estimate the scale** to choose an architecture. Precision doesn't matter; the **order of magnitude** does.

**Numbers to remember:**
- **1 day ≈ 86,400 seconds ≈ 10⁵ seconds** (rounded for mental math).
- **1 million requests/day ≈ 12 requests/second.** 100 million/day ≈ 1,200 QPS.
- **Peak** is usually 2–5× the average (a flash sale can be 10–100×).
- Latencies, by order of magnitude:

| Operation | Approximate time |
|---|---|
| RAM read | about 100 ns |
| SSD random read | about 100 µs |
| Round trip within a data center | about 0.5 ms |
| Redis command | about 0.1–1 ms |
| Indexed DB query | about 1–10 ms |
| Intercontinental round trip | about 100–150 ms |

- Reference capacities, highly dependent on hardware and workload: one Java API instance handles about 1,000–5,000 req/s for simple requests; a single PostgreSQL node handles a few thousand to tens of thousands of simple queries per second; Redis about 100,000 commands/second per node; one Kafka partition about 10 MB/s.

**Example: a URL shortener with 100 million new URLs a month and a 100:1 read-to-write ratio.**

| Step | Calculation | Result |
|---|---|---|
| Writes/second | 100M / (30 × 10⁵) | about **40 writes/s**, peak about 200 |
| Reads/second | 40 × 100 | about **4,000 reads/s**, peak about 20,000 |
| Size per record | URL about 500 bytes + metadata | about 1 KB |
| Storage for 5 years | 100M × 12 × 5 × 1 KB | about **6 TB** |
| Cache for the hottest 20% of a day | 4,000 × 10⁵ × 20% × 1 KB | about **80 GB** of RAM |

**Draw architectural conclusions** (this is what earns the points):
- 40 writes/s is tiny: one PostgreSQL primary is enough, **no sharding needed**.
- 20,000 reads/s at peak: put a **Redis cache** in front, plus a few horizontally scaled API instances.
- 6 TB over 5 years: one node can hold it, but partition by time or plan for splitting later.
- Short codes: 62⁷ ≈ 3.5 trillion combinations, plenty for 6 billion URLs.

**Tip:** state your assumptions out loud ("I'll assume..."), round aggressively, and **always end with a design decision** drawn from the numbers.

@@@ sd-autoscaling | Autoscaling hoạt động thế nào? Scale theo chỉ số gì, và có những bẫy nào? / How does autoscaling work, which metrics should drive it, and what are the pitfalls? | arch | scalability,kubernetes,autoscaling | qa | Nền tảng scale
### Tiếng Việt

**Các loại autoscaling:**

| Loại | Làm gì | Ví dụ |
|---|---|---|
| **Ngang theo pod hoặc instance** | Thêm hoặc bớt bản sao | Kubernetes **HPA**, AWS Auto Scaling Group |
| **Dọc theo pod** | Tăng hoặc giảm CPU và RAM request của pod | Kubernetes **VPA** (thường chỉ dùng để gợi ý cấu hình) |
| **Theo node** | Thêm máy khi pod không còn chỗ chạy | Cluster Autoscaler, **Karpenter** |
| **Theo sự kiện** | Scale theo độ dài hàng đợi, kể cả về 0 | **KEDA** (Kafka consumer lag, độ dài hàng đợi SQS hay RabbitMQ) |

**HPA:** `số pod mong muốn = ceil(số pod hiện tại × giá trị đo / giá trị mục tiêu)`. Ví dụ 4 pod, CPU trung bình 90%, mục tiêu 60%, thì cần ceil(4 × 90 / 60) = 6 pod.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef: { kind: Deployment, name: order-service }
  minReplicas: 3            # ≥ 2 để chịu lỗi, trải trên nhiều AZ
  maxReplicas: 30           # chặn trên để bảo vệ DB và chi phí
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 60 } }
  behavior:
    scaleDown: { stabilizationWindowSeconds: 300 }   # giảm chậm để tránh dao động
```

**Chọn chỉ số nào:**
- **CPU:** hợp với service nặng CPU. Service Java nặng I/O có thể chậm mà CPU vẫn thấp.
- **Request/giây mỗi pod** hoặc **latency:** sát với trải nghiệm người dùng hơn (cần Prometheus Adapter).
- **Consumer lag hoặc độ dài hàng đợi:** đúng cho worker xử lý message (KEDA). Lưu ý số consumer Kafka hiệu quả **không vượt quá số partition**.
- **Memory:** ít khi dùng để scale, vì JVM không trả lại bộ nhớ ngay nên dễ scale lên mà không scale xuống.

**Bẫy:**
1. **Scale chậm hơn tải tăng:** HPA đo mỗi 15 giây, cộng thời gian tạo node, kéo image, **JVM khởi động và warm-up**, có thể mất vài phút. Giải pháp: `minReplicas` đủ cao, **scale theo lịch** trước sự kiện biết trước (flash sale, 9 giờ sáng), giữ sẵn node dự phòng, khởi động nhanh hơn (CDS, AOT cache, image nhỏ).
2. **Thiếu `requests` CPU trong pod spec** thì HPA tính phần trăm CPU sai.
3. **Dao động lên xuống liên tục (flapping):** dùng `stabilizationWindowSeconds` và scale down chậm.
4. **Đẩy nghẽn xuống tầng dưới:** 30 pod × pool 20 kết nối = 600 kết nối vào PostgreSQL, có thể vượt `max_connections`. Cần PgBouncer, đặt `maxReplicas` hợp lý và giới hạn đồng thời.
5. **Readiness probe sai** thì pod mới nhận traffic khi chưa sẵn sàng, gây lỗi hàng loạt đúng lúc đang cần scale.
6. **Scale down làm đứt request đang chạy:** cần graceful shutdown (`server.shutdown=graceful` trong Spring), `preStop` hook và connection draining.

### English

**Types of autoscaling:**

| Type | What it does | Examples |
|---|---|---|
| **Horizontal, pods or instances** | Adds or removes replicas | Kubernetes **HPA**, AWS Auto Scaling Groups |
| **Vertical, pods** | Raises or lowers a pod's CPU and memory requests | Kubernetes **VPA** (often used only for recommendations) |
| **Nodes** | Adds machines when pods have nowhere to run | Cluster Autoscaler, **Karpenter** |
| **Event-driven** | Scales on queue length, including down to zero | **KEDA** (Kafka consumer lag, SQS or RabbitMQ queue length) |

**HPA:** `desired pods = ceil(current pods × measured value / target value)`. For example, 4 pods at 90% average CPU with a 60% target need ceil(4 × 90 / 60) = 6 pods.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef: { kind: Deployment, name: order-service }
  minReplicas: 3            # ≥ 2 for fault tolerance, spread across AZs
  maxReplicas: 30           # an upper bound protects the DB and the bill
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 60 } }
  behavior:
    scaleDown: { stabilizationWindowSeconds: 300 }   # scale down slowly to avoid oscillation
```

**Which metric to use:**
- **CPU:** suits CPU-bound services. An I/O-bound Java service can be slow while CPU stays low.
- **Requests per second per pod** or **latency:** closer to user experience (needs a Prometheus Adapter).
- **Consumer lag or queue length:** right for message workers (KEDA). Note that the number of useful Kafka consumers **can't exceed the partition count**.
- **Memory:** rarely used for scaling, because the JVM doesn't release memory promptly, so it tends to scale up without scaling down.

**Pitfalls:**
1. **Scaling lags behind rising load:** HPA samples every 15 seconds, plus node creation, image pulls, and **JVM startup and warm-up**, which can add up to minutes. Fixes: a high enough `minReplicas`, **scheduled scaling** ahead of known events (a flash sale, 9 a.m.), spare node capacity, faster startup (CDS, AOT cache, smaller images).
2. **Missing CPU `requests` in the pod spec** make the HPA's CPU percentage meaningless.
3. **Flapping up and down:** use `stabilizationWindowSeconds` and scale down slowly.
4. **Pushing the bottleneck downstream:** 30 pods × a pool of 20 connections = 600 connections to PostgreSQL, which can exceed `max_connections`. You need PgBouncer, a sensible `maxReplicas` and concurrency limits.
5. **A wrong readiness probe** sends traffic to new pods before they're ready, causing mass errors exactly when you need to scale.
6. **Scale-down cuts in-flight requests:** you need graceful shutdown (`server.shutdown=graceful` in Spring), a `preStop` hook and connection draining.

@@@ sd-queue-backpressure | Dùng hàng đợi để chịu tải đột biến thế nào? Backpressure là gì? / How do you use queues to absorb load spikes, and what is backpressure? | arch | scalability,messaging,backpressure | qa | Nền tảng scale
### Tiếng Việt

**Load leveling (san phẳng tải):** thay vì xử lý mọi việc trong request, API **nhận yêu cầu, ghi vào hàng đợi, trả 202 Accepted ngay**. Worker phía sau xử lý với tốc độ **ổn định mà hệ thống chịu được**. Tải đột biến được hàng đợi "hấp thụ" thay vì làm sập database.

```
Client → API (validate, ghi vào Kafka, trả 202 + requestId)
                │
                ▼
         Kafka topic  ──►  worker × N (tốc độ cố định) ──► DB, dịch vụ ngoài
                                    │
Client hỏi trạng thái (GET /requests/{id}) hoặc nhận webhook / thông báo khi xong
```

**Hợp với:** gửi email hoặc thông báo, tạo báo cáo, xử lý ảnh và video, import file, đồng bộ với hệ thống bên thứ ba, ghi log hoặc sự kiện analytics.
**Không hợp với:** việc người dùng cần kết quả ngay và nhất quán ngay (kiểm tra số dư khi thanh toán).

**Lợi ích:**
- Tách producer khỏi consumer: worker chết thì message vẫn còn trong hàng đợi.
- Scale worker độc lập theo độ dài hàng đợi (KEDA).
- Retry tự nhiên, có DLQ cho message lỗi.

**Backpressure:** cơ chế để phía chậm **báo cho phía nhanh giảm tốc**, thay vì để hàng đợi phình vô hạn rồi hết bộ nhớ.

| Cách | Ví dụ |
|---|---|
| **Hàng đợi có giới hạn, từ chối khi đầy** | `ThreadPoolExecutor` với `ArrayBlockingQueue(1000)`; đầy thì trả **429** hoặc **503** kèm `Retry-After` |
| **Kéo (pull) thay vì đẩy (push)** | Kafka consumer tự `poll` theo khả năng; RabbitMQ dùng `prefetch` (QoS) để giới hạn số message chưa ack |
| **Giới hạn đồng thời** | `Semaphore`, bulkhead của Resilience4j, `@ConcurrencyLimit` (Spring 7) |
| **Reactive Streams** | Subscriber yêu cầu `request(n)` (Project Reactor, WebFlux) |
| **Rate limiting ở cổng vào** | API gateway giới hạn theo user hoặc API key |
| **Load shedding** | Quá tải thì bỏ bớt request ít quan trọng trước (analytics), giữ request quan trọng (thanh toán) |

**Giám sát:** độ dài hàng đợi, **consumer lag**, tuổi của message cũ nhất. Lag tăng liên tục nghĩa là tốc độ xử lý thấp hơn tốc độ đến, cần thêm worker (và partition) hoặc tối ưu xử lý.

**Câu trả lời mẫu:** *"Với việc không cần kết quả ngay, tôi trả 202 và đẩy vào Kafka, để worker xử lý ở tốc độ database chịu được, scale worker theo consumer lag. Ở mọi chỗ có hàng đợi tôi đặt giới hạn: hàng đợi bị chặn trên, đầy thì trả 429 hoặc 503, để quá tải biến thành phản hồi có kiểm soát thay vì sập dây chuyền."*

### English

**Load leveling:** instead of doing all the work inside the request, the API **accepts the request, writes it to a queue, and immediately returns 202 Accepted**. Workers behind it process at a **steady rate the system can handle**. The queue "absorbs" spikes instead of letting them take down the database.

```
Client → API (validate, write to Kafka, return 202 + requestId)
                │
                ▼
         Kafka topic  ──►  workers × N (steady rate) ──► DB, external services
                                    │
Client polls the status (GET /requests/{id}) or gets a webhook / notification when done
```

**Fits:** sending emails or notifications, generating reports, image and video processing, file imports, syncing with third-party systems, logging or analytics events.
**Doesn't fit:** work where the user needs an immediate, consistent result (checking the balance during payment).

**Benefits:**
- Decouples producers from consumers: if workers die, messages stay in the queue.
- Workers scale independently on queue length (KEDA).
- Natural retries, with a DLQ for failing messages.

**Backpressure:** a mechanism for the slow side to **tell the fast side to slow down**, instead of letting a queue grow without bound until memory runs out.

| Approach | Example |
|---|---|
| **Bounded queues that reject when full** | A `ThreadPoolExecutor` with `ArrayBlockingQueue(1000)`; when full, return **429** or **503** with `Retry-After` |
| **Pull instead of push** | Kafka consumers `poll` at their own pace; RabbitMQ uses `prefetch` (QoS) to cap unacknowledged messages |
| **Concurrency limits** | A `Semaphore`, a Resilience4j bulkhead, `@ConcurrencyLimit` (Spring 7) |
| **Reactive Streams** | The subscriber signals `request(n)` (Project Reactor, WebFlux) |
| **Rate limiting at the edge** | The API gateway limits per user or API key |
| **Load shedding** | Under overload, drop less important requests first (analytics) and keep important ones (payments) |

**Monitoring:** queue length, **consumer lag**, and the age of the oldest message. Steadily growing lag means processing is slower than arrivals, so you need more workers (and partitions) or faster processing.

**A model answer:** *"For work that doesn't need an immediate result, I return 202 and push to Kafka, so workers process at a pace the database can handle, scaling workers on consumer lag. Every queue I use is bounded: when it's full I return 429 or 503, so overload becomes a controlled response instead of a cascading failure."*

@@@ sd-bottleneck | Hệ thống chậm khi tải tăng: bạn tìm và xử lý điểm nghẽn thế nào? / The system slows down under load: how do you find and fix the bottleneck? | arch | performance,scalability,troubleshooting | qa | Nền tảng scale
### Tiếng Việt

**Nguyên tắc: đo trước, sửa sau.** Không đoán, không scale bừa: thêm pod khi điểm nghẽn là database chỉ làm database chết nhanh hơn.

**Bước 1: Xác định triệu chứng bằng số liệu.**
- **RED** cho từng service: **R**ate (request/s), **E**rrors (tỷ lệ lỗi), **D**uration (p50, p95, **p99**). Nhìn p99 chứ không nhìn trung bình, vì trung bình che mất những request chậm.
- **USE** cho tài nguyên: **U**tilization, **S**aturation (hàng đợi, thread chờ), **E**rrors. Áp dụng cho CPU, RAM, disk, mạng, connection pool.
- Chậm từ lúc nào? Trùng với deploy, thay đổi cấu hình hay tăng traffic?

**Bước 2: Khoanh vùng bằng distributed tracing** (Jaeger, Tempo, Zipkin). Mở trace của một request chậm để biết thời gian nằm ở span nào: service A, query SQL, hay lời gọi HTTP ra ngoài.

**Bước 3: Kiểm tra các điểm nghẽn hay gặp, theo thứ tự:**

| Nơi | Dấu hiệu | Cách xử lý |
|---|---|---|
| **Database** | Query chậm trong `pg_stat_statements`, CPU DB cao, lock wait | `EXPLAIN ANALYZE`, thêm index, sửa **N+1** (JPA `JOIN FETCH`, `@EntityGraph`), phân trang theo keyset, cache, read replica |
| **Connection pool** | Thread chờ lấy kết nối, HikariCP `pending` > 0, lỗi `Connection is not available` | Transaction ngắn lại (không gọi HTTP trong transaction), tăng pool ở mức hợp lý, thêm PgBouncer |
| **Thread pool** | Tomcat hết thread, request xếp hàng | Tìm lời gọi blocking chậm; đặt timeout; dùng virtual threads; thêm bulkhead |
| **Gọi ra ngoài** | Span HTTP dài | **Timeout**, circuit breaker, cache, gọi song song, chuyển sang bất đồng bộ |
| **JVM** | GC pause dài, heap gần đầy | GC log, heap dump (`jcmd`), sửa rò rỉ bộ nhớ, chỉnh heap, chuyển G1 hoặc ZGC |
| **CPU** | CPU 100% | Profile bằng async-profiler hoặc JFR, xem flame graph: serialize JSON, regex, log quá nhiều, vòng lặp nặng |
| **Lock và tranh chấp** | Thread `BLOCKED` trong thread dump, row lock trong DB | Giảm phạm vi khóa, tránh hot row (ví dụ một dòng bộ đếm), dùng atomic update |

**Bước 4: Sửa điểm nghẽn lớn nhất, đo lại, lặp lại.** Gỡ một điểm nghẽn thì điểm nghẽn tiếp theo sẽ lộ ra.

**Bước 5: Ngăn tái diễn.** Load test (k6, Gatling) trong pipeline trước sự kiện lớn, alert theo SLO, và dashboard cho connection pool, GC, consumer lag.

**Câu chuyện mẫu (thay bằng chuyện thật của bạn):** *"API danh sách thiết bị tăng p99 từ 200 ms lên 3 giây khi số khách hàng tăng. Trace cho thấy 90% thời gian nằm trong DB; `pg_stat_statements` chỉ ra một query N+1 do lazy loading. Tôi đổi sang `JOIN FETCH`, thêm composite index, và phân trang theo keyset. p99 về lại khoảng 150 ms, CPU DB giảm từ 80% xuống 25%."*

### English

**Principle: measure first, fix second.** Don't guess and don't scale blindly: adding pods when the bottleneck is the database just kills the database faster.

**Step 1: Pin down the symptom with data.**
- **RED** for each service: **R**ate (requests/s), **E**rrors (error rate), **D**uration (p50, p95, **p99**). Look at p99, not the average, because averages hide slow requests.
- **USE** for resources: **U**tilization, **S**aturation (queues, waiting threads), **E**rrors. Apply it to CPU, memory, disk, network and connection pools.
- When did it start? Does it line up with a deploy, a config change or a traffic increase?

**Step 2: Narrow it down with distributed tracing** (Jaeger, Tempo, Zipkin). Open the trace of a slow request to see which span holds the time: service A, an SQL query, or an outbound HTTP call.

**Step 3: Check the usual bottlenecks, in order:**

| Where | Signs | Fixes |
|---|---|---|
| **Database** | Slow queries in `pg_stat_statements`, high DB CPU, lock waits | `EXPLAIN ANALYZE`, add indexes, fix **N+1** (JPA `JOIN FETCH`, `@EntityGraph`), keyset pagination, caching, read replicas |
| **Connection pool** | Threads waiting for connections, HikariCP `pending` > 0, `Connection is not available` errors | Shorter transactions (no HTTP calls inside a transaction), a sensibly larger pool, add PgBouncer |
| **Thread pool** | Tomcat runs out of threads, requests queue up | Find slow blocking calls; set timeouts; use virtual threads; add bulkheads |
| **Outbound calls** | Long HTTP spans | **Timeouts**, circuit breakers, caching, parallel calls, moving to asynchronous processing |
| **JVM** | Long GC pauses, heap nearly full | GC logs, heap dumps (`jcmd`), fix memory leaks, tune the heap, switch to G1 or ZGC |
| **CPU** | CPU at 100% | Profile with async-profiler or JFR and read the flame graph: JSON serialization, regexes, excessive logging, heavy loops |
| **Locks and contention** | `BLOCKED` threads in a thread dump, row locks in the DB | Narrow lock scope, avoid hot rows (for example a single counter row), use atomic updates |

**Step 4: Fix the biggest bottleneck, measure again, repeat.** Removing one bottleneck exposes the next.

**Step 5: Prevent recurrence.** Load tests (k6, Gatling) in the pipeline before big events, SLO-based alerts, and dashboards for connection pools, GC and consumer lag.

**A sample story (replace it with your real one):** *"The device-list API's p99 went from 200 ms to 3 seconds as the customer count grew. Tracing showed 90% of the time in the database; `pg_stat_statements` pointed to an N+1 query caused by lazy loading. I switched to `JOIN FETCH`, added a composite index and moved to keyset pagination. p99 went back to about 150 ms and DB CPU dropped from 80% to 25%."*
