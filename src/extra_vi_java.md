@@@ java-core-1 | HashMap hoạt động bên trong thế nào? / How does HashMap work internally? | java | | override
### Tiếng Việt

**Cấu trúc:** HashMap là một mảng các "bucket" (`Node<K,V>[] table`). Mỗi bucket chứa một danh sách liên kết, hoặc một cây đỏ-đen khi bucket quá đông.

**Khi `put(key, value)`:**

1. Tính `hash = key.hashCode() ^ (h >>> 16)`: XOR 16 bit cao xuống 16 bit thấp, để các key chỉ khác nhau ở bit cao vẫn rơi vào bucket khác nhau.
2. Tính chỉ số bucket: `index = (n - 1) & hash`, với `n` là kích thước mảng, luôn là lũy thừa của 2. Phép `&` này tương đương `% n` nhưng nhanh hơn.
3. Nếu bucket trống: tạo node mới.
4. Nếu bucket có sẵn phần tử: duyệt, so `hash` trước rồi mới gọi `equals`. Trùng key thì ghi đè value; không trùng thì thêm node vào cuối.
5. **Treeify:** khi một bucket có **từ 8 node** và mảng có **ít nhất 64 bucket**, danh sách chuyển thành cây đỏ-đen, nên trường hợp xấu nhất là O(log n) thay vì O(n). Nếu mảng chưa đủ 64, HashMap resize thay vì treeify. Khi bucket giảm còn 6 node thì cây quay lại thành danh sách.
6. **Resize:** khi `size > capacity × loadFactor` (mặc định 16 × 0.75 = 12), mảng tăng gấp đôi. Nhờ kích thước là lũy thừa của 2, mỗi node chỉ ở lại vị trí cũ hoặc dời đi đúng `oldCapacity`, không cần tính lại hash.

**`get(key)`:** tính hash, tìm bucket, so `hash` rồi `equals`. Trung bình O(1).

**Lưu ý hay bị hỏi:**
- Cho phép **một key `null`** (luôn nằm ở bucket 0) và nhiều value `null`.
- **Không thread-safe:** ghi đồng thời có thể làm mất dữ liệu. Ở Java 7, resize đồng thời còn có thể tạo vòng lặp vô hạn.
- Key nên **immutable**: nếu đổi field dùng trong `hashCode` sau khi `put`, sẽ không bao giờ tìm lại được entry đó.
- Biết trước số phần tử thì khởi tạo sẵn capacity để tránh resize nhiều lần: `new HashMap<>(expected / 0.75f + 1)`, hoặc `HashMap.newHashMap(expected)` từ Java 19.

### English

"HashMap is an array of buckets. On `put`, it spreads the key's `hashCode` by XOR-ing the high 16 bits into the low 16, then picks the bucket with `(n - 1) & hash`. The table size is always a power of two, so that's a cheap modulo.

If the bucket is empty, a new node goes in. Otherwise it walks the bucket comparing hash first, then `equals`: an equal key replaces the value, otherwise a node is appended.

When one bucket reaches 8 nodes and the table has at least 64 buckets, the list becomes a red-black tree, so the worst case is O(log n) instead of O(n). When size exceeds capacity times the load factor, 0.75 by default, the table doubles. Each entry either stays at its index or moves by exactly the old capacity, so no rehashing is needed.

It allows one null key, it isn't thread-safe, and keys should be immutable, because changing a field used in `hashCode` after insertion makes the entry unreachable. If I know the size in advance, I pre-size it to avoid repeated resizing."

@@@ java-core-2 | HashMap, ConcurrentHashMap và synchronizedMap khác nhau thế nào? / HashMap vs ConcurrentHashMap vs Collections.synchronizedMap? | java | | override
### Tiếng Việt

| | HashMap | Collections.synchronizedMap | ConcurrentHashMap |
|---|---|---|---|
| Thread-safe | Không | Có | Có |
| Cách khóa | Không khóa | Một khóa cho **cả map** | CAS và khóa **từng bucket** |
| Đọc | Không khóa | Có khóa | **Không khóa** (đọc biến `volatile`) |
| `null` key/value | Cho phép | Cho phép | **Không cho phép** |
| Iterator | Fail-fast (`ConcurrentModificationException`) | Fail-fast, phải tự `synchronized` khi duyệt | **Weakly consistent**, không ném lỗi |

**ConcurrentHashMap từ Java 8 hoạt động thế nào:**
- Bucket trống: chèn bằng **CAS** (compare-and-swap), không cần khóa.
- Bucket đã có phần tử: `synchronized` trên **node đầu tiên của bucket đó**. Hai thread ghi vào hai bucket khác nhau không chặn nhau.
- Đọc hoàn toàn không khóa.
- Resize được nhiều thread cùng giúp chuyển dữ liệu.
- (Java 7 dùng "segment", mặc định 16 segment khóa riêng. Java 8 bỏ cách này.)

**Vì sao không cho `null`:** trong môi trường đa luồng, `get(key) == null` sẽ không phân biệt được "không có key" với "value là null", vì giữa `containsKey` và `get` có thể có thread khác thay đổi map.

**Bẫy hay gặp: thao tác ghép không atomic.**

```java
// SAI: hai thread có thể cùng đọc ra null rồi cùng put
if (!map.containsKey(k)) map.put(k, 1);
// SAI: đọc rồi ghi, mất cập nhật
map.put(k, map.get(k) + 1);

// ĐÚNG: atomic
map.putIfAbsent(k, 1);
map.merge(k, 1, Integer::sum);
map.computeIfAbsent(k, x -> new ArrayList<>()).add(v);
```

**Khi nào dùng:** gần như luôn chọn ConcurrentHashMap khi cần map dùng chung giữa nhiều thread, ví dụ cache trong bộ nhớ. `synchronizedMap` chỉ hợp khi cần bọc nhanh một map có sẵn và tải thấp.

### English

"`HashMap` isn't thread-safe. `Collections.synchronizedMap` wraps every method in one lock for the whole map, so all threads serialize, and you still have to synchronize manually while iterating.

`ConcurrentHashMap` since Java 8 inserts into an empty bucket with CAS and otherwise locks only the first node of that bucket, so writers to different buckets don't block each other. Reads take no lock at all. Iterators are weakly consistent: they never throw `ConcurrentModificationException`. It rejects null keys and values, because in a concurrent map a null result would be ambiguous between 'absent' and 'mapped to null'.

The common bug is compound operations: check-then-put or get-then-put isn't atomic even on a concurrent map. I use `putIfAbsent`, `merge` or `computeIfAbsent`, for example `map.merge(key, 1, Integer::sum)` for counters."

@@@ java-core-3 | Quan hệ giữa equals() và hashCode() là gì? / What is the contract between equals() and hashCode()? | java | | override
### Tiếng Việt

**Hợp đồng (contract):**
1. Hai object `equals` nhau thì **bắt buộc** `hashCode` bằng nhau.
2. `hashCode` bằng nhau thì **chưa chắc** `equals` (đó là collision, chấp nhận được).
3. `equals` phải có tính phản xạ, đối xứng, bắc cầu, nhất quán, và `x.equals(null)` trả về `false`.

**Nếu override `equals` mà quên `hashCode`:**

```java
class User {
    String email;
    @Override public boolean equals(Object o) {
        return o instanceof User u && email.equals(u.email);
    }
    // quên hashCode → dùng hashCode mặc định của Object (khác nhau với mỗi object)
}

Set<User> set = new HashSet<>();
set.add(new User("a@x.com"));
set.contains(new User("a@x.com")); // false! hash khác → tìm sai bucket
```

Hai object "bằng nhau" nhưng nằm ở hai bucket khác nhau, nên `HashSet` không lọc được trùng và `HashMap.get` trả về `null`.

**Bẫy thứ hai: key bị thay đổi sau khi đưa vào map.** Nếu sửa field dùng trong `hashCode` sau khi `put`, entry vẫn nằm ở bucket cũ, nên không bao giờ tìm lại được. Vì vậy key nên immutable, ví dụ `String`, `Integer` hoặc `record`.

**Cách viết đúng trong thực tế:**
- Dùng **`record`** (Java 16+): tự sinh `equals`, `hashCode`, `toString` theo mọi field, và bất biến.
- Hoặc dùng `Objects.equals(...)` và `Objects.hash(field1, field2)`, hay để IDE hoặc Lombok `@EqualsAndHashCode` sinh ra.
- **Với JPA entity:** không dùng id tự sinh trong `hashCode`, vì id là `null` trước khi persist rồi mới có giá trị, làm hash thay đổi. Hãy dùng business key, hoặc trả về một hằng số cho `hashCode`.

### English

"If two objects are equal, they must have the same hash code; the reverse isn't required. If I override `equals` without `hashCode`, two equal objects get different default hash codes, land in different buckets, and a `HashSet` keeps duplicates while `HashMap.get` returns null for an equal key.

The second trap is mutating a key after insertion: the entry stays in the old bucket and becomes unreachable, so keys should be immutable.

In practice I use records, which generate both methods consistently, or `Objects.equals` and `Objects.hash`. For JPA entities I avoid the generated ID in `hashCode`, because it's null before persist and changes afterwards; I use a business key instead."

@@@ java-core-4 | Vì sao String là immutable? / Why is String immutable? | java | | override
### Tiếng Việt

String bất biến: mọi phương thức "sửa" như `concat`, `replace`, `toUpperCase` đều tạo object mới, object cũ giữ nguyên. Có 4 lý do chính:

1. **String pool:** nhiều biến cùng trỏ tới một literal `"hello"`. Nếu String sửa được, đổi qua một biến sẽ làm hỏng tất cả biến còn lại. Bất biến giúp chia sẻ an toàn và tiết kiệm bộ nhớ.
2. **Bảo mật:** String được dùng làm tên class khi class loading, đường dẫn file, URL, connection string. Nếu bị sửa sau khi đã kiểm tra quyền, kẻ tấn công có thể đổi `/safe/file` thành `/etc/passwd` giữa lúc kiểm tra và lúc dùng.
3. **Thread-safe miễn phí:** chia sẻ giữa các thread không cần đồng bộ.
4. **Cache được `hashCode`:** hash tính một lần rồi lưu trong field `hash`, nên String là key rất nhanh trong HashMap. Nếu String sửa được, hash sẽ sai.

**Hệ quả về hiệu năng:**

```java
// Chậm: mỗi vòng tạo String mới, O(n²) ký tự được copy
String s = "";
for (int i = 0; i < 10_000; i++) s += i;

// Nhanh: một buffer sửa được
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10_000; i++) sb.append(i);
String result = sb.toString();
```

- `StringBuilder`: sửa được, không đồng bộ, **dùng mặc định**.
- `StringBuffer`: sửa được, có `synchronized`, hiếm khi cần.
- Nối chuỗi đơn giản trên một dòng (`a + b + c`) thì compiler tự tối ưu, không cần StringBuilder.

**Câu hỏi phụ:** *"Vì sao mật khẩu nên lưu trong `char[]` thay vì `String`?"* Vì String bất biến, không xóa được khỏi bộ nhớ và có thể nằm trong pool tới khi GC dọn. `char[]` thì ghi đè bằng 0 ngay sau khi dùng được.

### English

"Four reasons. First, the string pool: many references share one literal, which is only safe if it can't change. Second, security: strings hold class names, file paths and connection details, and immutability means a value can't be changed after it's been validated. Third, thread safety for free. Fourth, the hash code is computed once and cached, which makes strings fast map keys.

The cost is that every modification creates a new object, so building a string in a loop with `+=` is O(n²); I use `StringBuilder` there. `StringBuffer` is the synchronized version and rarely needed.

A related point: passwords are better kept in a `char[]`, which can be wiped after use, because a String can't be cleared and stays in memory until it's collected."

@@@ java-core-5 | ArrayList và LinkedList khác nhau thế nào? StringBuilder và StringBuffer? / ArrayList vs LinkedList? StringBuilder vs StringBuffer? | java | | override
### Tiếng Việt

| Thao tác | ArrayList (mảng động) | LinkedList (danh sách liên kết đôi) |
|---|---|---|
| `get(i)` | **O(1)** | O(n), phải duyệt |
| `add(e)` vào cuối | O(1) trung bình (thỉnh thoảng phải mở rộng mảng) | O(1) |
| Chèn hoặc xóa ở giữa | O(n), phải dời phần tử | O(1) **nếu đã có node**, nhưng tìm tới node mất O(n) |
| Bộ nhớ | Gọn, các phần tử liền nhau | Mỗi phần tử tốn thêm 2 con trỏ (prev, next) và header của node |
| Cache CPU | **Rất tốt** | Kém, node nằm rải rác trong heap |

**Kết luận thực tế:** gần như **luôn dùng ArrayList**. Thế mạnh "chèn O(1)" của LinkedList chỉ có khi đã cầm sẵn iterator ở đúng vị trí. Trong đa số trường hợp, chi phí tìm vị trí và việc cache CPU kém làm LinkedList chậm hơn, kể cả với thao tác chèn.
- Cần queue hoặc stack: dùng **`ArrayDeque`**, nhanh hơn cả LinkedList lẫn class `Stack` cũ.
- ArrayList khi mở rộng tăng khoảng 1,5 lần (`old + old >> 1`). Biết trước kích thước thì dùng `new ArrayList<>(n)`.

**StringBuilder và StringBuffer:** cả hai đều là chuỗi sửa được. `StringBuffer` có `synchronized` trên mọi phương thức nên chậm hơn. Mặc định dùng `StringBuilder`, vì thường chỉ một thread dựng chuỗi.

### English

"`ArrayList` is a resizable array: O(1) random access and amortized O(1) append, but O(n) insert in the middle because elements shift. It grows by about 1.5 times.

`LinkedList` is a doubly linked list: O(1) insert or remove once you hold the node, but O(n) to reach it, extra memory for two pointers per element, and poor CPU cache locality. In practice `ArrayList` is faster for almost everything, even many middle inserts. For queues and stacks I use `ArrayDeque`.

`StringBuffer` is synchronized and `StringBuilder` isn't; I default to `StringBuilder` since a string is usually built by one thread."

@@@ java-core-6 | Checked và unchecked exception khác nhau thế nào? Bạn thiết kế xử lý lỗi trong service ra sao? / Checked vs unchecked exceptions, and how do you design error handling in a service? | java | | override
### Tiếng Việt

**Cây kế thừa:**

```
Throwable
├── Error                      ← lỗi JVM, không nên bắt: OutOfMemoryError, StackOverflowError
└── Exception
    ├── IOException, SQLException...   ← checked
    └── RuntimeException               ← unchecked
        ├── NullPointerException
        ├── IllegalArgumentException
        └── ...
```

- **Checked:** compiler bắt buộc phải `catch` hoặc khai báo `throws`. Dùng cho lỗi có thể **lường trước và phục hồi được**, ví dụ file không tồn tại hay mạng lỗi.
- **Unchecked** (`RuntimeException`): không bắt buộc xử lý. Thường do **lỗi lập trình** (null, sai tham số) hoặc lỗi nghiệp vụ mà tầng gọi không xử lý gì khác được.
- Có thể tự tạo checked exception bằng cách `extends Exception`, hoặc unchecked bằng `extends RuntimeException`.

**Cách thiết kế trong một Spring service:**

1. Tạo exception nghiệp vụ **unchecked**, mang mã lỗi: `OrderNotFoundException extends BusinessException`, trong đó `BusinessException` chứa `errorCode`.
2. Xử lý tập trung một chỗ bằng `@RestControllerAdvice`:

```java
@RestControllerAdvice
class GlobalHandler {
    @ExceptionHandler(OrderNotFoundException.class)
    ResponseEntity<ErrorResponse> notFound(OrderNotFoundException e) {
        return ResponseEntity.status(404).body(new ErrorResponse("ORDER_NOT_FOUND", e.getMessage()));
    }
    @ExceptionHandler(Exception.class)
    ResponseEntity<ErrorResponse> unexpected(Exception e) {
        log.error("Unexpected error", e);           // log một lần, kèm stack trace
        return ResponseEntity.status(500).body(new ErrorResponse("INTERNAL_ERROR", "Something went wrong"));
    }
}
```

3. **Không** nuốt exception (`catch (Exception e) {}`), **không** log rồi lại ném lên (bị log trùng), **không** dùng exception cho luồng logic bình thường.
4. Khi bọc exception, giữ nguyên nguyên nhân gốc: `throw new PaymentException("...", e)`.
5. Không trả stack trace hay chi tiết SQL ra cho client.

**Vì sao Spring và nhiều framework hiện đại ưa unchecked:** checked exception làm chữ ký phương thức bị "lây" `throws` qua nhiều tầng, và không dùng được trong lambda hay stream.

### English

"`Throwable` splits into `Error`, which signals JVM problems such as `OutOfMemoryError` and shouldn't be caught, and `Exception`. Checked exceptions must be caught or declared; they're for recoverable, expected conditions like I/O failures. Unchecked ones extend `RuntimeException` and usually mean programming errors or business failures the caller can't recover from.

In a Spring service I use unchecked domain exceptions that carry an error code, and handle them in one place with `@RestControllerAdvice`, mapping each to an HTTP status and a consistent error body. Unknown exceptions become a 500 and are logged once, with the stack trace. I never swallow exceptions, never log and rethrow, which logs duplicates, and always keep the cause when wrapping. Unchecked exceptions also work better with lambdas and streams, which is one reason modern frameworks prefer them."

@@@ jc-collection-map | Vì sao Map không kế thừa Collection? HashMap và TreeMap khác nhau thế nào? / Why doesn't Map extend Collection? HashMap vs TreeMap? | java | | override
### Tiếng Việt

**Vì sao Map không kế thừa Collection:** `Collection` mô tả một nhóm **phần tử đơn** với `add(E e)`. `Map` lưu **cặp key-value**, nên `add(E)` không có nghĩa: thêm cái gì, key hay value hay cặp? Thay vào đó Map cung cấp 3 **view** dạng collection:
- `keySet()` trả về `Set<K>`
- `values()` trả về `Collection<V>`
- `entrySet()` trả về `Set<Map.Entry<K,V>>`

**Sơ đồ collections framework:**

```
Collection
├── List   → ArrayList, LinkedList        (có thứ tự, cho trùng)
├── Set    → HashSet, LinkedHashSet, TreeSet (không trùng)
└── Queue  → ArrayDeque, PriorityQueue
Map (riêng) → HashMap, LinkedHashMap, TreeMap, ConcurrentHashMap
```

**HashMap và TreeMap:**

| | HashMap | TreeMap |
|---|---|---|
| Cấu trúc | Mảng bucket + hash | Cây đỏ-đen |
| Thứ tự duyệt | Không đảm bảo | **Tăng dần theo key** |
| `get`, `put`, `remove` | O(1) trung bình | **O(log n)** |
| Key `null` | Cho phép 1 | **Không**: ném `NullPointerException` vì phải so sánh key |
| Yêu cầu với key | `equals` + `hashCode` | `Comparable` hoặc truyền `Comparator` |
| API thêm | — | `firstKey`, `lastKey`, `floorKey`, `ceilingKey`, `headMap`, `subMap` |

**Khi nào dùng TreeMap:** cần duyệt theo thứ tự hoặc truy vấn khoảng. Ví dụ: tìm mức giá gần nhất nhỏ hơn hoặc bằng X bằng `floorKey(x)`, hay lấy các sự kiện trong một khoảng thời gian bằng `subMap(from, to)`.

**LinkedHashMap:** giữ thứ tự chèn, hoặc thứ tự truy cập nếu tạo với `accessOrder = true`. Đây là cách dựng LRU cache nhanh nhất:

```java
class LRU<K, V> extends LinkedHashMap<K, V> {
    private final int cap;
    LRU(int cap) { super(16, 0.75f, true); this.cap = cap; }
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> e) { return size() > cap; }
}
```

### English

"`Collection` models a group of single elements with `add(E)`; a map holds key-value pairs, so that method has no natural meaning. Instead `Map` exposes collection views: `keySet`, `values` and `entrySet`.

`HashMap` is a hash table: O(1) average operations, no ordering, one null key allowed. `TreeMap` is a red-black tree: O(log n) operations, keys kept sorted, and it supports range queries like `floorKey`, `ceilingKey` and `subMap`. It rejects null keys with natural ordering, because it has to compare them.

I use `TreeMap` when I need sorted iteration or range lookups, for example the nearest price below X. `LinkedHashMap` keeps insertion or access order, and with `removeEldestEntry` it becomes a simple LRU cache."

@@@ jc-string-pool | String constant pool là gì? String được lưu ở đâu? / What is the String constant pool, and where do strings live? | java | | override
### Tiếng Việt

**String pool** là vùng nhớ đặc biệt chứa các String literal, để tái sử dụng thay vì tạo nhiều bản giống nhau. **Từ Java 7, pool nằm trong heap** (trước đó ở PermGen), nên được GC dọn như object thường.

```java
String a = "hi";               // literal → lấy từ pool (tạo nếu chưa có)
String b = "hi";               // trỏ CÙNG object với a
String c = new String("hi");   // luôn tạo object MỚI trên heap
String d = c.intern();         // trả về bản trong pool

a == b      // true  (cùng object)
a == c      // false (khác object)
a.equals(c) // true  (cùng nội dung)
a == d      // true
```

**Câu hỏi bẫy:** *"`new String("hi")` tạo ra mấy object?"* Tối đa **2**: một literal `"hi"` trong pool (nếu chưa có) và một object mới trên heap.

**Nối chuỗi:**

```java
String x = "a" + "b";      // hằng số lúc compile → gộp thành "ab", nằm trong pool
String y = "ab";
x == y                      // true

String part = "a";
String z = part + "b";     // nối lúc chạy → object mới
z == y                      // false
```

**Bài học:**
- **Luôn so sánh String bằng `equals`**, không dùng `==`.
- `intern()` có thể tiết kiệm bộ nhớ khi có rất nhiều chuỗi trùng (ví dụ mã quốc gia đọc từ file), nhưng ít khi cần. JVM hiện đại còn có `-XX:+UseStringDeduplication` với G1.
- Pool chia sẻ an toàn được là **nhờ String immutable**.

### English

"String literals are interned in the string pool, which has lived in the heap since Java 7, not in PermGen. Two identical literals refer to the same object, so `==` is true for them, while `new String("hi")` always creates a new heap object: `==` is false but `equals` is true. `new String("hi")` can create up to two objects, the pooled literal and the new one. `intern()` returns the pooled instance.

Compile-time constants like `"a" + "b"` are folded into one pooled literal, but concatenation at runtime creates new objects. The practical rule is to always compare strings with `equals`. Sharing pooled strings is only safe because `String` is immutable."

@@@ jc-abstraction-encapsulation | Abstraction và encapsulation khác nhau thế nào? Có encapsulation mà không có abstraction được không? / Abstraction vs encapsulation: can you have encapsulation without abstraction? | java | | override
### Tiếng Việt

| | Abstraction (trừu tượng hóa) | Encapsulation (đóng gói) |
|---|---|---|
| Trả lời câu hỏi | Object **làm được gì**? | Dữ liệu được **bảo vệ** thế nào? |
| Mục đích | Ẩn **chi tiết cài đặt**, chỉ lộ ra hợp đồng | Ẩn **trạng thái**, chỉ cho sửa qua phương thức hợp lệ |
| Công cụ | `interface`, `abstract class` | `private` field, getter/setter có kiểm tra, immutable |
| Ví dụ | `PaymentGateway.charge()`, không cần biết bên dưới là VNPay hay Stripe | `BankAccount` có `private balance`, chỉ đổi qua `withdraw()` có kiểm tra số dư |

```java
// Abstraction: người gọi chỉ biết hợp đồng
interface PaymentGateway { Receipt charge(Money amount); }

// Encapsulation: bảo vệ bất biến "số dư không âm"
class BankAccount {
    private long balance;                       // không ai sửa trực tiếp được
    void withdraw(long amount) {
        if (amount > balance) throw new InsufficientFundsException();
        balance -= amount;
    }
    long balance() { return balance; }
}
```

**Có encapsulation mà không có abstraction không?** **Có.** Một class chỉ có field `private` cùng getter và setter "trần" là có đóng gói (về hình thức), nhưng không trừu tượng hóa gì cả: người gọi vẫn phải biết và phụ thuộc vào từng field. Loại class này thường gọi là "anemic model".

**Ngược lại**, có abstraction mà encapsulation kém cũng được: một interface đẹp nhưng bên trong để field `public`.

**Thiết kế tốt dùng cả hai:** interface nhỏ, rõ ràng (abstraction), còn trạng thái bên trong chỉ class đó được sửa và luôn giữ hợp lệ (encapsulation).

### English

"Abstraction is about what an object exposes: it hides implementation details behind a contract, such as a `PaymentGateway.charge()` interface that hides which provider is used. Encapsulation is about protecting state: fields are private and changed only through methods that keep invariants valid, such as a `withdraw` method that refuses to make a balance negative.

Yes, you can have encapsulation without abstraction. A class with private fields and plain getters and setters is technically encapsulated but abstracts nothing: callers still depend on every field. Good design combines both: a small, meaningful interface and state that only the class itself can change consistently."

@@@ jc-interface-private | Interface có private method được không? Để làm gì? / Can an interface have private methods? Why would it? | java | | override
### Tiếng Việt

**Có, từ Java 9.** Tóm tắt interface qua các phiên bản:

| Java | Interface có thể chứa |
|---|---|
| ≤ 7 | Chỉ method abstract và hằng `public static final` |
| 8 | Thêm **`default`** method (có thân hàm) và **`static`** method |
| 9 | Thêm **`private`** và **`private static`** method |

**Vì sao cần:** từ Java 8, interface có code thật trong `default` method. Khi nhiều default method dùng chung một đoạn logic, private method giúp **tái sử dụng mà không lộ ra ngoài**, vì nó không thuộc hợp đồng public.

```java
interface ReportExporter {
    default String toCsv(List<Row> rows)  { return header() + join(rows, ","); }
    default String toTsv(List<Row> rows)  { return header() + join(rows, "\t"); }

    private String join(List<Row> rows, String sep) {      // helper dùng chung, không public
        return rows.stream().map(r -> r.format(sep)).collect(Collectors.joining("\n"));
    }
    private static String header() { return "id,name,amount\n"; }
}
```

**Giới hạn vẫn còn:**
- Interface **không có trạng thái instance**: field luôn là `public static final`.
- Private method **không được** đánh dấu `default` hay `abstract`.
- Một class implement hai interface có default method trùng chữ ký thì **phải override** để chọn, ví dụ gọi `A.super.method()`.

**Khi nào nên dùng abstract class thay vì interface:** khi cần lưu trạng thái chung, cần constructor, hoặc cần method `protected`.

### English

"Yes, since Java 9. Java 8 added default and static methods, so interfaces started carrying real code; Java 9 added private and private static methods so those default methods can share helper logic without exposing it as part of the public contract.

Interfaces still can't hold instance state: fields are always public static final. If a class implements two interfaces with the same default method, it must override it and can pick one with `InterfaceName.super.method()`. When I need shared state, a constructor or protected methods, an abstract class is the better fit."

@@@ jc-ocp-violation | Có khi nào được phép vi phạm nguyên tắc Open/Closed không? / Is it ever acceptable to violate the Open/Closed Principle? | java | | override
### Tiếng Việt

**Nhắc lại OCP:** code nên **mở để mở rộng, đóng để sửa đổi**. Thêm tính năng mới bằng cách thêm class mới, không phải sửa code đang chạy ổn.

```java
// Vi phạm OCP: thêm phương thức thanh toán mới thì phải sửa switch
long fee(PaymentType t, long amount) {
    return switch (t) {
        case CARD -> amount * 2 / 100;
        case WALLET -> 1_000;
    };
}

// Theo OCP: thêm loại mới = thêm class implement interface
interface FeePolicy { long fee(long amount); }
class CardFee implements FeePolicy { public long fee(long a) { return a * 2 / 100; } }
class WalletFee implements FeePolicy { public long fee(long a) { return 1_000; } }
```

**Có, đôi khi vi phạm là lựa chọn đúng:**
- **Dự án nhỏ, prototype, sửa gấp:** thêm một nhánh `case` đơn giản và dễ đọc hơn việc tạo interface với một implementation duy nhất. Đây là nguyên tắc **YAGNI** (You Aren't Gonna Need It).
- **Biến thể chưa chắc sẽ xuất hiện:** trừu tượng hóa quá sớm tạo ra "abstraction sai", còn tốn kém hơn sửa code.
- **Quy tắc ba lần (rule of three):** lần thứ ba phải sửa cùng một `switch` để thêm biến thể mới thì mới tách interface.

**Nên tuân thủ OCP khi:** biến thể thật sự lặp lại và có xu hướng tăng, ví dụ phương thức thanh toán, quy tắc tính phí, kênh gửi thông báo, plugin.

**Lựa chọn trung gian với Java 21:** `sealed interface` kết hợp `switch` đầy đủ các trường hợp. Việc sửa vẫn phải làm, nhưng **compiler báo lỗi** ở mọi chỗ cần cập nhật khi thêm loại mới, nên không bỏ sót.

**Ví dụ thực tế để kể:** *"Ở DXC, [tính phí bảo hiểm theo loại sản phẩm]: ban đầu là một `switch`, đến khi có sản phẩm thứ ba thì tôi tách thành strategy..."* (thay bằng chuyện thật của bạn).

### English

"Yes, when the cost of the abstraction outweighs the benefit. In a small codebase, a prototype or an urgent fix, adding a case to an existing switch is simpler and clearer than creating an interface with a single implementation; that's YAGNI. Abstracting too early often produces the wrong abstraction, which is more expensive than editing code.

I apply OCP where variation is real and recurring, such as payment methods, fee rules or notification channels. A practical trigger is the rule of three: the third time I edit the same switch for a new variant, I extract an interface. With Java 21, a sealed interface plus an exhaustive switch is a middle ground: changes are still edits, but the compiler shows every place that must be updated."

@@@ jc-finally | Khối finally có thể làm mất exception từ try không? / Can a finally block override an exception thrown in try? | java | | override
### Tiếng Việt

**Có.** Nếu trong `finally` có `return` hoặc ném exception mới, exception gốc từ `try` **bị mất hoàn toàn**, không có log hay dấu vết gì.

```java
static int test() {
    try {
        throw new IllegalStateException("lỗi thật");
    } finally {
        return 1;          // exception "lỗi thật" biến mất, hàm trả về 1
    }
}
```

Vì vậy **không bao giờ `return` trong `finally`**. Hầu hết linter và IDE đều cảnh báo việc này.

**Các chi tiết hay bị hỏi tiếp:**

1. **`finally` vẫn chạy khi `try` có `return`**. Nhưng giá trị trả về đã được tính trước khi `finally` chạy:

```java
static int value() {
    int x = 1;
    try { return x; }          // giá trị 1 đã được "chốt"
    finally { x = 99; }        // không ảnh hưởng → hàm trả về 1
}
```

Lưu ý: nếu trả về một **object** và `finally` sửa nội dung object đó (ví dụ `list.add(...)`), người gọi sẽ thấy thay đổi, vì chỉ tham chiếu được chốt.

2. **`finally` không chạy** khi gọi `System.exit()`, JVM bị kill hoặc crash, hoặc thread bị treo vô hạn trong `try`.

3. **Cách đúng để đóng tài nguyên: try-with-resources (Java 7+)**

```java
try (Connection c = ds.getConnection();
     PreparedStatement ps = c.prepareStatement(sql)) {
    ...
}   // tự đóng theo thứ tự ngược lại
```

Nếu cả thân `try` lẫn `close()` cùng ném lỗi, exception của `close()` được giữ lại dưới dạng **suppressed** (lấy bằng `e.getSuppressed()`), còn exception gốc không bị mất. Đây là ưu điểm lớn so với tự viết `finally { c.close(); }`.

### English

"Yes. If the finally block returns or throws a new exception, the original exception from try is silently discarded, which is why a return inside finally is considered a bug and linters flag it.

Related details: finally runs even when try returns, but the return value is already evaluated, so reassigning a local variable in finally doesn't change what's returned, although mutating a returned object does show. Finally doesn't run on `System.exit` or if the JVM crashes.

For resources I use try-with-resources: resources are closed automatically in reverse order, and if `close()` also throws, that exception is attached to the original as a suppressed exception instead of replacing it."

@@@ jc-generics | Generics: type erasure là gì? Wildcard ? extends và ? super dùng khi nào? / Generics: what is type erasure, and when do you use ? extends vs ? super? | java | java-core,generics | qa | Java core
### Tiếng Việt

**Generics** cho phép kiểm tra kiểu lúc compile: `List<String>` không cho thêm `Integer`, và không cần ép kiểu khi lấy ra.

**Type erasure (xóa kiểu):** thông tin kiểu generic **chỉ tồn tại lúc compile**. Sau khi compile, `List<String>` và `List<Integer>` đều chỉ là `List`, và `T` bị thay bằng `Object` (hoặc bằng cận trên, ví dụ `T extends Number` thành `Number`). Java làm vậy để **tương thích ngược** với code viết trước Java 5.

**Hệ quả của erasure (hay bị hỏi):**

```java
new T();                          // ✗ không biết T là gì lúc chạy
new T[10];                        // ✗
obj instanceof List<String>       // ✗ chỉ viết được: obj instanceof List<?>
List<String>.class                // ✗
// Hai method chỉ khác kiểu generic → trùng chữ ký sau erasure:
void f(List<String> a) {}
void f(List<Integer> a) {}        // ✗ lỗi "same erasure"
```

Cách vượt qua khi cần kiểu lúc chạy: truyền `Class<T>` vào, ví dụ `objectMapper.readValue(json, User.class)`, hoặc `TypeReference<List<User>>` của Jackson.

**Generics là bất biến (invariant):** `List<Integer>` **không phải** là con của `List<Number>`, dù `Integer` là con của `Number`. Nếu được phép, có thể thêm `Double` vào một list chỉ được chứa `Integer`.

**Wildcard và quy tắc PECS (Producer Extends, Consumer Super):**

| | `? extends T` | `? super T` |
|---|---|---|
| Ý nghĩa | T hoặc lớp con của T | T hoặc lớp cha của T |
| Đọc ra | Được, nhận kiểu `T` | Chỉ nhận kiểu `Object` |
| Ghi vào | **Không** (trừ `null`) | **Được**, ghi `T` |
| Dùng khi | Collection là **nguồn dữ liệu** (producer) | Collection là **nơi nhận** (consumer) |

```java
// Producer: chỉ đọc số ra để cộng → extends
double sum(List<? extends Number> nums) {
    double s = 0;
    for (Number n : nums) s += n.doubleValue();
    return s;
}
sum(List.of(1, 2, 3));        // List<Integer> dùng được
sum(List.of(1.5, 2.5));       // List<Double> dùng được

// Consumer: chỉ ghi Integer vào → super
void fill(List<? super Integer> out) {
    for (int i = 0; i < 3; i++) out.add(i);
}
fill(new ArrayList<Number>()); // dùng được
fill(new ArrayList<Object>()); // dùng được
```

Ví dụ trong JDK: `Collections.copy(List<? super T> dest, List<? extends T> src)`. Nguồn dùng `extends`, đích dùng `super`.

### English

"Generics give compile-time type safety. They're implemented with type erasure: generic type information exists only at compile time, and at runtime `List<String>` is just `List`, with `T` replaced by `Object` or its bound. That was done for backward compatibility. Consequences: you can't write `new T()`, create a generic array, check `instanceof List<String>`, or overload methods that differ only in type parameters. When I need the type at runtime, I pass a `Class<T>` or a type token.

Generics are invariant: `List<Integer>` isn't a `List<Number>`, otherwise you could add a Double to a list of Integers. Wildcards add flexibility, following PECS, producer extends, consumer super. If a collection produces values that I read, I use `? extends T`; if it consumes values that I write, I use `? super T`. `Collections.copy` is the classic example: the source is `? extends T` and the destination is `? super T`."
