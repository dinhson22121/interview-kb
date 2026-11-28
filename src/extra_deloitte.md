@@@ co-deloitte | Deloitte (SDE2 Java) | company | deloitte,consulting | guide
Bộ câu hỏi tổng hợp từ một bài chia sẻ trên cộng đồng luyện phỏng vấn, mô tả 4 vòng của vị trí SDE2 Java. Đây là mẫu câu **rất điển hình cho mọi vị trí Java mid đến senior** ở công ty dịch vụ và tư vấn (EPAM, mgm, Deloitte...), nên nên ôn kỹ cả khi không ứng tuyển Deloitte.

*Nguồn là bài tổng hợp từ cộng đồng, không phải tài liệu chính thức của Deloitte; quy trình thật có thể khác theo quốc gia và dự án.*

### Vòng 1: Online assessment

- [ ] [Ký tự không lặp đầu tiên trong chuỗi](#coding-4)
- [ ] [Phát hiện chu trình trong linked list](#dsa-linked-list-cycle)
- [ ] Trắc nghiệm OOP: [4 trụ cột OOP](#jc-oop-pillars), [Overloading và overriding](#jc-overload-override)
- [ ] Trắc nghiệm exception: [finally và exception](#jc-finally)
- [ ] Trắc nghiệm DBMS: [Chuẩn hóa 1NF–3NF](#sql-normalization), [Các loại JOIN](#sql-joins)

### Vòng 2: Core Java & DSA

- [ ] [`==` và `.equals()`, vì sao String khác](#jc-equals-operator) · [String pool](#jc-string-pool)
- [ ] [Vì sao phải override equals() và hashCode() cùng nhau](#java-core-3)
- [ ] [HashMap hoạt động bên trong, Java 8 thay đổi gì](#java-core-1)
- [ ] [HashMap, LinkedHashMap, TreeMap](#jc-map-impls)
- [ ] [4 trụ cột OOP, kèm ví dụ từ dự án](#jc-oop-pillars)
- [ ] [Interface và abstract class](#jc-interface-vs-abstract)
- [ ] [Overloading và overriding: compile time hay runtime](#jc-overload-override)
- [ ] [Two Sum](#coding-3)
- [ ] [Diamond problem và cách Java tránh](#jc-diamond)

### Vòng 3: Spring, SQL & Design

- [ ] [Dependency injection, vì sao constructor injection](#spring-1)
- [ ] [Bean scope: khi nào dùng khác singleton](#sp-scopes)
- [ ] [@Component, @Service, @Repository, @Controller](#sp-stereotypes)
- [ ] [N+1 query trong JPA](#jpa-16)
- [ ] [@Transactional: REQUIRED và REQUIRES_NEW](#spring-4)
- [ ] [Idempotency trong REST API](#microservices-5)
- [ ] [Thiết kế rate limiter](#system-design-18)
- [ ] [synchronized và ReentrantLock](#jc-sync-vs-lock)

### Vòng 4: Manager / HR

- [ ] [Kể về một bug khó bạn đã sửa](#behavioral-hard-bug)
- [ ] [Vì sao muốn vào công ty này](#hr-screening-3)
- [ ] [Bất đồng với đồng nghiệp về quyết định kỹ thuật](#behavioral-3)
- [ ] [Bạn có câu hỏi nào cho chúng tôi không](#hr-questions-to-ask)

### Gợi ý ôn

- Vòng 2 và 3 hỏi **"vì sao"** nhiều hơn "là gì": mỗi câu chuẩn bị một ví dụ từ dự án thật (DXC: Spring Boot cho bảo hiểm nhân thọ; Opswat: Go và Java).
- Về "Why Deloitte": nhấn vào làm nhiều domain và khách hàng lớn, môi trường tư vấn, cơ hội tiếp xúc trực tiếp khách hàng. Kinh nghiệm outsourcing ở DXC là điểm cộng.

@@@ jc-equals-operator | `==` và `.equals()` khác nhau thế nào? Vì sao String lại "lạ"? / What's the difference between `==` and `.equals()`, and why does String behave differently? | java | equals,string,deloitte | qa | Java core
### Tiếng Việt

- **`==`**: với kiểu nguyên thủy (`int`, `double`...) thì so **giá trị**; với object thì so **tham chiếu**, tức hai biến có trỏ tới **cùng một object** trong heap không.
- **`.equals()`**: so **nội dung** theo logic mà class định nghĩa. Mặc định trong `Object`, `equals()` **chính là `==`**; các class như `String`, `Integer`, `List`, record đều override để so nội dung.

```java
String a = "hello";
String b = "hello";
String c = new String("hello");

a == b        // true  : cả hai literal trỏ cùng một object trong String pool
a == c        // false : new String() luôn tạo object mới trên heap
a.equals(c)   // true  : cùng nội dung
a == c.intern() // true : intern() trả về bản trong pool
```

**Vì sao String "lạ":** các **string literal** được lưu trong **String constant pool**; JVM dùng lại cùng một object cho literal giống nhau (làm được vì String **bất biến**). Nên `==` giữa hai literal đôi khi trả `true`, khiến người ta tưởng `==` so nội dung. Chuỗi tạo lúc chạy (`new String`, nối chuỗi với biến, đọc từ input) là object khác, nên `==` trả `false`. Xem [String pool](#jc-string-pool).

**Bẫy tương tự với Integer cache:**
```java
Integer x = 127, y = 127;   x == y  // true  : Integer cache giá trị từ -128 đến 127
Integer p = 128, q = 128;   p == q  // false : ngoài khoảng cache, hai object khác nhau
```

**Quy tắc:**
- So **nội dung object** thì luôn dùng `equals()` (hoặc `Objects.equals(a, b)` để an toàn với `null`).
- Viết `"ACTIVE".equals(status)` thay vì `status.equals("ACTIVE")` để tránh NPE khi `status` null.
- `==` chỉ dùng cho kiểu nguyên thủy, enum (mỗi giá trị enum là singleton), hoặc khi thật sự muốn kiểm tra cùng một object.
- Override `equals()` thì **bắt buộc** override `hashCode()`. Xem [equals và hashCode](#java-core-3).

### English

- **`==`**: for primitives (`int`, `double`...) it compares **values**; for objects it compares **references**, meaning whether both variables point to **the same object** on the heap.
- **`.equals()`**: compares **content** according to the logic the class defines. By default in `Object`, `equals()` **is just `==`**; classes such as `String`, `Integer`, `List` and records override it to compare content.

```java
String a = "hello";
String b = "hello";
String c = new String("hello");

a == b        // true  : both literals point to the same object in the String pool
a == c        // false : new String() always creates a new heap object
a.equals(c)   // true  : same content
a == c.intern() // true : intern() returns the pooled copy
```

**Why String seems "odd":** **string literals** live in the **String constant pool**; the JVM reuses one object for identical literals (possible because String is **immutable**). So `==` between two literals sometimes returns `true`, which tricks people into thinking `==` compares content. Strings created at runtime (`new String`, concatenation with variables, input) are different objects, so `==` returns `false`. See [String pool](#jc-string-pool).

**A similar trap with the Integer cache:**
```java
Integer x = 127, y = 127;   x == y  // true  : Integer caches values from -128 to 127
Integer p = 128, q = 128;   p == q  // false : outside the cache, two different objects
```

**Rules:**
- To compare **object content**, always use `equals()` (or `Objects.equals(a, b)` to be null-safe).
- Write `"ACTIVE".equals(status)` instead of `status.equals("ACTIVE")` to avoid an NPE when `status` is null.
- Use `==` only for primitives, enums (each enum value is a singleton), or when you really mean "the same object".
- If you override `equals()`, you **must** override `hashCode()`. See [equals and hashCode](#java-core-3).

@@@ jc-map-impls | HashMap, LinkedHashMap và TreeMap khác nhau thế nào? / How do HashMap, LinkedHashMap and TreeMap differ? | java | collections,hashmap,deloitte | qa | Java core
### Tiếng Việt

| | **HashMap** | **LinkedHashMap** | **TreeMap** |
|---|---|---|---|
| Cấu trúc | Mảng bucket + linked list / cây đỏ đen | HashMap + **danh sách liên kết đôi** nối các entry | **Cây đỏ đen** |
| Thứ tự duyệt | **Không đảm bảo** | **Thứ tự chèn** (hoặc thứ tự truy cập) | **Sắp xếp theo key** (tự nhiên hoặc `Comparator`) |
| get / put / remove | **O(1)** trung bình | O(1) | **O(log n)** |
| Key `null` | Cho phép 1 key null | Cho phép 1 key null | **Không** (ném NPE với thứ tự tự nhiên) |
| Yêu cầu với key | `equals()` + `hashCode()` đúng | Như HashMap | `Comparable` hoặc `Comparator`; **so sánh phải nhất quán với equals** |
| Bộ nhớ | Ít nhất | Nhiều hơn (thêm 2 con trỏ mỗi entry) | Nhiều hơn (node cây) |
| API riêng | | `removeEldestEntry` | `firstKey`, `floorKey`, `ceilingKey`, `headMap`, `subMap`... (`NavigableMap`) |

**Khi nào dùng:**
- **HashMap:** mặc định, chỉ cần tra cứu nhanh.
- **LinkedHashMap:** cần **giữ thứ tự chèn** (trả JSON theo thứ tự cố định, loại trùng mà giữ thứ tự) hoặc làm **LRU cache**:
```java
class LruCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    LruCache(int capacity) { super(16, 0.75f, true); this.capacity = capacity; } // accessOrder = true
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> e) { return size() > capacity; }
}
```
- **TreeMap:** cần **key có thứ tự** hoặc **truy vấn khoảng**: bảng giá theo bậc (`floorEntry(amount)`), lịch theo thời gian, "tìm mốc nhỏ hơn hoặc bằng x".
```java
TreeMap<Integer, Double> taxBrackets = new TreeMap<>(Map.of(0, 0.05, 5_000_000, 0.10, 10_000_000, 0.15));
taxBrackets.floorEntry(7_000_000).getValue();   // 0.10
```

**Đồng thời:** cả ba **không thread-safe**. Dùng `ConcurrentHashMap` (thay HashMap) hoặc `ConcurrentSkipListMap` (thay TreeMap). Xem [HashMap vs ConcurrentHashMap](#java-core-2).

### English

| | **HashMap** | **LinkedHashMap** | **TreeMap** |
|---|---|---|---|
| Structure | Bucket array + linked lists / red-black trees | HashMap + a **doubly linked list** through the entries | A **red-black tree** |
| Iteration order | **Not guaranteed** | **Insertion order** (or access order) | **Sorted by key** (natural order or a `Comparator`) |
| get / put / remove | **O(1)** average | O(1) | **O(log n)** |
| `null` keys | One null key allowed | One null key allowed | **No** (NPE with natural ordering) |
| Key requirements | Correct `equals()` + `hashCode()` | Same as HashMap | `Comparable` or a `Comparator`; **ordering must be consistent with equals** |
| Memory | Lowest | More (two extra pointers per entry) | More (tree nodes) |
| Extra API | | `removeEldestEntry` | `firstKey`, `floorKey`, `ceilingKey`, `headMap`, `subMap`... (`NavigableMap`) |

**When to use which:**
- **HashMap:** the default, when you just need fast lookups.
- **LinkedHashMap:** when you need to **keep insertion order** (JSON in a fixed order, de-duplicating while preserving order) or build an **LRU cache**:
```java
class LruCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    LruCache(int capacity) { super(16, 0.75f, true); this.capacity = capacity; } // accessOrder = true
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> e) { return size() > capacity; }
}
```
- **TreeMap:** when you need **ordered keys** or **range queries**: tiered pricing (`floorEntry(amount)`), time-ordered schedules, "find the largest key ≤ x".
```java
TreeMap<Integer, Double> taxBrackets = new TreeMap<>(Map.of(0, 0.05, 5_000_000, 0.10, 10_000_000, 0.15));
taxBrackets.floorEntry(7_000_000).getValue();   // 0.10
```

**Concurrency:** none of the three is **thread-safe**. Use `ConcurrentHashMap` (instead of HashMap) or `ConcurrentSkipListMap` (instead of TreeMap). See [HashMap vs ConcurrentHashMap](#java-core-2).

@@@ jc-oop-pillars | 4 trụ cột của OOP là gì? Cho ví dụ từ dự án thật. / What are the 4 pillars of OOP? Give a real example from a project. | java | oop,deloitte | qa | Java core
### Tiếng Việt

| Trụ cột | Ý nghĩa | Trong Java |
|---|---|---|
| **Encapsulation** (đóng gói) | Gom dữ liệu và hành vi vào một chỗ, **ẩn trạng thái bên trong**, chỉ cho thay đổi qua method có kiểm soát | Field `private`, method public kiểm tra quy tắc |
| **Abstraction** (trừu tượng hóa) | Chỉ lộ ra **cái gì** (what), giấu **làm thế nào** (how) | Interface, abstract class |
| **Inheritance** (kế thừa) | Class con dùng lại và mở rộng class cha | `extends`, `implements` |
| **Polymorphism** (đa hình) | Cùng một lời gọi, **hành vi khác nhau** tùy object thật | Overriding (runtime), overloading (compile time) |

**Một ví dụ xuyên suốt (thay bằng domain dự án của bạn, ví dụ bảo hiểm ở DXC):**

```java
// Abstraction: phần còn lại của hệ thống chỉ biết "tính phí", không biết cách tính
public interface PremiumCalculator {
    Money calculate(Policy policy);
}

// Inheritance: dùng chung phần kiểm tra và làm tròn
public abstract class BasePremiumCalculator implements PremiumCalculator {
    public final Money calculate(Policy p) {
        if (!p.isActive()) throw new PolicyNotActiveException(p.id());
        return basePremium(p).multiply(riskFactor(p)).roundTo(1_000);
    }
    protected abstract Money basePremium(Policy p);
    protected BigDecimal riskFactor(Policy p) { return BigDecimal.ONE; }
}

public class LifeInsuranceCalculator extends BasePremiumCalculator {
    protected Money basePremium(Policy p) { return p.sumAssured().percent(1.2); }
    @Override protected BigDecimal riskFactor(Policy p) { return p.insured().isSmoker() ? new BigDecimal("1.5") : BigDecimal.ONE; }
}

// Encapsulation: không ai sửa trạng thái Policy trực tiếp; chuyển trạng thái phải qua quy tắc
public class Policy {
    private PolicyStatus status;
    public void lapse() {
        if (status != PolicyStatus.ACTIVE) throw new IllegalStateException("Only active policies can lapse");
        status = PolicyStatus.LAPSED;
    }
}

// Polymorphism: service gọi một method, object thật quyết định cách tính
Money premium = calculators.get(policy.type()).calculate(policy);
```

**Cách kể trong phỏng vấn:** *"Ở DXC chúng tôi có nhiều loại hợp đồng bảo hiểm với công thức tính phí khác nhau. Tôi định nghĩa interface `PremiumCalculator` (abstraction), một abstract class chứa phần kiểm tra và làm tròn dùng chung (inheritance), mỗi loại sản phẩm override phần riêng, và service chọn calculator theo loại hợp đồng qua một Map do Spring inject (polymorphism). Trạng thái hợp đồng chỉ thay đổi qua method có kiểm tra quy tắc (encapsulation). Thêm sản phẩm mới chỉ cần thêm một class, không sửa code cũ, tức là đúng Open/Closed."*

**Lưu ý:** nói thêm "**ưu tiên composition hơn inheritance**": kế thừa sâu làm code cứng nhắc; chỉ dùng khi thật sự là quan hệ "là một" (is-a).

### English

| Pillar | Meaning | In Java |
|---|---|---|
| **Encapsulation** | Bundle data and behaviour together, **hide internal state**, and allow changes only through controlled methods | `private` fields, public methods that enforce rules |
| **Abstraction** | Expose only **what** something does, hide **how** | Interfaces, abstract classes |
| **Inheritance** | A subclass reuses and extends its parent | `extends`, `implements` |
| **Polymorphism** | One call, **different behaviour** depending on the actual object | Overriding (runtime), overloading (compile time) |

**One running example (replace it with your project's domain, e.g. insurance at DXC):**

```java
// Abstraction: the rest of the system only knows "calculate a premium", not how
public interface PremiumCalculator {
    Money calculate(Policy policy);
}

// Inheritance: shared validation and rounding
public abstract class BasePremiumCalculator implements PremiumCalculator {
    public final Money calculate(Policy p) {
        if (!p.isActive()) throw new PolicyNotActiveException(p.id());
        return basePremium(p).multiply(riskFactor(p)).roundTo(1_000);
    }
    protected abstract Money basePremium(Policy p);
    protected BigDecimal riskFactor(Policy p) { return BigDecimal.ONE; }
}

public class LifeInsuranceCalculator extends BasePremiumCalculator {
    protected Money basePremium(Policy p) { return p.sumAssured().percent(1.2); }
    @Override protected BigDecimal riskFactor(Policy p) { return p.insured().isSmoker() ? new BigDecimal("1.5") : BigDecimal.ONE; }
}

// Encapsulation: nobody changes Policy state directly; transitions go through the rules
public class Policy {
    private PolicyStatus status;
    public void lapse() {
        if (status != PolicyStatus.ACTIVE) throw new IllegalStateException("Only active policies can lapse");
        status = PolicyStatus.LAPSED;
    }
}

// Polymorphism: the service calls one method; the actual object decides how to calculate
Money premium = calculators.get(policy.type()).calculate(policy);
```

**How to tell it in an interview:** *"At DXC we had many insurance policy types with different premium formulas. I defined a `PremiumCalculator` interface (abstraction), an abstract class holding the shared validation and rounding (inheritance), each product overrode its specific part, and the service picked a calculator by policy type through a Map injected by Spring (polymorphism). Policy state only changed through methods that enforced the rules (encapsulation). Adding a new product meant adding one class without touching existing code, which is Open/Closed."*

**Note:** also mention "**prefer composition over inheritance**": deep inheritance makes code rigid; use it only for a genuine "is-a" relationship.

@@@ jc-interface-vs-abstract | Interface và abstract class khác nhau thế nào? Khi nào chọn cái nào? / Interface vs abstract class: how do they differ, and when do you choose each? | java | oop,interface,deloitte | qa | Java core
### Tiếng Việt

| | **Interface** | **Abstract class** |
|---|---|---|
| Kế thừa | Class implement **nhiều** interface | Class chỉ extends **một** class |
| Trạng thái (field) | Chỉ hằng số `public static final` | Field instance bình thường, mọi access modifier |
| Constructor | Không | Có (gọi qua `super(...)`) |
| Method | Abstract, `default` (Java 8), `static`, `private` (Java 9) | Abstract và method thường, mọi access modifier |
| Ý nghĩa | **Hợp đồng / khả năng** ("có thể làm gì": `Comparable`, `Serializable`, `PaymentGateway`) | **Bộ khung dùng chung** cho một họ class có quan hệ "là một" |
| Tiến hóa API | Thêm `default` method mà không làm vỡ class cũ | Thêm method thường dễ dàng |

**Chọn interface khi:**
- Định nghĩa **hợp đồng** giữa các tầng hoặc module: `OrderRepository`, `PaymentGateway`, `NotificationSender`. Dễ mock khi test, dễ đổi implementation, đúng Dependency Inversion.
- Các class **không liên quan** cùng có một khả năng.
- Cần "đa kế thừa" về kiểu.
- Đây là **lựa chọn mặc định**.

**Chọn abstract class khi:**
- Một họ class **chia sẻ trạng thái và code** chung (field, constructor, logic khởi tạo).
- Muốn dùng **Template Method**: cố định khung thuật toán (`final` method), để class con điền từng bước. Ví dụ `BasePremiumCalculator` ở [4 trụ cột OOP](#jc-oop-pillars), hoặc `AbstractBatchJob` với các bước đọc, xử lý, ghi.
- Cần method `protected` hoặc field không phải hằng số.

**Kết hợp phổ biến:** interface làm hợp đồng, abstract class làm phần cài đặt cơ sở (như `List` và `AbstractList` trong JDK). Code bên ngoài phụ thuộc vào **interface**, không vào abstract class.

**Câu trả lời mẫu:** *"Mặc định tôi dùng interface để định nghĩa hợp đồng, vì class có thể implement nhiều interface, dễ mock và dễ thay implementation. Tôi chỉ dùng abstract class khi một họ class thật sự chia sẻ trạng thái hoặc khung xử lý, ví dụ Template Method cho các batch job."*

### English

| | **Interface** | **Abstract class** |
|---|---|---|
| Inheritance | A class implements **many** interfaces | A class extends **one** class |
| State (fields) | Only `public static final` constants | Ordinary instance fields, any access modifier |
| Constructors | No | Yes (called via `super(...)`) |
| Methods | Abstract, `default` (Java 8), `static`, `private` (Java 9) | Abstract and concrete methods, any access modifier |
| Meaning | **A contract / capability** ("what it can do": `Comparable`, `Serializable`, `PaymentGateway`) | **A shared skeleton** for a family of classes in an "is-a" relationship |
| API evolution | Add `default` methods without breaking existing classes | Add concrete methods easily |

**Choose an interface when:**
- Defining a **contract** between layers or modules: `OrderRepository`, `PaymentGateway`, `NotificationSender`. Easy to mock in tests, easy to swap implementations, in line with Dependency Inversion.
- **Unrelated** classes share a capability.
- You need "multiple inheritance" of type.
- It's **the default choice**.

**Choose an abstract class when:**
- A family of classes **shares state and code** (fields, constructors, initialization logic).
- You want a **Template Method**: fix the algorithm's skeleton (a `final` method) and let subclasses fill in the steps. For example `BasePremiumCalculator` in [the 4 pillars of OOP](#jc-oop-pillars), or an `AbstractBatchJob` with read, process and write steps.
- You need `protected` methods or non-constant fields.

**A common combination:** an interface as the contract plus an abstract class as the base implementation (like `List` and `AbstractList` in the JDK). Outside code depends on the **interface**, not the abstract class.

**A model answer:** *"By default I use interfaces to define contracts, because a class can implement several, they're easy to mock and implementations are easy to swap. I only use an abstract class when a family of classes genuinely shares state or a processing skeleton, for example a Template Method for batch jobs."*

@@@ jc-diamond | Diamond problem là gì? Java tránh nó thế nào? / What is the diamond problem, and how does Java avoid it? | java | oop,interface,deloitte | qa | Java core
### Tiếng Việt

**Diamond problem:** class `D` kế thừa từ `B` và `C`, cả hai đều kế thừa `A` và override cùng một method. Gọi `d.hello()` thì dùng bản của `B` hay `C`? Sơ đồ kế thừa có hình kim cương, nên gọi là diamond.

```
      A.hello()
     /         \
 B.hello()   C.hello()
     \         /
         D   → dùng bản nào?
```

C++ cho phép đa kế thừa class nên phải xử lý vấn đề này (virtual inheritance).

**Java tránh bằng cách:**
1. **Class chỉ được extends một class**, nên không thể có diamond qua class, và cũng không có xung đột về **trạng thái** (field).
2. **Interface có thể implement nhiều**, nhưng trước Java 8 interface không có code nên không có gì xung đột.
3. Từ **Java 8 có `default` method**, nên xung đột có thể xảy ra trở lại. Java giải quyết theo 3 quy tắc:
   - **Class thắng interface:** method của class (hoặc class cha) luôn được ưu tiên hơn `default` method.
   - **Interface cụ thể hơn thắng:** nếu `B extends A` và cả hai có default `hello()`, thì bản của `B` thắng.
   - Còn lại vẫn mơ hồ thì **lỗi compile**, class phải **tự override** và có thể chọn rõ bản nào bằng `X.super.method()`.

```java
interface Flyer   { default String move() { return "fly"; } }
interface Swimmer { default String move() { return "swim"; } }

class Duck implements Flyer, Swimmer {
    // Không override thì lỗi compile: "inherits unrelated defaults for move()"
    @Override public String move() {
        return Flyer.super.move() + " and " + Swimmer.super.move();   // chọn rõ ràng
    }
}
```

**Câu trả lời mẫu:** *"Java không cho đa kế thừa class nên tránh được diamond về trạng thái. Với default method trong interface, nếu hai interface cùng có một default method thì compiler bắt class phải override và có thể gọi rõ `InterfaceName.super.method()`. Class luôn thắng interface, và interface cụ thể hơn thắng interface cha."*

### English

**The diamond problem:** class `D` inherits from `B` and `C`, which both inherit from `A` and override the same method. When you call `d.hello()`, is it `B`'s version or `C`'s? The inheritance graph is diamond-shaped, hence the name.

```
      A.hello()
     /         \
 B.hello()   C.hello()
     \         /
         D   → which one?
```

C++ allows multiple class inheritance, so it has to deal with this (virtual inheritance).

**How Java avoids it:**
1. **A class can extend only one class**, so there's no diamond through classes, and no conflicts over **state** (fields).
2. **A class can implement many interfaces**, but before Java 8 interfaces had no code, so there was nothing to conflict.
3. **Java 8 added `default` methods**, so conflicts became possible again. Java resolves them with 3 rules:
   - **Classes win over interfaces:** a method from the class (or a superclass) always takes priority over a `default` method.
   - **The more specific interface wins:** if `B extends A` and both have a default `hello()`, `B`'s version wins.
   - If it's still ambiguous, it's a **compile error**: the class must **override it itself**, and can pick one explicitly with `X.super.method()`.

```java
interface Flyer   { default String move() { return "fly"; } }
interface Swimmer { default String move() { return "swim"; } }

class Duck implements Flyer, Swimmer {
    // Without an override, compile error: "inherits unrelated defaults for move()"
    @Override public String move() {
        return Flyer.super.move() + " and " + Swimmer.super.move();   // explicit choice
    }
}
```

**A model answer:** *"Java doesn't allow multiple class inheritance, so it avoids the diamond problem for state. With default methods, if two interfaces have the same default method, the compiler forces the class to override it, and it can call `InterfaceName.super.method()` explicitly. Classes always win over interfaces, and a more specific interface wins over its parent."*

@@@ jc-overload-override | Overloading và overriding khác nhau thế nào? Cái nào quyết định lúc compile, cái nào lúc runtime? / Overloading vs overriding: which is resolved at compile time and which at runtime? | java | oop,polymorphism,deloitte | qa | Java core
### Tiếng Việt

| | **Overloading** (nạp chồng) | **Overriding** (ghi đè) |
|---|---|---|
| Là gì | Nhiều method **cùng tên, khác tham số** trong cùng class (hoặc class con) | Class con **định nghĩa lại** method của class cha, **cùng chữ ký** |
| Quyết định lúc | **Compile time** (static binding), theo **kiểu khai báo** của tham số | **Runtime** (dynamic dispatch), theo **kiểu thật** của object |
| Kiểu đa hình | Đa hình tĩnh | Đa hình động |
| Kiểu trả về | Có thể khác (nhưng chỉ khác kiểu trả về thì **không** phải overload) | Giống hoặc là kiểu con (covariant return) |
| Access modifier | Tùy ý | **Không được hẹp hơn** (public không thể thành protected) |
| Checked exception | Tùy ý | **Không được ném rộng hơn** method cha |
| `static`, `private`, `final` | Overload được | **Không override được** (static chỉ bị **che**, gọi là method hiding) |

**Ví dụ cho thấy sự khác biệt:**
```java
class Animal { String sound() { return "..."; } }
class Dog extends Animal { @Override String sound() { return "Woof"; } }

class Printer {
    String print(Animal a) { return "animal"; }
    String print(Dog d)    { return "dog"; }
}

Animal a = new Dog();
a.sound();                  // "Woof"   : overriding, chọn theo kiểu THẬT (Dog) lúc runtime
new Printer().print(a);     // "animal" : overloading, chọn theo kiểu KHAI BÁO (Animal) lúc compile
```

Câu thứ hai là **bẫy hay gặp**: dù object thật là `Dog`, compiler đã chọn `print(Animal)` vì biến `a` khai báo kiểu `Animal`.

**Static method:**
```java
class Parent { static String who() { return "parent"; } }
class Child extends Parent { static String who() { return "child"; } }   // hiding, không phải overriding
Parent p = new Child();
p.who();   // "parent" : static gắn theo kiểu khai báo
```

**Thực hành tốt:** luôn dùng `@Override` để compiler báo lỗi nếu chữ ký không khớp (ví dụ viết nhầm `equals(MyClass o)` thay vì `equals(Object o)`, thành ra overload chứ không phải override).

### English

| | **Overloading** | **Overriding** |
|---|---|---|
| What | Several methods with **the same name and different parameters** in one class (or a subclass) | A subclass **redefines** a parent method with **the same signature** |
| Resolved at | **Compile time** (static binding), by the **declared type** of the arguments | **Runtime** (dynamic dispatch), by the **actual type** of the object |
| Kind of polymorphism | Static polymorphism | Dynamic polymorphism |
| Return type | Can differ (but a different return type alone is **not** an overload) | Same, or a subtype (covariant return) |
| Access modifier | Anything | **Can't be narrower** (public can't become protected) |
| Checked exceptions | Anything | **Can't throw broader** ones than the parent method |
| `static`, `private`, `final` | Can be overloaded | **Can't be overridden** (statics are only **hidden**, called method hiding) |

**An example showing the difference:**
```java
class Animal { String sound() { return "..."; } }
class Dog extends Animal { @Override String sound() { return "Woof"; } }

class Printer {
    String print(Animal a) { return "animal"; }
    String print(Dog d)    { return "dog"; }
}

Animal a = new Dog();
a.sound();                  // "Woof"   : overriding, chosen by the ACTUAL type (Dog) at runtime
new Printer().print(a);     // "animal" : overloading, chosen by the DECLARED type (Animal) at compile time
```

The second line is **a common trap**: even though the actual object is a `Dog`, the compiler already chose `print(Animal)` because `a` is declared as `Animal`.

**Static methods:**
```java
class Parent { static String who() { return "parent"; } }
class Child extends Parent { static String who() { return "child"; } }   // hiding, not overriding
Parent p = new Child();
p.who();   // "parent" : statics bind to the declared type
```

**Good practice:** always use `@Override` so the compiler complains if the signature doesn't match (for example writing `equals(MyClass o)` instead of `equals(Object o)` by mistake, which overloads instead of overriding).

@@@ jc-sync-vs-lock | synchronized và ReentrantLock khác nhau thế nào? Khi nào thật sự cần Lock? / synchronized vs ReentrantLock: how do they differ, and when do you actually need a Lock? | java | concurrency,lock,deloitte | qa | Java core
### Tiếng Việt

Cả hai đều là khóa **reentrant** (thread đang giữ khóa có thể lấy lại khóa đó) và đảm bảo **mutual exclusion** cùng **visibility** (happens-before).

| | `synchronized` | `ReentrantLock` |
|---|---|---|
| Cú pháp | Từ khóa, khóa và mở **tự động** (kể cả khi có exception) | Phải gọi `lock()` và **`unlock()` trong `finally`** |
| Thử lấy khóa không chờ | Không | **`tryLock()`**, `tryLock(timeout)` |
| Ngắt khi đang chờ | Không | **`lockInterruptibly()`** |
| Công bằng (fairness) | Không | `new ReentrantLock(true)`: thread chờ lâu nhất được trước |
| Nhiều điều kiện chờ | Một (`wait/notify`) | **Nhiều `Condition`** (`notFull`, `notEmpty`) |
| Khóa và mở ở hai method khác nhau | Không (theo block) | Được |
| Kiểm tra trạng thái | Không | `isLocked()`, `getQueueLength()` |
| Virtual threads (Java 21–23) | **Gây pinning** khi chặn trong block | Không pinning. Java 24 đã sửa cho `synchronized` |

```java
private final ReentrantLock lock = new ReentrantLock();

public boolean transfer(Account from, Account to, Money amount) throws InterruptedException {
    if (!lock.tryLock(500, TimeUnit.MILLISECONDS)) {
        return false;                       // không chờ mãi: báo bận thay vì treo thread
    }
    try {
        from.debit(amount);
        to.credit(amount);
        return true;
    } finally {
        lock.unlock();                      // BẮT BUỘC trong finally
    }
}
```

**Khi nào thật sự cần `ReentrantLock`:**
- Cần **timeout** hoặc **thử khóa** để tránh treo hoặc deadlock.
- Cần **hủy được** khi đang chờ (shutdown, hủy request).
- Cần **nhiều condition** (bounded buffer tự cài).
- Cần **fairness**.
- Chạy trên **virtual threads với Java 21–23** và có I/O bên trong vùng khóa.

**Còn lại thì dùng `synchronized`**: ngắn hơn, không quên `unlock`, JVM tối ưu tốt.

**Các lựa chọn khác nên nhắc:**
- `ReentrantReadWriteLock` hoặc `StampedLock`: nhiều đọc, ít ghi.
- `AtomicInteger`, `LongAdder`, `ConcurrentHashMap.compute()`: thao tác đơn giản, không cần khóa.
- **Khóa trong JVM chỉ có tác dụng trong một instance.** Ứng dụng chạy nhiều pod thì phải khóa ở **database** (optimistic/pessimistic locking, unique constraint) hoặc [khóa phân tán](#sd-distributed-lock). Đây là điểm ghi điểm ở vòng senior.

### English

Both are **reentrant** locks (a thread holding the lock can acquire it again) and guarantee **mutual exclusion** and **visibility** (happens-before).

| | `synchronized` | `ReentrantLock` |
|---|---|---|
| Syntax | A keyword; locks and unlocks **automatically** (even on exceptions) | You must call `lock()` and **`unlock()` in `finally`** |
| Try without waiting | No | **`tryLock()`**, `tryLock(timeout)` |
| Interruptible while waiting | No | **`lockInterruptibly()`** |
| Fairness | No | `new ReentrantLock(true)`: the longest-waiting thread goes first |
| Multiple wait conditions | One (`wait/notify`) | **Many `Condition`s** (`notFull`, `notEmpty`) |
| Lock and unlock in different methods | No (block-scoped) | Yes |
| State inspection | No | `isLocked()`, `getQueueLength()` |
| Virtual threads (Java 21–23) | **Pins** when blocking inside the block | No pinning. Java 24 fixed this for `synchronized` |

```java
private final ReentrantLock lock = new ReentrantLock();

public boolean transfer(Account from, Account to, Money amount) throws InterruptedException {
    if (!lock.tryLock(500, TimeUnit.MILLISECONDS)) {
        return false;                       // don't wait forever: report busy instead of hanging
    }
    try {
        from.debit(amount);
        to.credit(amount);
        return true;
    } finally {
        lock.unlock();                      // MUST be in finally
    }
}
```

**When you actually need `ReentrantLock`:**
- You need a **timeout** or a **try-lock** to avoid hanging or deadlocks.
- Waiting must be **cancellable** (shutdown, request cancellation).
- You need **multiple conditions** (a hand-rolled bounded buffer).
- You need **fairness**.
- You run on **virtual threads with Java 21–23** and do I/O inside the locked region.

**Otherwise use `synchronized`**: shorter, no forgotten `unlock`, and well optimized by the JVM.

**Other options worth mentioning:**
- `ReentrantReadWriteLock` or `StampedLock`: many reads, few writes.
- `AtomicInteger`, `LongAdder`, `ConcurrentHashMap.compute()`: simple operations without locks.
- **A JVM lock only works within one instance.** An application running on several pods must lock in the **database** (optimistic/pessimistic locking, unique constraints) or use a [distributed lock](#sd-distributed-lock). This earns points in senior rounds.

@@@ dsa-linked-list-cycle | Phát hiện chu trình trong linked list (và tìm điểm bắt đầu chu trình). / Detect a cycle in a linked list (and find where the cycle starts). | coding | dsa,linked-list,two-pointers,deloitte | qa | DSA
### Tiếng Việt

**Đề bài:** cho `head` của một linked list, kiểm tra list có chu trình không (một node trỏ ngược về node trước đó). LeetCode [141](https://leetcode.com/problems/linked-list-cycle/) (Easy), mở rộng [142](https://leetcode.com/problems/linked-list-cycle-ii/) (Medium).

**Cách 1: HashSet.** Duyệt list, lưu node đã gặp; gặp lại node cũ thì có chu trình. O(n) thời gian, **O(n) bộ nhớ**.

**Cách 2: Floyd (rùa và thỏ), O(1) bộ nhớ.** Con trỏ `slow` đi 1 bước, `fast` đi 2 bước. Có chu trình thì `fast` sẽ **đuổi kịp** `slow` bên trong vòng (mỗi bước khoảng cách giảm 1); không có thì `fast` chạm `null`.

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;      // so sánh THAM CHIẾU node, không phải giá trị
    }
    return false;
}
```

**Mở rộng (142): tìm node bắt đầu chu trình.** Sau khi gặp nhau, đưa một con trỏ về `head`, rồi cho **cả hai đi 1 bước** mỗi lần; chỗ chúng gặp nhau là điểm bắt đầu chu trình.

```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;
        }
    }
    return null;
}
```

**Vì sao đúng:** gọi `a` là khoảng cách từ head tới đầu chu trình, `b` là quãng từ đầu chu trình tới điểm gặp, `c` là độ dài chu trình. `fast` đi gấp đôi `slow`, nên 2(a + b) = a + b + k·c, suy ra **a = k·c − b**. Tức đi `a` bước từ head bằng đúng đi `a` bước từ điểm gặp, cả hai cùng tới đầu chu trình.

**Độ phức tạp:** O(n) thời gian, O(1) bộ nhớ.

**Khi nói:** nêu cách HashSet trước (dễ, O(n) bộ nhớ), rồi tối ưu bằng Floyd. Hỏi interviewer có được sửa list không (không nên). Case biên: list rỗng, một node, một node tự trỏ vào chính nó.

### English

**Problem:** given the `head` of a linked list, determine whether it has a cycle (some node points back to an earlier node). LeetCode [141](https://leetcode.com/problems/linked-list-cycle/) (Easy), extended in [142](https://leetcode.com/problems/linked-list-cycle-ii/) (Medium).

**Approach 1: a HashSet.** Walk the list storing visited nodes; seeing one again means a cycle. O(n) time, **O(n) memory**.

**Approach 2: Floyd (tortoise and hare), O(1) memory.** `slow` moves 1 step and `fast` moves 2. With a cycle, `fast` **catches up** with `slow` inside the loop (the gap shrinks by 1 each step); without one, `fast` reaches `null`.

```java
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;      // compare node REFERENCES, not values
    }
    return false;
}
```

**Extension (142): find the node where the cycle starts.** After they meet, move one pointer back to `head`, then advance **both one step** at a time; where they meet is the start of the cycle.

```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return p;
        }
    }
    return null;
}
```

**Why it works:** let `a` be the distance from the head to the cycle start, `b` the distance from the cycle start to the meeting point, and `c` the cycle length. `fast` travels twice as far as `slow`, so 2(a + b) = a + b + k·c, which gives **a = k·c − b**. So walking `a` steps from the head equals walking `a` steps from the meeting point: both land at the cycle start.

**Complexity:** O(n) time, O(1) memory.

**When presenting:** give the HashSet approach first (simple, O(n) memory), then optimize with Floyd. Ask whether you may modify the list (you shouldn't). Edge cases: an empty list, one node, a single node pointing to itself.

@@@ spring-1 | IoC và dependency injection là gì? Vì sao nên dùng constructor injection thay vì field injection? / What are IoC and dependency injection, and why prefer constructor injection over field injection? | spring | | override
### Tiếng Việt

**IoC (Inversion of Control):** thay vì object **tự tạo** các phụ thuộc của nó (`new PaymentClient()`), việc tạo và nối object được **giao cho container** (Spring `ApplicationContext`). **Dependency injection** là cách thực hiện IoC: container **truyền phụ thuộc vào** object.

**Lợi ích:** giảm phụ thuộc chặt (class phụ thuộc vào interface, không vào cách tạo implementation), **dễ test** (truyền mock vào), dễ đổi implementation theo cấu hình hay profile, và quản lý vòng đời tập trung.

**Ba cách inject:**

| | Constructor | Setter | Field (`@Autowired` trên field) |
|---|---|---|---|
| Field `final`, bất biến | **Có** | Không | Không |
| Bắt buộc phải có phụ thuộc | **Có**: thiếu là lỗi lúc khởi động | Không (tùy chọn) | Không rõ ràng |
| Test không cần Spring | **`new OrderService(mockRepo, mockClient)`** | Được | Phải dùng reflection hoặc Spring |
| Phát hiện class quá nhiều trách nhiệm | **Dễ**: constructor 8 tham số là dấu hiệu | Khó | Rất khó (thêm field quá dễ) |
| Phụ thuộc vòng (A cần B, B cần A) | **Báo lỗi ngay khi khởi động** | Che giấu | Che giấu |
| Dùng khi | **Mặc định** | Phụ thuộc tùy chọn, có giá trị mặc định | Tránh, trừ trong test |

```java
@Service
public class OrderService {
    private final OrderRepository repo;
    private final PaymentClient payment;

    // Chỉ có 1 constructor thì không cần @Autowired (từ Spring 4.3)
    public OrderService(OrderRepository repo, PaymentClient payment) {
        this.repo = repo;
        this.payment = payment;
    }
}
// Hoặc ngắn gọn với Lombok: @RequiredArgsConstructor trên class có field final
```

**Nhiều implementation cho một interface:** dùng `@Qualifier("stripe")`, `@Primary`, hoặc inject `Map<String, PaymentGateway>` / `List<PaymentGateway>` để chọn theo khóa lúc chạy (Strategy pattern).

**Câu trả lời mẫu:** *"DI nghĩa là Spring tạo và truyền phụ thuộc vào class thay vì class tự `new`. Tôi dùng constructor injection vì field có thể `final`, phụ thuộc bắt buộc thể hiện rõ, test được bằng `new` với mock mà không cần khởi động Spring, và phụ thuộc vòng bị phát hiện ngay. Constructor quá dài cũng nhắc tôi rằng class đang làm quá nhiều việc."*

### English

**IoC (Inversion of Control):** instead of an object **creating** its own dependencies (`new PaymentClient()`), creating and wiring objects is **handed to a container** (Spring's `ApplicationContext`). **Dependency injection** is how IoC is done: the container **passes dependencies into** the object.

**Benefits:** looser coupling (a class depends on an interface, not on how the implementation is built), **easy testing** (pass in mocks), swapping implementations by configuration or profile, and centralized lifecycle management.

**Three ways to inject:**

| | Constructor | Setter | Field (`@Autowired` on a field) |
|---|---|---|---|
| `final`, immutable fields | **Yes** | No | No |
| Dependency is mandatory | **Yes**: missing ones fail at startup | No (optional) | Unclear |
| Test without Spring | **`new OrderService(mockRepo, mockClient)`** | Yes | Needs reflection or Spring |
| Spotting a class with too many responsibilities | **Easy**: an 8-parameter constructor is a warning | Hard | Very hard (adding a field is too easy) |
| Circular dependencies (A needs B, B needs A) | **Fail fast at startup** | Hidden | Hidden |
| Use for | **The default** | Optional dependencies with defaults | Avoid, except in tests |

```java
@Service
public class OrderService {
    private final OrderRepository repo;
    private final PaymentClient payment;

    // With a single constructor, @Autowired isn't needed (since Spring 4.3)
    public OrderService(OrderRepository repo, PaymentClient payment) {
        this.repo = repo;
        this.payment = payment;
    }
}
// Or concisely with Lombok: @RequiredArgsConstructor on a class with final fields
```

**Several implementations of one interface:** use `@Qualifier("stripe")`, `@Primary`, or inject a `Map<String, PaymentGateway>` / `List<PaymentGateway>` to choose by key at runtime (the Strategy pattern).

**A model answer:** *"DI means Spring creates dependencies and passes them into a class instead of the class calling `new`. I use constructor injection because fields can be `final`, mandatory dependencies are explicit, I can test with `new` and mocks without starting Spring, and circular dependencies are caught immediately. A very long constructor also reminds me the class is doing too much."*

@@@ sp-scopes | Spring có những bean scope nào? Khi nào dùng scope khác singleton? / What bean scopes does Spring have, and when would you use something other than singleton? | spring | spring,bean-scope,deloitte | qa | Spring core
### Tiếng Việt

| Scope | Số instance | Dùng khi |
|---|---|---|
| **singleton** (mặc định) | **Một** cho mỗi `ApplicationContext` | Hầu hết bean: service, repository, controller, client. Bean phải **stateless** hoặc thread-safe |
| **prototype** | **Mới mỗi lần** được lấy từ container | Object có trạng thái riêng, không chia sẻ: builder, parser không thread-safe, task có dữ liệu riêng |
| **request** | Một cho mỗi HTTP request | Dữ liệu theo request: request context, audit info |
| **session** | Một cho mỗi HTTP session | Dữ liệu theo phiên đăng nhập (giỏ hàng trong web app truyền thống) |
| **application** | Một cho mỗi `ServletContext` | Hiếm dùng |
| **websocket** | Một cho mỗi phiên WebSocket | |

**Lưu ý quan trọng:**
1. **Singleton không phải thread-safe tự động.** Một instance phục vụ mọi request đồng thời, nên **không lưu trạng thái theo request vào field**:
```java
@Service
class ReportService {
    private User currentUser;          // SAI: request A và B ghi đè lên nhau
    public Report build(User u) { this.currentUser = u; ... }
}
```
2. **Inject prototype vào singleton**: prototype chỉ được tạo **một lần** lúc singleton được tạo, nên mất ý nghĩa. Cách đúng: `ObjectProvider<MyPrototype>` (gọi `getObject()` mỗi lần cần), `@Lookup` method, hoặc proxy (`proxyMode = ScopedProxyMode.TARGET_CLASS`).
3. **Inject request/session scope vào singleton** cần **scoped proxy**: Spring inject một proxy, mỗi lần gọi proxy tìm đúng bean của request hiện tại. `@RequestScope` và `@SessionScope` đã bật sẵn proxy.
4. Spring **không quản lý việc hủy** bean prototype (`@PreDestroy` không được gọi).
5. Với nhiều instance ứng dụng (nhiều pod), session scope chỉ đúng khi dùng session dùng chung (Spring Session + Redis) hoặc sticky session. Xem [Stateless và stateful](#sd-stateless-stateful).

```java
@Component
@RequestScope                       // một instance mỗi HTTP request, đã có proxy
class RequestContext { String correlationId; String tenantId; }

@Service
class InvoiceService {
    private final ObjectProvider<PdfRenderer> renderers;   // PdfRenderer là prototype, không thread-safe
    InvoiceService(ObjectProvider<PdfRenderer> renderers) { this.renderers = renderers; }
    byte[] render(Invoice i) { return renderers.getObject().render(i); }   // instance mới mỗi lần
}
```

### English

| Scope | Number of instances | Use when |
|---|---|---|
| **singleton** (default) | **One** per `ApplicationContext` | Most beans: services, repositories, controllers, clients. The bean must be **stateless** or thread-safe |
| **prototype** | **A new one every time** it's requested from the container | Objects with their own unshared state: builders, non-thread-safe parsers, tasks with their own data |
| **request** | One per HTTP request | Per-request data: request context, audit info |
| **session** | One per HTTP session | Per-login-session data (a cart in a traditional web app) |
| **application** | One per `ServletContext` | Rarely used |
| **websocket** | One per WebSocket session | |

**Important points:**
1. **Singletons are not automatically thread-safe.** One instance serves all concurrent requests, so **don't store per-request state in fields**:
```java
@Service
class ReportService {
    private User currentUser;          // WRONG: requests A and B overwrite each other
    public Report build(User u) { this.currentUser = u; ... }
}
```
2. **Injecting a prototype into a singleton**: the prototype is created **only once**, when the singleton is created, so it loses its point. The right ways: `ObjectProvider<MyPrototype>` (call `getObject()` each time), a `@Lookup` method, or a proxy (`proxyMode = ScopedProxyMode.TARGET_CLASS`).
3. **Injecting request/session-scoped beans into a singleton** needs a **scoped proxy**: Spring injects a proxy, and each call finds the bean for the current request. `@RequestScope` and `@SessionScope` enable the proxy already.
4. Spring **doesn't manage destruction** of prototype beans (`@PreDestroy` isn't called).
5. With several application instances (several pods), session scope only works with a shared session store (Spring Session + Redis) or sticky sessions. See [Stateless vs stateful](#sd-stateless-stateful).

```java
@Component
@RequestScope                       // one instance per HTTP request, proxy included
class RequestContext { String correlationId; String tenantId; }

@Service
class InvoiceService {
    private final ObjectProvider<PdfRenderer> renderers;   // PdfRenderer is a prototype, not thread-safe
    InvoiceService(ObjectProvider<PdfRenderer> renderers) { this.renderers = renderers; }
    byte[] render(Invoice i) { return renderers.getObject().render(i); }   // a new instance each time
}
```

@@@ sp-stereotypes | @Component, @Service, @Repository và @Controller khác nhau thế nào? / How do @Component, @Service, @Repository and @Controller differ? | spring | spring,annotations,deloitte | qa | Spring core
### Tiếng Việt

Cả bốn đều là **stereotype annotation**: đánh dấu class để **component scanning** tìm thấy và đăng ký làm bean. `@Service`, `@Repository`, `@Controller` đều được meta-annotate bằng `@Component`.

| Annotation | Tầng | Có thêm gì ngoài `@Component` |
|---|---|---|
| `@Component` | Chung, không thuộc tầng cụ thể | Không |
| `@Service` | Logic nghiệp vụ | **Không có hành vi kỹ thuật thêm**; chỉ thể hiện ý nghĩa, giúp đọc code và viết pointcut AOP theo tầng |
| `@Repository` | Truy cập dữ liệu | **Dịch exception**: `PersistenceExceptionTranslationPostProcessor` chuyển exception riêng của JPA, JDBC, Hibernate thành `DataAccessException` thống nhất của Spring (ví dụ `DataIntegrityViolationException`) |
| `@Controller` | Web (MVC) | Được `DispatcherServlet` nhận diện là handler; method trả **tên view** |
| `@RestController` | REST API | = `@Controller` + `@ResponseBody`: giá trị trả về được ghi thẳng vào body (JSON) |

**Vì sao không dùng `@Component` cho tất cả?**
- `@Repository` và `@Controller` có **hành vi thật** khác biệt như trên.
- `@Service` giúp **đọc kiến trúc** ngay từ annotation, viết AOP hay ArchUnit test theo tầng ("controller không được gọi thẳng repository").
- Với Spring Data JPA, interface `extends JpaRepository` **không cần** `@Repository`: Spring Data tự tạo bean và đã có dịch exception.

**Các annotation liên quan hay bị hỏi kèm:**
- `@Configuration` + `@Bean`: khai báo bean bằng code, dùng cho class của thư viện bên ngoài (không gắn annotation vào được) hoặc khi cần logic tạo bean.
- `@ControllerAdvice` / `@RestControllerAdvice`: xử lý exception tập trung cho mọi controller.
- `@ComponentScan`: `@SpringBootApplication` đã gồm sẵn, quét package chứa class main và các package con. Đặt class ở **ngoài** package đó thì không được quét.

### English

All four are **stereotype annotations**: they mark a class so **component scanning** finds it and registers it as a bean. `@Service`, `@Repository` and `@Controller` are all meta-annotated with `@Component`.

| Annotation | Layer | What it adds beyond `@Component` |
|---|---|---|
| `@Component` | Generic, no specific layer | Nothing |
| `@Service` | Business logic | **No extra technical behaviour**; it only conveys meaning, aiding readability and layer-based AOP pointcuts |
| `@Repository` | Data access | **Exception translation**: `PersistenceExceptionTranslationPostProcessor` converts JPA-, JDBC- and Hibernate-specific exceptions into Spring's uniform `DataAccessException` hierarchy (e.g. `DataIntegrityViolationException`) |
| `@Controller` | Web (MVC) | Recognized by `DispatcherServlet` as a handler; methods return a **view name** |
| `@RestController` | REST APIs | = `@Controller` + `@ResponseBody`: return values are written straight to the body (JSON) |

**Why not use `@Component` for everything?**
- `@Repository` and `@Controller` have the **real behavioural differences** above.
- `@Service` lets you **read the architecture** from the annotations and write layer-based AOP or ArchUnit tests ("controllers must not call repositories directly").
- With Spring Data JPA, an interface that `extends JpaRepository` **doesn't need** `@Repository`: Spring Data creates the bean and already translates exceptions.

**Related annotations often asked alongside:**
- `@Configuration` + `@Bean`: declare beans in code, for third-party classes (which you can't annotate) or when bean creation needs logic.
- `@ControllerAdvice` / `@RestControllerAdvice`: centralized exception handling for all controllers.
- `@ComponentScan`: already included in `@SpringBootApplication`, scanning the main class's package and its subpackages. Classes placed **outside** that package aren't scanned.

@@@ spring-4 | @Transactional: propagation REQUIRED (mặc định) và REQUIRES_NEW khác nhau thế nào? Isolation là gì? / @Transactional: how do the default REQUIRED propagation and REQUIRES_NEW differ, and what is isolation? | spring | | override
### Tiếng Việt

**Propagation** quyết định method `@Transactional` làm gì **khi đã có transaction đang chạy** ở nơi gọi nó.

| Propagation | Đã có transaction | Chưa có transaction |
|---|---|---|
| **REQUIRED** (mặc định) | **Tham gia** transaction đó | Tạo mới |
| **REQUIRES_NEW** | **Tạm dừng** transaction ngoài, **tạo transaction mới độc lập** | Tạo mới |
| SUPPORTS | Tham gia | Chạy không transaction |
| MANDATORY | Tham gia | Ném exception |
| NOT_SUPPORTED | Tạm dừng, chạy không transaction | Chạy không transaction |
| NEVER | Ném exception | Chạy không transaction |
| NESTED | Tạo **savepoint** trong transaction ngoài; rollback về savepoint được | Tạo mới |

**REQUIRED và REQUIRES_NEW bằng ví dụ:** ghi **audit log** cho thao tác chuyển tiền, kể cả khi chuyển tiền thất bại.

```java
@Service
class TransferService {
    private final AuditService audit;     // bean KHÁC, để đi qua proxy

    @Transactional                        // REQUIRED
    public void transfer(TransferCmd cmd) {
        audit.log("TRANSFER_ATTEMPT", cmd);        // REQUIRES_NEW: commit ngay, độc lập
        accountRepo.debit(cmd.from(), cmd.amount());
        accountRepo.credit(cmd.to(), cmd.amount());   // lỗi ở đây → rollback debit/credit, audit VẪN còn
    }
}

@Service
class AuditService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void log(String action, Object data) { auditRepo.save(new AuditEntry(action, data)); }
}
```

- Nếu `log()` dùng REQUIRED: nó **chung** transaction với `transfer()`, chuyển tiền lỗi thì audit **cũng bị rollback**.
- Với REQUIRES_NEW: audit có transaction **riêng, commit ngay**, không bị ảnh hưởng.

**Bẫy hay bị hỏi:**
1. **Gọi nội bộ trong cùng class** (`this.log()`) **không đi qua proxy**, nên `@Transactional` của method được gọi **bị bỏ qua**. Phải đặt ở bean khác.
2. **REQUIRES_NEW dùng thêm một kết nối DB** trong khi kết nối ngoài vẫn bị giữ. Dùng nhiều dưới tải cao có thể **cạn connection pool** hoặc deadlock pool.
3. **"Transaction silently rolled back because it has been marked as rollback-only":** method trong REQUIRED ném exception (đánh dấu rollback-only), method ngoài bắt exception rồi vẫn cố commit. Cả transaction vẫn bị rollback và có `UnexpectedRollbackException`.
4. Mặc định chỉ **rollback với unchecked exception** (`RuntimeException`, `Error`); checked exception thì **vẫn commit**. Dùng `rollbackFor = Exception.class` nếu cần.
5. `@Transactional` trên method **private** hoặc gọi từ ngoài Spring không có tác dụng.

**Isolation** (mức cô lập giữa các transaction đồng thời):

| Mức | Chống được | PostgreSQL / MySQL mặc định |
|---|---|---|
| READ_UNCOMMITTED | Không chống gì (dirty read) | |
| **READ_COMMITTED** | Dirty read | **PostgreSQL**, Oracle |
| **REPEATABLE_READ** | + Non-repeatable read | **MySQL InnoDB** |
| SERIALIZABLE | + Phantom read, mọi bất thường | |

`@Transactional(isolation = Isolation.DEFAULT)` dùng mặc định của DB. Mức cao hơn an toàn hơn nhưng giảm đồng thời và gây lỗi serialization phải retry. Thực tế thường giữ READ_COMMITTED và dùng **optimistic locking** (`@Version`) hoặc `SELECT ... FOR UPDATE` cho chỗ cần. Xem [Optimistic vs pessimistic locking](#database-14).

### English

**Propagation** decides what a `@Transactional` method does **when a transaction is already running** in its caller.

| Propagation | A transaction exists | No transaction |
|---|---|---|
| **REQUIRED** (default) | **Joins** it | Creates one |
| **REQUIRES_NEW** | **Suspends** the outer transaction and **creates a new, independent one** | Creates one |
| SUPPORTS | Joins | Runs without a transaction |
| MANDATORY | Joins | Throws an exception |
| NOT_SUPPORTED | Suspends it and runs without a transaction | Runs without a transaction |
| NEVER | Throws an exception | Runs without a transaction |
| NESTED | Creates a **savepoint** in the outer transaction; can roll back to it | Creates one |

**REQUIRED vs REQUIRES_NEW by example:** writing an **audit log** for a money transfer, even when the transfer fails.

```java
@Service
class TransferService {
    private final AuditService audit;     // a DIFFERENT bean, so the call goes through the proxy

    @Transactional                        // REQUIRED
    public void transfer(TransferCmd cmd) {
        audit.log("TRANSFER_ATTEMPT", cmd);        // REQUIRES_NEW: commits immediately, independently
        accountRepo.debit(cmd.from(), cmd.amount());
        accountRepo.credit(cmd.to(), cmd.amount());   // failure here → debit/credit roll back, the audit STAYS
    }
}

@Service
class AuditService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void log(String action, Object data) { auditRepo.save(new AuditEntry(action, data)); }
}
```

- If `log()` used REQUIRED, it would **share** `transfer()`'s transaction, and a failed transfer would roll back the audit **too**.
- With REQUIRES_NEW, the audit has **its own transaction that commits immediately**, unaffected.

**Commonly asked traps:**
1. **Internal calls within the same class** (`this.log()`) **bypass the proxy**, so the called method's `@Transactional` is **ignored**. Put it in another bean.
2. **REQUIRES_NEW takes a second DB connection** while the outer one is still held. Heavy use under load can **exhaust the connection pool** or deadlock it.
3. **"Transaction silently rolled back because it has been marked as rollback-only":** an inner REQUIRED method throws (marking rollback-only), the outer method catches the exception and still tries to commit. The whole transaction rolls back anyway with an `UnexpectedRollbackException`.
4. By default it only **rolls back on unchecked exceptions** (`RuntimeException`, `Error`); checked exceptions **still commit**. Use `rollbackFor = Exception.class` if needed.
5. `@Transactional` on **private** methods, or on calls from outside Spring, has no effect.

**Isolation** (how concurrent transactions are isolated from each other):

| Level | Prevents | PostgreSQL / MySQL default |
|---|---|---|
| READ_UNCOMMITTED | Nothing (dirty reads) | |
| **READ_COMMITTED** | Dirty reads | **PostgreSQL**, Oracle |
| **REPEATABLE_READ** | + Non-repeatable reads | **MySQL InnoDB** |
| SERIALIZABLE | + Phantom reads, all anomalies | |

`@Transactional(isolation = Isolation.DEFAULT)` uses the database's default. Higher levels are safer but reduce concurrency and cause serialization failures that need retries. In practice people usually keep READ_COMMITTED and use **optimistic locking** (`@Version`) or `SELECT ... FOR UPDATE` where needed. See [Optimistic vs pessimistic locking](#database-14).

@@@ behavioral-hard-bug | Kể về một bug khó nhất bạn từng sửa. / Walk me through a challenging bug you fixed. | behavioral | behavioral,debugging,deloitte | qa | Behavioral
### Tiếng Việt

**Interviewer muốn thấy:** cách bạn **điều tra có hệ thống** (không đoán mò), dùng công cụ, giữ bình tĩnh, và **ngăn bug tái diễn**. Cách sửa ít quan trọng hơn quá trình.

**Khung STAR, tập trung vào phần Action:**
1. **Situation (15 giây):** hệ thống gì, triệu chứng gì, ảnh hưởng ra sao (bao nhiêu user, mất tiền, vi phạm SLA).
2. **Task:** vai trò của bạn: được giao, tự nhận, hay đang trực sự cố.
3. **Action (phần chính, khoảng 60%):**
   - Tái hiện được chưa? Thu hẹp phạm vi thế nào (môi trường, thời điểm, loại dữ liệu)?
   - Dùng **công cụ** gì: log có trace id, metrics, thread dump, heap dump, `EXPLAIN ANALYZE`, profiler, debugger, `git bisect`.
   - Đã loại trừ giả thuyết nào, vì sao.
   - **Nguyên nhân gốc** (root cause) là gì, không chỉ triệu chứng.
   - Sửa thế nào, **kiểm chứng** thế nào (test tái hiện bug, deploy dần).
4. **Result:** con số cụ thể; và **bài học, việc làm để không tái diễn** (thêm test, alert, sửa quy trình, chia sẻ với nhóm).

**Ví dụ mẫu (thay bằng chuyện thật của bạn):**
*"Ở [DXC], hệ thống tính phí bảo hiểm thỉnh thoảng tạo **trùng hóa đơn** cho cùng một hợp đồng, khoảng 0,1% số hợp đồng mỗi tháng, gây khiếu nại từ khách hàng.*
*Bug không tái hiện được ở local. Tôi lọc log theo các hợp đồng bị trùng và thấy hai bản ghi được tạo cách nhau vài mili giây, **ở hai pod khác nhau**. Từ đó tôi nghi đến xử lý đồng thời: job tính phí dùng `@Scheduled`, và sau khi scale lên 2 pod thì **cả hai pod cùng chạy job**. Code kiểm tra 'đã có hóa đơn chưa' rồi mới insert, nhưng hai pod cùng kiểm tra trước khi bên kia kịp insert (lỗi check-then-act). Khóa `synchronized` sẵn có chỉ tác dụng trong một JVM.*
*Tôi sửa ở ba lớp: thêm **unique constraint** `(policy_id, billing_period)` để DB chặn trùng tuyệt đối; dùng **ShedLock** để mỗi lần chỉ một pod chạy job; và xử lý `DataIntegrityViolationException` như một trường hợp idempotent. Tôi viết integration test với Testcontainers chạy hai luồng song song để tái hiện bug trước khi sửa.*
*Sau khi deploy, không còn hóa đơn trùng. Tôi viết script dọn dữ liệu trùng cũ, và đề xuất checklist review: mọi job định kỳ phải an toàn khi chạy nhiều instance."*

**Lưu ý:**
- Chọn bug có **chiều sâu kỹ thuật** (đồng thời, transaction, memory leak, hiệu năng, timezone, cache) chứ không phải lỗi gõ nhầm.
- Nói "**tôi**" làm gì, nhưng ghi nhận người khác nếu có giúp.
- Chuẩn bị cho câu hỏi tiếp: "Nếu làm lại thì bạn làm khác gì?", "Sao không phát hiện sớm hơn?"

### English

**What the interviewer wants to see:** that you **investigate systematically** (not by guessing), use tools, stay calm, and **prevent recurrence**. The process matters more than the fix.

**The STAR framework, focused on Action:**
1. **Situation (15 seconds):** which system, what symptom, what impact (how many users, money lost, SLA breached).
2. **Task:** your role: assigned, volunteered, or on call.
3. **Action (the main part, about 60%):**
   - Could you reproduce it? How did you narrow it down (environment, timing, data type)?
   - Which **tools**: logs with trace ids, metrics, thread dumps, heap dumps, `EXPLAIN ANALYZE`, a profiler, a debugger, `git bisect`.
   - Which hypotheses you ruled out, and why.
   - The **root cause**, not just the symptom.
   - How you fixed it and **verified** it (a test reproducing the bug, gradual rollout).
4. **Result:** concrete numbers, plus **lessons and what you did to prevent recurrence** (tests, alerts, process changes, sharing with the team).

**A sample story (replace it with your real one):**
*"At [DXC], the premium billing system occasionally created **duplicate invoices** for the same policy, about 0.1% of policies a month, causing customer complaints.*
*It didn't reproduce locally. I filtered logs for the duplicated policies and saw the two records were created a few milliseconds apart, **on two different pods**. That pointed to concurrency: the billing job used `@Scheduled`, and after scaling to 2 pods **both pods ran the job**. The code checked 'is there already an invoice?' and then inserted, but both pods checked before either inserted (a check-then-act bug). The existing `synchronized` lock only worked within one JVM.*
*I fixed it at three levels: a **unique constraint** on `(policy_id, billing_period)` so the database blocks duplicates absolutely; **ShedLock** so only one pod runs the job at a time; and handling `DataIntegrityViolationException` as an idempotent case. Before fixing it, I wrote a Testcontainers integration test running two threads in parallel to reproduce the bug.*
*After the deploy there were no more duplicate invoices. I wrote a script to clean up the old duplicates and proposed a review checklist item: every scheduled job must be safe to run on multiple instances."*

**Notes:**
- Pick a bug with **technical depth** (concurrency, transactions, memory leaks, performance, time zones, caching), not a typo.
- Say what "**I**" did, but credit others who helped.
- Prepare for follow-ups: "What would you do differently?", "Why wasn't it caught earlier?"

@@@ hr-questions-to-ask | Khi được hỏi "Bạn có câu hỏi nào cho chúng tôi không?", nên hỏi gì? / What should you ask when they say "What questions do you have for me?" | hr | hr,closing,deloitte | qa | HR screening
### Tiếng Việt

**Luôn có câu hỏi.** Trả lời "không có" làm bạn trông thiếu quan tâm. Chuẩn bị 5–6 câu, chọn 2–3 câu **phù hợp với người phỏng vấn**, và tránh hỏi những gì đã có trên website hay vừa được nói.

**Hỏi kỹ sư hoặc tech lead:**
- "Một ngày làm việc điển hình của team như thế nào? Tỷ lệ giữa phát triển tính năng mới và bảo trì?"
- "Quy trình từ lúc merge code đến khi lên production mất bao lâu? Team deploy thường xuyên cỡ nào?"
- "Thách thức kỹ thuật lớn nhất của team trong 6 tháng tới là gì?"
- "Code review và testing được làm thế nào? Team đang dùng AI coding tools ra sao?"
- "Gần đây team gặp sự cố production nào, và đã rút ra điều gì?"

**Hỏi manager:**
- "Sau 3 tháng và 6 tháng, như thế nào thì được xem là tôi làm tốt ở vị trí này?"
- "Team có bao nhiêu người, cơ cấu thế nào? Tôi sẽ làm việc với ai nhiều nhất?"
- "Lộ trình phát triển từ SDE2 lên senior hoặc lead ở đây như thế nào?"
- "Anh/chị thích điều gì nhất khi làm việc ở đây?"

**Riêng với công ty tư vấn hoặc outsourcing (Deloitte, EPAM, mgm):**
- "Vị trí này làm cho dự án hoặc khách hàng nào? Domain gì? Dự án dự kiến kéo dài bao lâu?"
- "Mức độ làm việc trực tiếp với khách hàng như thế nào? Có onsite không?"
- "Khi dự án kết thúc thì việc chuyển dự án diễn ra ra sao?"

**Câu kết hữu ích:** "Các bước tiếp theo của quy trình là gì, và khi nào tôi có thể nhận phản hồi?"

**Tránh ở vòng kỹ thuật:** lương, thưởng, số ngày nghỉ (để dành cho vòng HR hoặc khi có offer); "Có làm remote 100% không?" ngay câu đầu; câu hỏi chỉ cần tra Google là ra.

### English

**Always have questions.** Saying "none" makes you look uninterested. Prepare 5–6, pick 2–3 that **fit the interviewer**, and avoid asking what's on the website or was just covered.

**For engineers or tech leads:**
- "What does a typical day look like for the team? How does work split between new features and maintenance?"
- "How long does it take from merging code to reaching production? How often does the team deploy?"
- "What's the team's biggest technical challenge in the next 6 months?"
- "How are code review and testing done? How is the team using AI coding tools?"
- "What production incident did the team have recently, and what did you learn from it?"

**For managers:**
- "After 3 and 6 months, what would success look like for me in this role?"
- "How big is the team and how is it structured? Who would I work with most?"
- "What does the path from SDE2 to senior or lead look like here?"
- "What do you enjoy most about working here?"

**Specifically for consulting or outsourcing firms (Deloitte, EPAM, mgm):**
- "Which project or client is this role for? What domain? How long is it expected to last?"
- "How much direct client contact is there? Any onsite work?"
- "When a project ends, how does moving to the next one work?"

**A useful closing question:** "What are the next steps in the process, and when can I expect feedback?"

**Avoid in technical rounds:** salary, bonuses, leave days (save them for the HR round or the offer); opening with "Is it 100% remote?"; anything a quick search would answer.
