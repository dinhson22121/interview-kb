@@@ jn-versions | Các phiên bản Java LTS và tính năng chính của từng bản? Nên dùng bản nào? / What are the Java LTS versions, their headline features, and which should you use? | java-new | java-version,lts | qa | Tổng quan phiên bản
### Tiếng Việt

**Nhịp phát hành:** từ Java 10, cứ **6 tháng có một bản** (tháng 3 và tháng 9). Cứ **2 năm có một bản LTS** (hỗ trợ dài hạn). Bản không phải LTS chỉ được cập nhật khoảng 6 tháng, nên production gần như luôn chạy LTS.

| Bản | Năm | Loại | Tính năng đáng nhớ |
|---|---|---|---|
| **8** | 2014 | LTS | Lambda, Stream API, `Optional`, `java.time`, default method |
| **11** | 2018 | LTS | `var` (từ 10), `HttpClient` mới, `String.isBlank/strip/lines/repeat`, chạy file `.java` trực tiếp |
| **17** | 2021 | LTS | **Records**, **sealed classes**, **text blocks**, **switch expression**, pattern matching cho `instanceof`, NPE dễ đọc |
| **21** | 2023 | LTS | **Virtual threads**, **record patterns**, **pattern matching cho switch**, **sequenced collections**, Generational ZGC |
| **25** | 2025 | LTS | **Scoped values**, file nguồn gọn và `void main()` không cần class, `import module`, code trước `super(...)` trong constructor, compact object headers, AOT cache cải tiến khởi động |
| 26 | 03/2026 | Thường | HTTP/3 cho `HttpClient`, AOT object caching với mọi GC, chuẩn bị cho "final thật sự là final", G1 nhanh hơn |
| 27 | 09/2026 | Thường | **G1 là GC mặc định ở mọi môi trường**, **compact object headers bật mặc định**, trao đổi khóa hậu lượng tử (post-quantum) cho TLS 1.3 |
| 28 | 03/2027 | Thường | Dự kiến có những tính năng đầu tiên của Project Valhalla (value objects) |

**Preview, incubator là gì:** tính năng **preview** đã thiết kế xong nhưng còn có thể đổi, phải bật bằng `--enable-preview`. **Incubator** là API thử nghiệm (ví dụ Vector API). Không dùng hai loại này ở production.

Ở bản 27, structured concurrency, lazy constants và primitive types trong pattern **vẫn đang preview**.

**Nên dùng bản nào:**
- **Dự án mới: Java 25** (LTS mới nhất). Spring Boot 4 hỗ trợ tốt và khuyến nghị bản này.
- **Dự án đang chạy:** tối thiểu **Java 21**. Spring Boot 3 và 4 đều yêu cầu tối thiểu Java 17.
- **Còn ở Java 8 hoặc 11:** nâng lên, vì các bản này đã hết hoặc sắp hết hỗ trợ miễn phí, và đang bỏ lỡ virtual threads cùng những cải tiến GC lớn.

**Câu trả lời mẫu khi được hỏi "Bạn dùng Java bản nào?":** *"Dự án gần nhất của tôi chạy Java [17/21]. Tôi đã dùng records cho DTO, switch expression và pattern matching, và [virtual threads cho các service nặng I/O]. Nếu bắt đầu dự án mới hôm nay, tôi chọn Java 25 vì là LTS mới nhất."* Nói đúng bản bạn đã dùng thật.

### English

**Release cadence:** since Java 10 there's **a release every 6 months** (March and September). **Every 2 years one release is LTS** (long-term support). Non-LTS releases get about 6 months of updates, so production almost always runs an LTS.

| Version | Year | Type | Notable features |
|---|---|---|---|
| **8** | 2014 | LTS | Lambdas, the Stream API, `Optional`, `java.time`, default methods |
| **11** | 2018 | LTS | `var` (from 10), the new `HttpClient`, `String.isBlank/strip/lines/repeat`, running a `.java` file directly |
| **17** | 2021 | LTS | **Records**, **sealed classes**, **text blocks**, **switch expressions**, pattern matching for `instanceof`, helpful NPE messages |
| **21** | 2023 | LTS | **Virtual threads**, **record patterns**, **pattern matching for switch**, **sequenced collections**, Generational ZGC |
| **25** | 2025 | LTS | **Scoped values**, compact source files and `void main()` without a class, `import module`, code before `super(...)` in constructors, compact object headers, an improved AOT cache for startup |
| 26 | 03/2026 | Regular | HTTP/3 for `HttpClient`, AOT object caching with any GC, preparing to make final mean final, faster G1 |
| 27 | 09/2026 | Regular | **G1 as the default GC in all environments**, **compact object headers on by default**, post-quantum hybrid key exchange for TLS 1.3 |
| 28 | 03/2027 | Regular | Expected to bring the first Project Valhalla features (value objects) |

**What preview and incubator mean:** a **preview** feature is fully designed but may still change, and must be enabled with `--enable-preview`. An **incubator** is an experimental API (for example the Vector API). Don't use either in production.

As of 27, structured concurrency, lazy constants and primitive types in patterns are **still in preview**.

**Which version to use:**
- **New projects: Java 25** (the latest LTS). Spring Boot 4 supports it well and recommends it.
- **Running projects:** at least **Java 21**. Spring Boot 3 and 4 both require Java 17 at minimum.
- **Still on Java 8 or 11:** upgrade, because free support for these has ended or is ending, and you're missing virtual threads and major GC improvements.

**A model answer to "Which Java version do you use?":** *"My last project ran Java [17/21]. I used records for DTOs, switch expressions and pattern matching, and [virtual threads for I/O-heavy services]. If I started a new project today, I'd pick Java 25 because it's the latest LTS."* Name only the versions you've really used.

@@@ jn-records | Record là gì? Khi nào dùng, khi nào không? / What is a record, and when should and shouldn't you use one? | java-new | records,java17 | qa | Java 14–17
### Tiếng Việt

**Record** (chính thức từ Java 16) là class chỉ để **chứa dữ liệu bất biến**. Một dòng khai báo, compiler tự sinh: constructor đầy đủ, accessor (`name()`, không có tiền tố `get`), `equals`, `hashCode`, `toString`.

```java
public record Money(BigDecimal amount, String currency) {
    // Compact constructor: kiểm tra và chuẩn hóa, không cần gán field
    public Money {
        Objects.requireNonNull(amount);
        if (amount.signum() < 0) throw new IllegalArgumentException("amount < 0");
        currency = currency.toUpperCase();
    }
    // Được thêm method và static factory
    public Money plus(Money other) { return new Money(amount.add(other.amount), currency); }
    public static Money vnd(long v) { return new Money(BigDecimal.valueOf(v), "VND"); }
}
```

**Đặc điểm:**
- Field là `private final`; record là `final` (không kế thừa được) nhưng **implement interface được**.
- Không có setter; muốn đổi giá trị thì tạo bản mới (kiểu "wither" như `plus` ở trên).
- **Bất biến nông (shallow):** nếu field là `List` thì list bên trong vẫn sửa được. Dùng `List.copyOf(...)` trong compact constructor.

**Dùng khi:**
- DTO request và response, sự kiện Kafka, value object (`Money`, `Email`), key ghép trong `Map`, kết quả trung gian trong stream.
- Projection của Spring Data JPA: `List<OrderSummary> findByStatus(...)` với `OrderSummary` là record.
- `@ConfigurationProperties` của Spring Boot (bind qua constructor).
- Jackson hỗ trợ record từ 2.12.

**Không dùng khi:**
- **JPA entity:** entity cần constructor không tham số, field thay đổi được và proxy lazy loading (kế thừa class), mà record không đáp ứng được.
- Object có trạng thái thay đổi theo vòng đời (ví dụ đơn hàng đi qua nhiều trạng thái).

**Record hay Lombok `@Value`/`@Data`:** record là tính năng của ngôn ngữ, không cần thư viện hay annotation processor, và hoạt động với record patterns (Java 21). Lombok vẫn hữu ích cho `@Builder` hoặc class cần thay đổi được.

### English

A **record** (final since Java 16) is a class meant only to **hold immutable data**. One line of declaration and the compiler generates: the canonical constructor, accessors (`name()`, no `get` prefix), `equals`, `hashCode` and `toString`.

```java
public record Money(BigDecimal amount, String currency) {
    // Compact constructor: validate and normalize, no field assignments needed
    public Money {
        Objects.requireNonNull(amount);
        if (amount.signum() < 0) throw new IllegalArgumentException("amount < 0");
        currency = currency.toUpperCase();
    }
    // Methods and static factories are allowed
    public Money plus(Money other) { return new Money(amount.add(other.amount), currency); }
    public static Money vnd(long v) { return new Money(BigDecimal.valueOf(v), "VND"); }
}
```

**Characteristics:**
- Fields are `private final`; a record is `final` (can't be extended) but **can implement interfaces**.
- No setters; to change a value you create a new instance ("withers" like `plus` above).
- **Shallow immutability:** if a field is a `List`, the list itself can still be modified. Use `List.copyOf(...)` in the compact constructor.

**Use them for:**
- Request and response DTOs, Kafka events, value objects (`Money`, `Email`), composite `Map` keys, intermediate results in streams.
- Spring Data JPA projections: `List<OrderSummary> findByStatus(...)` with `OrderSummary` as a record.
- Spring Boot `@ConfigurationProperties` (constructor binding).
- Jackson supports records since 2.12.

**Don't use them for:**
- **JPA entities:** entities need a no-arg constructor, mutable fields and lazy-loading proxies (subclassing), none of which records allow.
- Objects whose state changes over their lifecycle (for example an order moving through statuses).

**Records vs Lombok `@Value`/`@Data`:** records are a language feature, need no library or annotation processor, and work with record patterns (Java 21). Lombok is still useful for `@Builder` or mutable classes.

@@@ jn-sealed-pattern | Sealed class và pattern matching (instanceof, switch, record pattern) dùng thế nào? / How do sealed classes and pattern matching (instanceof, switch, record patterns) work together? | java-new | sealed,pattern-matching,java21 | qa | Java 14–17
### Tiếng Việt

**1. Pattern matching cho `instanceof` (Java 16):** kiểm tra và ép kiểu trong một bước.

```java
// Cũ
if (obj instanceof String) { String s = (String) obj; use(s.length()); }
// Mới
if (obj instanceof String s && !s.isBlank()) { use(s.length()); }
```

**2. Sealed class (Java 17):** giới hạn **chính xác những class nào được kế thừa**. Dùng để mô hình hóa một tập trạng thái hoặc kết quả **đóng**.

```java
public sealed interface PaymentResult permits Success, Declined, Pending {}
public record Success(String txId, BigDecimal amount) implements PaymentResult {}
public record Declined(String reason)                implements PaymentResult {}
public record Pending(Instant retryAt)                implements PaymentResult {}
```

Class con phải là `final`, `sealed`, hoặc `non-sealed`.

**3. Pattern matching cho switch và record pattern (Java 21):** switch theo kiểu, **bóc tách luôn field** của record, thêm điều kiện bằng `when`.

```java
String describe(PaymentResult r) {
    return switch (r) {
        case Success(var txId, var amount) when amount.compareTo(LIMIT) > 0 -> "Large payment " + txId;
        case Success(var txId, var amount) -> "Paid " + amount + " (" + txId + ")";
        case Declined(var reason)          -> "Declined: " + reason;
        case Pending p                     -> "Retry at " + p.retryAt();
        // KHÔNG cần default: compiler biết đã đủ mọi trường hợp
    };
}
```

**Vì sao kết hợp này mạnh:**
- **Kiểm tra đầy đủ lúc compile (exhaustiveness):** thêm `Refunded` vào `permits` thì mọi `switch` thiếu nhánh **báo lỗi compile**, thay vì lỗi lúc chạy như khi có `default`.
- Thay thế mẫu Visitor dài dòng và chuỗi `if-else instanceof`.
- Mô hình hóa kiểu "tổng" (algebraic data types): kết quả API, sự kiện domain, lệnh trong state machine.

**Lưu ý thêm:**
- `case null ->` được phép trong switch mới; không có thì switch ném NPE như trước.
- Thứ tự `case` có ý nghĩa: case cụ thể hơn (có `when`) phải đứng trước. Đặt sai thì compile báo "dominated".
- Unnamed pattern `_` (chính thức từ Java 22) cho field không dùng: `case Declined(_) -> ...`.
- Primitive types trong pattern (`case int i`) vẫn là preview ở Java 27.

### English

**1. Pattern matching for `instanceof` (Java 16):** test and cast in one step.

```java
// Old
if (obj instanceof String) { String s = (String) obj; use(s.length()); }
// New
if (obj instanceof String s && !s.isBlank()) { use(s.length()); }
```

**2. Sealed classes (Java 17):** restrict **exactly which classes may extend a type**. Use them to model a **closed** set of states or results.

```java
public sealed interface PaymentResult permits Success, Declined, Pending {}
public record Success(String txId, BigDecimal amount) implements PaymentResult {}
public record Declined(String reason)                implements PaymentResult {}
public record Pending(Instant retryAt)                implements PaymentResult {}
```

Subclasses must be `final`, `sealed` or `non-sealed`.

**3. Pattern matching for switch and record patterns (Java 21):** switch on type, **destructure the record's fields** directly, and add conditions with `when`.

```java
String describe(PaymentResult r) {
    return switch (r) {
        case Success(var txId, var amount) when amount.compareTo(LIMIT) > 0 -> "Large payment " + txId;
        case Success(var txId, var amount) -> "Paid " + amount + " (" + txId + ")";
        case Declined(var reason)          -> "Declined: " + reason;
        case Pending p                     -> "Retry at " + p.retryAt();
        // NO default needed: the compiler knows every case is covered
    };
}
```

**Why the combination is powerful:**
- **Compile-time exhaustiveness checks:** add `Refunded` to `permits` and every `switch` missing a branch **fails to compile**, instead of failing at runtime as it would with a `default`.
- It replaces verbose Visitor patterns and `if-else instanceof` chains.
- It models "sum" types (algebraic data types): API results, domain events, state-machine commands.

**More details:**
- `case null ->` is allowed in the new switch; without it the switch throws an NPE as before.
- `case` order matters: more specific cases (with `when`) must come first. Getting it wrong is a "dominated" compile error.
- The unnamed pattern `_` (final since Java 22) for unused fields: `case Declined(_) -> ...`.
- Primitive types in patterns (`case int i`) are still in preview in Java 27.

@@@ jn-small-features | Những tính năng nhỏ hay dùng từ Java 9 đến 21 là gì? / What small, everyday features arrived between Java 9 and 21? | java-new | java-version,collections | qa | Java 9–21
### Tiếng Việt

| Tính năng | Bản | Ví dụ |
|---|---|---|
| Factory cho collection bất biến | 9 | `List.of(1, 2)`, `Set.of("a")`, `Map.of("k", 1)`. **Không cho phép `null`**, sửa sẽ ném `UnsupportedOperationException` |
| `Optional` bổ sung | 9–11 | `ifPresentOrElse`, `or`, `stream()`, `isEmpty()`, `orElseThrow()` |
| `var` (suy luận kiểu biến local) | 10 | `var orders = new ArrayList<Order>();`. Chỉ cho biến local; dùng khi kiểu đã rõ ở vế phải |
| `List.copyOf`, `Collectors.toUnmodifiableList` | 10 | Bản sao bất biến |
| `HttpClient` chuẩn | 11 | Hỗ trợ HTTP/2, async; HTTP/3 từ Java 26 |
| `String` mới | 11–15 | `isBlank()`, `strip()` (hiểu Unicode, khác `trim()`), `lines()`, `repeat(n)`, `formatted(...)` |
| **Switch expression** | 14 | `int days = switch (m) { case FEB -> 28; case APR, JUN -> 30; default -> 31; };` Không rơi xuống case sau (fall-through), dùng `yield` trong block |
| **Text block** | 15 | Chuỗi nhiều dòng bằng `"""`, tiện cho SQL, JSON trong test |
| **NPE dễ đọc** | 14 (bật mặc định 15) | `Cannot invoke "Address.city()" because the return value of "User.address()" is null` |
| `Stream.toList()` | 16 | Ngắn hơn `collect(Collectors.toList())`, nhưng trả list **bất biến** |
| `mapMulti`, `takeWhile`, `dropWhile`, `iterate` có điều kiện dừng | 9–16 | Tiện ích cho stream |
| **Sequenced collections** | 21 | `list.getFirst()`, `getLast()`, `reversed()`, `addFirst`; `LinkedHashMap.firstEntry()`, `pollLastEntry()` |
| `Math.clamp`, `StringBuilder.repeat`, `String.indexOf(ch, from, to)` | 21 | Tiện ích nhỏ |
| **Stream gatherers** | 24 | Toán tử trung gian tự định nghĩa: `stream.gather(Gatherers.windowFixed(3))` để chia cửa sổ cố định |

**Bẫy hay bị hỏi:**
- `Stream.toList()` trả list bất biến, còn `Collectors.toList()` trả `ArrayList` sửa được. Đổi qua lại có thể làm code đang chạy bị lỗi.
- `List.of(...)` ném NPE khi gặp `null`, kể cả `contains(null)`.
- `var` **không** làm Java thành ngôn ngữ kiểu động: kiểu vẫn cố định lúc compile.

### English

| Feature | Version | Example |
|---|---|---|
| Immutable collection factories | 9 | `List.of(1, 2)`, `Set.of("a")`, `Map.of("k", 1)`. **No `null` allowed**; modifying throws `UnsupportedOperationException` |
| `Optional` additions | 9–11 | `ifPresentOrElse`, `or`, `stream()`, `isEmpty()`, `orElseThrow()` |
| `var` (local variable type inference) | 10 | `var orders = new ArrayList<Order>();`. Local variables only; use it when the type is obvious from the right-hand side |
| `List.copyOf`, `Collectors.toUnmodifiableList` | 10 | Immutable copies |
| Standard `HttpClient` | 11 | HTTP/2 and async support; HTTP/3 since Java 26 |
| New `String` methods | 11–15 | `isBlank()`, `strip()` (Unicode-aware, unlike `trim()`), `lines()`, `repeat(n)`, `formatted(...)` |
| **Switch expressions** | 14 | `int days = switch (m) { case FEB -> 28; case APR, JUN -> 30; default -> 31; };` No fall-through; use `yield` inside a block |
| **Text blocks** | 15 | Multi-line strings with `"""`, handy for SQL and JSON in tests |
| **Helpful NPEs** | 14 (on by default in 15) | `Cannot invoke "Address.city()" because the return value of "User.address()" is null` |
| `Stream.toList()` | 16 | Shorter than `collect(Collectors.toList())`, but returns an **immutable** list |
| `mapMulti`, `takeWhile`, `dropWhile`, `iterate` with a stop condition | 9–16 | Stream utilities |
| **Sequenced collections** | 21 | `list.getFirst()`, `getLast()`, `reversed()`, `addFirst`; `LinkedHashMap.firstEntry()`, `pollLastEntry()` |
| `Math.clamp`, `StringBuilder.repeat`, `String.indexOf(ch, from, to)` | 21 | Small utilities |
| **Stream gatherers** | 24 | Custom intermediate operations: `stream.gather(Gatherers.windowFixed(3))` for fixed-size windows |

**Commonly asked traps:**
- `Stream.toList()` returns an immutable list, while `Collectors.toList()` returns a mutable `ArrayList`. Swapping one for the other can break working code.
- `List.of(...)` throws an NPE on `null`, even for `contains(null)`.
- `var` does **not** make Java dynamically typed: the type is still fixed at compile time.

@@@ jn-virtual-threads | Virtual threads hoạt động thế nào? Bẫy khi dùng là gì? / How do virtual threads work, and what are the pitfalls? | java-new | virtual-threads,concurrency,java21 | qa | Java 21
### Tiếng Việt

*Xem thêm câu ngắn hơn: [Virtual threads là gì](#concurrency-16).*

**Vấn đề cũ:** mỗi platform thread là một thread của hệ điều hành, tốn khoảng 1 MB stack và chi phí chuyển ngữ cảnh. Server thread-per-request với 200 thread thì tối đa khoảng 200 request đồng thời, dù phần lớn thời gian các thread chỉ **ngồi chờ I/O** (DB, HTTP).

**Virtual thread (Java 21):** thread do **JVM quản lý**, rất nhẹ (vài trăm byte đến vài KB), có thể tạo **hàng triệu** cái. Chúng chạy trên một nhóm nhỏ **carrier thread** (ForkJoinPool, mặc định bằng số CPU). Khi virtual thread **chặn ở I/O**, JVM **gỡ nó khỏi carrier** (unmount) và cho virtual thread khác chạy. I/O xong thì gắn lại.

Kết quả: viết code **đồng bộ, dễ đọc**, nhưng đạt được throughput gần như code reactive.

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Price>> fs = suppliers.stream()
        .map(s -> executor.submit(() -> client.fetchPrice(s)))   // mỗi task một virtual thread
        .toList();
    // ...
}
// Spring Boot 3.2+: spring.threads.virtual.enabled=true
// → Tomcat, @Async, @Scheduled, Kafka listener dùng virtual threads
```

**Hợp với:** service **nặng I/O**, nhiều request đồng thời, gọi DB và HTTP. **Không giúp gì** cho tác vụ **nặng CPU** (tính toán, nén, mã hóa), vì số CPU không đổi.

**Bẫy:**

| Bẫy | Giải thích | Cách xử lý |
|---|---|---|
| **Pinning** | Ở Java 21–23, virtual thread chặn bên trong `synchronized` sẽ **dính chặt** vào carrier, không gỡ ra được. Vài cái như vậy là hết carrier | **Java 24 (JEP 491) đã sửa** cho `synchronized`. Ở Java 21 thì đổi sang `ReentrantLock`. Native call (JNI) vẫn gây pinning. Phát hiện bằng JFR event `jdk.VirtualThreadPinned` |
| **Không pool** virtual thread | Chúng rẻ, tạo mới cho mỗi task | Dùng `newVirtualThreadPerTaskExecutor()`, không dùng fixed pool |
| **Tài nguyên phía sau vẫn có giới hạn** | 10.000 virtual thread cùng gọi DB, mà connection pool chỉ có 20 | Giới hạn bằng `Semaphore`, rate limit; cấu hình pool hợp lý. Virtual thread **không** làm DB mạnh hơn |
| **`ThreadLocal`** | Hàng triệu thread, mỗi cái một bản ThreadLocal, nên tốn bộ nhớ; cache đắt tiền đặt trong ThreadLocal mất tác dụng | Dùng **Scoped values** (Java 25); tránh cache trong ThreadLocal |
| Đo đạc | Thread dump truyền thống không còn phù hợp | `jcmd <pid> Thread.dump_to_file -format=json` |

**Câu trả lời mẫu:** *"Virtual threads cho phép giữ mô hình thread-per-request đơn giản mà vẫn phục vụ hàng chục nghìn request chờ I/O. Tôi bật bằng một property trong Spring Boot, nhưng vẫn giới hạn đồng thời ở chỗ gọi DB hoặc API ngoài, và ở Java 21 thì kiểm tra pinning do `synchronized`."*

### English

*See also the shorter question: [What are virtual threads](#concurrency-16).*

**The old problem:** each platform thread is an operating-system thread, costing about 1 MB of stack plus context-switch overhead. A thread-per-request server with 200 threads handles at most about 200 concurrent requests, even though most of the time those threads are just **waiting on I/O** (DB, HTTP).

**Virtual threads (Java 21):** threads **managed by the JVM**, very light (hundreds of bytes to a few KB), so you can create **millions**. They run on a small set of **carrier threads** (a ForkJoinPool, sized to the CPU count by default). When a virtual thread **blocks on I/O**, the JVM **unmounts it from the carrier** and runs another virtual thread. When the I/O completes, it's mounted again.

The result: you write **synchronous, readable** code and get throughput close to reactive code.

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Price>> fs = suppliers.stream()
        .map(s -> executor.submit(() -> client.fetchPrice(s)))   // one virtual thread per task
        .toList();
    // ...
}
// Spring Boot 3.2+: spring.threads.virtual.enabled=true
// → Tomcat, @Async, @Scheduled and Kafka listeners use virtual threads
```

**Good for:** **I/O-heavy** services with many concurrent requests calling databases and HTTP APIs. **No help** for **CPU-heavy** work (computation, compression, encryption), because the number of CPUs doesn't change.

**Pitfalls:**

| Pitfall | Explanation | How to handle it |
|---|---|---|
| **Pinning** | In Java 21–23, a virtual thread blocking inside `synchronized` gets **pinned** to its carrier and can't be unmounted. A few of those and the carriers run out | **Java 24 (JEP 491) fixed this** for `synchronized`. On Java 21, switch to `ReentrantLock`. Native calls (JNI) still pin. Detect it with the JFR event `jdk.VirtualThreadPinned` |
| **Pooling** virtual threads | They're cheap; create a new one per task | Use `newVirtualThreadPerTaskExecutor()`, not a fixed pool |
| **Downstream resources are still limited** | 10,000 virtual threads call the DB at once, but the connection pool has 20 connections | Limit with a `Semaphore` or rate limiting, and size pools sensibly. Virtual threads **don't** make the database stronger |
| **`ThreadLocal`** | Millions of threads, each with its own ThreadLocal copy, waste memory; expensive objects cached in ThreadLocals stop paying off | Use **scoped values** (Java 25); avoid caching in ThreadLocals |
| Observability | Traditional thread dumps don't fit well | `jcmd <pid> Thread.dump_to_file -format=json` |

**A model answer:** *"Virtual threads let us keep the simple thread-per-request model while serving tens of thousands of requests waiting on I/O. I enable them with one property in Spring Boot, but I still limit concurrency at calls to the database or external APIs, and on Java 21 I check for pinning caused by `synchronized`."*

@@@ jn-scoped-structured | Scoped values và structured concurrency là gì? / What are scoped values and structured concurrency? | java-new | virtual-threads,concurrency,java25 | qa | Java 25+
### Tiếng Việt

Cả hai thuộc Project Loom, được thiết kế để đi cùng virtual threads.

**1. Scoped values (chính thức ở Java 25, JEP 506): thay `ThreadLocal`** để truyền ngữ cảnh (user hiện tại, request id, tenant) xuống các tầng sâu mà không phải thêm tham số.

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// Ở filter hoặc controller: gắn giá trị cho phạm vi của lời gọi
ScopedValue.where(CURRENT_USER, user).run(() -> orderService.placeOrder(cmd));

// Ở tầng sâu bất kỳ trong lời gọi đó
User u = CURRENT_USER.get();
```

| | `ThreadLocal` | `ScopedValue` |
|---|---|---|
| Thay đổi | `set()` lúc nào cũng được | **Bất biến** trong phạm vi; muốn đổi thì mở phạm vi lồng mới |
| Thời gian sống | Đến khi `remove()`. **Quên gọi** thì rò rỉ dữ liệu sang request sau khi thread được tái sử dụng trong pool | **Tự hết** khi `run()` kết thúc |
| Chi phí với triệu thread | Cao | Thấp, chia sẻ được cho thread con |

**2. Structured concurrency (vẫn preview ở Java 27):** coi một nhóm task song song là **một đơn vị**: cùng bắt đầu, cùng kết thúc, lỗi một cái thì hủy những cái còn lại.

```java
// Lấy user và đơn hàng song song; một cái lỗi thì cái kia bị hủy
try (var scope = StructuredTaskScope.open()) {          // API bản preview gần đây
    Subtask<User>        user   = scope.fork(() -> userClient.get(id));
    Subtask<List<Order>> orders = scope.fork(() -> orderClient.list(id));
    scope.join();                                       // chờ cả hai, ném lỗi nếu một cái thất bại
    return new Profile(user.get(), orders.get());
}
```

**Vì sao tốt hơn `CompletableFuture` hoặc `ExecutorService` tự quản:**
- Không có **task mồ côi**: hết khối `try` thì mọi task con chắc chắn đã xong hoặc đã bị hủy.
- **Tự hủy khi lỗi:** user service lỗi thì không phải ngồi chờ order service vô ích.
- Thread dump thể hiện **quan hệ cha con**, dễ debug.
- Scoped values được **kế thừa tự động** vào các task con.

**Khi phỏng vấn:** nói rõ structured concurrency **vẫn là preview** (API đã đổi qua nhiều vòng), nên production hiện dùng `CompletableFuture` hoặc virtual-thread executor, và chuyển sang khi API chính thức.

### English

Both are part of Project Loom and are designed to go with virtual threads.

**1. Scoped values (final in Java 25, JEP 506): a replacement for `ThreadLocal`** for passing context (current user, request id, tenant) to deep layers without adding parameters.

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// In a filter or controller: bind the value for the scope of the call
ScopedValue.where(CURRENT_USER, user).run(() -> orderService.placeOrder(cmd));

// At any depth inside that call
User u = CURRENT_USER.get();
```

| | `ThreadLocal` | `ScopedValue` |
|---|---|---|
| Mutability | `set()` any time | **Immutable** within the scope; to change it, open a new nested scope |
| Lifetime | Until `remove()`. **Forget it** and data leaks into the next request when a pooled thread is reused | **Ends automatically** when `run()` returns |
| Cost with millions of threads | High | Low, shareable with child threads |

**2. Structured concurrency (still in preview in Java 27):** treats a group of parallel tasks as **one unit**: they start together and finish together, and if one fails the others are cancelled.

```java
// Fetch the user and their orders in parallel; if one fails, the other is cancelled
try (var scope = StructuredTaskScope.open()) {          // recent preview API
    Subtask<User>        user   = scope.fork(() -> userClient.get(id));
    Subtask<List<Order>> orders = scope.fork(() -> orderClient.list(id));
    scope.join();                                       // waits for both, throws if one failed
    return new Profile(user.get(), orders.get());
}
```

**Why it beats `CompletableFuture` or a hand-managed `ExecutorService`:**
- No **orphaned tasks**: when the `try` block ends, every subtask has definitely finished or been cancelled.
- **Automatic cancellation on failure:** if the user service fails, you don't wait pointlessly for the order service.
- Thread dumps show the **parent-child relationship**, which makes debugging easier.
- Scoped values are **inherited automatically** by subtasks.

**In an interview:** say clearly that structured concurrency **is still in preview** (the API has changed across several rounds), so production code today uses `CompletableFuture` or a virtual-thread executor, and you'd switch once the API is final.

@@@ jn-java25 | Java 25 (LTS) có gì mới đáng chú ý? / What's notable in Java 25 (LTS)? | java-new | java25,lts | qa | Java 25+
### Tiếng Việt

**Ngôn ngữ, cho code gọn hơn:**

| Tính năng | JEP | Ví dụ, ý nghĩa |
|---|---|---|
| **Compact source files và instance main** | 512 | File chỉ cần `void main() { IO.println("Hi"); }`, không cần `public class` và `static`. Tiện cho script, bài tập, công cụ nhỏ |
| **Module import declarations** | 511 | `import module java.base;` để import mọi package public của một module bằng một dòng |
| **Flexible constructor bodies** | 513 | Được viết code (kiểm tra tham số) **trước** `super(...)` hoặc `this(...)`, miễn là không dùng `this` |

```java
class Employee extends Person {
    Employee(String name, int age) {
        if (age < 18) throw new IllegalArgumentException("too young");  // trước đây phải đặt sau super()
        super(name);
    }
}
```

**Thư viện và đồng thời:**
- **Scoped values** chính thức (JEP 506). Xem [Scoped values và structured concurrency](#jn-scoped-structured).
- **Key Derivation Function API** (JEP 510), ví dụ HKDF, phục vụ mật mã hiện đại.
- Structured concurrency và stable values (sau đổi tên thành lazy constants) vẫn là preview.

**Hiệu năng và vận hành:**
- **Compact object headers** (JEP 519): header object giảm từ 12–16 byte xuống **8 byte**, nên **giảm heap khoảng 10–20%** với ứng dụng có nhiều object nhỏ. Ở Java 25 phải bật bằng `-XX:+UseCompactObjectHeaders`; **Java 27 bật mặc định**.
- **AOT cache (Project Leyden)** (JEP 514, 515): chạy thử một lần để ghi lại class đã nạp và profile method, các lần sau **khởi động và đạt tốc độ tối đa nhanh hơn**. Hữu ích cho container cần scale nhanh. Từ Java 26, AOT object caching dùng được với mọi GC.
- **Generational Shenandoah** chính thức (JEP 521).
- **JFR:** đo thời gian CPU và theo dõi thời gian gọi method chính xác hơn.

**Những thứ bị bỏ:** port x86 32-bit.

**Từ 25 đến 27, những điểm đáng biết:** HTTP/3 cho `HttpClient` (26), chuẩn bị cấm đổi field `final` bằng reflection (26), G1 là GC mặc định ở mọi môi trường (27), compact object headers bật mặc định (27), TLS 1.3 có trao đổi khóa lai hậu lượng tử (27).

**Khi phỏng vấn:** không cần thuộc số JEP. Nên nêu 2–3 điểm có ý nghĩa với backend: *"Java 25 là LTS mới, scoped values thay ThreadLocal khi dùng virtual threads, compact object headers giảm bộ nhớ, và AOT cache cải thiện thời gian khởi động trong Kubernetes."*

### English

**Language, for more concise code:**

| Feature | JEP | Example, meaning |
|---|---|---|
| **Compact source files and instance main** | 512 | A file can be just `void main() { IO.println("Hi"); }`, no `public class` or `static`. Handy for scripts, exercises and small tools |
| **Module import declarations** | 511 | `import module java.base;` imports every public package of a module in one line |
| **Flexible constructor bodies** | 513 | You can write code (argument validation) **before** `super(...)` or `this(...)`, as long as it doesn't use `this` |

```java
class Employee extends Person {
    Employee(String name, int age) {
        if (age < 18) throw new IllegalArgumentException("too young");  // previously had to go after super()
        super(name);
    }
}
```

**Libraries and concurrency:**
- **Scoped values** are final (JEP 506). See [Scoped values and structured concurrency](#jn-scoped-structured).
- The **Key Derivation Function API** (JEP 510), for example HKDF, for modern cryptography.
- Structured concurrency and stable values (later renamed lazy constants) remain in preview.

**Performance and operations:**
- **Compact object headers** (JEP 519): object headers shrink from 12–16 bytes to **8 bytes**, **cutting heap use by about 10–20%** in applications with many small objects. In Java 25 you enable them with `-XX:+UseCompactObjectHeaders`; **Java 27 turns them on by default**.
- **AOT cache (Project Leyden)** (JEP 514, 515): a training run records loaded classes and method profiles, so later runs **start up and reach peak speed faster**. Useful for containers that need to scale quickly. Since Java 26, AOT object caching works with any GC.
- **Generational Shenandoah** is final (JEP 521).
- **JFR:** more accurate CPU-time profiling and method timing.

**Removed:** the 32-bit x86 port.

**Worth knowing from 25 to 27:** HTTP/3 for `HttpClient` (26), groundwork to stop reflection from changing `final` fields (26), G1 as the default GC in all environments (27), compact object headers on by default (27), and post-quantum hybrid key exchange in TLS 1.3 (27).

**In an interview:** you don't need the JEP numbers. Name 2–3 points that matter for backend work: *"Java 25 is the new LTS, scoped values replace ThreadLocal when using virtual threads, compact object headers reduce memory, and the AOT cache improves startup time in Kubernetes."*

@@@ sn-versions | Spring Boot 2, 3, 4 khác nhau thế nào? Nâng cấp cần chú ý gì? / How do Spring Boot 2, 3 and 4 differ, and what should you watch for when upgrading? | spring-new | spring-boot,migration | qa | Tổng quan phiên bản
### Tiếng Việt

| | Spring Boot 2.x | Spring Boot 3.x | Spring Boot 4.x |
|---|---|---|---|
| Ra mắt | 2018 | 11/2022 | 11/2025 (4.1 vào 06/2026) |
| Spring Framework | 5 | 6 | 7 |
| Java tối thiểu | 8 | **17** | 17 (khuyến nghị **25**) |
| Jakarta EE | `javax.*` | **`jakarta.*`** (EE 9/10) | Jakarta EE 11 (Servlet 6.1, JPA 3.2) |
| Hibernate | 5 | 6 | 7 |
| Jackson | 2 | 2 | **3** |
| Điểm nhấn | | AOT và GraalVM native, Observation API (Micrometer), ProblemDetail, HTTP interface, virtual threads (3.2) | API versioning, `@Retryable`/`@ConcurrencyLimit` trong core, JSpecify null safety, chia nhỏ module auto-config, HTTP service client groups |

**Nâng cấp 2 lên 3, phần tốn công nhất:**
1. Nâng Java lên 17 trước.
2. Đổi **`javax.*` sang `jakarta.*`** (persistence, servlet, validation). Dùng **OpenRewrite** (`rewrite-spring`) để sửa tự động.
3. Thư viện bên thứ ba phải có bản hỗ trợ Jakarta.
4. Spring Security 6: bỏ `WebSecurityConfigurerAdapter`, chuyển sang bean `SecurityFilterChain`.
5. Spring Cloud Sleuth bị thay bằng **Micrometer Tracing**.
6. Hibernate 6 đổi cách sinh SQL và một số kiểu dữ liệu, cần chạy lại test tích hợp.
7. Nên đi qua 2.7 trước, sửa hết cảnh báo deprecation rồi mới lên 3.0.

**Nâng cấp 3 lên 4, những điểm hay vướng:**
1. **Jackson 3:** package đổi thành `tools.jackson`, một số mặc định đổi (cách xử lý ngày giờ, property không biết). Test serialization có thể lỗi mà không báo trước.
2. **Module auto-config được chia nhỏ:** starter đổi tên rõ nghĩa hơn (ví dụ `spring-boot-starter-webmvc`), có starter riêng cho test. Có starter "classic" để chuyển dần.
3. Bỏ Undertow (chưa hỗ trợ Servlet 6.1), bỏ các API đã deprecated từ 3.x.
4. Spring Security 7, Hibernate 7, JUnit 6.
5. Cách làm: nâng lên **3.5 mới nhất trước**, sửa cảnh báo deprecation, rồi chạy OpenRewrite recipe cho Boot 4.

**Câu trả lời mẫu:** *"Tôi đã [nâng cấp / làm việc trên] Spring Boot [3.x]. Khó nhất khi lên 3 là đổi javax sang jakarta và thư viện cũ chưa hỗ trợ; tôi dùng OpenRewrite cho phần cơ học và dựa vào test tích hợp với Testcontainers để bắt lỗi Hibernate 6."* Điền đúng trải nghiệm của bạn.

### English

| | Spring Boot 2.x | Spring Boot 3.x | Spring Boot 4.x |
|---|---|---|---|
| Released | 2018 | 11/2022 | 11/2025 (4.1 in 06/2026) |
| Spring Framework | 5 | 6 | 7 |
| Minimum Java | 8 | **17** | 17 (**25** recommended) |
| Jakarta EE | `javax.*` | **`jakarta.*`** (EE 9/10) | Jakarta EE 11 (Servlet 6.1, JPA 3.2) |
| Hibernate | 5 | 6 | 7 |
| Jackson | 2 | 2 | **3** |
| Highlights | | AOT and GraalVM native, the Observation API (Micrometer), ProblemDetail, HTTP interfaces, virtual threads (3.2) | API versioning, `@Retryable`/`@ConcurrencyLimit` in core, JSpecify null safety, modularized auto-configuration, HTTP service client groups |

**Upgrading 2 to 3, the most work:**
1. Move to Java 17 first.
2. Rename **`javax.*` to `jakarta.*`** (persistence, servlet, validation). Use **OpenRewrite** (`rewrite-spring`) to automate it.
3. Third-party libraries need Jakarta-compatible versions.
4. Spring Security 6: `WebSecurityConfigurerAdapter` is gone; use `SecurityFilterChain` beans.
5. Spring Cloud Sleuth is replaced by **Micrometer Tracing**.
6. Hibernate 6 changes SQL generation and some types, so rerun integration tests.
7. Go through 2.7 first, fix every deprecation warning, then move to 3.0.

**Upgrading 3 to 4, common snags:**
1. **Jackson 3:** the package becomes `tools.jackson` and some defaults change (date handling, unknown properties). Serialization tests can break without warning.
2. **Modularized auto-configuration:** starters get clearer names (for example `spring-boot-starter-webmvc`), with dedicated test starters. "Classic" starters exist for a gradual migration.
3. Undertow is dropped (no Servlet 6.1 support yet), and APIs deprecated in 3.x are removed.
4. Spring Security 7, Hibernate 7, JUnit 6.
5. Approach: upgrade to **the latest 3.5 first**, fix deprecation warnings, then run the OpenRewrite recipe for Boot 4.

**A model answer:** *"I [upgraded / worked on] Spring Boot [3.x]. The hardest part of moving to 3 was javax to jakarta and old libraries without support; I used OpenRewrite for the mechanical changes and relied on integration tests with Testcontainers to catch Hibernate 6 issues."* Fill in your real experience.

@@@ sn-boot3 | Spring Boot 3.x có những tính năng mới nào đáng dùng? / Which Spring Boot 3.x features are worth using? | spring-new | spring-boot,observability,testcontainers | qa | Spring Boot 3
### Tiếng Việt

| Tính năng | Bản | Dùng thế nào, lợi ích |
|---|---|---|
| **ProblemDetail (RFC 9457, trước là 7807)** | 3.0 | Format lỗi chuẩn `{type, title, status, detail, instance}`. Bật `spring.mvc.problemdetails.enabled=true` hoặc trả `ProblemDetail` từ `@ExceptionHandler` |
| **Observability với Micrometer** | 3.0 | Observation API: một lần đo cho ra **cả metrics lẫn trace**. Micrometer Tracing thay Sleuth, xuất qua OpenTelemetry hoặc Zipkin. Trace id tự có trong log |
| **HTTP interface** (`@HttpExchange`) | 3.0 | Khai báo interface, Spring sinh client, giống Feign nhưng có sẵn |
| **AOT và GraalVM native image** | 3.0 | Biên dịch thành file chạy native: khởi động khoảng 0,1 giây, ít RAM. Đổi lại build lâu, reflection phải khai báo, không có JIT nên throughput lúc chạy lâu có thể thấp hơn |
| **Testcontainers `@ServiceConnection`** | 3.1 | Container trong test tự cấu hình datasource, không cần `@DynamicPropertySource` |
| **Docker Compose support** | 3.1 | Chạy app ở local thì tự `docker compose up` theo `compose.yaml` và tự nối kết nối |
| **SSL bundles** | 3.1 | Cấu hình keystore và truststore một chỗ, dùng lại cho web server, RestClient, Kafka, Redis |
| **Virtual threads** | 3.2 | `spring.threads.virtual.enabled=true` |
| **`RestClient`, `JdbcClient`** | 3.2 | API fluent, đồng bộ, hiện đại hơn `RestTemplate` và `JdbcTemplate` |
| **CDS** | 3.3 | Class Data Sharing để khởi động nhanh hơn mà không cần native image |
| **Structured logging** | 3.4 | `logging.structured.format.console=ecs` (hoặc `logstash`, `gelf`) để log ra JSON, đẩy thẳng vào ELK hoặc Loki |
| **`@MockitoBean`, `@MockitoSpyBean`** | 3.4 | Thay `@MockBean`, `@SpyBean` (đã deprecated và bị bỏ ở Boot 4) |

```java
// Testcontainers + @ServiceConnection
@SpringBootTest
@Testcontainers
class OrderRepositoryIT {
    @Container @ServiceConnection
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:17");
    // không cần cấu hình spring.datasource.* nữa
}

// ProblemDetail
@ExceptionHandler(OrderNotFoundException.class)
ProblemDetail handle(OrderNotFoundException e) {
    ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    pd.setProperty("orderId", e.getOrderId());
    return pd;
}
```

**Nên chọn 3–4 cái mình đã dùng thật để kể** khi được hỏi "Bạn dùng tính năng mới nào của Spring Boot 3?". Testcontainers với `@ServiceConnection`, ProblemDetail, RestClient và observability là những câu dễ ghi điểm.

### English

| Feature | Version | Usage, benefit |
|---|---|---|
| **ProblemDetail (RFC 9457, formerly 7807)** | 3.0 | A standard error format `{type, title, status, detail, instance}`. Enable `spring.mvc.problemdetails.enabled=true` or return a `ProblemDetail` from an `@ExceptionHandler` |
| **Observability with Micrometer** | 3.0 | The Observation API: one instrumentation produces **both metrics and traces**. Micrometer Tracing replaces Sleuth, exporting via OpenTelemetry or Zipkin. Trace ids appear in logs automatically |
| **HTTP interfaces** (`@HttpExchange`) | 3.0 | Declare an interface and Spring generates the client, like Feign but built in |
| **AOT and GraalVM native images** | 3.0 | Compile to a native executable: about 0.1 s startup and low memory. In exchange, builds are slow, reflection must be declared, and without a JIT, long-running throughput can be lower |
| **Testcontainers `@ServiceConnection`** | 3.1 | Containers in tests configure the datasource automatically, no `@DynamicPropertySource` needed |
| **Docker Compose support** | 3.1 | Running the app locally runs `docker compose up` from `compose.yaml` and wires the connections automatically |
| **SSL bundles** | 3.1 | Configure keystores and truststores in one place and reuse them for the web server, RestClient, Kafka and Redis |
| **Virtual threads** | 3.2 | `spring.threads.virtual.enabled=true` |
| **`RestClient`, `JdbcClient`** | 3.2 | Fluent, synchronous APIs, more modern than `RestTemplate` and `JdbcTemplate` |
| **CDS** | 3.3 | Class Data Sharing for faster startup without a native image |
| **Structured logging** | 3.4 | `logging.structured.format.console=ecs` (or `logstash`, `gelf`) to log JSON straight into ELK or Loki |
| **`@MockitoBean`, `@MockitoSpyBean`** | 3.4 | Replace `@MockBean` and `@SpyBean` (deprecated, and removed in Boot 4) |

```java
// Testcontainers + @ServiceConnection
@SpringBootTest
@Testcontainers
class OrderRepositoryIT {
    @Container @ServiceConnection
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:17");
    // no spring.datasource.* configuration needed anymore
}

// ProblemDetail
@ExceptionHandler(OrderNotFoundException.class)
ProblemDetail handle(OrderNotFoundException e) {
    ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    pd.setProperty("orderId", e.getOrderId());
    return pd;
}
```

**Pick 3–4 features you've really used to talk about** when asked "Which new Spring Boot 3 features have you used?". Testcontainers with `@ServiceConnection`, ProblemDetail, RestClient and observability are easy points to score.

@@@ sn-http-clients | RestTemplate, WebClient, RestClient và HTTP interface: nên dùng cái nào? / RestTemplate, WebClient, RestClient and HTTP interfaces: which should you use? | spring-new | spring-boot,http-client | qa | Spring Boot 3
### Tiếng Việt

| Client | Kiểu | Trạng thái | Dùng khi |
|---|---|---|---|
| `RestTemplate` | Đồng bộ, API dạng template | **Maintenance mode**; đội Spring đã công bố lộ trình deprecate trong dòng 7.x | Code cũ, không viết mới |
| `WebClient` | **Reactive**, không chặn (WebFlux) | Đang phát triển | Ứng dụng reactive, hoặc cần gọi song song bằng Reactor |
| **`RestClient`** | Đồng bộ, **API fluent** giống WebClient | **Mặc định cho code mới** (từ 6.1 / Boot 3.2) | App Spring MVC thông thường, đặc biệt khi dùng virtual threads |
| **HTTP interface** (`@HttpExchange`) | Khai báo interface, chạy trên RestClient hoặc WebClient | Có sẵn từ 6.0 | Client có nhiều endpoint, muốn code gọn như Feign |

```java
// RestClient
RestClient client = RestClient.builder()
    .baseUrl("https://payment.internal")
    .defaultHeader("X-Service", "order")
    .requestInterceptor(new TracingInterceptor())
    .build();

PaymentResponse res = client.post().uri("/payments")
    .body(new PaymentRequest(orderId, amount))
    .retrieve()
    .onStatus(HttpStatusCode::is4xxClientError, (req, resp) -> { throw new PaymentRejected(); })
    .body(PaymentResponse.class);

// HTTP interface
@HttpExchange("/payments")
interface PaymentClient {
    @PostExchange PaymentResponse create(@RequestBody PaymentRequest req);
    @GetExchange("/{id}") PaymentResponse get(@PathVariable String id);
}
```

**Spring Boot 4 / Framework 7: HTTP service client groups.** Khai báo `@ImportHttpServices(group = "payment", types = PaymentClient.class)` thì Spring tự tạo bean client, cấu hình `base-url` và timeout qua `application.yml` theo nhóm. Không cần viết `HttpServiceProxyFactory` bằng tay nữa.

**OpenFeign:** Spring Cloud OpenFeign đã vào chế độ bảo trì; đội Spring khuyên chuyển sang HTTP interface.

**Dù dùng client nào, đều phải cấu hình:**
- **Timeout** (connect và read). Mặc định có thể chờ rất lâu, làm cạn thread.
- Retry có giới hạn và chỉ cho request idempotent (Boot 4 có `@Retryable` trong core), circuit breaker (Resilience4j).
- Connection pool, truyền trace header, log có che dữ liệu nhạy cảm.

### English

| Client | Style | Status | Use when |
|---|---|---|---|
| `RestTemplate` | Synchronous, template-style API | **Maintenance mode**; the Spring team has announced a deprecation path in the 7.x line | Legacy code, not for new code |
| `WebClient` | **Reactive**, non-blocking (WebFlux) | Actively developed | Reactive applications, or parallel calls with Reactor |
| **`RestClient`** | Synchronous, **fluent API** like WebClient | **The default for new code** (since 6.1 / Boot 3.2) | Regular Spring MVC apps, especially with virtual threads |
| **HTTP interfaces** (`@HttpExchange`) | Declarative interfaces running on RestClient or WebClient | Built in since 6.0 | Clients with many endpoints, when you want Feign-like concise code |

```java
// RestClient
RestClient client = RestClient.builder()
    .baseUrl("https://payment.internal")
    .defaultHeader("X-Service", "order")
    .requestInterceptor(new TracingInterceptor())
    .build();

PaymentResponse res = client.post().uri("/payments")
    .body(new PaymentRequest(orderId, amount))
    .retrieve()
    .onStatus(HttpStatusCode::is4xxClientError, (req, resp) -> { throw new PaymentRejected(); })
    .body(PaymentResponse.class);

// HTTP interface
@HttpExchange("/payments")
interface PaymentClient {
    @PostExchange PaymentResponse create(@RequestBody PaymentRequest req);
    @GetExchange("/{id}") PaymentResponse get(@PathVariable String id);
}
```

**Spring Boot 4 / Framework 7: HTTP service client groups.** Declare `@ImportHttpServices(group = "payment", types = PaymentClient.class)` and Spring creates the client beans, with `base-url` and timeouts configured per group in `application.yml`. No more hand-written `HttpServiceProxyFactory`.

**OpenFeign:** Spring Cloud OpenFeign is in maintenance mode, and the Spring team recommends moving to HTTP interfaces.

**Whichever client you use, always configure:**
- **Timeouts** (connect and read). Defaults can wait a very long time and exhaust threads.
- Bounded retries for idempotent requests only (Boot 4 has `@Retryable` in core), and a circuit breaker (Resilience4j).
- A connection pool, trace-header propagation, and logs that mask sensitive data.

@@@ sn-boot4 | Spring Boot 4 / Spring Framework 7 có gì mới? / What's new in Spring Boot 4 and Spring Framework 7? | spring-new | spring-boot,spring7,api-versioning | qa | Spring Boot 4
### Tiếng Việt

Spring Framework 7 và Spring Boot 4 ra mắt tháng 11/2025; Spring Boot 4.1 ra mắt tháng 6/2026.

**1. API versioning có sẵn** (MVC và WebFlux). Trước đây phải tự làm bằng URL hoặc header.

```java
@RestController
@RequestMapping("/api/orders")
class OrderController {
    @GetMapping(path = "/{id}", version = "1")   OrderV1 getV1(@PathVariable long id) { ... }
    @GetMapping(path = "/{id}", version = "2+")  OrderV2 getV2(@PathVariable long id) { ... } // từ v2 trở lên
}
// application.yml: spring.mvc.apiversion.use.header: X-API-Version
```

- Hỗ trợ 4 cách đọc version: path, header, query param, media type.
- Kiểm tra version hợp lệ, có version mặc định.
- **Header deprecation chuẩn RFC** (`Deprecation`, `Sunset`) để báo client sắp bỏ version cũ.
- RestClient, WebClient và HTTP interface tự gắn version khi gọi.

**2. Resilience có sẵn trong core** (trước cần Spring Retry hoặc Resilience4j):

```java
@Configuration @EnableResilientMethods
class ResilienceConfig {}

@Retryable(maxAttempts = 3, delay = 200, multiplier = 2, includes = TimeoutException.class)
public Rate fetchRate(String pair) { ... }

@ConcurrencyLimit(10)    // tối đa 10 lời gọi đồng thời, hữu ích với virtual threads
public Report generate() { ... }
```

Circuit breaker vẫn cần Resilience4j.

**3. Null safety với JSpecify:** toàn bộ Spring dùng `@Nullable`/`@NonNull` của `org.jspecify`. IDE và NullAway phát hiện NPE lúc compile; Kotlin hiểu đúng kiểu nullable.

**4. Chia nhỏ auto-configuration:** jar `spring-boot-autoconfigure` khổng lồ được tách thành các module nhỏ theo công nghệ, nên ứng dụng nhẹ hơn, khởi động nhanh hơn và native image nhỏ hơn.

**5. Các điểm khác:**
- **Jackson 3** là mặc định.
- `BeanRegistrar`: đăng ký bean bằng code, thân thiện với AOT.
- `RestTestClient` để test API.
- `JmsClient`, HTTP service client groups.
- Jakarta EE 11, Hibernate 7, Spring Security 7 (hỗ trợ MFA tốt hơn), JUnit 6.

**6. Spring Boot 4.1 (06/2026):**
- Tự cấu hình **gRPC** server và client.
- Annotation **`@RedisListener`**, cấu hình sẵn listener container cho Redis pub/sub.
- Đọc phần lớn **biến môi trường OpenTelemetry** chuẩn.
- **Chống SSRF** cho HTTP client.
- Khởi tạo JPA **bất đồng bộ** (`spring.jpa.bootstrap`) để giảm thời gian khởi động.
- Lấy kết nối JDBC **lazy** (chỉ lấy khi thật sự cần).

**Khi phỏng vấn:** chưa dùng Boot 4 ở production thì nói thật, rồi nêu 2–3 thay đổi bạn thấy có giá trị nhất (API versioning, `@Retryable` có sẵn, Jackson 3 cần chú ý khi nâng cấp). Như vậy cho thấy bạn theo dõi hệ sinh thái.

### English

Spring Framework 7 and Spring Boot 4 shipped in November 2025; Spring Boot 4.1 shipped in June 2026.

**1. Built-in API versioning** (MVC and WebFlux). Previously you had to roll your own with URLs or headers.

```java
@RestController
@RequestMapping("/api/orders")
class OrderController {
    @GetMapping(path = "/{id}", version = "1")   OrderV1 getV1(@PathVariable long id) { ... }
    @GetMapping(path = "/{id}", version = "2+")  OrderV2 getV2(@PathVariable long id) { ... } // v2 and above
}
// application.yml: spring.mvc.apiversion.use.header: X-API-Version
```

- Four ways to read the version: path, header, query parameter, media type.
- Validation of supported versions, plus a default version.
- **RFC-standard deprecation headers** (`Deprecation`, `Sunset`) to tell clients an old version is going away.
- RestClient, WebClient and HTTP interfaces add the version automatically when calling.

**2. Resilience built into core** (previously Spring Retry or Resilience4j):

```java
@Configuration @EnableResilientMethods
class ResilienceConfig {}

@Retryable(maxAttempts = 3, delay = 200, multiplier = 2, includes = TimeoutException.class)
public Rate fetchRate(String pair) { ... }

@ConcurrencyLimit(10)    // at most 10 concurrent calls, useful with virtual threads
public Report generate() { ... }
```

Circuit breakers still need Resilience4j.

**3. Null safety with JSpecify:** all of Spring uses `@Nullable`/`@NonNull` from `org.jspecify`. IDEs and NullAway catch NPEs at compile time, and Kotlin sees the correct nullable types.

**4. Modularized auto-configuration:** the huge `spring-boot-autoconfigure` jar is split into small per-technology modules, so applications are lighter, start faster and produce smaller native images.

**5. Other changes:**
- **Jackson 3** is the default.
- `BeanRegistrar`: programmatic, AOT-friendly bean registration.
- `RestTestClient` for testing APIs.
- `JmsClient` and HTTP service client groups.
- Jakarta EE 11, Hibernate 7, Spring Security 7 (better MFA support), JUnit 6.

**6. Spring Boot 4.1 (06/2026):**
- **gRPC** server and client auto-configuration.
- A **`@RedisListener`** annotation, with a preconfigured listener container for Redis pub/sub.
- Reads most standard **OpenTelemetry environment variables**.
- **SSRF protection** for HTTP clients.
- **Asynchronous** JPA bootstrap (`spring.jpa.bootstrap`) to reduce startup time.
- **Lazy** JDBC connection fetching (acquired only when actually needed).

**In an interview:** if you haven't used Boot 4 in production, say so honestly, then name 2–3 changes you find most valuable (API versioning, built-in `@Retryable`, Jackson 3 as an upgrade risk). That shows you follow the ecosystem.

@@@ sn-startup | Làm sao để ứng dụng Spring khởi động nhanh và tốn ít bộ nhớ: GraalVM native, CDS hay AOT cache? / How do you make a Spring app start fast and use less memory: GraalVM native, CDS or the AOT cache? | spring-new | spring-boot,graalvm,performance | qa | Spring Boot 3
### Tiếng Việt

**Vì sao quan trọng:** trong Kubernetes, khởi động chậm (10–30 giây) làm autoscale chậm, deploy lâu, và tốn tiền khi phải giữ nhiều pod dự phòng. Serverless càng cần khởi động nhanh.

| Cách | Khởi động | Bộ nhớ | Đánh đổi |
|---|---|---|---|
| JVM bình thường | Chậm (vài giây đến vài chục giây) | Cao | Không phải làm gì; JIT cho throughput tốt khi chạy lâu |
| **CDS** (Class Data Sharing, Boot 3.3+) | Nhanh hơn khoảng 30–40% | Giảm nhẹ | Cần một lần chạy huấn luyện khi build image; dễ áp dụng |
| **AOT cache của JDK** (Project Leyden, Java 24–25+) | Nhanh hơn nhiều so với CDS | Giảm | Cần chạy huấn luyện (`-XX:AOTCacheOutput`); vẫn là JVM đầy đủ, **không đổi code** |
| **GraalVM native image** | **Rất nhanh** (khoảng 0,05–0,2 giây) | **Thấp nhất** | Build lâu (vài phút) và tốn RAM khi build; reflection, proxy, resource phải khai báo (Spring AOT lo phần lớn); thư viện có thể chưa hỗ trợ; không có JIT nên throughput đỉnh khi chạy lâu có thể thấp hơn; debug khó hơn |
| Bật lazy init, giảm bean | Nhanh hơn một chút | | Lỗi cấu hình chỉ lộ ra lúc request đầu tiên |

**Spring AOT** (từ Boot 3): lúc build, Spring xử lý trước cấu hình bean và sinh code Java thay cho việc quét và reflection lúc chạy. Đây là điều kiện để làm native image, và cũng giúp JVM thường khởi động nhanh hơn.

```bash
# Native image bằng buildpacks
./mvnw -Pnative spring-boot:build-image
# hoặc biên dịch native trực tiếp
./mvnw -Pnative native:compile
```

**Chọn cách nào:**
- Service chạy lâu, tải cao, ổn định: **JVM + CDS hoặc AOT cache**. Giữ JIT, áp dụng ít rủi ro.
- Function serverless, CLI, service scale-to-zero, hoặc cần mật độ pod rất cao: **native image**.
- Luôn **đo** bằng số liệu thực (thời gian khởi động, RSS, p99 latency), đừng chọn theo cảm tính.

**Câu trả lời mẫu:** *"Với microservice chạy lâu trên Kubernetes, tôi giữ JVM và bật CDS hoặc AOT cache để khởi động nhanh hơn mà không đổi code. Native image tôi dành cho workload scale-to-zero, vì nó đổi throughput và thời gian build lấy thời gian khởi động."*

### English

**Why it matters:** in Kubernetes, slow startup (10–30 seconds) means slow autoscaling, long deployments and the cost of keeping spare pods. Serverless needs fast startup even more.

| Approach | Startup | Memory | Trade-offs |
|---|---|---|---|
| Plain JVM | Slow (seconds to tens of seconds) | High | Nothing to do; the JIT gives good long-running throughput |
| **CDS** (Class Data Sharing, Boot 3.3+) | About 30–40% faster | Slightly lower | Needs one training run when building the image; easy to adopt |
| **The JDK AOT cache** (Project Leyden, Java 24–25+) | Much faster than CDS | Lower | Needs a training run (`-XX:AOTCacheOutput`); still a full JVM, **no code changes** |
| **GraalVM native image** | **Very fast** (about 0.05–0.2 s) | **Lowest** | Slow builds (minutes) that need lots of RAM; reflection, proxies and resources must be declared (Spring AOT handles most of it); libraries may not support it; no JIT, so peak long-running throughput can be lower; harder to debug |
| Lazy init, fewer beans | A bit faster | | Configuration errors only surface on the first request |

**Spring AOT** (since Boot 3): at build time, Spring pre-processes the bean configuration and generates Java code instead of scanning and reflecting at runtime. It's a prerequisite for native images, and it also helps regular JVMs start faster.

```bash
# Native image with buildpacks
./mvnw -Pnative spring-boot:build-image
# or compile natively directly
./mvnw -Pnative native:compile
```

**Which to pick:**
- Long-running, high-load, steady services: **JVM + CDS or the AOT cache**. You keep the JIT, with low adoption risk.
- Serverless functions, CLIs, scale-to-zero services, or very high pod density: **native image**.
- Always **measure** with real numbers (startup time, RSS, p99 latency) rather than going by feel.

**A model answer:** *"For long-running microservices on Kubernetes I keep the JVM and enable CDS or the AOT cache to start faster without code changes. I reserve native images for scale-to-zero workloads, because they trade throughput and build time for startup time."*
