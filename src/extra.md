@@@ plan | Kế hoạch ôn 2 tuần | guide | ke-hoach | guide
Kế hoạch 14 ngày, khoảng 3–4 giờ mỗi ngày, dùng chung cho mọi vị trí Senior Backend. Trước mỗi cuộc phỏng vấn cụ thể, mở trang của công ty đó trong mục Công ty để dồn thời gian vào vòng nặng nhất.

### Tuần 1: Phủ kín kiến thức nền

| Ngày | Chủ đề | Đầu ra |
|---|---|---|
| 1 | Java core: collections (HashMap internals, ConcurrentHashMap), equals/hashCode, immutability, generics | 30 câu trả lời miệng, mỗi câu dưới 60 giây |
| 2 | JVM và concurrency: memory model, GC (G1, ZGC), ClassLoader, ExecutorService, CompletableFuture, virtual threads, locks | Giải thích được 1 memory leak và 1 deadlock bạn từng gặp |
| 3 | Java 8–21: Stream API, Optional, records, sealed classes, pattern matching | 10 bài stream code tay không IDE |
| 4 | Spring: IoC/DI, bean lifecycle, AOP proxy, `@Transactional`, auto-configuration, Security filter chain | Vẽ được luồng một request qua Spring Boot |
| 5 | Database: index, EXPLAIN, isolation levels, locking, JPA/Hibernate (N+1, lazy/eager, cache) | 10 câu SQL trung bình (JOIN, window function, GROUP BY/HAVING) |
| 6 | Microservices và messaging: saga, outbox, idempotency, circuit breaker, Kafka | 1 trang ghi chú trade-off cho từng pattern |
| 7 | Mock lần 1: 90 phút hỏi nhanh bằng tiếng Anh, có ghi âm | Danh sách lỗ hổng để vá ở tuần 2 |

Song song mỗi ngày: 2 bài coding (xem tag `#dsa` và `#coding`), nói to độ phức tạp Big-O. Nếu đang nhắm Grab hoặc Axon, tăng lên 3–4 bài mức medium mỗi ngày.

### Tuần 2: Nâng tầm senior và luyện thể hiện

| Ngày | Chủ đề | Đầu ra |
|---|---|---|
| 8 | System design 1: khung trả lời, caching, load balancing, CDN ở mức khái niệm | URL shortener và rate limiter, 35 phút mỗi bài |
| 9 | System design 2: hệ thống Opswat làm case, cộng một bài quy mô lớn (ride matching hoặc ví điện tử) | Sơ đồ kiến trúc và 5 quyết định thiết kế bảo vệ được |
| 10 | Cloud và DevOps: Docker, Kubernetes cơ bản, CI/CD, AWS cơ bản, observability | Mô tả pipeline từ commit đến production |
| 11 | Design patterns, SOLID, testing (JUnit 5, Mockito, Testcontainers), REST API design | 1 bài refactor nhỏ, giải thích bằng tiếng Anh |
| 12 | Behavioral: 8 câu chuyện STAR; AI-assisted development | Bản nháp 8 câu chuyện, mỗi câu 2 phút |
| 13 | Mock lần 2 full theo đúng quy trình của công ty sắp phỏng vấn | Sửa 3 điểm yếu nhất |
| 14 | Ôn nhẹ: self-introduction, lý do rời Opswat, câu hỏi ngược | Nghỉ sớm, không học mới |

### Điểm cần ưu tiên theo hồ sơ của bạn

- **Lỗ hổng CDN, cloud và CI/CD:** vòng senior hay hỏi, nên ngày 8 và 10 không được cắt; xem bài "Vá điểm yếu CI/CD".
- **Go và Java:** công ty Java (EPAM, mgm) sẽ hỏi sâu Java gần đây bạn dùng thế nào; công ty dùng Go (Grab) sẽ quan tâm kinh nghiệm Go ở Opswat.
- **Hai kiểu công ty:** công ty dịch vụ hỏi lý thuyết và kinh nghiệm làm với khách hàng; công ty product hỏi DSA và system design sâu hơn.

@@@ cicd-fix | Vá điểm yếu CI/CD trong 2–3 ngày | guide | cicd,ke-hoach | guide
CI/CD là điểm yếu dễ vá nhất: phỏng vấn senior developer chỉ hỏi ở mức "hiểu và đã từng làm". Cách nhanh nhất là tự dựng một pipeline thật, sau đó trả lời bằng kinh nghiệm thay vì lý thuyết.

### Dựng một pipeline hoàn chỉnh (8–10 giờ)

1. **CI cơ bản:** mỗi push/PR chạy build, unit test; fail thì chặn merge (branch protection).
2. **Quality gate:** lint/static analysis (Checkstyle hoặc SonarCloud), coverage JaCoCo, dependency scan.
3. **Đóng gói:** multi-stage Dockerfile, tag theo commit SHA, push lên GHCR.
4. **CD:** deploy tự động lên `kind` local hoặc cloud free tier, manual approval trước production.
5. **Vận hành:** health check sau deploy, rollback về image trước, secrets từ GitHub Secrets.

### Khái niệm cần nói trôi chảy

- CI, continuous delivery và continuous deployment khác nhau ở đâu.
- Chiến lược deploy: rolling, blue-green, canary.
- Branching: trunk-based so với GitFlow, feature flag.
- Build once, promote cùng một image qua dev → staging → prod.
- Database migration: Flyway/Liquibase, expand → migrate → contract.
- Tối ưu pipeline: cache, chạy song song, test pyramid.
- Zero-downtime: readiness/liveness probe, graceful shutdown.

### Tận dụng kinh nghiệm sẵn có

Ghi lại pipeline ở Opswat và DXC: công cụ gì, các stage từ commit đến production, ai approve release, một lần pipeline hỏng và cách xử lý. Câu trả lời tốt nhất: "ở công ty quy trình như thế này, và tôi đã tự dựng lại một pipeline tương tự để hiểu từng bước."

@@@ co-epam | EPAM Systems | company | epam,outsourcing | guide
Công ty dịch vụ phần mềm toàn cầu; vòng technical nặng lý thuyết Java hỏi nhanh, ít LeetCode.

### Quy trình (theo báo cáo ứng viên)

1. **HR screening ~25 phút:** câu hỏi HR, kiểm tra tiếng Anh ([Glassdoor](https://static.glassdoor.nl/Interview/EPAM-Systems-Senior-Software-Engineer-Interview-Questions-EI_IE15544.0,12_KO13,37_IP45.htm)).
2. **Technical ~90 phút:** từ cơ bản đến nâng cao; senior bị hỏi thêm cloud, CI/CD và vận hành backend ([Glassdoor](https://static.glassdoor.nl/Interview/EPAM-Systems-Senior-Software-Engineer-Interview-Questions-EI_IE15544.0,12_KO13,37_IP45.htm)). Chủ đề hay gặp: Java cơ bản, Spring Boot, microservices, thường kèm một bài code ([Glassdoor](https://static.glassdoor.com.br/Interview/EPAM-Systems-Senior-Java-Developer-Interview-Questions-EI_IE15544.0,12_KO13,34_IP3.htm)).
3. **Manager hoặc client interview:** kinh nghiệm bản thân và tình huống nơi làm việc ([Glassdoor, TP.HCM](https://www.glassdoor.com.br/Entrevista/EPAM-Systems-Entrevista-E15544-RVW81756317.htm)).

### Trọng tâm

- Trả lời ngắn và chính xác, chịu được câu hỏi vặn liên tục về Java, Spring, database.
- Kafka được hỏi sâu: DLQ, message key ([Glassdoor](https://www.glassdoor.com/Interview/EPAM-Systems-Interview-E15544-RVW100340369.htm)).
- Câu hỏi về công cụ AI, prompt và token ([Glassdoor](https://www.glassdoor.com.hk/Interview/EPAM-Systems-Interview-E15544-RVW85790472.htm)).
- Kinh nghiệm outsourcing ở DXC là lợi thế; chuẩn bị chuyện làm việc với khách hàng nước ngoài.

### Ưu tiên ôn

- [HashMap internals](#java-core-1), [ConcurrentHashMap](#java-core-2), [JVM memory](#jvm-10), [GC](#jvm-11)
- [@Transactional](#spring-3), [Propagation và isolation](#spring-4), [N+1](#jpa-16)
- [Kafka message key](#kafka-11), [DLQ](#kafka-13), [Outbox](#microservices-4)
- [CI/CD: pipeline dự án cũ](#cicd-2), [Rollout strategies](#cicd-5)
- Cloud (senior hay bị hỏi): [Kiến trúc AWS tổng quan](#aws-big-picture), [IAM](#aws-iam), [RDS Multi-AZ vs replica](#aws-rds), [CDN](#sd-cdn)
- [Longest substring](#coding-1), [Group by range bằng stream](#coding-2)
- [Làm việc với yêu cầu không rõ của khách hàng](#behavioral-4), [Dùng AI tools](#ai-tools-13)
- Câu hỏi nhanh từ một buổi phỏng vấn EPAM Ấn Độ (2 vòng technical, vị trí 3–7 năm, [video GenZ Career](https://www.youtube.com/watch?v=VZ3T2gFlEiA)): [Abstraction vs encapsulation](#jc-abstraction-encapsulation), [String pool](#jc-string-pool), [Private method trong interface](#jc-interface-private), [Vi phạm OCP](#jc-ocp-violation), [finally đè exception](#jc-finally), [Map vs Collection, HashMap vs TreeMap](#jc-collection-map), [Không cần @SpringBootApplication](#sp-without-sba), [DispatcherServlet](#sp-dispatcher), [@RequestParam vs @PathVariable](#sp-param-path), [Spring profiles](#sp-profiles), [REST stateless](#arch-rest), [Circuit breaker mở quá lâu](#arch-cb-open), [TDD/BDD/test pyramid](#eng-testing), [SDLC và Agile](#eng-sdlc-agile), [Trapping Rain Water](#dsa-rain-water)
- Lưu ý: "22 LPA" trong video là lương EPAM Ấn Độ (Lakhs Per Annum, khoảng ₫600M/năm), không áp dụng cho Việt Nam.

@@@ co-mgm | mgm technology partners | company | mgm,outsourcing | guide
Công ty phần mềm gốc Đức, có văn phòng TP.HCM và Đà Nẵng; tiếng Anh và live coding Java là hai cửa chính.

### Quy trình (theo tin tuyển dụng và báo cáo ứng viên)

1. **Vòng 1:** lọc CV và gọi phỏng vấn với HR ([TopDev](https://topdev.vn/amp/viec-lam/java-developer-mgm-technology-partners-vietnam-2032497)). Một ứng viên ở TP.HCM tháng 12/2025 mô tả: lọc CV, cuộc gọi kiểm tra tiếng Anh, rồi vòng technical 1 ([Glassdoor](https://www.glassdoor.ca/Interview/mgm-technology-partners-Interview-Questions-E1170616.htm)).
2. **Vòng 2:** technical live coding bằng tiếng Anh ([TopDev](https://topdev.vn/amp/viec-lam/java-developer-mgm-technology-partners-vietnam-2032497)).
3. **Có thể có:** bài test online trước phỏng vấn, khoảng 20 câu trắc nghiệm Java và SQL cộng một câu tự luận; báo cáo này từ văn phòng Porto nên ở Việt Nam có thể khác ([Glassdoor](https://fr.glassdoor.be/Entretien/mgm-technology-partners-Entretien-E1170616-RVW101345990.htm)).

### Trọng tâm

- Tin tuyển dụng yêu cầu giao tiếp tiếng Anh tốt cả nói và viết ([ITviec](https://itviec.com/viec-lam-it/java-developer-da-nang-hcmc-mgm-technology-partners-vietnam-0014)), nên vòng tiếng Anh là vòng loại thật sự.
- Live coding Java: viết code sạch, có test, nói to khi làm.
- Một số buổi phỏng vấn xoay quanh Linux, Docker và Kubernetes ([Glassdoor](https://www.glassdoor.ca/Interview/mgm-technology-partners-Interview-Questions-E1170616.htm)).
- SQL và Java cơ bản cho phần trắc nghiệm.

### Ưu tiên ôn

- [Tell me about yourself](#hr-screening-1), [Làm việc với khách hàng quốc tế](#hr-screening-5)
- [Stream API](#java-modern-7), [Equals/hashCode](#java-core-3), [Exceptions](#java-core-6)
- Toàn bộ tag `#coding`, `#dsa` và `#sql`
- [Dockerfile cho Java](#docker-k8s-12), [K8s objects](#docker-k8s-13), [Probes](#docker-k8s-14)
- [Testing Spring Boot](#spring-10), [Design patterns và SOLID](#spring-9)
- [CrashLoopBackOff](#k8s-debug), [Xử lý sự cố production](#troubleshoot-10min)

@@@ co-grab | Grab | company | grab,product | guide
Công ty product quy mô Đông Nam Á; vòng coding và system design khó hơn hẳn các công ty dịch vụ.

### Quy trình (theo báo cáo ứng viên)

1. **HR screening:** giới thiệu ngắn, có ứng viên ở TP.HCM mô tả chỉ khoảng 15 phút ([Taro](https://www.jointaro.com/interviews/companies/grab/work-experiences/software-engineer-ho-chi-minh-city-september-10-2019-4-fddfc697)).
2. **Live coding:** ứng viên khuyên luyện LeetCode nhiều ([Taro](https://www.jointaro.com/interviews/companies/grab/work-experiences/software-engineer-ho-chi-minh-city-september-10-2019-4-fddfc697)); một ứng viên Senior ở TP.HCM gặp hai bài live coding trong một buổi ([Taro](https://www.jointaro.com/interviews/companies/grab/experiences/senior-software-engineer-ho-chi-minh-city-april-6-2024-no-offer-negative-418070e2/)).
3. **System design:** ở mức senior xoay quanh bài toán quy mô lớn đặc thù khu vực như ghép chuyến, bản đồ, thanh toán ([techinterview.org](https://www.techinterview.org/companies/grab-interview-guide/?format=md)).
4. **Hiring manager / behavioral:** khoảng 45 phút về leadership và teamwork ([hw.glich.co](https://hw.glich.co/resources/companies/grab/interview-process/g4-software-engineer)).

Toàn bộ quá trình thường mất 4–6 tuần ([techinterview.org](https://www.techinterview.org/companies/grab-interview-guide/)).

### Trọng tâm

- DSA mức easy–medium, làm nhanh và đúng: array, string, hash map, cây, đồ thị.
- System design có số liệu: ước lượng QPS, lưu trữ, phân vùng dữ liệu, xử lý lỗi.
- Một ứng viên backend từng bị hỏi Golang, system và database ([Taro](https://www.jointaro.com/interviews/companies/grab/experiences/backend-developer-vietnam-november-25-2018-no-offer-positive-bac77e7d/)); kinh nghiệm Go ở Opswat là điểm cộng, nên chuẩn bị nói về goroutine, channel, context.
- Nhiều vị trí backend ở TP.HCM thuộc domain thanh toán ([Grab Careers](https://www.grab.careers/en/jobs/744000144226510/senior-software-engineer-backend/)), nên idempotency và tính nhất quán dữ liệu rất đáng ôn.

### Ưu tiên ôn

- Toàn bộ tag `#dsa` và `#coding`
- [Design ride matching](#sd-ride-matching), [Design wallet/ledger](#sd-wallet), [Rate limiter](#system-design-18), [Scale database](#system-design-20)
- [Idempotency](#microservices-5), [Saga](#microservices-3), [Outbox](#microservices-4), [Kafka delivery](#kafka-12)
- Go (kinh nghiệm Opswat): [Worker pool + context](#go-worker-pool), [Channels](#go-channels), [Context](#go-context), [Goroutine leak](#go-goroutine-leak), [Map và concurrency](#go-map), [Mutex vs atomic](#go-sync), [Race condition](#go-race), [GC](#go-gc)
- [System design framework](#sd-checklist), [Consistent hashing](#sd-consistent-hashing), [Distributed lock](#sd-distributed-lock), [Flash sale](#sd-flash-sale), [Double-entry ledger](#sd-double-entry), [Xử lý tiền](#go-money)
- [Production incident](#behavioral-2), [Bất đồng với đồng nghiệp](#behavioral-3), [Mentoring](#behavioral-7)

@@@ co-axon | Axon | company | axon,product | guide
Công ty product (body camera, phần mềm cho lực lượng an toàn công cộng) có văn phòng kỹ thuật ở TP.HCM; phỏng vấn nặng DSA và yêu cầu giải thích trade-off.

*Lưu ý: trang này là Axon (Axon Enterprise). Nếu bạn nhắm Axon Active (công ty gia công gốc Thụy Sĩ), quy trình khác: ứng viên mô tả 2 vòng, vòng 1 với Technical Lead và Head of Department ([Glassdoor](https://www.glassdoor.co.in/Interview/AXON-ACTIVE-Java-Software-Developer-Interview-Questions-EI_IE1063309.0,11_KO12,35.htm)).*

### Quy trình (theo báo cáo ứng viên)

1. Một ứng viên ở TP.HCM mô tả 4 vòng trong 2 tuần: lọc CV, test online, nói chuyện với senior engineer, rồi onsite 4 giờ với 4 interviewer, vòng khó nhất ([Glassdoor](https://www.glassdoor.com.br/Entrevista/Axon-Entrevista-E1597674-RVW41496445.htm)).
2. Câu hỏi được nhắc: sinh chuỗi theo bàn phím điện thoại, binary tree, hash table, thiết kế kiến trúc, dynamic programming ([Glassdoor](https://www.glassdoor.com.au/Interview/Axon-Interview-E1597674-RVW17537841.htm)); ứng viên khác gặp câu hỏi CS và system design ([Glassdoor](https://www.glassdoor.com.hk/Interview/Axon-Interview-E1597674-RVW90693581.htm)).
3. Email trước buổi phỏng vấn có thể báo nội dung từ DSA, OOP đến API design ([Glassdoor](https://www.glassdoor.sg/Interview/Axon-Interview-E1597674-RVW95653280.htm)).

Vị trí ở TP.HCM làm hybrid, onsite từ thứ Ba đến thứ Sáu ([Axon Careers](https://job-boards.greenhouse.io/axon/jobs/7694598003)).

### Trọng tâm

- Làm đúng chưa đủ: một ứng viên TP.HCM tháng 9/2026 giải được bài nhưng bị loại vì không giải thích được trade-off và độ phức tạp ([Glassdoor](https://clear.glassdoor.nl/Interview/Axon-Interview-E1597674-RVW86305866.htm)). Luôn nói time/space complexity và phương án thay thế.
- OOP và API design: thiết kế class, interface, REST endpoint sạch.
- Domain bảo mật: kinh nghiệm cybersecurity ở Opswat liên quan trực tiếp.

### Ưu tiên ôn

- [Letter combinations (bàn phím điện thoại)](#dsa-phone-letters), [Cây nhị phân](#dsa-tree-level), [LRU cache](#dsa-lru), [Coin change (DP)](#dsa-coin-change)
- Toàn bộ tag `#dsa` và `#coding`
- [REST API design](#spring-8), [Design patterns và SOLID](#spring-9), [Spring Security và auth](#spring-7)
- [Kiến trúc dự án gần nhất](#system-design-16), [Caching](#system-design-19)
- Security (gắn với kinh nghiệm Opswat): [OWASP API](#sec-owasp-api), [OAuth/OIDC](#sec-oauth), [JWT](#sec-jwt), [mTLS](#sec-mtls), [RBAC/ABAC](#sec-rbac-abac), [Bảo vệ PII](#sec-pii), [STRIDE](#sec-stride)

@@@ dsa-lru | Implement an LRU cache with O(1) get and put. | coding | dsa,design | qa | DSA
Kết hợp hash map (tra cứu O(1)) với danh sách liên kết đôi (di chuyển và xóa O(1)): phần tử mới dùng đưa lên đầu, khi đầy thì xóa phần tử ở cuối. Trong Java, `LinkedHashMap` với `accessOrder = true` làm sẵn việc này; interviewer thường muốn bạn tự cài.

```java
class LRUCache {
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0), tail = new Node(0, 0);

    LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    int get(int key) {
        Node n = map.get(key);
        if (n == null) return -1;
        moveToFront(n);
        return n.val;
    }

    void put(int key, int val) {
        Node n = map.get(key);
        if (n != null) {
            n.val = val;
            moveToFront(n);
            return;
        }
        if (map.size() == capacity) {
            Node lru = tail.prev;
            unlink(lru);
            map.remove(lru.key);
        }
        n = new Node(key, val);
        map.put(key, n);
        addFront(n);
    }

    private void moveToFront(Node n) { unlink(n); addFront(n); }
    private void unlink(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void addFront(Node n) {
        n.next = head.next; n.prev = head;
        head.next.prev = n; head.next = n;
    }

    private static class Node {
        int key, val; Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }
}
```

"Both operations are O(1) time; space is O(capacity). For concurrent access I'd wrap it with a lock, or use a library such as Caffeine in production."

@@@ dsa-top-k | Return the k most frequent elements of an array. | coding | dsa,heap | qa | DSA
Đếm tần suất bằng map, rồi giữ min-heap kích thước k. Time O(n log k), space O(n). Có thể làm O(n) bằng bucket sort theo tần suất.

```java
int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.merge(n, 1, Integer::sum);
    PriorityQueue<Map.Entry<Integer, Integer>> heap =
        new PriorityQueue<>(Map.Entry.comparingByValue());
    for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
        heap.offer(e);
        if (heap.size() > k) heap.poll();
    }
    return heap.stream().mapToInt(Map.Entry::getKey).toArray();
}
```

@@@ dsa-merge-intervals | Merge all overlapping intervals. | coding | dsa,sorting | qa | DSA
Sắp xếp theo điểm bắt đầu, rồi gộp nếu khoảng hiện tại chồng lên khoảng cuối cùng trong kết quả. Time O(n log n) do sắp xếp, space O(n).

```java
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
    List<int[]> out = new ArrayList<>();
    for (int[] cur : intervals) {
        if (!out.isEmpty() && out.get(out.size() - 1)[1] >= cur[0]) {
            out.get(out.size() - 1)[1] = Math.max(out.get(out.size() - 1)[1], cur[1]);
        } else {
            out.add(cur);
        }
    }
    return out.toArray(new int[0][]);
}
```

"Hỏi lại interviewer: hai khoảng chạm nhau như [1,2] và [2,3] có tính là chồng không."

@@@ dsa-islands | Count the number of islands in a grid of '1' (land) and '0' (water). | coding | dsa,graph | qa | DSA
Duyệt từng ô; gặp đất chưa thăm thì tăng bộ đếm và BFS/DFS để đánh dấu cả hòn đảo. Time O(m·n), space O(m·n) trong trường hợp xấu nhất. Dùng BFS với queue để tránh stack overflow trên lưới lớn.

```java
int numIslands(char[][] grid) {
    int m = grid.length, n = grid[0].length, count = 0;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] != '1') continue;
            count++;
            Deque<int[]> q = new ArrayDeque<>();
            q.add(new int[]{i, j});
            grid[i][j] = '0';
            while (!q.isEmpty()) {
                int[] c = q.poll();
                for (int[] d : dirs) {
                    int r = c[0] + d[0], col = c[1] + d[1];
                    if (r >= 0 && r < m && col >= 0 && col < n && grid[r][col] == '1') {
                        grid[r][col] = '0';
                        q.add(new int[]{r, col});
                    }
                }
            }
        }
    }
    return count;
}
```

"Nếu không được sửa input, dùng mảng `boolean[][] visited` riêng."

@@@ dsa-rotated-search | Search for a target in a rotated sorted array in O(log n). | coding | dsa,binary-search | qa | DSA
Binary search: ở mỗi bước, ít nhất một nửa đã được sắp xếp; kiểm tra target có nằm trong nửa đó không để quyết định đi trái hay phải. Time O(log n), space O(1).

```java
int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```

@@@ dsa-phone-letters | Generate all letter combinations of a phone-keypad digit string. | coding | dsa,backtracking,axon | qa | DSA
Backtracking: mỗi chữ số chọn lần lượt từng chữ cái, đệ quy sang chữ số tiếp theo. Time O(4^n · n) vì mỗi số có tối đa 4 chữ cái, space O(n) cho đệ quy (không tính kết quả). Dạng bài này từng được báo cáo ở Axon.

```java
private static final String[] KEYS = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

List<String> letterCombinations(String digits) {
    List<String> out = new ArrayList<>();
    if (digits.isEmpty()) return out;
    backtrack(digits, 0, new StringBuilder(), out);
    return out;
}

private void backtrack(String digits, int i, StringBuilder cur, List<String> out) {
    if (i == digits.length()) {
        out.add(cur.toString());
        return;
    }
    for (char c : KEYS[digits.charAt(i) - '0'].toCharArray()) {
        cur.append(c);
        backtrack(digits, i + 1, cur, out);
        cur.deleteCharAt(cur.length() - 1);
    }
}
```

@@@ dsa-tree-level | Binary tree: level-order traversal, and invert the tree. | coding | dsa,tree | qa | DSA
Level order dùng BFS với queue, xử lý theo từng tầng bằng cách lấy kích thước queue đầu mỗi vòng. Invert là đệ quy đổi chỗ con trái và con phải. Cả hai đều O(n) time; space O(w) với w là độ rộng lớn nhất (BFS) hoặc O(h) với h là chiều cao (đệ quy).

```java
List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> out = new ArrayList<>();
    if (root == null) return out;
    Deque<TreeNode> q = new ArrayDeque<>(List.of(root));
    while (!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            TreeNode n = q.poll();
            level.add(n.val);
            if (n.left != null) q.add(n.left);
            if (n.right != null) q.add(n.right);
        }
        out.add(level);
    }
    return out;
}

TreeNode invert(TreeNode root) {
    if (root == null) return null;
    TreeNode left = invert(root.left);
    root.left = invert(root.right);
    root.right = left;
    return root;
}
```

@@@ dsa-coin-change | Coin change: the fewest coins that make up an amount. | coding | dsa,dp | qa | DSA
Dynamic programming từ dưới lên: `dp[a]` là số đồng ít nhất để tạo ra `a`, với `dp[a] = min(dp[a - c] + 1)` qua mọi đồng `c`. Time O(amount · số loại đồng), space O(amount). Greedy sai với bộ đồng như {1, 3, 4} và amount 6.

```java
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int c : coins) {
            if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

@@@ dsa-course-schedule | Can all courses be finished given prerequisite pairs? (cycle detection) | coding | dsa,graph | qa | DSA
Topological sort theo thuật toán Kahn: đếm in-degree, đưa các nút có in-degree 0 vào queue, lấy ra và giảm in-degree của nút kề. Nếu xử lý được đủ mọi nút thì không có chu trình. Time O(V + E), space O(V + E). Ứng dụng thực tế: thứ tự khởi động service hoặc chạy migration có phụ thuộc.

```java
boolean canFinish(int n, int[][] prereq) {
    List<List<Integer>> g = new ArrayList<>();
    for (int i = 0; i < n; i++) g.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] p : prereq) { g.get(p[1]).add(p[0]); indeg[p[0]]++; }
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.add(i);
    int seen = 0;
    while (!q.isEmpty()) {
        int u = q.poll(); seen++;
        for (int v : g.get(u)) if (--indeg[v] == 0) q.add(v);
    }
    return seen == n;
}
```

@@@ sd-ride-matching | Design a ride-hailing service that matches riders with nearby drivers. | arch | system-design,grab,geo | qa | System design
*Bài kiểu Grab: luôn bắt đầu bằng làm rõ yêu cầu và ước lượng tải.*

"**Requirements.** Riders request a ride; we find nearby available drivers and offer the trip; one driver accepts. Non-functional: match within a few seconds, a driver is never assigned twice, highly available.

**Estimates.** Say 1 million online drivers sending a location every 4 seconds: about 250,000 location writes per second. That's the hot path, so locations don't go to a relational database.

**Components.**

- A *location service* receives driver updates over a persistent connection, gRPC or WebSocket. It keeps the latest position in memory or Redis, indexed by geospatial cell (geohash or H3), and partitioned by city or cell so each node handles one region.
- A *matching service* takes a ride request, looks up drivers in the rider's cell and neighbouring cells, ranks them by ETA rather than straight-line distance, and offers the trip to the best one with a short timeout, moving to the next on decline or timeout.
- A *trip service* owns the trip state machine (requested, matched, arriving, in progress, completed) in a durable database, and publishes events to Kafka for pricing, notifications and analytics.

**Consistency.** To avoid assigning one driver to two trips, I take a short lock or do an atomic compare-and-set on the driver's status (available to reserved), for example Redis `SET NX` with a TTL, and only then send the offer.

**Failure handling.** Location data is ephemeral, so losing a node only costs a few seconds until drivers report again. Trip state is durable and every state transition is idempotent, so retries from mobile clients are safe.

**Scaling.** Partition by geography, because almost all queries are local. Hot cells in city centres can be split into smaller cells."

@@@ sd-wallet | Design a wallet / payment ledger that never loses or double-counts money. | arch | system-design,grab,payments | qa | System design
"**Requirements.** Top up, pay and transfer between users; balances must always be correct; every request may be retried; full audit trail.

**Data model.** A double-entry ledger: each transaction writes at least two immutable entries, a debit and a credit, that sum to zero. The balance is derived from entries, and I keep a cached balance column updated in the same database transaction for fast reads. Amounts are stored as integers in the smallest currency unit, never floating point.

**Correctness.**

- *Idempotency:* every request carries an idempotency key stored with a unique constraint in the same transaction, so a retry returns the original result instead of charging twice.
- *Concurrency:* update the balance with a conditional statement, such as `UPDATE wallet SET balance = balance - :amt WHERE id = :id AND balance >= :amt`, or with optimistic locking on a version column. This prevents overdrafts under concurrent payments.
- *Transfers across shards:* if both wallets are in one database, use one local transaction. Across services or shards, use a saga with a pending state and compensation, never a distributed transaction.

**External payment providers.** Calls are asynchronous: create a pending record, call the provider with our idempotency key, and confirm through the callback or by polling. A daily reconciliation job compares our ledger with provider reports and flags mismatches.

**Events.** Use the outbox pattern to publish 'payment completed' events to Kafka, so downstream services see every committed transaction exactly once in effect.

**Scale.** Shard by wallet ID. Hot merchant wallets can be split into sub-accounts that are summed for reads."

@@@ sources | Nguồn tham khảo | guide | huong-dan | guide
Các bài trong mục Go, Security, AWS, PostgreSQL internals và một phần System design được viết lại bằng lời của kho này, dựa trên danh sách chủ đề và câu hỏi phỏng vấn của [knowledge base của nathan.huynh](https://minhnhat97kg.github.io/docsify/). Mỗi bài có link "Tham khảo thêm" tới bài gốc để đọc chi tiết, kèm code Go.

Thông tin quy trình phỏng vấn trong mục Công ty lấy từ báo cáo ứng viên trên Glassdoor, Taro và tin tuyển dụng; link nằm ngay trong từng trang công ty. Quy trình thực tế có thể khác, hãy hỏi lại recruiter.
