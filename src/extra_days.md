@@@ day-1 | Day 1: Java core | plan | lo-trinh | guide | Day 1
**Mục tiêu:** Collections, HashMap, String, OOP, exception, generics.

### Lý thuyết (13 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [HashMap hoạt động bên trong thế nào?](#java-core-1)
- [ ] [HashMap, ConcurrentHashMap và synchronizedMap khác nhau thế nào?](#java-core-2)
- [ ] [Quan hệ giữa equals() và hashCode() là gì?](#java-core-3)
- [ ] [Vì sao String là immutable?](#java-core-4)
- [ ] [ArrayList và LinkedList khác nhau thế nào? StringBuilder và StringBuffer?](#java-core-5)
- [ ] [Checked và unchecked exception khác nhau thế nào? Bạn thiết kế xử lý lỗi trong service ra sao?](#java-core-6)
- [ ] [Abstraction và encapsulation khác nhau thế nào? Có encapsulation mà không có abstraction được không?](#jc-abstraction-encapsulation)
- [ ] [String constant pool là gì? String được lưu ở đâu?](#jc-string-pool)
- [ ] [Interface có private method được không? Để làm gì?](#jc-interface-private)
- [ ] [Có khi nào được phép vi phạm nguyên tắc Open/Closed không?](#jc-ocp-violation)
- [ ] [Khối finally có thể làm mất exception từ try không?](#jc-finally)
- [ ] [Vì sao Map không kế thừa Collection? HashMap và TreeMap khác nhau thế nào?](#jc-collection-map)
- [ ] [Generics: type erasure là gì? Wildcard ? extends và ? super dùng khi nào?](#jc-generics)

### Coding: Arrays & hashing

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [1. Two Sum](https://leetcode.com/problems/two-sum/) (Easy)
- [ ] [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) (Medium)
- [ ] [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) (Medium)
- [ ] [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-2 | Day 2: JVM & concurrency | plan | lo-trinh | guide | Day 2
**Mục tiêu:** Bộ nhớ JVM, GC, class loader, thread pool, virtual threads, Java 8–21.

### Lý thuyết (19 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [Explain the Stream API. What is the difference between map and flatMap?](#java-modern-7)
- [ ] [What is Optional for, and how is it misused?](#java-modern-9)
- [ ] [Describe the JVM memory areas.](#jvm-10)
- [ ] [Which garbage collectors do you know, and how do you choose?](#jvm-11)
- [ ] [How do you find a memory leak?](#jvm-12)
- [ ] [How do class loaders work?](#jvm-13)
- [ ] [volatile vs synchronized vs Atomic classes?](#concurrency-14)
- [ ] [How does ThreadPoolExecutor decide when to create threads?](#concurrency-15)
- [ ] [What are virtual threads and when would you use them?](#concurrency-16)
- [ ] [What is a deadlock and how do you prevent and diagnose it?](#concurrency-17)
- [ ] [How do you run several remote calls in parallel and combine the results?](#concurrency-18)
- [ ] [What newer Java features have you used?](#java-modern-8)
- [ ] [Các phiên bản Java LTS và tính năng chính của từng bản? Nên dùng bản nào?](#jn-versions)
- [ ] [Record là gì? Khi nào dùng, khi nào không?](#jn-records)
- [ ] [Sealed class và pattern matching (instanceof, switch, record pattern) dùng thế nào?](#jn-sealed-pattern)
- [ ] [Những tính năng nhỏ hay dùng từ Java 9 đến 21 là gì?](#jn-small-features)
- [ ] [Virtual threads hoạt động thế nào? Bẫy khi dùng là gì?](#jn-virtual-threads)
- [ ] [Scoped values và structured concurrency là gì?](#jn-scoped-structured)
- [ ] [Java 25 (LTS) có gì mới đáng chú ý?](#jn-java25)

### Coding: Arrays & hashing

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] Làm lại 347 trong 10 phút (min-heap kích thước k)
- [ ] [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) (Easy)
- [ ] [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) (Medium)
- [ ] [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-3 | Day 3: Spring & Spring Boot | plan | lo-trinh | guide | Day 3
**Mục tiêu:** IoC, bean lifecycle, @Transactional, AOP, auto-configuration, Security, MVC.

### Lý thuyết (19 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [What are IoC and dependency injection? Which injection type do you prefer?](#spring-1)
- [ ] [Describe the bean lifecycle and scopes.](#spring-2)
- [ ] [How does @Transactional work, and when does it silently not work?](#spring-3)
- [ ] [Explain propagation and isolation.](#spring-4)
- [ ] [How does Spring Boot auto-configuration work?](#spring-5)
- [ ] [How does Spring AOP work, and what are its limits?](#spring-6)
- [ ] [How does Spring Security process a request? How did authentication work in your last system?](#spring-7)
- [ ] [How do you design and version a REST API?](#spring-8)
- [ ] [Which design patterns have you actually used? Explain SOLID briefly.](#spring-9)
- [ ] [How do you test a Spring Boot service?](#spring-10)
- [ ] [Can a Spring Boot app run without @SpringBootApplication?](#sp-without-sba)
- [ ] [What is DispatcherServlet? Walk through the Spring MVC request flow.](#sp-dispatcher)
- [ ] [@RequestParam vs @PathVariable: can you use both in one method?](#sp-param-path)
- [ ] [How do you configure different databases per environment?](#sp-profiles)
- [ ] [Spring Boot 2, 3, 4 khác nhau thế nào? Nâng cấp cần chú ý gì?](#sn-versions)
- [ ] [Spring Boot 3.x có những tính năng mới nào đáng dùng?](#sn-boot3)
- [ ] [RestTemplate, WebClient, RestClient và HTTP interface: nên dùng cái nào?](#sn-http-clients)
- [ ] [Spring Boot 4](#sn-boot4)
- [ ] [Làm sao để ứng dụng Spring khởi động nhanh và tốn ít bộ nhớ: GraalVM native, CDS hay AOT cache?](#sn-startup)

### Coding: Two pointers

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) (Easy)
- [ ] [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) (Medium)
- [ ] [15. 3Sum](https://leetcode.com/problems/3sum/) (Medium)

### Buổi tối

- [ ] CI/CD lab bước 1–2: CI cơ bản và quality gate ([hướng dẫn](#cicd-fix))

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-4 | Day 4: Database, JPA & SQL | plan | lo-trinh | guide | Day 4
**Mục tiêu:** Index, locking, isolation, N+1, PostgreSQL internals, SQL.

### Lý thuyết (27 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [How would you add vector search with PostgreSQL?](#pgvector)
- [ ] [What is the N+1 problem and how do you fix it?](#jpa-16)
- [ ] [Lazy vs eager loading? What is LazyInitializationException?](#jpa-17)
- [ ] [Explain entity states and the first- and second-level cache.](#jpa-18)
- [ ] [How do you handle large batch inserts or updates with JPA?](#jpa-19)
- [ ] [How do indexes work, and when does an index not get used?](#database-11)
- [ ] [What is a covering index? Clustered vs non-clustered?](#database-12)
- [ ] [A query is slow in production. What do you do?](#database-13)
- [ ] [Optimistic vs pessimistic locking?](#database-14)
- [ ] [What is ACID? When would you choose NoSQL?](#database-15)
- [ ] [Find the second highest salary.](#sql-7)
- [ ] [Find the top 3 salaries in each department.](#sql-8)
- [ ] [Find duplicate emails, and customers who have never placed an order.](#sql-9)
- [ ] [WHERE vs HAVING? INNER vs LEFT JOIN? UNION vs UNION ALL?](#sql-10)
- [ ] [Các loại JOIN trong SQL khác nhau thế nào?](#sql-joins)
- [ ] [Chuẩn hóa dữ liệu (1NF, 2NF, 3NF) là gì? Khi nào nên phi chuẩn hóa?](#sql-normalization)
- [ ] [Window function là gì? Cho ví dụ ROW_NUMBER, RANK, LAG, tổng lũy kế.](#sql-window)
- [ ] [Có những loại NoSQL nào? Khi nào chọn SQL, khi nào chọn NoSQL?](#nosql-types)
- [ ] [Thiết kế dữ liệu trong MongoDB thế nào: embed hay reference?](#nosql-mongodb)
- [ ] [Cassandra hoạt động thế nào? Thiết kế bảng ra sao?](#nosql-cassandra)
- [ ] [How does PostgreSQL guarantee atomicity and durability after a crash?](#pg-acid-wal)
- [ ] [What is MVCC, and why does PostgreSQL need VACUUM?](#pg-mvcc)
- [ ] [Read committed vs repeatable read vs serializable in PostgreSQL?](#pg-isolation)
- [ ] [Beyond B-tree: when do you use Hash, GIN, GiST or partial indexes?](#pg-indexes)
- [ ] [When and how do you partition a large table?](#pg-partitioning)
- [ ] [Why use PgBouncer if the app already has a connection pool?](#pg-pooling)
- [ ] [Tricky SQL questions: EXISTS vs IN, NULL, deleting 10 million rows.](#sql-tricky)

### Coding: Sliding window

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) (Easy)
- [ ] [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) (Medium)
- [ ] [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) (Medium)

### Buổi tối

- [ ] CI/CD lab bước 3: multi-stage Dockerfile, push image lên GHCR

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-5 | Day 5: Microservices & Kafka | plan | lo-trinh | guide | Day 5
**Mục tiêu:** Saga, outbox, idempotency, resilience, REST, Kafka.

### Lý thuyết (27 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [Monolith vs microservices: when would you choose each?](#microservices-1)
- [ ] [Các service giao tiếp với nhau thế nào? Khi nào dùng đồng bộ (sync), khi nào bất đồng bộ (async)?](#microservices-2)
- [ ] [How do you make an operation idempotent?](#microservices-5)
- [ ] [How do you make calls between services resilient?](#microservices-6)
- [ ] [What does an API gateway do? How is authentication handled across services?](#microservices-7)
- [ ] [How do you observe and debug a distributed system?](#microservices-8)
- [ ] [Explain the CAP theorem in practical terms.](#microservices-9)
- [ ] [What are REST principles? Is REST always stateless?](#arch-rest)
- [ ] [What happens if a circuit breaker stays open too long?](#arch-cb-open)
- [ ] [Trong một service, xử lý đồng bộ và bất đồng bộ khác nhau thế nào? @Async, CompletableFuture, reactive, virtual threads?](#sync-async-code)
- [ ] [Mô tả toàn bộ hành trình của một request từ lúc client gửi đến khi nhận response.](#request-flow)
- [ ] [Làm sao giữ dữ liệu nhất quán giữa các service? Saga pattern là gì?](#microservices-3)
- [ ] [Outbox pattern là gì? Hoạt động cụ thể thế nào?](#microservices-4)
- [ ] [Explain topics, partitions, offsets and consumer groups.](#kafka-10)
- [ ] [What is a message key and why use it?](#kafka-11)
- [ ] [What delivery guarantees does Kafka offer?](#kafka-12)
- [ ] [What is a dead letter queue? What happens after a message lands there?](#kafka-13)
- [ ] [What is a rebalance, and what is consumer lag?](#kafka-14)
- [ ] [Kafka và RabbitMQ khác nhau thế nào? Khi nào chọn cái nào?](#kafka-15)
- [ ] [RabbitMQ hoạt động thế nào? Exchange có những loại nào?](#rabbitmq-basics)
- [ ] [Làm sao để RabbitMQ không mất message? Retry và dead letter làm thế nào?](#rabbitmq-reliability)
- [ ] [Kafka đảm bảo thứ tự thế nào? Retry khi xử lý lỗi mà không làm hỏng thứ tự?](#kafka-ordering-retry)
- [ ] [Kafka giữ dữ liệu bao lâu? Log compaction là gì?](#kafka-retention)
- [ ] [Two-phase commit (2PC) là gì? Vì sao microservices ít dùng?](#dt-2pc)
- [ ] [TCC (Try-Confirm-Cancel) là gì? Khác Saga thế nào?](#dt-tcc)
- [ ] [So sánh các cách xử lý giao dịch phân tán: 2PC, Saga, TCC, Outbox.](#dt-compare)
- [ ] [Why is Kafka fast, and what are ISR and exactly-once?](#kafka-internals)

### Coding: Stack

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) (Easy)
- [ ] [155. Min Stack](https://leetcode.com/problems/min-stack/) (Medium)
- [ ] [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) (Medium)

### Buổi tối

- [ ] CI/CD lab bước 4: deploy lên kind, manual approval

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-6 | Day 6: Go | plan | lo-trinh | guide | Day 6
**Mục tiêu:** Concurrency, context, map, slice, interface, GC, xử lý tiền (quan trọng cho Grab).

### Lý thuyết (14 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [Buffered vs unbuffered channels: how do they behave?](#go-channels)
- [ ] [Implement a worker pool that stops cleanly on cancellation.](#go-worker-pool)
- [ ] [How does the context package work?](#go-context)
- [ ] [defer, panic and recover: what are the traps?](#go-defer)
- [ ] [What is a goroutine leak and how do you find it?](#go-goroutine-leak)
- [ ] [How are interfaces represented, and why can a nil error be non-nil?](#go-interface-nil)
- [ ] [How does a Go map work, and how do you make it concurrency-safe?](#go-map)
- [ ] [Explain slice internals and the append gotcha.](#go-slices)
- [ ] [Stack vs heap in Go: what is escape analysis?](#go-stack-heap)
- [ ] [How does Go's garbage collector work, compared with the JVM?](#go-gc)
- [ ] [Mutex vs RWMutex vs atomic: when do you use each?](#go-sync)
- [ ] [Race condition vs data race: how do you detect and fix them?](#go-race)
- [ ] [How do you handle money in code and in the database?](#go-money)
- [ ] [How do SOLID and interfaces look in idiomatic Go?](#go-design)

### Coding: Binary search

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [704. Binary Search](https://leetcode.com/problems/binary-search/) (Easy)
- [ ] [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) (Medium)
- [ ] [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) (Medium)

### Buổi tối

- [ ] CI/CD lab bước 5: probes, rollback, secrets

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-7 | Day 7: Mock 1 & ôn lại | plan | lo-trinh | guide | Day 7
**Mục tiêu:** Mock 90 phút bằng tiếng Anh cho Ngày 1–6, ghi âm, lập danh sách lỗ hổng.

### Việc cần làm

- [ ] Nhắn "mock Java core" hoặc "mock Spring" để luyện hỏi đáp với Claude
- [ ] Ôn lại mọi câu chưa đánh dấu "đã thuộc" của Ngày 1–6
- [ ] Viết ra 5 lỗ hổng lớn nhất để vá trong tuần 2

### Coding: Linked list

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) (Easy)
- [ ] [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) (Easy)
- [ ] [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) (Easy)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-8 | Day 8: System design 1 | plan | lo-trinh | guide | Day 8
**Mục tiêu:** Khung trả lời 45 phút, caching, CDN, scale database, consistent hashing.

### Lý thuyết (23 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [What is your framework for a 45-minute system design interview?](#sd-checklist)
- [ ] [Ước lượng dung lượng (back-of-the-envelope) làm thế nào? Những con số nào cần nhớ?](#sd-estimation)
- [ ] [Scale dọc (vertical) và scale ngang (horizontal) khác nhau thế nào? Khi nào chọn cái nào?](#sd-scale-up-out)
- [ ] [Stateless và stateful khác nhau thế nào? Cho ví dụ ở từng tầng của hệ thống.](#sd-stateless-stateful)
- [ ] [Làm sao scale và vận hành thành phần stateful (WebSocket, database, StatefulSet)? Chuyển một service stateful sang stateless thế nào?](#sd-stateful-scaling)
- [ ] [Load balancer hoạt động thế nào? L4 và L7 khác gì? Có những thuật toán nào?](#sd-load-balancer)
- [ ] [High availability là gì? 99,9% và 99,99% khác nhau bao nhiêu? Thiết kế thế nào để không có điểm hỏng duy nhất?](#sd-availability)
- [ ] [Autoscaling hoạt động thế nào? Scale theo chỉ số gì, và có những bẫy nào?](#sd-autoscaling)
- [ ] [Dùng hàng đợi để chịu tải đột biến thế nào? Backpressure là gì?](#sd-queue-backpressure)
- [ ] [Hệ thống chậm khi tải tăng: bạn tìm và xử lý điểm nghẽn thế nào?](#sd-bottleneck)
- [ ] [Design a URL shortener.](#system-design-17)
- [ ] [Design a rate limiter.](#system-design-18)
- [ ] [How do you use caching, and what can go wrong?](#system-design-19)
- [ ] [How do you scale a database?](#system-design-20)
- [ ] [How does a CDN work, and what can it do for an API?](#sd-cdn)
- [ ] [What is consistent hashing and why use it?](#sd-consistent-hashing)
- [ ] [Replication and sharding: how do you choose a shard key?](#db-replication-sharding)
- [ ] [Có những chiến lược cache nào? Cache-aside, read-through, write-through, write-behind khác nhau ra sao?](#cache-patterns)
- [ ] [Cache penetration, cache breakdown (stampede) và cache avalanche là gì? Xử lý thế nào?](#cache-problems)
- [ ] [Làm sao giữ cache và database nhất quán?](#cache-consistency)
- [ ] [Redis có những kiểu dữ liệu nào? Dùng cho bài toán gì? Vì sao Redis nhanh?](#redis-structures)
- [ ] [Redis lưu dữ liệu xuống đĩa và chạy HA thế nào? Khi bộ nhớ đầy thì sao?](#redis-ha)
- [ ] [Cache cục bộ (Caffeine) và cache phân tán (Redis) khác nhau thế nào? Khi nào dùng cả hai?](#cache-local-vs-distributed)

### Việc cần làm

- [ ] Tự vẽ URL shortener và rate limiter trong 35 phút mỗi bài, nói to bằng tiếng Anh

### Coding: Linked list

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [19. Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) (Medium)
- [ ] [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) (Medium)
- [ ] [146. LRU Cache](https://leetcode.com/problems/lru-cache/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-9 | Day 9: System design 2 | plan | lo-trinh | guide | Day 9
**Mục tiêu:** Bài quy mô lớn (ride matching, ví, flash sale), lock, consistency, kiến trúc dự án cũ.

### Lý thuyết (10 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [Describe the architecture of your last project.](#system-design-16)
- [ ] [Design a ride-hailing service that matches riders with nearby drivers.](#sd-ride-matching)
- [ ] [Design a wallet](#sd-wallet)
- [ ] [How does double-entry bookkeeping work in a ledger?](#sd-double-entry)
- [ ] [Design a flash sale: 1,000 items, one million users clicking at once.](#sd-flash-sale)
- [ ] [How do you implement a distributed lock, and what can go wrong?](#sd-distributed-lock)
- [ ] [What is eventual consistency, and when is it acceptable?](#sd-eventual)
- [ ] [How do you migrate a monolith to microservices safely?](#sd-strangler)
- [ ] [What is hexagonal (ports and adapters) architecture?](#arch-hexagonal)
- [ ] [DRY, KISS, YAGNI: duplication or coupling?](#arch-principles)

### Việc cần làm

- [ ] Vẽ sơ đồ kiến trúc Opswat, chuẩn bị 3 quyết định thiết kế bảo vệ được

### Coding: Trees

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) (Easy)
- [ ] [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) (Easy)
- [ ] [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-10 | Day 10: CI/CD, Docker, K8s & AWS | plan | lo-trinh | guide | Day 10
**Mục tiêu:** Pipeline, deploy strategies, probes, AWS cơ bản, xử lý sự cố.

### Lý thuyết (31 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [What is the difference between CI, continuous delivery and continuous deployment?](#cicd-1)
- [ ] [Walk me through the pipeline of your last project.](#cicd-2)
- [ ] [What stages should a good pipeline have, and in what order?](#cicd-3)
- [ ] [What does 'build once, deploy many' mean?](#cicd-4)
- [ ] [Compare rolling, blue-green and canary deployments.](#cicd-5)
- [ ] [How do you deploy database changes without downtime?](#cicd-6)
- [ ] [How do you roll back a bad release?](#cicd-7)
- [ ] [Trunk-based development vs GitFlow?](#cicd-8)
- [ ] [How do you manage secrets in a pipeline?](#cicd-9)
- [ ] [The pipeline takes 40 minutes. How do you speed it up?](#cicd-10)
- [ ] [What quality gates do you put in a pipeline?](#cicd-11)
- [ ] [Image vs container? How do you write a good Dockerfile for a Java service?](#docker-k8s-12)
- [ ] [Explain Pod, Deployment, Service, Ingress, ConfigMap and Secret.](#docker-k8s-13)
- [ ] [Liveness vs readiness probes?](#docker-k8s-14)
- [ ] [How do you set resources and scale?](#docker-k8s-15)
- [ ] [Which cloud services have you used?](#cloud-16)
- [ ] [What is infrastructure as code, and why use it?](#cloud-17)
- [ ] [What are the twelve-factor principles you apply most?](#cloud-18)
- [ ] [Walk me through a typical secure web architecture on AWS.](#aws-big-picture)
- [ ] [Security Group vs Network ACL vs WAF?](#aws-sg-nacl)
- [ ] [How do IAM roles and policies work? How do you apply least privilege?](#aws-iam)
- [ ] [What is envelope encryption with KMS?](#aws-kms)
- [ ] [Secrets Manager vs Parameter Store, and how does rotation work?](#aws-secrets)
- [ ] [RDS Multi-AZ vs read replicas?](#aws-rds)
- [ ] [What should a backend engineer know about S3?](#aws-s3)
- [ ] [When would you use AWS Lambda, and what are its limits?](#aws-lambda)
- [ ] [How does EC2 Auto Scaling work?](#aws-autoscaling)
- [ ] [What do you need to know about running services on EKS?](#aws-eks)
- [ ] [How do you build a small, secure Docker image for a Go service?](#docker-go)
- [ ] [A pod is in CrashLoopBackOff. How do you debug it?](#k8s-debug)
- [ ] [Production is slow and alerts are firing. Walk me through the first 10 minutes.](#troubleshoot-10min)

### Coding: Trees

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) (Medium)
- [ ] [235. Lowest Common Ancestor of a BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) (Medium)
- [ ] [230. Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-11 | Day 11: Security & testing | plan | lo-trinh | guide | Day 11
**Mục tiêu:** JWT, OAuth, OWASP, mã hóa, mTLS, phân quyền, test pyramid (quan trọng cho Axon).

### Lý thuyết (13 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [TDD vs BDD, and what is the test pyramid?](#eng-testing)
- [ ] [How does JWT work, and how do you revoke one?](#sec-jwt)
- [ ] [Explain OAuth 2.0 and OpenID Connect. Which flow would you use?](#sec-oauth)
- [ ] [How should passwords be stored?](#sec-password)
- [ ] [Hashing vs encryption, and how do you manage keys?](#sec-crypto)
- [ ] [How do you protect PII at rest, and still search it?](#sec-pii)
- [ ] [What are the most important OWASP API security risks?](#sec-owasp-api)
- [ ] [How do you prevent SQL injection?](#sec-sqli)
- [ ] [XSS vs CSRF: what are they and how do you defend?](#sec-xss-csrf)
- [ ] [What is mTLS and when do you use it?](#sec-mtls)
- [ ] [RBAC vs ABAC: how do you design authorization?](#sec-rbac-abac)
- [ ] [What is Zero Trust?](#sec-zero-trust)
- [ ] [How do you threat-model a feature? Explain STRIDE.](#sec-stride)

### Coding: Intervals & heap

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) (Medium)
- [ ] [57. Insert Interval](https://leetcode.com/problems/insert-interval/) (Medium)
- [ ] [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-12 | Day 12: Behavioral & AI | plan | lo-trinh | guide | Day 12
**Mục tiêu:** 8 câu chuyện STAR bằng chuyện thật, AI tools, Agile.

### Lý thuyết (32 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [Bạn dùng công cụ AI coding trong công việc thế nào?](#ai-tools-13)
- [ ] [How do you write an effective prompt for a coding task?](#ai-tools-14)
- [ ] [What are tokens, and how do you control token usage and cost?](#ai-tools-15)
- [ ] [LLM hoạt động thế nào? Token, context window, temperature, hallucination là gì?](#ai-llm-basics)
- [ ] [RAG (Retrieval-Augmented Generation) là gì? Mô tả một pipeline RAG hoàn chỉnh.](#ai-rag)
- [ ] [Embedding và vector database hoạt động thế nào? Chọn pgvector hay vector DB chuyên dụng?](#ai-embeddings)
- [ ] [Tool calling (function calling) và AI agent hoạt động thế nào? Khi nào nên và không nên dùng agent?](#ai-tool-calling)
- [ ] [MCP (Model Context Protocol) là gì? Vì sao cần?](#ai-mcp)
- [ ] [Tích hợp LLM vào ứng dụng Spring Boot thế nào? Spring AI hay LangChain4j?](#ai-spring-ai)
- [ ] [Đưa tính năng LLM lên production cần lưu ý gì về chi phí, độ trễ, độ tin cậy và đánh giá chất lượng?](#ai-production)
- [ ] [Rủi ro bảo mật của ứng dụng LLM là gì? Prompt injection là gì và phòng chống thế nào?](#ai-security)
- [ ] [System design: thiết kế trợ lý AI hỏi đáp trên tài liệu nội bộ cho nhiều khách hàng (multi-tenant).](#ai-sd-assistant)
- [ ] [Vibe coding là gì? Khác gì với AI-assisted engineering? Khi nào chấp nhận được?](#ai-dev-vibe-coding)
- [ ] [AI coding agent (Claude Code, Cursor, Copilot agent) hoạt động thế nào? Khác autocomplete và chat ra sao?](#ai-dev-agentic-tools)
- [ ] [Quy trình làm việc hiệu quả với AI coding agent trên một tính năng thật là gì?](#ai-dev-workflow)
- [ ] [Context engineering cho AI coding agent là gì? (CLAUDE.md, AGENTS.md, rules, MCP)](#ai-dev-context)
- [ ] [Làm sao review và kiểm soát chất lượng code do AI sinh ra?](#ai-dev-review)
- [ ] [Đưa AI vào quy trình phát triển của cả nhóm (SDLC) thế nào? Đo hiệu quả ra sao?](#ai-dev-team)
- [ ] [Subagent, chạy nhiều agent song song và agent trong CI dùng thế nào?](#ai-dev-multi-agent)
- [ ] [Tell me about the most challenging project you've worked on.](#behavioral-1)
- [ ] [Describe a production incident you handled.](#behavioral-2)
- [ ] [Tell me about a disagreement with a teammate or lead.](#behavioral-3)
- [ ] [How do you handle unclear or changing requirements from a client?](#behavioral-4)
- [ ] [Tell me about a time you had to push back on a client or say no.](#behavioral-5)
- [ ] [Tell me about a deadline you were at risk of missing.](#behavioral-6)
- [ ] [Have you mentored or led other engineers?](#behavioral-7)
- [ ] [Tell me about a mistake you made.](#behavioral-8)
- [ ] [How do you do code review, and how do you handle technical debt?](#behavioral-9)
- [ ] [How do you estimate work and work in Scrum?](#behavioral-10)
- [ ] [How do you learn a new domain or technology quickly?](#behavioral-11)
- [ ] [Where do you see yourself in three years?](#behavioral-12)
- [ ] [What is the SDLC, and why is Agile usually preferred over Waterfall?](#eng-sdlc-agile)

### Việc cần làm

- [ ] Điền hết các chỗ [...] bằng chuyện thật, mỗi câu chuyện nói trong 2 phút

### Coding: Graphs

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) (Medium)
- [ ] [133. Clone Graph](https://leetcode.com/problems/clone-graph/) (Medium)
- [ ] [207. Course Schedule](https://leetcode.com/problems/course-schedule/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-13 | Day 13: HR & Mock 2 | plan | lo-trinh | guide | Day 13
**Mục tiêu:** Mock đầy đủ theo quy trình công ty sắp phỏng vấn: HR, technical, manager.

### Lý thuyết (9 câu)

*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*

- [ ] [Tell me about yourself.](#hr-screening-1)
- [ ] [Why did you leave your last company?](#hr-screening-2)
- [ ] [Why do you want to join our company?](#hr-screening-3)
- [ ] [What are you looking for in your next role?](#hr-screening-4)
- [ ] [What is your experience working with international clients or teams?](#hr-screening-5)
- [ ] [What is your salary expectation?](#hr-screening-6)
- [ ] [When can you start? Are you interviewing elsewhere?](#hr-screening-7)
- [ ] [Are you open to working on a project chosen after you join, or in a different time zone?](#hr-screening-8)
- [ ] [What is your strongest technology, and your weakest?](#hr-screening-9)

### Việc cần làm

- [ ] Mock full với Claude: 30 phút HR, 60 phút technical, 30 phút behavioral
- [ ] Sửa 3 điểm yếu nhất sau buổi mock

### Coding: Dynamic programming

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) (Easy)
- [ ] [198. House Robber](https://leetcode.com/problems/house-robber/) (Medium)
- [ ] [322. Coin Change](https://leetcode.com/problems/coin-change/) (Medium)

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt

@@@ day-14 | Day 14: Ôn nhẹ | plan | lo-trinh | guide | Day 14
**Mục tiêu:** Không học mới. Ôn câu chưa thuộc, chuẩn bị tinh thần và câu hỏi ngược.

### Việc cần làm

- [ ] Đọc lại [checklist trước ngày phỏng vấn](#checklist-truoc-ngay-phong-van)
- [ ] Chuẩn bị [câu hỏi hỏi ngược interviewer](#cau-hoi-nen-hoi)
- [ ] Đọc trang công ty sắp phỏng vấn trong mục Công ty
- [ ] Self-introduction 90 giây, nói lại 3 lần
- [ ] Ngủ sớm

### Coding: Ôn lại

*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*

- [ ] Làm lại 3 bài bị vấp nhiều nhất trong 13 ngày qua

### Chốt ngày

- [ ] Ghi âm 2 câu khó nhất, nghe lại
- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy
- [ ] Ghi lại câu còn vấp và bài coding bị kẹt
