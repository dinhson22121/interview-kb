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

**Structure:** a HashMap is an array of "buckets" (`Node<K,V>[] table`). Each bucket holds a linked list, or a red-black tree when the bucket gets crowded.

**On `put(key, value)`:**

1. Compute `hash = key.hashCode() ^ (h >>> 16)`: XOR the high 16 bits into the low 16 bits, so keys that differ only in their high bits still land in different buckets.
2. Compute the bucket index: `index = (n - 1) & hash`, where `n` is the table size, always a power of two. This `&` is equivalent to `% n` but faster.
3. If the bucket is empty: create a new node.
4. If the bucket already has entries: walk it, comparing `hash` first and only then calling `equals`. An equal key overwrites the value; otherwise a node is appended at the end.
5. **Treeify:** when one bucket reaches **8 nodes** and the table has **at least 64 buckets**, the list becomes a red-black tree, so the worst case is O(log n) instead of O(n). If the table is smaller than 64, HashMap resizes instead of treeifying. When a bucket shrinks to 6 nodes, the tree turns back into a list.
6. **Resize:** when `size > capacity × loadFactor` (by default 16 × 0.75 = 12), the table doubles. Because sizes are powers of two, each node either stays at its old index or moves by exactly `oldCapacity`, so hashes don't need to be recomputed.

**`get(key)`:** compute the hash, find the bucket, compare `hash` and then `equals`. O(1) on average.

**Points interviewers often follow up on:**
- It allows **one `null` key** (always stored in bucket 0) and any number of `null` values.
- **Not thread-safe:** concurrent writes can lose data. In Java 7, concurrent resizing could even create an infinite loop.
- Keys should be **immutable**: if you change a field used in `hashCode` after `put`, that entry can never be found again.
- If you know the expected number of entries, pre-size the map to avoid repeated resizing: `new HashMap<>(expected / 0.75f + 1)`, or `HashMap.newHashMap(expected)` since Java 19.

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

| | HashMap | Collections.synchronizedMap | ConcurrentHashMap |
|---|---|---|---|
| Thread-safe | No | Yes | Yes |
| Locking | None | One lock for the **whole map** | CAS plus a lock **per bucket** |
| Reads | No lock | Locked | **Lock-free** (reads `volatile` fields) |
| `null` key/value | Allowed | Allowed | **Not allowed** |
| Iterator | Fail-fast (`ConcurrentModificationException`) | Fail-fast; you must `synchronized` on the map while iterating | **Weakly consistent**, never throws |

**How ConcurrentHashMap works since Java 8:**
- Empty bucket: insert with **CAS** (compare-and-swap), no lock needed.
- Non-empty bucket: `synchronized` on **the first node of that bucket only**. Two threads writing to different buckets don't block each other.
- Reads take no lock at all.
- Resizing is helped along by several threads moving entries in parallel.
- (Java 7 used "segments", 16 independently locked segments by default. Java 8 dropped that design.)

**Why nulls aren't allowed:** in a concurrent map, `get(key) == null` couldn't distinguish "key absent" from "value is null", because another thread can change the map between a `containsKey` call and a `get` call.

**The common bug: compound operations aren't atomic.**

```java
// WRONG: two threads can both see "absent" and both put
if (!map.containsKey(k)) map.put(k, 1);
// WRONG: read then write, updates get lost
map.put(k, map.get(k) + 1);

// RIGHT: atomic
map.putIfAbsent(k, 1);
map.merge(k, 1, Integer::sum);
map.computeIfAbsent(k, x -> new ArrayList<>()).add(v);
```

**When to use which:** almost always ConcurrentHashMap when a map is shared between threads, for example an in-memory cache. `synchronizedMap` only makes sense for quickly wrapping an existing map under low load.

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

**The contract:**
1. If two objects are `equals`, their `hashCode` **must** be equal.
2. Equal hash codes **don't** imply `equals` (that's a collision, which is acceptable).
3. `equals` must be reflexive, symmetric, transitive and consistent, and `x.equals(null)` must return `false`.

**If you override `equals` but forget `hashCode`:**

```java
class User {
    String email;
    @Override public boolean equals(Object o) {
        return o instanceof User u && email.equals(u.email);
    }
    // forgot hashCode → Object's default hashCode (different for every object)
}

Set<User> set = new HashSet<>();
set.add(new User("a@x.com"));
set.contains(new User("a@x.com")); // false! different hash → wrong bucket
```

Two "equal" objects end up in two different buckets, so a `HashSet` fails to remove duplicates and `HashMap.get` returns `null`.

**The second trap: mutating a key after it's in the map.** If you change a field used in `hashCode` after `put`, the entry stays in the old bucket and can never be found again. That's why keys should be immutable, such as `String`, `Integer` or a `record`.

**How to write it correctly in practice:**
- Use a **`record`** (Java 16+): it generates `equals`, `hashCode` and `toString` from all fields, and it's immutable.
- Or use `Objects.equals(...)` and `Objects.hash(field1, field2)`, or let the IDE or Lombok `@EqualsAndHashCode` generate them.
- **For JPA entities:** don't use the generated ID in `hashCode`, because the ID is `null` before persist and only gets a value afterwards, which changes the hash. Use a business key, or return a constant from `hashCode`.

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

String is immutable: every "modifying" method such as `concat`, `replace` or `toUpperCase` returns a new object and leaves the original unchanged. There are four main reasons:

1. **The string pool:** many variables can point to the same literal `"hello"`. If strings were mutable, changing it through one variable would corrupt all the others. Immutability makes sharing safe and saves memory.
2. **Security:** strings are used for class names during class loading, file paths, URLs and connection strings. If they could be changed after a permission check, an attacker could swap `/safe/file` for `/etc/passwd` between the check and the use.
3. **Thread safety for free:** they can be shared between threads without synchronization.
4. **Cached `hashCode`:** the hash is computed once and stored in the `hash` field, which makes String a very fast HashMap key. If strings were mutable, that cached hash would become wrong.

**Performance consequence:**

```java
// Slow: every iteration creates a new String, O(n²) characters copied
String s = "";
for (int i = 0; i < 10_000; i++) s += i;

// Fast: one mutable buffer
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10_000; i++) sb.append(i);
String result = sb.toString();
```

- `StringBuilder`: mutable, not synchronized, **the default choice**.
- `StringBuffer`: mutable, `synchronized`, rarely needed.
- Simple concatenation on one line (`a + b + c`) is optimized by the compiler, so it doesn't need a StringBuilder.

**Follow-up question:** *"Why should passwords be kept in a `char[]` rather than a `String`?"* Because a String is immutable, it can't be wiped from memory and may stay there until the GC collects it. A `char[]` can be overwritten with zeros right after use.

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

| Operation | ArrayList (dynamic array) | LinkedList (doubly linked list) |
|---|---|---|
| `get(i)` | **O(1)** | O(n), must traverse |
| `add(e)` at the end | O(1) amortized (occasionally grows the array) | O(1) |
| Insert or remove in the middle | O(n), elements shift | O(1) **if you already hold the node**, but reaching it is O(n) |
| Memory | Compact, elements are contiguous | Each element costs 2 extra pointers (prev, next) plus a node header |
| CPU cache | **Very good** | Poor, nodes are scattered across the heap |

**Practical conclusion:** almost **always use ArrayList**. LinkedList's "O(1) insert" only helps when you already hold an iterator at the right position. In most cases, the cost of finding the position and the poor cache behavior make LinkedList slower, even for inserts.
- For a queue or stack: use **`ArrayDeque`**, which is faster than both LinkedList and the legacy `Stack` class.
- ArrayList grows by about 1.5 times (`old + old >> 1`). If you know the size, use `new ArrayList<>(n)`.

**StringBuilder vs StringBuffer:** both are mutable character sequences. `StringBuffer` has `synchronized` on every method, so it's slower. Default to `StringBuilder`, since a string is usually built by a single thread.

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

**The hierarchy:**

```
Throwable
├── Error                      ← JVM problems, don't catch: OutOfMemoryError, StackOverflowError
└── Exception
    ├── IOException, SQLException...   ← checked
    └── RuntimeException               ← unchecked
        ├── NullPointerException
        ├── IllegalArgumentException
        └── ...
```

- **Checked:** the compiler forces you to `catch` it or declare `throws`. Used for errors that are **expected and recoverable**, such as a missing file or a network failure.
- **Unchecked** (`RuntimeException`): handling isn't enforced. Usually caused by **programming errors** (null, invalid arguments) or business failures the caller can't do anything else about.
- You create your own checked exception by extending `Exception`, or an unchecked one by extending `RuntimeException`.

**How I design error handling in a Spring service:**

1. Create **unchecked** domain exceptions that carry an error code: `OrderNotFoundException extends BusinessException`, where `BusinessException` holds an `errorCode`.
2. Handle them centrally in one place with `@RestControllerAdvice`:

```java
@RestControllerAdvice
class GlobalHandler {
    @ExceptionHandler(OrderNotFoundException.class)
    ResponseEntity<ErrorResponse> notFound(OrderNotFoundException e) {
        return ResponseEntity.status(404).body(new ErrorResponse("ORDER_NOT_FOUND", e.getMessage()));
    }
    @ExceptionHandler(Exception.class)
    ResponseEntity<ErrorResponse> unexpected(Exception e) {
        log.error("Unexpected error", e);           // log once, with the stack trace
        return ResponseEntity.status(500).body(new ErrorResponse("INTERNAL_ERROR", "Something went wrong"));
    }
}
```

3. **Don't** swallow exceptions (`catch (Exception e) {}`), **don't** log and then rethrow (it gets logged twice), and **don't** use exceptions for normal control flow.
4. When wrapping an exception, keep the root cause: `throw new PaymentException("...", e)`.
5. Never return stack traces or SQL details to the client.

**Why Spring and many modern frameworks prefer unchecked exceptions:** checked exceptions spread `throws` clauses through every layer of method signatures, and they don't work inside lambdas and streams.

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

**Why Map doesn't extend Collection:** `Collection` describes a group of **single elements** with `add(E e)`. A `Map` stores **key-value pairs**, so `add(E)` has no meaning: add what, the key, the value or the pair? Instead, Map provides three **collection views**:
- `keySet()` returns a `Set<K>`
- `values()` returns a `Collection<V>`
- `entrySet()` returns a `Set<Map.Entry<K,V>>`

**The collections framework at a glance:**

```
Collection
├── List   → ArrayList, LinkedList        (ordered, duplicates allowed)
├── Set    → HashSet, LinkedHashSet, TreeSet (no duplicates)
└── Queue  → ArrayDeque, PriorityQueue
Map (separate) → HashMap, LinkedHashMap, TreeMap, ConcurrentHashMap
```

**HashMap vs TreeMap:**

| | HashMap | TreeMap |
|---|---|---|
| Structure | Bucket array + hashing | Red-black tree |
| Iteration order | Not guaranteed | **Ascending by key** |
| `get`, `put`, `remove` | O(1) average | **O(log n)** |
| `null` key | One allowed | **No**: throws `NullPointerException` because keys must be compared |
| Requirement on keys | `equals` + `hashCode` | `Comparable`, or pass a `Comparator` |
| Extra API | — | `firstKey`, `lastKey`, `floorKey`, `ceilingKey`, `headMap`, `subMap` |

**When to use TreeMap:** when you need sorted iteration or range queries. For example: finding the nearest price less than or equal to X with `floorKey(x)`, or getting the events in a time range with `subMap(from, to)`.

**LinkedHashMap:** keeps insertion order, or access order when created with `accessOrder = true`. That's the quickest way to build an LRU cache:

```java
class LRU<K, V> extends LinkedHashMap<K, V> {
    private final int cap;
    LRU(int cap) { super(16, 0.75f, true); this.cap = cap; }
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> e) { return size() > cap; }
}
```

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

The **string pool** is a special memory area that holds String literals so they can be reused instead of creating many identical copies. **Since Java 7 the pool lives in the heap** (before that it was in PermGen), so it's garbage-collected like ordinary objects.

```java
String a = "hi";               // literal → taken from the pool (created if absent)
String b = "hi";               // points to the SAME object as a
String c = new String("hi");   // always creates a NEW object on the heap
String d = c.intern();         // returns the pooled instance

a == b      // true  (same object)
a == c      // false (different objects)
a.equals(c) // true  (same content)
a == d      // true
```

**Trick question:** *"How many objects does `new String("hi")` create?"* Up to **2**: the literal `"hi"` in the pool (if not already there) and one new object on the heap.

**Concatenation:**

```java
String x = "a" + "b";      // compile-time constants → folded into "ab", pooled
String y = "ab";
x == y                      // true

String part = "a";
String z = part + "b";     // concatenated at runtime → new object
z == y                      // false
```

**Takeaways:**
- **Always compare strings with `equals`**, never with `==`.
- `intern()` can save memory when there are huge numbers of duplicate strings (for example country codes read from a file), but it's rarely needed. Modern JVMs also offer `-XX:+UseStringDeduplication` with G1.
- The pool can be shared safely **only because String is immutable**.

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

| | Abstraction | Encapsulation |
|---|---|---|
| Answers the question | **What can** the object do? | How is the data **protected**? |
| Purpose | Hide **implementation details**, expose only a contract | Hide **state**, allow changes only through valid methods |
| Tools | `interface`, `abstract class` | `private` fields, validating getters/setters, immutability |
| Example | `PaymentGateway.charge()`: the caller doesn't need to know whether VNPay or Stripe is behind it | `BankAccount` with a `private balance`, changed only through `withdraw()`, which checks the balance |

```java
// Abstraction: the caller only knows the contract
interface PaymentGateway { Receipt charge(Money amount); }

// Encapsulation: protects the invariant "balance is never negative"
class BankAccount {
    private long balance;                       // nobody can change it directly
    void withdraw(long amount) {
        if (amount > balance) throw new InsufficientFundsException();
        balance -= amount;
    }
    long balance() { return balance; }
}
```

**Can you have encapsulation without abstraction?** **Yes.** A class with only `private` fields and plain getters and setters is encapsulated (in form), but it abstracts nothing: callers still have to know and depend on every field. Such classes are often called an "anemic model".

**The reverse** is also possible: a clean interface whose implementation exposes `public` fields has abstraction but poor encapsulation.

**Good design uses both:** a small, clear interface (abstraction), and internal state that only the class itself can change and always keeps valid (encapsulation).

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

**Yes, since Java 9.** How interfaces evolved:

| Java | An interface can contain |
|---|---|
| ≤ 7 | Only abstract methods and `public static final` constants |
| 8 | Adds **`default`** methods (with a body) and **`static`** methods |
| 9 | Adds **`private`** and **`private static`** methods |

**Why they're needed:** since Java 8, interfaces contain real code in `default` methods. When several default methods share some logic, a private method lets them **reuse it without exposing it**, because it isn't part of the public contract.

```java
interface ReportExporter {
    default String toCsv(List<Row> rows)  { return header() + join(rows, ","); }
    default String toTsv(List<Row> rows)  { return header() + join(rows, "\t"); }

    private String join(List<Row> rows, String sep) {      // shared helper, not public
        return rows.stream().map(r -> r.format(sep)).collect(Collectors.joining("\n"));
    }
    private static String header() { return "id,name,amount\n"; }
}
```

**Limits that still apply:**
- Interfaces have **no instance state**: fields are always `public static final`.
- A private method **can't** be `default` or `abstract`.
- If a class implements two interfaces with default methods of the same signature, it **must override** the method to choose, for example by calling `A.super.method()`.

**When to use an abstract class instead of an interface:** when you need shared state, a constructor, or `protected` methods.

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

**A reminder of OCP:** code should be **open for extension, closed for modification**. A new feature is added by adding a new class, not by editing code that already works.

```java
// Violates OCP: adding a payment method means editing the switch
long fee(PaymentType t, long amount) {
    return switch (t) {
        case CARD -> amount * 2 / 100;
        case WALLET -> 1_000;
    };
}

// Follows OCP: a new type = a new class implementing the interface
interface FeePolicy { long fee(long amount); }
class CardFee implements FeePolicy { public long fee(long a) { return a * 2 / 100; } }
class WalletFee implements FeePolicy { public long fee(long a) { return 1_000; } }
```

**Yes, sometimes violating it is the right call:**
- **Small projects, prototypes, urgent fixes:** adding a simple `case` is easier to read than creating an interface with a single implementation. That's **YAGNI** (You Aren't Gonna Need It).
- **When it's unclear whether more variants will appear:** abstracting too early creates the "wrong abstraction", which costs more than editing code.
- **The rule of three:** only when you edit the same `switch` for the third time to add a variant do you extract an interface.

**Follow OCP when:** variation is real, recurring and likely to grow, for example payment methods, fee rules, notification channels or plugins.

**A middle ground in Java 21:** a `sealed interface` combined with an exhaustive `switch`. You still edit code, but **the compiler reports an error** at every place that must change when you add a new type, so nothing is missed.

**A real example to tell:** *"At DXC, [insurance premium calculation by product type]: it started as a `switch`, and when the third product arrived I extracted a strategy..."* (replace with your own story).

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

**Yes.** If the `finally` block contains a `return` or throws a new exception, the original exception from `try` is **completely lost**, with no log or trace.

```java
static int test() {
    try {
        throw new IllegalStateException("the real error");
    } finally {
        return 1;          // "the real error" disappears, the method returns 1
    }
}
```

That's why you should **never `return` inside `finally`**. Most linters and IDEs warn about it.

**Details interviewers often follow up on:**

1. **`finally` still runs when `try` returns**. But the return value is computed before `finally` runs:

```java
static int value() {
    int x = 1;
    try { return x; }          // the value 1 is already "captured"
    finally { x = 99; }        // no effect → the method returns 1
}
```

Note: if you return an **object** and `finally` changes that object's contents (for example `list.add(...)`), the caller will see the change, because only the reference was captured.

2. **`finally` doesn't run** when `System.exit()` is called, when the JVM is killed or crashes, or when the thread hangs forever inside `try`.

3. **The right way to close resources: try-with-resources (Java 7+)**

```java
try (Connection c = ds.getConnection();
     PreparedStatement ps = c.prepareStatement(sql)) {
    ...
}   // closed automatically, in reverse order
```

If both the `try` body and `close()` throw, the exception from `close()` is kept as a **suppressed** exception (available through `e.getSuppressed()`), and the original exception isn't lost. That's a big advantage over writing `finally { c.close(); }` by hand.

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

**Generics** enable type checking at compile time: a `List<String>` won't accept an `Integer`, and you don't need casts when reading elements.

**Type erasure:** generic type information **exists only at compile time**. After compilation, `List<String>` and `List<Integer>` are both just `List`, and `T` is replaced with `Object` (or with its upper bound, so `T extends Number` becomes `Number`). Java did this for **backward compatibility** with code written before Java 5.

**Consequences of erasure (frequently asked):**

```java
new T();                          // ✗ T is unknown at runtime
new T[10];                        // ✗
obj instanceof List<String>       // ✗ only allowed: obj instanceof List<?>
List<String>.class                // ✗
// Two methods that differ only in generic type → same signature after erasure:
void f(List<String> a) {}
void f(List<Integer> a) {}        // ✗ "same erasure" error
```

Workarounds when you need the type at runtime: pass a `Class<T>`, for example `objectMapper.readValue(json, User.class)`, or use Jackson's `TypeReference<List<User>>`.

**Generics are invariant:** `List<Integer>` is **not** a subtype of `List<Number>`, even though `Integer` is a subtype of `Number`. If it were, you could add a `Double` to a list that may only contain `Integer`s.

**Wildcards and the PECS rule (Producer Extends, Consumer Super):**

| | `? extends T` | `? super T` |
|---|---|---|
| Meaning | T or a subclass of T | T or a superclass of T |
| Reading | Allowed, you get a `T` | You only get an `Object` |
| Writing | **Not allowed** (except `null`) | **Allowed**, you can write a `T` |
| Use when | The collection is a **source of data** (producer) | The collection is a **destination** (consumer) |

```java
// Producer: only read numbers to add them up → extends
double sum(List<? extends Number> nums) {
    double s = 0;
    for (Number n : nums) s += n.doubleValue();
    return s;
}
sum(List.of(1, 2, 3));        // a List<Integer> works
sum(List.of(1.5, 2.5));       // a List<Double> works

// Consumer: only write Integers into it → super
void fill(List<? super Integer> out) {
    for (int i = 0; i < 3; i++) out.add(i);
}
fill(new ArrayList<Number>()); // works
fill(new ArrayList<Object>()); // works
```

A JDK example: `Collections.copy(List<? super T> dest, List<? extends T> src)`. The source uses `extends`, the destination uses `super`.

