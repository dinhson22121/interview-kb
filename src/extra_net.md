@@@ net-osi | Mô hình OSI có mấy tầng? Mỗi tầng làm gì? Backend engineer cần quan tâm tầng nào? / What are the layers of the OSI model, what does each do, and which matter to a backend engineer? | network | osi,networking | qa | Networking
### Tiếng Việt

**OSI** là mô hình khái niệm chia việc truyền dữ liệu qua mạng thành **7 tầng**, mỗi tầng chỉ dùng dịch vụ của tầng ngay dưới và phục vụ tầng ngay trên. Thực tế Internet chạy theo **mô hình TCP/IP 4 tầng**, nhưng OSI vẫn được dùng để **nói chuyện và khoanh vùng lỗi** ("lỗi ở L4 hay L7?").

| # | Tầng OSI | Làm gì | Đơn vị dữ liệu | Ví dụ giao thức, thiết bị | TCP/IP |
|---|---|---|---|---|---|
| 7 | **Application** | Giao thức mà ứng dụng dùng | Data / message | **HTTP, gRPC, DNS, SMTP, WebSocket, MQTT** | Application |
| 6 | Presentation | Định dạng, mã hóa, nén | | TLS (thường xếp ở đây hoặc giữa 4 và 7), JSON, protobuf, gzip | Application |
| 5 | Session | Mở, duy trì, đóng phiên | | Phiên TLS, RPC session | Application |
| 4 | **Transport** | Truyền giữa hai **process** (theo **port**): tin cậy, thứ tự, kiểm soát luồng | **Segment** (TCP) / datagram (UDP) | **TCP, UDP, QUIC** | Transport |
| 3 | **Network** | Định tuyến giữa các mạng theo **địa chỉ IP** | **Packet** | IP, ICMP (ping), router | Internet |
| 2 | Data link | Truyền trong một mạng cục bộ theo **địa chỉ MAC** | Frame | Ethernet, Wi-Fi, ARP, switch, VLAN | Link |
| 1 | Physical | Tín hiệu điện, quang, sóng | Bit | Cáp, cáp quang, hub | Link |

Mẹo nhớ từ tầng 1 lên 7: **"Please Do Not Throw Sausage Pizza Away"**.

**Đóng gói (encapsulation):** khi gửi, dữ liệu đi **từ trên xuống**, mỗi tầng **thêm header** của mình: HTTP request được bọc trong TCP segment (port), rồi IP packet (IP), rồi Ethernet frame (MAC). Khi nhận, dữ liệu đi từ dưới lên và từng tầng bóc header ra.

**Backend engineer cần quan tâm:**
- **L7:** HTTP method, status, header, cookie, REST, gRPC, DNS. Hầu hết công việc hằng ngày.
- **L4:** TCP và UDP, port, connection pool, keep-alive, timeout, số kết nối tối đa, `TIME_WAIT`.
- **L3:** IP, subnet, CIDR (`10.0.0.0/16`), routing, VPC, NAT. Cần khi làm cloud và Kubernetes.
- **L2, L1:** hầu như không, trừ khi làm hạ tầng.

**Vì sao interviewer hỏi OSI:** để xem bạn phân biệt được các khái niệm hay dùng:
- **Load balancer L4 và L7:** L4 chỉ thấy IP và port; L7 đọc được URL, header nên định tuyến theo path được. Xem [Load balancer](#sd-load-balancer).
- **Firewall L3/L4** (Security Group chặn theo IP, port) và **WAF L7** (chặn SQL injection trong nội dung HTTP).
- **Khoanh vùng lỗi:** `ping` không được thì nghi L3; `telnet host 5432` hoặc `nc -vz` không mở được kết nối thì nghi L4 (port đóng, firewall); kết nối được mà trả 502 hay 401 thì là L7.

### English

**OSI** is a conceptual model that splits network communication into **7 layers**; each layer uses the services of the one below and serves the one above. The real Internet runs on the **4-layer TCP/IP model**, but OSI is still used to **talk about and isolate problems** ("is this an L4 or L7 issue?").

| # | OSI layer | What it does | Data unit | Example protocols, devices | TCP/IP |
|---|---|---|---|---|---|
| 7 | **Application** | The protocols applications use | Data / message | **HTTP, gRPC, DNS, SMTP, WebSocket, MQTT** | Application |
| 6 | Presentation | Formatting, encryption, compression | | TLS (usually placed here or between 4 and 7), JSON, protobuf, gzip | Application |
| 5 | Session | Opening, maintaining and closing sessions | | TLS sessions, RPC sessions | Application |
| 4 | **Transport** | Delivery between two **processes** (by **port**): reliability, ordering, flow control | **Segment** (TCP) / datagram (UDP) | **TCP, UDP, QUIC** | Transport |
| 3 | **Network** | Routing between networks by **IP address** | **Packet** | IP, ICMP (ping), routers | Internet |
| 2 | Data link | Delivery within a local network by **MAC address** | Frame | Ethernet, Wi-Fi, ARP, switches, VLANs | Link |
| 1 | Physical | Electrical, optical or radio signals | Bit | Cables, fibre, hubs | Link |

A mnemonic from layer 1 up to 7: **"Please Do Not Throw Sausage Pizza Away"**.

**Encapsulation:** when sending, data travels **top-down** and each layer **adds its own header**: the HTTP request is wrapped in a TCP segment (ports), then an IP packet (IPs), then an Ethernet frame (MACs). When receiving, data travels bottom-up and each layer strips its header.

**What a backend engineer should care about:**
- **L7:** HTTP methods, statuses, headers, cookies, REST, gRPC, DNS. Most daily work.
- **L4:** TCP and UDP, ports, connection pools, keep-alive, timeouts, connection limits, `TIME_WAIT`.
- **L3:** IP, subnets, CIDR (`10.0.0.0/16`), routing, VPCs, NAT. Needed for cloud and Kubernetes.
- **L2, L1:** rarely, unless you work on infrastructure.

**Why interviewers ask about OSI:** to see whether you can distinguish commonly used concepts:
- **L4 vs L7 load balancers:** L4 sees only IPs and ports; L7 reads URLs and headers, so it can route by path. See [Load balancer](#sd-load-balancer).
- **L3/L4 firewalls** (Security Groups block by IP and port) vs **L7 WAFs** (block SQL injection inside HTTP content).
- **Isolating failures:** if `ping` fails, suspect L3; if `telnet host 5432` or `nc -vz` can't open a connection, suspect L4 (closed port, firewall); if it connects but returns 502 or 401, it's L7.

@@@ net-tcp-udp | TCP và UDP khác nhau thế nào? Bắt tay 3 bước, đóng kết nối, TIME_WAIT là gì? / How do TCP and UDP differ? What are the three-way handshake, connection teardown and TIME_WAIT? | network | tcp,udp,networking | qa | Networking
### Tiếng Việt

| | **TCP** | **UDP** |
|---|---|---|
| Kết nối | **Có** (bắt tay trước khi gửi) | **Không**, gửi luôn |
| Tin cậy | Đảm bảo tới nơi: ACK, gửi lại khi mất | Không đảm bảo, có thể mất |
| Thứ tự | Đảm bảo đúng thứ tự | Có thể đến sai thứ tự |
| Kiểm soát luồng, tắc nghẽn | Có (sliding window, congestion control) | Không |
| Header | 20+ byte | 8 byte |
| Độ trễ | Cao hơn (bắt tay, chờ gửi lại) | Thấp |
| Dùng cho | HTTP/1.1, HTTP/2, database, SSH, email, Kafka | DNS, video call, game, streaming trực tiếp, **QUIC (HTTP/3)**, metrics (StatsD) |

**Bắt tay 3 bước (mở kết nối):**
```
Client ── SYN (seq=x) ──────────────► Server
Client ◄─ SYN-ACK (seq=y, ack=x+1) ── Server
Client ── ACK (ack=y+1) ────────────► Server    → kết nối ESTABLISHED
```
Mất **1 round trip** trước khi gửi được dữ liệu; cộng thêm TLS handshake. Vì vậy **tái sử dụng kết nối** (keep-alive, connection pool) rất quan trọng: tạo kết nối mới cho mỗi request tới service ở xa có thể tốn hàng chục đến hàng trăm ms.

**Đóng kết nối (4 bước):** FIN, ACK, FIN, ACK. Bên **chủ động đóng** rơi vào trạng thái **`TIME_WAIT`** khoảng 2 × MSL (thường 60 giây trên Linux) để đảm bảo gói cuối không bị lạc sang kết nối mới.

**Vấn đề thực tế hay gặp:**
- **Quá nhiều `TIME_WAIT`:** service mở rồi đóng kết nối liên tục (không dùng pool) thì cạn **ephemeral port**, lỗi "Cannot assign requested address". Sửa: dùng connection pool, HTTP keep-alive.
- **Connection reset / broken pipe:** một bên (thường là load balancer hoặc NAT) đóng kết nối idle trong khi pool phía mình vẫn nghĩ còn sống. Sửa: đặt idle timeout của pool **ngắn hơn** của LB, bật validation hoặc keep-alive. HikariCP có `maxLifetime` và `keepaliveTime` cho việc này.
- **Connect timeout và read timeout:** connect timeout là thời gian chờ bắt tay (nên ngắn, 1–3 giây); read timeout là thời gian chờ dữ liệu trả về (tùy API). Thiếu timeout thì thread bị treo.
- **Head-of-line blocking:** TCP giao dữ liệu đúng thứ tự, nên một gói mất làm mọi dữ liệu phía sau phải chờ. Đây là lý do HTTP/3 chuyển sang QUIC trên UDP.

**Khi nào chọn UDP:** khi dữ liệu cũ không còn giá trị (video, giọng nói, vị trí trong game), cần độ trễ thấp nhất, hoặc gửi nhiều gói nhỏ và chấp nhận mất vài gói (metrics). Nếu cần tin cậy trên UDP thì ứng dụng tự xây (như QUIC làm).

### English

| | **TCP** | **UDP** |
|---|---|---|
| Connection | **Yes** (a handshake before sending) | **No**, just send |
| Reliability | Guaranteed delivery: ACKs and retransmission | Not guaranteed; packets can be lost |
| Ordering | Guaranteed order | Can arrive out of order |
| Flow and congestion control | Yes (sliding window, congestion control) | No |
| Header | 20+ bytes | 8 bytes |
| Latency | Higher (handshake, waiting for retransmits) | Low |
| Used for | HTTP/1.1, HTTP/2, databases, SSH, email, Kafka | DNS, video calls, games, live streaming, **QUIC (HTTP/3)**, metrics (StatsD) |

**The three-way handshake (opening a connection):**
```
Client ── SYN (seq=x) ──────────────► Server
Client ◄─ SYN-ACK (seq=y, ack=x+1) ── Server
Client ── ACK (ack=y+1) ────────────► Server    → connection ESTABLISHED
```
It costs **1 round trip** before data can flow, plus the TLS handshake. That's why **connection reuse** (keep-alive, connection pools) matters so much: opening a new connection per request to a distant service can cost tens to hundreds of ms.

**Closing a connection (4 steps):** FIN, ACK, FIN, ACK. The side that **closes first** enters **`TIME_WAIT`** for about 2 × MSL (often 60 seconds on Linux) to make sure late packets don't leak into a new connection.

**Common real-world problems:**
- **Too many `TIME_WAIT` sockets:** a service that keeps opening and closing connections (no pooling) exhausts **ephemeral ports**, giving "Cannot assign requested address". Fix: connection pools, HTTP keep-alive.
- **Connection reset / broken pipe:** one side (often a load balancer or NAT) closes an idle connection while your pool still thinks it's alive. Fix: set the pool's idle timeout **shorter** than the LB's, enable validation or keep-alive. HikariCP has `maxLifetime` and `keepaliveTime` for this.
- **Connect vs read timeouts:** the connect timeout covers the handshake (keep it short, 1–3 seconds); the read timeout covers waiting for the response (depends on the API). Missing timeouts leave threads hanging.
- **Head-of-line blocking:** TCP delivers data in order, so one lost packet makes everything behind it wait. That's why HTTP/3 moved to QUIC over UDP.

**When to choose UDP:** when stale data is worthless (video, voice, game positions), when you need the lowest latency, or when sending many small packets where losing a few is fine (metrics). If you need reliability over UDP, the application builds it (as QUIC does).

@@@ net-http-versions | HTTP/1.1, HTTP/2 và HTTP/3 khác nhau thế nào? HTTPS và TLS handshake hoạt động ra sao? / How do HTTP/1.1, HTTP/2 and HTTP/3 differ, and how do HTTPS and the TLS handshake work? | network | http,tls,networking | qa | Networking
### Tiếng Việt

| | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Transport | TCP | TCP | **QUIC trên UDP** |
| Định dạng | Text | **Nhị phân** (frame) | Nhị phân |
| Nhiều request trên 1 kết nối | Lần lượt (keep-alive); trình duyệt mở khoảng 6 kết nối song song | **Multiplexing**: nhiều stream song song trên 1 kết nối | Multiplexing, stream độc lập |
| Head-of-line blocking | Ở tầng HTTP | Hết ở tầng HTTP, **vẫn còn ở tầng TCP** | **Không còn** (mỗi stream độc lập) |
| Nén header | Không | HPACK | QPACK |
| Bắt tay | TCP + TLS (2–3 round trip) | TCP + TLS | **QUIC gộp transport và TLS 1.3: 1 round trip**, 0-RTT khi kết nối lại |
| Đổi mạng (Wi-Fi sang 4G) | Mất kết nối | Mất kết nối | **Giữ được kết nối** (connection ID) |

**Ý nghĩa với backend:**
- **gRPC chạy trên HTTP/2:** multiplexing và streaming. Kết nối HTTP/2 sống lâu nên load balancer L4 dồn hết request vào một pod; cần LB L7 hoặc client-side balancing.
- HTTP/3 giúp nhiều nhất cho **mobile và mạng chập chờn**; thường được bật ở CDN hoặc load balancer, service nội bộ vẫn dùng HTTP/1.1 hoặc HTTP/2. Java `HttpClient` hỗ trợ HTTP/3 từ Java 26.

**HTTPS = HTTP chạy trên TLS.** TLS cung cấp: **mã hóa** (không đọc trộm được), **toàn vẹn** (không sửa được), **xác thực** (đúng là server đó, nhờ chứng chỉ).

**TLS 1.3 handshake (rút gọn):**
```
Client ── ClientHello: phiên bản, cipher hỗ trợ, key share (ECDHE) ──────► Server
Client ◄─ ServerHello: cipher đã chọn, key share; Certificate; Finished ── Server
     (client kiểm tra chứng chỉ: do CA tin cậy ký? đúng tên miền? còn hạn?)
Client ── Finished ─────────────────────────────────────────────────────► Server
        → hai bên tự tính ra cùng một khóa phiên (đối xứng) từ trao đổi ECDHE
```
- **Mã hóa bất đối xứng** (ECDHE, chữ ký RSA/ECDSA) chỉ dùng lúc bắt tay để trao khóa và xác thực; dữ liệu sau đó mã hóa **đối xứng** (AES-GCM, ChaCha20) vì nhanh hơn nhiều.
- **Forward secrecy:** khóa phiên tạm thời, nên lộ private key của server sau này cũng không giải mã được lưu lượng cũ.
- TLS 1.3 mất **1 round trip** (TLS 1.2 mất 2).

**Thực tế vận hành:**
- **TLS termination** ở load balancer hoặc ingress; nội bộ có thể dùng HTTP thường hoặc **mTLS** (service mesh) theo yêu cầu bảo mật. Xem [mTLS](#sec-mtls).
- Chứng chỉ hết hạn là nguyên nhân sự cố rất phổ biến: tự động gia hạn (Let's Encrypt, cert-manager, ACM) và cảnh báo trước khi hết hạn.
- **HSTS** để trình duyệt luôn dùng HTTPS.

### English

| | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Transport | TCP | TCP | **QUIC over UDP** |
| Format | Text | **Binary** (frames) | Binary |
| Several requests on one connection | One after another (keep-alive); browsers open about 6 parallel connections | **Multiplexing**: many parallel streams on one connection | Multiplexing, independent streams |
| Head-of-line blocking | At the HTTP layer | Gone at the HTTP layer, **still present at the TCP layer** | **Gone** (each stream is independent) |
| Header compression | No | HPACK | QPACK |
| Handshake | TCP + TLS (2–3 round trips) | TCP + TLS | **QUIC combines transport and TLS 1.3: 1 round trip**, 0-RTT on reconnect |
| Network change (Wi-Fi to 4G) | Connection lost | Connection lost | **Connection survives** (connection IDs) |

**What this means for backends:**
- **gRPC runs on HTTP/2:** multiplexing and streaming. HTTP/2 connections are long-lived, so an L4 load balancer sends every request to one pod; you need an L7 LB or client-side balancing.
- HTTP/3 helps most on **mobile and flaky networks**; it's usually enabled at the CDN or load balancer while internal services stay on HTTP/1.1 or HTTP/2. Java's `HttpClient` supports HTTP/3 since Java 26.

**HTTPS = HTTP over TLS.** TLS provides **encryption** (no eavesdropping), **integrity** (no tampering) and **authentication** (it really is that server, thanks to its certificate).

**The TLS 1.3 handshake (simplified):**
```
Client ── ClientHello: versions, supported ciphers, key share (ECDHE) ──► Server
Client ◄─ ServerHello: chosen cipher, key share; Certificate; Finished ── Server
     (the client checks the certificate: signed by a trusted CA? right domain? not expired?)
Client ── Finished ─────────────────────────────────────────────────────► Server
        → both sides derive the same (symmetric) session key from the ECDHE exchange
```
- **Asymmetric cryptography** (ECDHE, RSA/ECDSA signatures) is used only during the handshake to agree on keys and authenticate; the data afterwards is encrypted **symmetrically** (AES-GCM, ChaCha20) because it's much faster.
- **Forward secrecy:** session keys are ephemeral, so even if the server's private key leaks later, old traffic can't be decrypted.
- TLS 1.3 takes **1 round trip** (TLS 1.2 took 2).

**Operational reality:**
- **TLS termination** happens at the load balancer or ingress; internally you can use plain HTTP or **mTLS** (a service mesh), depending on security requirements. See [mTLS](#sec-mtls).
- Expired certificates are a very common cause of incidents: renew automatically (Let's Encrypt, cert-manager, ACM) and alert before expiry.
- **HSTS** makes browsers always use HTTPS.

@@@ net-dns | DNS hoạt động thế nào? Các loại bản ghi, TTL và những lỗi hay gặp? / How does DNS work? Record types, TTLs and common problems? | network | dns,networking | qa | Networking
### Tiếng Việt

**DNS** chuyển tên miền (`api.shop.vn`) thành địa chỉ IP. Chạy chủ yếu trên **UDP port 53** (TCP khi phản hồi lớn hoặc chuyển zone).

**Quá trình phân giải:**
```
App → cache của OS / trình duyệt → Recursive resolver (của ISP, 8.8.8.8, VPC resolver)
   → Root server (.) → TLD server (.vn) → Authoritative server của shop.vn → trả IP
   (mỗi bước được cache theo TTL)
```

**Các loại bản ghi hay gặp:**

| Bản ghi | Ý nghĩa | Ví dụ |
|---|---|---|
| **A / AAAA** | Tên → IPv4 / IPv6 | `api.shop.vn → 203.0.113.10` |
| **CNAME** | Tên → tên khác (bí danh) | `www → shop-lb-123.elb.amazonaws.com` |
| **MX** | Mail server của domain | |
| **TXT** | Văn bản: xác minh domain, SPF, DKIM | |
| **NS** | Server có thẩm quyền của zone | |
| **SRV** | Host và port của một dịch vụ | Service discovery |
| Alias (Route 53) | Giống CNAME nhưng dùng được ở gốc domain | `shop.vn → ALB` |

**TTL:** thời gian bản ghi được cache. TTL dài thì ít truy vấn hơn, nhưng **đổi IP lan chậm**. Trước khi migrate hoặc failover, **hạ TTL xuống** (ví dụ 60 giây) từ vài ngày trước.

**DNS trong hệ thống backend:**
- **Load balancing và failover bằng DNS:** trả nhiều IP, GeoDNS (trả region gần nhất), health-check failover (Route 53). Hạn chế: client cache theo TTL nên chuyển hướng không tức thì.
- **Kubernetes:** CoreDNS phân giải `order-service.default.svc.cluster.local` thành ClusterIP của Service; **service discovery** nội bộ dựa vào đây.
- **JVM cache DNS:** Java có cache DNS riêng (`networkaddress.cache.ttl`). Nếu cache quá lâu, sau khi IP của DB hoặc API đổi (failover RDS), app vẫn gọi IP cũ. Đặt TTL hợp lý (ví dụ 30–60 giây).

**Lỗi hay gặp:**
- "It's always DNS": đổi bản ghi nhưng nơi khác vẫn thấy IP cũ do cache.
- Pod không phân giải được tên do CoreDNS quá tải; độ trễ DNS cộng vào mọi request nếu không cache.
- Sai bản ghi khi migrate gây downtime; quên gia hạn domain.
- Công cụ kiểm tra: `dig api.shop.vn`, `nslookup`, `dig +trace`.

### English

**DNS** turns domain names (`api.shop.vn`) into IP addresses. It runs mostly over **UDP port 53** (TCP for large responses or zone transfers).

**The resolution process:**
```
App → OS / browser cache → Recursive resolver (ISP, 8.8.8.8, VPC resolver)
   → Root server (.) → TLD server (.vn) → shop.vn's authoritative server → returns the IP
   (each step is cached according to TTL)
```

**Common record types:**

| Record | Meaning | Example |
|---|---|---|
| **A / AAAA** | Name → IPv4 / IPv6 | `api.shop.vn → 203.0.113.10` |
| **CNAME** | Name → another name (an alias) | `www → shop-lb-123.elb.amazonaws.com` |
| **MX** | The domain's mail servers | |
| **TXT** | Text: domain verification, SPF, DKIM | |
| **NS** | The zone's authoritative servers | |
| **SRV** | Host and port of a service | Service discovery |
| Alias (Route 53) | Like CNAME but allowed at the domain apex | `shop.vn → ALB` |

**TTL:** how long a record is cached. A long TTL means fewer lookups but **IP changes propagate slowly**. Before a migration or failover, **lower the TTL** (say to 60 seconds) a few days in advance.

**DNS in backend systems:**
- **Load balancing and failover via DNS:** multiple IPs, GeoDNS (nearest region), health-checked failover (Route 53). The limitation: clients cache by TTL, so redirection isn't instant.
- **Kubernetes:** CoreDNS resolves `order-service.default.svc.cluster.local` to the Service's ClusterIP; internal **service discovery** relies on this.
- **JVM DNS caching:** Java has its own DNS cache (`networkaddress.cache.ttl`). If it caches too long, after a DB or API IP changes (an RDS failover) the app keeps calling the old IP. Set a sensible TTL (for example 30–60 seconds).

**Common problems:**
- "It's always DNS": you changed a record but other places still see the old IP because of caching.
- Pods can't resolve names because CoreDNS is overloaded; DNS latency adds to every request without caching.
- Wrong records during a migration cause downtime; forgotten domain renewals.
- Tools: `dig api.shop.vn`, `nslookup`, `dig +trace`.
