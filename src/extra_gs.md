@@@ co-goldman | Goldman Sachs (Java backend) | company | goldman-sachs,finance,product | guide
Bộ câu hỏi tổng hợp từ một bài chia sẻ của ứng viên, mô tả **5 vòng** phỏng vấn Java backend. Ngân hàng đầu tư nên trọng tâm là **Java core sâu**, **concurrency**, **bảo mật**, **tối ưu database** và **tính đúng đắn** (tiền, giao dịch).

*Nguồn là chia sẻ từ cộng đồng, không phải tài liệu chính thức; quy trình thật khác nhau theo team và quốc gia.*

### Vòng 1: Online assessment

- [ ] [Kiểm tra chuỗi ngoặc có `*`](#dsa-valid-paren-star) (LeetCode 678, Medium)
- [ ] [K từ xuất hiện nhiều nhất](#dsa-top-k-words) (LeetCode 692, Medium) · liên quan: [Top K elements](#dsa-top-k)

### Vòng 2: DSA + Java core

- [ ] [Đảo linked list theo từng cặp](#dsa-swap-pairs) (LeetCode 24, Medium)
- [ ] [`==` và `.equals()`](#jc-equals-operator)
- [ ] [HashMap hoạt động bên trong](#java-core-1)
- [ ] [Xử lý va chạm: linked list và cây (Java 8+), vì sao load factor 0.75](#jc-hashmap-collision)
- [ ] [Java Memory Model](#jc-jmm)
- [ ] [Các cách đảm bảo thread safety](#jc-thread-safety) · [synchronized và ReentrantLock](#jc-sync-vs-lock) · [volatile, synchronized, Atomic](#concurrency-14)

### Vòng 3: Spring Boot + Low-level design

- [ ] [LLD rate limiter: tối đa 5 request/user/phút](#lld-rate-limiter) · [Thiết kế rate limiter (phân tán)](#system-design-18)
- [ ] [@Component, @Service, @Repository](#sp-stereotypes)
- [ ] [Bean scope](#sp-scopes) · [Vòng đời bean](#spring-2)
- [ ] [Quá trình khởi động Spring Boot](#sp-boot-startup)
- [ ] [@Transactional hoạt động bên trong và các bẫy](#spring-3) · [Propagation](#spring-4)

### Vòng 4: Security + tối ưu database

- [ ] [Tối ưu câu SQL](#db-query-optimization) · [Query chậm ở production](#database-13)
- [ ] [OAuth và JWT, hết hạn token, thu hồi JWT, refresh token](#sec-token-lifecycle) · [OAuth 2.0 / OIDC](#sec-oauth) · [JWT](#sec-jwt)

### Vòng 5: HR + culture fit

- [ ] [Vì sao muốn vào công ty](#hr-screening-3)
- [ ] [Áp lực và deadline, làm việc với team toàn cầu, định hướng phát triển](#hr-culture-fit)
- [ ] [Câu hỏi nên hỏi lại interviewer](#hr-questions-to-ask)

### Gợi ý ôn

- Ngân hàng rất coi trọng **tính đúng**: khi trả lời luôn nhắc idempotency, transaction, xử lý tiền bằng `BigDecimal` hoặc số nguyên đơn vị nhỏ nhất, audit log.
- Câu rate limiter "5 request/user/phút" là **LLD**: interviewer muốn thấy **code chạy được và thread-safe**, sau đó mới mở rộng sang Redis.
- Kinh nghiệm bảo hiểm ở DXC (dữ liệu nhạy cảm, compliance) và bảo mật ở Opswat (forward auth) là chất liệu tốt cho vòng 4.

@@@ dsa-valid-paren-star | Kiểm tra chuỗi ngoặc hợp lệ khi `*` có thể là `(`, `)` hoặc rỗng. / Validate a parenthesis string where `*` can be `(`, `)` or empty. | coding | dsa,greedy,string,goldman-sachs | qa | DSA
### Tiếng Việt

**Đề bài:** chuỗi gồm `(`, `)` (đề gốc dùng `{` `}`, cách giải y hệt) và `*`; mỗi `*` có thể là ngoặc mở, ngoặc đóng hoặc rỗng. Hỏi chuỗi có thể cân bằng không. LeetCode [678. Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) (Medium).

Ví dụ: `"(*)"` → true, `"(*))"` → true (`*` là `(`), `"(()"` → false, `"*)("` → false.

**Ý tưởng tham lam: theo dõi khoảng số ngoặc mở có thể có.** Vì `*` có nhiều lựa chọn, số ngoặc mở đang chờ đóng không phải một số mà là một **khoảng** `[lo, hi]`:
- `lo`: số ngoặc mở **ít nhất** có thể (coi `*` là `)` khi được).
- `hi`: số ngoặc mở **nhiều nhất** có thể (coi `*` là `(`).

| Ký tự | lo | hi |
|---|---|---|
| `(` | +1 | +1 |
| `)` | −1 | −1 |
| `*` | −1 (coi là `)`) | +1 (coi là `(`) |

- Nếu `hi < 0`: kể cả coi mọi `*` là `(` vẫn thừa `)`, nên **false ngay**.
- `lo` không được âm (không thể có số ngoặc mở âm): `lo = max(lo, 0)`.
- Cuối cùng hợp lệ nếu `lo == 0` (có cách chọn để đóng hết).

```java
public boolean checkValidString(String s) {
    int lo = 0, hi = 0;
    for (char c : s.toCharArray()) {
        if (c == '(')      { lo++; hi++; }
        else if (c == ')') { lo--; hi--; }
        else               { lo--; hi++; }      // '*'
        if (hi < 0) return false;               // quá nhiều ')'
        lo = Math.max(lo, 0);
    }
    return lo == 0;
}
```

**Độ phức tạp:** O(n) thời gian, O(1) bộ nhớ.

**Cách khác để nói khi phỏng vấn:**
- **Hai stack** lưu **chỉ số** của `(` và `*`. Gặp `)` thì ưu tiên ghép với `(`, hết thì ghép với `*`, hết nữa thì false. Cuối cùng ghép từng `(` còn lại với một `*` **đứng sau nó** (chỉ số lớn hơn). O(n) thời gian, O(n) bộ nhớ, dễ giải thích hơn.
- Quy hoạch động O(n³) hoặc backtracking O(3ⁿ): chỉ nêu để cho thấy bạn biết, rồi tối ưu.

**Case biên:** chuỗi rỗng (true), chỉ có `*`, `*` đứng trước `(` như `"*("` (false, vì `*` sau không đóng được `(`).

### English

**Problem:** a string of `(`, `)` (the original uses `{` `}`; the solution is identical) and `*`, where each `*` can be an opening bracket, a closing bracket or empty. Can the string be balanced? LeetCode [678. Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) (Medium).

Examples: `"(*)"` → true, `"(*))"` → true (`*` as `(`), `"(()"` → false, `"*)("` → false.

**Greedy idea: track the range of possible open-bracket counts.** Because `*` has several choices, the number of open brackets waiting to be closed isn't one number but a **range** `[lo, hi]`:
- `lo`: the **fewest** possible open brackets (treat `*` as `)` when possible).
- `hi`: the **most** possible open brackets (treat `*` as `(`).

| Character | lo | hi |
|---|---|---|
| `(` | +1 | +1 |
| `)` | −1 | −1 |
| `*` | −1 (as `)`) | +1 (as `(`) |

- If `hi < 0`: even treating every `*` as `(` leaves too many `)`, so **return false immediately**.
- `lo` can't go negative (there's no negative count of open brackets): `lo = max(lo, 0)`.
- At the end it's valid if `lo == 0` (some choice closes everything).

```java
public boolean checkValidString(String s) {
    int lo = 0, hi = 0;
    for (char c : s.toCharArray()) {
        if (c == '(')      { lo++; hi++; }
        else if (c == ')') { lo--; hi--; }
        else               { lo--; hi++; }      // '*'
        if (hi < 0) return false;               // too many ')'
        lo = Math.max(lo, 0);
    }
    return lo == 0;
}
```

**Complexity:** O(n) time, O(1) memory.

**Alternatives to mention in an interview:**
- **Two stacks** holding the **indices** of `(` and `*`. On `)`, match a `(` first, otherwise a `*`, otherwise false. At the end, match each remaining `(` with a `*` that comes **after it** (a larger index). O(n) time, O(n) memory, and easier to explain.
- DP in O(n³) or backtracking in O(3ⁿ): mention them only to show you know them, then optimize.

**Edge cases:** an empty string (true), only `*`, and `*` before `(` as in `"*("` (false, because a `*` before it can't close that `(`).

@@@ dsa-top-k-words | K từ xuất hiện nhiều nhất, sắp theo tần suất rồi theo thứ tự từ điển. / Top K frequent words, sorted by frequency then lexicographically. | coding | dsa,heap,hashmap,goldman-sachs | qa | DSA
### Tiếng Việt

**Đề bài:** cho mảng từ `words` và `k`, trả về `k` từ xuất hiện nhiều nhất, **tần suất giảm dần**; cùng tần suất thì **theo thứ tự từ điển tăng dần**. LeetCode [692. Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) (Medium).

Ví dụ: `["i","love","leetcode","i","love","coding"], k = 2` → `["i","love"]` (cùng 2 lần, `"i"` < `"love"`).

**Bước 1:** đếm bằng `HashMap<String, Integer>`: O(n).

**Bước 2, cách A: sắp xếp toàn bộ.** O(m log m) với m là số từ khác nhau. Đủ tốt và dễ viết:
```java
public List<String> topKFrequent(String[] words, int k) {
    Map<String, Integer> count = new HashMap<>();
    for (String w : words) count.merge(w, 1, Integer::sum);
    return count.keySet().stream()
        .sorted(Comparator.comparing((String w) -> count.get(w)).reversed()
                          .thenComparing(Comparator.naturalOrder()))
        .limit(k)
        .toList();
}
```

**Bước 2, cách B: min-heap kích thước k.** O(m log k), tốt hơn khi m rất lớn và k nhỏ. Phần khó là **comparator của heap phải ngược với thứ tự kết quả**: phần tử "kém nhất" nằm ở đỉnh để bị loại, tức **tần suất thấp hơn**, hoặc cùng tần suất thì **từ lớn hơn theo từ điển**.

```java
public List<String> topKFrequent(String[] words, int k) {
    Map<String, Integer> count = new HashMap<>();
    for (String w : words) count.merge(w, 1, Integer::sum);

    PriorityQueue<String> heap = new PriorityQueue<>((a, b) -> {
        int fa = count.get(a), fb = count.get(b);
        return fa != fb ? Integer.compare(fa, fb)   // tần suất thấp lên đỉnh
                        : b.compareTo(a);           // cùng tần suất: từ LỚN hơn lên đỉnh
    });
    for (String w : count.keySet()) {
        heap.offer(w);
        if (heap.size() > k) heap.poll();           // loại phần tử kém nhất
    }
    List<String> result = new ArrayList<>();
    while (!heap.isEmpty()) result.add(heap.poll());
    Collections.reverse(result);                    // heap trả từ kém đến tốt, nên đảo lại
    return result;
}
```

**Lỗi hay mắc:** viết comparator cùng chiều với kết quả (`a.compareTo(b)`) cho heap, làm loại nhầm từ đúng khi cùng tần suất; quên đảo kết quả cuối.

**Cách C: bucket sort theo tần suất** (mảng danh sách theo số lần xuất hiện), mỗi bucket sắp theo từ điển: gần O(n), nêu khi được hỏi tối ưu thêm.

**Mở rộng hay gặp:** dữ liệu là **stream** không chứa hết trong bộ nhớ thì dùng Count-Min Sketch kết hợp heap (gần đúng), hoặc đếm phân tán theo shard rồi gộp top-k.

### English

**Problem:** given `words` and `k`, return the `k` most frequent words, **by descending frequency**; ties are broken by **ascending lexicographical order**. LeetCode [692. Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/) (Medium).

Example: `["i","love","leetcode","i","love","coding"], k = 2` → `["i","love"]` (both appear twice, and `"i"` < `"love"`).

**Step 1:** count with a `HashMap<String, Integer>`: O(n).

**Step 2, approach A: sort everything.** O(m log m), where m is the number of distinct words. Good enough and easy to write:
```java
public List<String> topKFrequent(String[] words, int k) {
    Map<String, Integer> count = new HashMap<>();
    for (String w : words) count.merge(w, 1, Integer::sum);
    return count.keySet().stream()
        .sorted(Comparator.comparing((String w) -> count.get(w)).reversed()
                          .thenComparing(Comparator.naturalOrder()))
        .limit(k)
        .toList();
}
```

**Step 2, approach B: a min-heap of size k.** O(m log k), better when m is huge and k is small. The tricky part is that **the heap's comparator must be the reverse of the result order**: the "worst" element sits on top to be evicted, meaning **lower frequency**, or on a tie the **lexicographically larger word**.

```java
public List<String> topKFrequent(String[] words, int k) {
    Map<String, Integer> count = new HashMap<>();
    for (String w : words) count.merge(w, 1, Integer::sum);

    PriorityQueue<String> heap = new PriorityQueue<>((a, b) -> {
        int fa = count.get(a), fb = count.get(b);
        return fa != fb ? Integer.compare(fa, fb)   // lower frequency on top
                        : b.compareTo(a);           // tie: the LARGER word on top
    });
    for (String w : count.keySet()) {
        heap.offer(w);
        if (heap.size() > k) heap.poll();           // evict the worst element
    }
    List<String> result = new ArrayList<>();
    while (!heap.isEmpty()) result.add(heap.poll());
    Collections.reverse(result);                    // the heap yields worst to best, so reverse
    return result;
}
```

**Common mistakes:** giving the heap a comparator in the same direction as the result (`a.compareTo(b)`), which evicts the right word on ties; forgetting to reverse at the end.

**Approach C: bucket sort by frequency** (an array of lists indexed by count), sorting each bucket lexicographically: close to O(n); mention it if asked to optimize further.

**A common extension:** if the data is a **stream** that doesn't fit in memory, use a Count-Min Sketch with a heap (approximate), or count per shard and merge the top-k results.

@@@ dsa-swap-pairs | Đảo linked list theo từng cặp: 1→2→3→4→5 thành 2→1→4→3→5. / Swap a linked list in pairs: 1→2→3→4→5 becomes 2→1→4→3→5. | coding | dsa,linked-list,goldman-sachs | qa | DSA
### Tiếng Việt

**Đề bài:** đổi chỗ từng cặp node liền kề, **đổi node chứ không đổi giá trị**. Số node lẻ thì node cuối giữ nguyên. LeetCode [24. Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) (Medium).

**Cách lặp với dummy node** (nên trình bày cách này, O(1) bộ nhớ). Dummy đứng trước `head` để cặp đầu tiên được xử lý giống mọi cặp khác, không cần trường hợp đặc biệt.

```
prev → a → b → next      ⇒      prev → b → a → next
```

```java
public ListNode swapPairs(ListNode head) {
    ListNode dummy = new ListNode(0, head);
    ListNode prev = dummy;
    while (prev.next != null && prev.next.next != null) {
        ListNode a = prev.next;
        ListNode b = a.next;
        // nối lại 3 con trỏ, theo đúng thứ tự để không mất phần còn lại của list
        a.next = b.next;     // a trỏ tới phần sau cặp
        b.next = a;          // b đứng trước a
        prev.next = b;       // node trước cặp trỏ tới b
        prev = a;            // a giờ là node cuối của cặp, làm prev cho cặp tiếp theo
    }
    return dummy.next;
}
```

Chạy với `1→2→3→4→5`: cặp (1,2) thành `2→1`, `prev = 1`; cặp (3,4) thành `4→3`, `prev = 3`; còn mỗi `5` nên dừng. Kết quả `2→1→4→3→5`.

**Cách đệ quy** (ngắn, nhưng O(n) bộ nhớ stack):
```java
public ListNode swapPairs(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode second = head.next;
    head.next = swapPairs(second.next);
    second.next = head;
    return second;
}
```

**Độ phức tạp:** O(n) thời gian; lặp O(1) bộ nhớ, đệ quy O(n).

**Mẹo với bài linked list:** dùng dummy node; **vẽ ra giấy** các con trỏ trước khi code; viết các phép gán theo thứ tự "nối phần sau trước, rồi mới nối phần trước". Mở rộng hay gặp: đảo theo nhóm k node (LeetCode 25, Hard, có thể bỏ qua).

**Case biên:** list rỗng, 1 node, số node chẵn, số node lẻ.

### English

**Problem:** swap every two adjacent nodes, **swapping the nodes, not the values**. With an odd count, the last node stays. LeetCode [24. Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) (Medium).

**The iterative approach with a dummy node** (present this one, O(1) memory). The dummy sits before `head` so the first pair is handled like every other pair, with no special case.

```
prev → a → b → next      ⇒      prev → b → a → next
```

```java
public ListNode swapPairs(ListNode head) {
    ListNode dummy = new ListNode(0, head);
    ListNode prev = dummy;
    while (prev.next != null && prev.next.next != null) {
        ListNode a = prev.next;
        ListNode b = a.next;
        // rewire 3 pointers, in the right order so the rest of the list isn't lost
        a.next = b.next;     // a points past the pair
        b.next = a;          // b goes before a
        prev.next = b;       // the node before the pair points to b
        prev = a;            // a is now the pair's last node, the prev for the next pair
    }
    return dummy.next;
}
```

Walking through `1→2→3→4→5`: pair (1,2) becomes `2→1`, `prev = 1`; pair (3,4) becomes `4→3`, `prev = 3`; only `5` is left, so stop. Result: `2→1→4→3→5`.

**The recursive approach** (shorter, but O(n) stack memory):
```java
public ListNode swapPairs(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode second = head.next;
    head.next = swapPairs(second.next);
    second.next = head;
    return second;
}
```

**Complexity:** O(n) time; O(1) memory iteratively, O(n) recursively.

**Linked-list tips:** use a dummy node; **draw the pointers on paper** before coding; order the assignments so you "link the tail first, then the head". A common extension: reversing in groups of k (LeetCode 25, Hard, safe to skip).

**Edge cases:** an empty list, 1 node, an even count, an odd count.

@@@ jc-hashmap-collision | HashMap xử lý va chạm thế nào (linked list hay cây ở Java 8+)? Vì sao load factor là 0.75? / How does HashMap handle collisions (linked lists vs trees in Java 8+), and why is the load factor 0.75? | java | hashmap,collections,goldman-sachs | qa | Java core
### Tiếng Việt

*Câu này đào sâu hơn [HashMap hoạt động bên trong](#java-core-1).*

**Va chạm (collision):** hai key khác nhau rơi vào **cùng một bucket**. Index bucket được tính từ hash: `index = (n - 1) & hash`, trong đó `n` là dung lượng (luôn là **lũy thừa của 2** để phép `&` thay được phép `%` cho nhanh), còn `hash = h ^ (h >>> 16)` trộn 16 bit cao xuống bit thấp để key có hashCode chỉ khác ở bit cao vẫn phân tán đều.

**Java 7 trở về trước:** mỗi bucket là **linked list**. Nhiều key cùng bucket thì tìm kiếm thành **O(n)**. Kẻ tấn công có thể cố tình gửi nhiều key cùng hash (ví dụ tên tham số HTTP) để làm server chậm (**hash flooding DoS**).

**Java 8+:** bucket bắt đầu là linked list, nhưng **chuyển thành cây đỏ đen** (treeify) khi:
- số node trong bucket **≥ `TREEIFY_THRESHOLD = 8`**, **và**
- dung lượng bảng **≥ `MIN_TREEIFY_CAPACITY = 64`** (nếu bảng còn nhỏ hơn thì **resize** thay vì treeify, vì va chạm nhiều khi bảng nhỏ là bình thường).

Bucket dạng cây tìm kiếm **O(log n)** thay vì O(n). Khi số node giảm còn **≤ `UNTREEIFY_THRESHOLD = 6`** (thường do resize tách bucket), cây chuyển lại thành linked list. Khoảng chênh 8 và 6 tránh việc chuyển qua lại liên tục.

**Vì sao ngưỡng là 8:** với hàm hash tốt và load factor 0.75, số node trong một bucket theo **phân phối Poisson** (λ ≈ 0.5). Xác suất một bucket có 8 node là khoảng **6 phần 100 triệu**. Nên treeify gần như chỉ xảy ra khi **hashCode tệ hoặc bị tấn công**: nó là cơ chế phòng thủ, không phải đường chạy bình thường. Node cây cũng tốn khoảng **gấp đôi bộ nhớ** node thường, nên không treeify sớm.

Cây sắp xếp theo hash; nếu trùng hash mà key implement `Comparable` thì dùng `compareTo` để phân nhánh. Vì vậy key nên implement `Comparable` nếu có thể.

**Load factor 0.75:** khi `size > capacity × loadFactor` thì **resize**: gấp đôi dung lượng và phân bổ lại entry (Java 8 chỉ cần xét 1 bit: entry giữ nguyên index hoặc chuyển sang `index + oldCap`, không cần tính hash lại).

| Load factor | Ảnh hưởng |
|---|---|
| Thấp (0.5) | Ít va chạm, tra cứu nhanh, nhưng **tốn bộ nhớ** và resize thường xuyên |
| **0.75** | **Cân bằng** giữa thời gian và bộ nhớ: va chạm vẫn ít (như phân tích Poisson ở trên), bảng không quá thưa |
| Cao (1.0+) | Tiết kiệm bộ nhớ, nhưng nhiều va chạm, tra cứu chậm hơn |

**Ý nghĩa thực tế:**
- Biết trước số phần tử thì **khởi tạo đủ dung lượng** để tránh resize: Java 19+ có `HashMap.newHashMap(expectedSize)`; trước đó dùng `new HashMap<>((int) (expected / 0.75f) + 1)`.
- `hashCode()` tệ (ví dụ luôn trả `1`) biến mọi thứ thành một bucket: vẫn chạy đúng nhưng rất chậm.
- **Không sửa field tham gia `hashCode` của key** sau khi đã đặt vào map: entry nằm sai bucket và không tìm lại được.

### English

*This digs deeper than [How HashMap works internally](#java-core-1).*

**A collision:** two different keys land in **the same bucket**. The bucket index comes from the hash: `index = (n - 1) & hash`, where `n` is the capacity (always **a power of 2** so `&` can replace the slower `%`), and `hash = h ^ (h >>> 16)` mixes the high 16 bits into the low bits so keys whose hashCodes differ only in high bits still spread evenly.

**Java 7 and earlier:** each bucket is a **linked list**. Many keys in one bucket make lookups **O(n)**. An attacker can deliberately send many keys with the same hash (for example HTTP parameter names) to slow the server down (**hash-flooding DoS**).

**Java 8+:** a bucket starts as a linked list but is **converted to a red-black tree** (treeified) when:
- the bucket holds **≥ `TREEIFY_THRESHOLD = 8`** nodes, **and**
- the table capacity is **≥ `MIN_TREEIFY_CAPACITY = 64`** (if the table is smaller, it **resizes** instead of treeifying, because many collisions in a small table are normal).

A tree bucket searches in **O(log n)** instead of O(n). When the node count falls to **≤ `UNTREEIFY_THRESHOLD = 6`** (usually because a resize splits the bucket), it turns back into a linked list. The gap between 8 and 6 prevents flip-flopping.

**Why the threshold is 8:** with a good hash function and a 0.75 load factor, bucket sizes follow a **Poisson distribution** (λ ≈ 0.5). The probability of one bucket holding 8 nodes is about **6 in 100 million**. So treeification practically only happens with **bad hashCodes or an attack**: it's a defensive mechanism, not the normal path. Tree nodes also take about **twice the memory** of regular nodes, so you don't treeify early.

The tree is ordered by hash; when hashes tie and the key implements `Comparable`, `compareTo` decides the branch. So keys should implement `Comparable` where possible.

**Load factor 0.75:** when `size > capacity × loadFactor`, the map **resizes**: it doubles the capacity and redistributes entries (in Java 8 only one bit needs checking: an entry keeps its index or moves to `index + oldCap`, with no rehashing).

| Load factor | Effect |
|---|---|
| Low (0.5) | Few collisions and fast lookups, but **more memory** and frequent resizes |
| **0.75** | **A balance** between time and memory: collisions stay rare (per the Poisson analysis above) without the table being too sparse |
| High (1.0+) | Saves memory, but more collisions and slower lookups |

**Practical consequences:**
- If you know the element count, **pre-size the map** to avoid resizes: Java 19+ has `HashMap.newHashMap(expectedSize)`; before that, `new HashMap<>((int) (expected / 0.75f) + 1)`.
- A bad `hashCode()` (say, always returning `1`) puts everything in one bucket: still correct, but very slow.
- **Never mutate fields used in a key's `hashCode` after putting it in the map**: the entry ends up in the wrong bucket and can't be found again.

@@@ jc-jmm | Java Memory Model là gì? Visibility, reordering và happens-before? / What is the Java Memory Model? Visibility, reordering and happens-before? | java | concurrency,jmm,goldman-sachs | qa | Java core
### Tiếng Việt

**Java Memory Model (JMM)** (đặc tả trong JLS chương 17, từ Java 5) định nghĩa **khi nào một thread chắc chắn thấy được giá trị mà thread khác đã ghi**. Không có JMM, code đa luồng sẽ chạy khác nhau trên mỗi CPU và JVM.

*Đừng nhầm với **cấu trúc bộ nhớ JVM** (heap, stack, metaspace): đó là câu hỏi khác. Xem [JVM memory](#jvm-10).*

**Vì sao cần:** để chạy nhanh, phần cứng và compiler làm hai việc:
1. **Cache:** mỗi core có cache riêng; giá trị ghi có thể nằm trong cache hoặc register, **thread khác chưa thấy** (vấn đề **visibility**).
2. **Sắp xếp lại lệnh (reordering):** compiler, JIT và CPU đổi thứ tự lệnh nếu **trong một thread** kết quả không đổi, nhưng thread khác có thể thấy thứ tự lạ.

```java
class Worker {
    private boolean running = true;        // không volatile
    void run()  { while (running) { /* work */ } }   // có thể lặp MÃI MÃI
    void stop() { running = false; }                 // thread khác gọi
}
```
JIT có thể đưa việc đọc `running` ra ngoài vòng lặp (thành `while (true)`), nên thread chạy không bao giờ thấy `false`. Sửa: `volatile boolean running`.

**Ba tính chất cần đảm bảo:**
- **Atomicity:** thao tác không bị chia cắt. `count++` gồm đọc, cộng, ghi nên **không atomic**. Ghi `long` hoặc `double` không volatile cũng có thể không atomic trên JVM 32-bit.
- **Visibility:** giá trị ghi được thread khác thấy.
- **Ordering:** thứ tự thao tác được giữ như mong đợi.

**Happens-before:** nếu thao tác A *happens-before* B thì mọi thứ A ghi đều **thấy được** ở B. Các quy tắc chính:

| Quy tắc | Ý nghĩa |
|---|---|
| Thứ tự chương trình | Trong một thread, lệnh trước happens-before lệnh sau |
| **Monitor lock** | `unlock` một monitor happens-before `lock` tiếp theo trên **cùng** monitor đó (`synchronized`, `Lock`) |
| **volatile** | Ghi biến volatile happens-before mọi lần đọc sau đó của biến đó |
| Thread start | `t.start()` happens-before mọi lệnh trong thread `t` |
| Thread join | Mọi lệnh trong `t` happens-before `t.join()` trả về |
| Field `final` | Sau khi constructor xong (và `this` không bị lộ ra sớm), thread khác thấy đúng giá trị field `final` |
| Bắc cầu | A trước B, B trước C, thì A trước C |
| Thư viện concurrent | Đặt vào `ConcurrentHashMap`, `BlockingQueue`, `Future.get()`... có happens-before với thread lấy ra |

**Công cụ và ý nghĩa:**

| Công cụ | Atomicity | Visibility | Ordering |
|---|---|---|---|
| `volatile` | Chỉ với đọc/ghi đơn lẻ (**không** với `count++`) | Có | Có (ngăn reordering quanh nó) |
| `synchronized` / `Lock` | Có (cho cả block) | Có | Có |
| `AtomicInteger`, `LongAdder` | Có (CAS) | Có | Có |

**Ví dụ kinh điển: double-checked locking cho singleton phải có `volatile`:**
```java
class Config {
    private static volatile Config instance;          // thiếu volatile thì thread khác có thể thấy object CHƯA khởi tạo xong
    static Config get() {
        if (instance == null) {
            synchronized (Config.class) {
                if (instance == null) instance = new Config();
            }
        }
        return instance;
    }
}
```
`new Config()` gồm cấp bộ nhớ, chạy constructor, gán tham chiếu; không có `volatile` thì bước gán có thể bị đưa lên trước bước chạy constructor. (Cách đơn giản hơn: holder class hoặc `enum`.)

**Câu trả lời mẫu:** *"JMM định nghĩa khi nào giá trị một thread ghi được thread khác thấy. Do cache CPU và reordering, nếu không có quan hệ happens-before thì không có gì đảm bảo. Tôi tạo happens-before bằng `synchronized` hoặc Lock, `volatile` cho cờ trạng thái, hoặc dùng class trong `java.util.concurrent`. Lưu ý `volatile` chỉ đảm bảo visibility, không làm `count++` thành atomic."*

### English

The **Java Memory Model (JMM)** (specified in JLS chapter 17, since Java 5) defines **when one thread is guaranteed to see a value another thread wrote**. Without it, multithreaded code would behave differently on every CPU and JVM.

*Don't confuse it with **JVM memory structure** (heap, stack, metaspace): that's a different question. See [JVM memory](#jvm-10).*

**Why it's needed:** to run fast, hardware and compilers do two things:
1. **Caching:** each core has its own cache; a written value may sit in a cache or register where **other threads can't see it yet** (the **visibility** problem).
2. **Reordering:** the compiler, JIT and CPU reorder instructions when the result **within one thread** is unchanged, but other threads may observe a strange order.

```java
class Worker {
    private boolean running = true;        // not volatile
    void run()  { while (running) { /* work */ } }   // may loop FOREVER
    void stop() { running = false; }                 // called from another thread
}
```
The JIT may hoist the read of `running` out of the loop (turning it into `while (true)`), so the running thread never sees `false`. The fix: `volatile boolean running`.

**Three properties to guarantee:**
- **Atomicity:** an operation can't be split. `count++` is a read, an add and a write, so it's **not atomic**. Writes to non-volatile `long` or `double` may not be atomic on 32-bit JVMs either.
- **Visibility:** a written value is seen by other threads.
- **Ordering:** operations keep the expected order.

**Happens-before:** if action A *happens-before* B, everything A wrote is **visible** to B. The main rules:

| Rule | Meaning |
|---|---|
| Program order | Within one thread, an earlier statement happens-before a later one |
| **Monitor lock** | An `unlock` of a monitor happens-before every later `lock` of **the same** monitor (`synchronized`, `Lock`) |
| **volatile** | A write to a volatile variable happens-before every later read of it |
| Thread start | `t.start()` happens-before every action in thread `t` |
| Thread join | Every action in `t` happens-before `t.join()` returns |
| `final` fields | After a constructor finishes (and `this` didn't escape early), other threads see the correct values of `final` fields |
| Transitivity | A before B and B before C means A before C |
| Concurrent libraries | Putting into a `ConcurrentHashMap`, a `BlockingQueue`, `Future.get()`... happens-before the thread that takes it out |

**Tools and what they guarantee:**

| Tool | Atomicity | Visibility | Ordering |
|---|---|---|---|
| `volatile` | Only single reads/writes (**not** `count++`) | Yes | Yes (prevents reordering around it) |
| `synchronized` / `Lock` | Yes (for the whole block) | Yes | Yes |
| `AtomicInteger`, `LongAdder` | Yes (CAS) | Yes | Yes |

**The classic example: double-checked locking for a singleton needs `volatile`:**
```java
class Config {
    private static volatile Config instance;          // without volatile, another thread may see a HALF-constructed object
    static Config get() {
        if (instance == null) {
            synchronized (Config.class) {
                if (instance == null) instance = new Config();
            }
        }
        return instance;
    }
}
```
`new Config()` means allocate memory, run the constructor, assign the reference; without `volatile`, the assignment can be reordered before the constructor runs. (Simpler alternatives: a holder class or an `enum`.)

**A model answer:** *"The JMM defines when a value written by one thread becomes visible to another. Because of CPU caches and reordering, nothing is guaranteed without a happens-before relationship. I create happens-before with `synchronized` or Locks, `volatile` for status flags, or classes from `java.util.concurrent`. Note that `volatile` only guarantees visibility; it doesn't make `count++` atomic."*

@@@ jc-thread-safety | Có những cách nào để code thread-safe? Chọn cách nào khi nào? / What are the ways to make code thread-safe, and when do you use each? | java | concurrency,thread-safety,goldman-sachs | qa | Java core
### Tiếng Việt

**Thread-safe:** code chạy đúng khi nhiều thread cùng gọi, không cần bên gọi đồng bộ thêm. Vấn đề chỉ xảy ra khi có **trạng thái dùng chung và có thể thay đổi**. Nên các cách xử lý, theo thứ tự nên ưu tiên:

| # | Cách | Ý tưởng | Ví dụ |
|---|---|---|---|
| 1 | **Không chia sẻ trạng thái (stateless)** | Không có gì dùng chung thì không có race | Service Spring không có field thay đổi; mọi dữ liệu qua tham số |
| 2 | **Bất biến (immutable)** | Object không đổi sau khi tạo thì đọc thoải mái | `record`, field `final`, `List.copyOf`, `String`, `BigDecimal` |
| 3 | **Giới hạn trong một thread (thread confinement)** | Mỗi thread dùng bản riêng | Biến local, `ThreadLocal` (nhớ `remove()`), mỗi request một object |
| 4 | **Collection concurrent** | Dùng cấu trúc đã thread-safe | `ConcurrentHashMap` (`compute`, `merge` atomic), `CopyOnWriteArrayList`, `BlockingQueue` |
| 5 | **Atomic / CAS** | Thao tác đơn không khóa | `AtomicInteger.incrementAndGet()`, `LongAdder` cho bộ đếm nhiều thread ghi |
| 6 | **Khóa** | Chỉ một thread vào vùng găng | `synchronized`, `ReentrantLock`, `ReadWriteLock`. Xem [synchronized vs Lock](#jc-sync-vs-lock) |
| 7 | **`volatile`** | Chỉ để **visibility** của cờ hoặc tham chiếu | `volatile boolean shutdown`. Xem [JMM](#jc-jmm) |

**Bẫy hay gặp:**
1. **Check-then-act không atomic dù dùng collection thread-safe:**
```java
if (!map.containsKey(k)) map.put(k, v);        // SAI: hai thread cùng thấy "chưa có"
map.putIfAbsent(k, v);                          // ĐÚNG: atomic
map.computeIfAbsent(k, key -> load(key));       // ĐÚNG
map.merge(word, 1, Integer::sum);               // đếm atomic
```
2. **Đồng bộ trên các object khác nhau** thì không bảo vệ được gì; mọi chỗ truy cập cùng dữ liệu phải dùng **cùng một khóa**.
3. **`Collections.synchronizedList`** vẫn phải tự khóa khi **duyệt** (iterate).
4. **`SimpleDateFormat`** không thread-safe; dùng `DateTimeFormatter` (bất biến).
5. **Deadlock** khi lấy nhiều khóa theo thứ tự khác nhau; luôn lấy theo **thứ tự cố định**. Xem [Deadlock](#concurrency-17).
6. **Thread-safe trong một JVM ≠ đúng khi chạy nhiều instance:** nhiều pod thì phải dựa vào database (unique constraint, optimistic locking `@Version`, `SELECT ... FOR UPDATE`) hoặc khóa phân tán.

**Kiểm thử:** race condition hiếm khi lộ ra ở unit test thông thường. Dùng test chạy song song nhiều lần (`ExecutorService` + `CountDownLatch`), **jcstress** cho kiểm thử sâu, và review code kỹ.

**Câu trả lời mẫu:** *"Tôi ưu tiên tránh trạng thái dùng chung: service stateless, object bất biến như record. Khi buộc phải chia sẻ, tôi dùng collection concurrent với các thao tác atomic như `merge`, `computeIfAbsent`, hoặc Atomic class; chỉ dùng khóa khi cần bảo vệ nhiều biến cùng lúc. Và với ứng dụng nhiều instance, tính đúng đắn cuối cùng nằm ở database."*

### English

**Thread-safe:** code behaves correctly when called by many threads at once, with no extra synchronization by callers. Problems only arise with **shared, mutable state**. So the approaches, in order of preference:

| # | Approach | Idea | Example |
|---|---|---|---|
| 1 | **Don't share state (stateless)** | Nothing shared, no race | Spring services with no mutable fields; all data passed as parameters |
| 2 | **Immutability** | Objects that never change after construction can be read freely | `record`, `final` fields, `List.copyOf`, `String`, `BigDecimal` |
| 3 | **Thread confinement** | Each thread uses its own copy | Local variables, `ThreadLocal` (remember `remove()`), one object per request |
| 4 | **Concurrent collections** | Use structures that are already thread-safe | `ConcurrentHashMap` (atomic `compute`, `merge`), `CopyOnWriteArrayList`, `BlockingQueue` |
| 5 | **Atomics / CAS** | Lock-free single operations | `AtomicInteger.incrementAndGet()`, `LongAdder` for counters written by many threads |
| 6 | **Locks** | Only one thread in the critical section | `synchronized`, `ReentrantLock`, `ReadWriteLock`. See [synchronized vs Lock](#jc-sync-vs-lock) |
| 7 | **`volatile`** | Only for **visibility** of flags or references | `volatile boolean shutdown`. See [JMM](#jc-jmm) |

**Common traps:**
1. **Check-then-act isn't atomic even with a thread-safe collection:**
```java
if (!map.containsKey(k)) map.put(k, v);        // WRONG: two threads both see "absent"
map.putIfAbsent(k, v);                          // RIGHT: atomic
map.computeIfAbsent(k, key -> load(key));       // RIGHT
map.merge(word, 1, Integer::sum);               // atomic counting
```
2. **Synchronizing on different objects** protects nothing; every access to the same data must use **the same lock**.
3. **`Collections.synchronizedList`** still needs manual locking while **iterating**.
4. **`SimpleDateFormat`** isn't thread-safe; use `DateTimeFormatter` (immutable).
5. **Deadlocks** when acquiring several locks in different orders; always acquire them in **a fixed order**. See [Deadlock](#concurrency-17).
6. **Thread-safe within one JVM ≠ correct across instances:** with several pods, rely on the database (unique constraints, optimistic locking with `@Version`, `SELECT ... FOR UPDATE`) or a distributed lock.

**Testing:** race conditions rarely show up in ordinary unit tests. Use tests that run in parallel many times (`ExecutorService` + `CountDownLatch`), **jcstress** for deep testing, and careful code review.

**A model answer:** *"I prefer to avoid shared state: stateless services and immutable objects like records. When sharing is unavoidable, I use concurrent collections with atomic operations such as `merge` and `computeIfAbsent`, or Atomic classes, and only use locks when several variables must be protected together. And for multi-instance applications, correctness ultimately lives in the database."*

@@@ lld-rate-limiter | LLD: thiết kế rate limiter cho phép tối đa 5 request mỗi user mỗi phút. / LLD: design a rate limiter allowing at most 5 requests per user per minute. | arch | lld,rate-limiter,concurrency,goldman-sachs | qa | Low-level design
### Tiếng Việt

*Đây là câu **low-level design**: interviewer muốn **code chạy được, thread-safe, dễ mở rộng**. Phiên bản phân tán và so sánh thuật toán xem [Thiết kế rate limiter](#system-design-18).*

**1. Làm rõ yêu cầu (hỏi trước khi code):**
- "1 phút" là **cửa sổ cố định** (00:00–00:59) hay **cửa sổ trượt** (60 giây gần nhất)? Fixed window cho phép tới 10 request quanh ranh giới phút (5 lúc 00:59 + 5 lúc 01:00); nếu cần chặt chẽ thì dùng sliding window.
- Một instance hay nhiều instance? Vượt giới hạn thì trả gì (**HTTP 429** + `Retry-After`)?
- Giới hạn có thể khác nhau theo user hoặc gói không?

**2. Thiết kế class:**
```java
public interface RateLimiter {
    boolean tryAcquire(String userId);
}

public interface Clock { long nowMillis(); }      // inject để test được, không gọi System.currentTimeMillis() trực tiếp
```
Interface cho phép đổi thuật toán (sliding log, token bucket) hoặc implementation (in-memory, Redis) mà không sửa code gọi: đúng Open/Closed và Strategy pattern.

**3. Sliding window log (chính xác tuyệt đối, phù hợp giới hạn nhỏ như 5):**
```java
public class SlidingWindowRateLimiter implements RateLimiter {
    private final int limit;
    private final long windowMillis;
    private final Clock clock;
    private final ConcurrentHashMap<String, Deque<Long>> logs = new ConcurrentHashMap<>();

    public SlidingWindowRateLimiter(int limit, Duration window, Clock clock) {
        this.limit = limit; this.windowMillis = window.toMillis(); this.clock = clock;
    }

    @Override
    public boolean tryAcquire(String userId) {
        Deque<Long> log = logs.computeIfAbsent(userId, id -> new ArrayDeque<>());
        synchronized (log) {                               // khóa theo TỪNG USER, user khác không phải chờ
            long now = clock.nowMillis();
            while (!log.isEmpty() && log.peekFirst() <= now - windowMillis) {
                log.pollFirst();                           // bỏ các request đã ra khỏi cửa sổ 60 giây
            }
            if (log.size() >= limit) return false;
            log.addLast(now);
            return true;
        }
    }
}
// new SlidingWindowRateLimiter(5, Duration.ofMinutes(1), System::currentTimeMillis)
```
- Bộ nhớ: tối đa 5 timestamp mỗi user, O(1) mỗi lần gọi.
- **Thread-safety:** `computeIfAbsent` atomic tạo deque; khóa trên deque của **từng user** nên không có tranh chấp toàn cục.
- **Dọn dẹp:** user không còn hoạt động vẫn chiếm entry trong map. Dùng job định kỳ xóa deque rỗng, hoặc dùng cache có hết hạn (Caffeine `expireAfterAccess(2, MINUTES)`).

**4. Token bucket (cho phép burst, phổ biến trong thực tế):** mỗi user có xô chứa tối đa 5 token, nạp lại 5 token mỗi phút (1 token mỗi 12 giây); mỗi request lấy 1 token. Chỉ lưu 2 số (`tokens`, `lastRefill`) nên tiết kiệm bộ nhớ khi giới hạn lớn (ví dụ 1.000 request/phút).
```java
private static final class Bucket {
    double tokens; long lastRefill;
    synchronized boolean tryConsume(long now, int capacity, double refillPerMs) {
        tokens = Math.min(capacity, tokens + (now - lastRefill) * refillPerMs);
        lastRefill = now;
        if (tokens < 1) return false;
        tokens -= 1;
        return true;
    }
}
```

**5. Tích hợp với Spring:** `OncePerRequestFilter` hoặc `HandlerInterceptor`, lấy `userId` từ token đã xác thực (không phải từ header client tự gửi); vượt giới hạn trả **429** kèm `Retry-After` và `X-RateLimit-Remaining`. Thực tế có thể dùng Bucket4j hoặc Resilience4j RateLimiter, hoặc đặt ở API gateway.

**6. Nhiều instance: chuyển state sang Redis** để mọi pod dùng chung. Sliding window bằng sorted set trong **Lua script** (atomic):
```lua
-- KEYS[1]=rl:{userId}  ARGV: now, window_ms, limit, request_id
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, ARGV[1] - ARGV[2])
if redis.call('ZCARD', KEYS[1]) >= tonumber(ARGV[3]) then return 0 end
redis.call('ZADD', KEYS[1], ARGV[1], ARGV[4])
redis.call('PEXPIRE', KEYS[1], ARGV[2])
return 1
```
Redis lỗi thì chọn **fail-open** (cho qua, ưu tiên availability) hay **fail-closed** (chặn, ưu tiên bảo vệ): nói rõ lựa chọn theo nghiệp vụ.

**7. Test:** dùng `Clock` giả: 5 request đầu được, request thứ 6 bị chặn, tua đồng hồ thêm 60 giây thì được lại; test đồng thời: 100 thread cùng gọi cho một user thì đúng 5 lần thành công.

### English

*This is a **low-level design** question: the interviewer wants **working, thread-safe, extensible code**. For the distributed version and algorithm comparison, see [Design a rate limiter](#system-design-18).*

**1. Clarify requirements (ask before coding):**
- Is "1 minute" a **fixed window** (00:00–00:59) or a **sliding window** (the last 60 seconds)? A fixed window allows up to 10 requests around a minute boundary (5 at 00:59 + 5 at 01:00); if it must be strict, use a sliding window.
- One instance or many? What happens when the limit is exceeded (**HTTP 429** + `Retry-After`)?
- Can limits differ per user or plan?

**2. Class design:**
```java
public interface RateLimiter {
    boolean tryAcquire(String userId);
}

public interface Clock { long nowMillis(); }      // injected for testability; don't call System.currentTimeMillis() directly
```
The interface lets you swap the algorithm (sliding log, token bucket) or the implementation (in-memory, Redis) without changing callers: Open/Closed and the Strategy pattern.

**3. Sliding window log (exact, a good fit for small limits like 5):**
```java
public class SlidingWindowRateLimiter implements RateLimiter {
    private final int limit;
    private final long windowMillis;
    private final Clock clock;
    private final ConcurrentHashMap<String, Deque<Long>> logs = new ConcurrentHashMap<>();

    public SlidingWindowRateLimiter(int limit, Duration window, Clock clock) {
        this.limit = limit; this.windowMillis = window.toMillis(); this.clock = clock;
    }

    @Override
    public boolean tryAcquire(String userId) {
        Deque<Long> log = logs.computeIfAbsent(userId, id -> new ArrayDeque<>());
        synchronized (log) {                               // lock PER USER; other users don't wait
            long now = clock.nowMillis();
            while (!log.isEmpty() && log.peekFirst() <= now - windowMillis) {
                log.pollFirst();                           // drop requests outside the 60-second window
            }
            if (log.size() >= limit) return false;
            log.addLast(now);
            return true;
        }
    }
}
// new SlidingWindowRateLimiter(5, Duration.ofMinutes(1), System::currentTimeMillis)
```
- Memory: at most 5 timestamps per user, O(1) per call.
- **Thread safety:** `computeIfAbsent` creates the deque atomically; locking on **each user's** deque avoids global contention.
- **Cleanup:** inactive users still occupy map entries. Run a periodic job that removes empty deques, or use an expiring cache (Caffeine `expireAfterAccess(2, MINUTES)`).

**4. Token bucket (allows bursts, common in practice):** each user has a bucket of at most 5 tokens, refilled at 5 tokens per minute (1 token every 12 seconds); each request takes 1 token. It stores only 2 numbers (`tokens`, `lastRefill`), so it saves memory for large limits (say 1,000 requests/minute).
```java
private static final class Bucket {
    double tokens; long lastRefill;
    synchronized boolean tryConsume(long now, int capacity, double refillPerMs) {
        tokens = Math.min(capacity, tokens + (now - lastRefill) * refillPerMs);
        lastRefill = now;
        if (tokens < 1) return false;
        tokens -= 1;
        return true;
    }
}
```

**5. Spring integration:** a `OncePerRequestFilter` or `HandlerInterceptor` that takes `userId` from the authenticated token (not from a header the client sets); over the limit, return **429** with `Retry-After` and `X-RateLimit-Remaining`. In practice you might use Bucket4j or Resilience4j's RateLimiter, or enforce it at the API gateway.

**6. Many instances: move the state to Redis** so every pod shares it. A sliding window with a sorted set inside a **Lua script** (atomic):
```lua
-- KEYS[1]=rl:{userId}  ARGV: now, window_ms, limit, request_id
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, ARGV[1] - ARGV[2])
if redis.call('ZCARD', KEYS[1]) >= tonumber(ARGV[3]) then return 0 end
redis.call('ZADD', KEYS[1], ARGV[1], ARGV[4])
redis.call('PEXPIRE', KEYS[1], ARGV[2])
return 1
```
If Redis fails, choose **fail-open** (let requests through, favouring availability) or **fail-closed** (block them, favouring protection): state the choice according to the business.

**7. Tests:** with a fake `Clock`: the first 5 requests pass, the 6th is blocked, advancing the clock 60 seconds lets requests through again; a concurrency test: 100 threads calling for one user yield exactly 5 successes.

@@@ sp-boot-startup | Spring Boot khởi động thế nào từ `SpringApplication.run()` đến khi nhận request? / How does Spring Boot start up, from `SpringApplication.run()` to serving requests? | spring | spring-boot,internals,goldman-sachs | qa | Spring core
### Tiếng Việt

```java
@SpringBootApplication          // = @Configuration + @EnableAutoConfiguration + @ComponentScan
public class App { public static void main(String[] args) { SpringApplication.run(App.class, args); } }
```

**Các bước chính khi gọi `SpringApplication.run()`:**

1. **Tạo `SpringApplication`:** đoán loại ứng dụng (Servlet, Reactive, hay không phải web) dựa vào thư viện có trên classpath; nạp `ApplicationContextInitializer` và `ApplicationListener` khai báo trong các file `META-INF/spring.factories`.
2. **Chuẩn bị `Environment`:** đọc cấu hình theo thứ tự ưu tiên: tham số dòng lệnh > biến môi trường > `application-{profile}.yml` > `application.yml`...; xác định **profile** đang bật.
3. **In banner**, rồi **tạo `ApplicationContext`** phù hợp (với web Servlet là `AnnotationConfigServletWebServerApplicationContext`).
4. **Nạp định nghĩa bean (bean definitions)**, chưa tạo object:
   - **Component scanning** từ package của class main: tìm `@Component`, `@Service`, `@Repository`, `@Controller`, `@Configuration`.
   - **Auto-configuration:** `@EnableAutoConfiguration` đọc danh sách class trong `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Boot 4 chia thành nhiều module nhỏ). Mỗi class chỉ được áp dụng khi **điều kiện** đúng: `@ConditionalOnClass` (có thư viện trên classpath), `@ConditionalOnMissingBean` (**bạn chưa tự khai báo bean đó**), `@ConditionalOnProperty`... Đây là lý do thêm `spring-boot-starter-data-jpa` là tự có `DataSource`, `EntityManagerFactory`, và vì sao bean bạn tự khai báo **ghi đè** được cấu hình mặc định.
5. **`refresh()` context**, phần nặng nhất:
   - Chạy `BeanFactoryPostProcessor` (xử lý `@Configuration`, thay placeholder `${...}`).
   - Đăng ký `BeanPostProcessor` (những thứ tạo **proxy** cho `@Transactional`, `@Async`, AOP, xử lý `@Autowired`).
   - **Tạo các singleton bean** (không lazy): khởi tạo, inject phụ thuộc, gọi `@PostConstruct` / `afterPropertiesSet`, áp proxy. Xem [Vòng đời bean](#spring-2).
   - **Khởi động web server nhúng** (Tomcat mặc định) ở bước `onRefresh`.
6. **Chạy `ApplicationRunner` và `CommandLineRunner`** (logic khởi động của bạn: warm cache, kiểm tra kết nối).
7. Phát sự kiện **`ApplicationReadyEvent`**; ứng dụng sẵn sàng. Actuator readiness chuyển sang `ACCEPTING_TRAFFIC`, nên Kubernetes bắt đầu gửi request.

**Các sự kiện theo thứ tự:** `ApplicationStartingEvent` → `ApplicationEnvironmentPreparedEvent` → `ApplicationContextInitializedEvent` → `ApplicationPreparedEvent` → `ContextRefreshedEvent` → `ApplicationStartedEvent` → `ApplicationReadyEvent` (lỗi thì `ApplicationFailedEvent`).

**Câu hỏi tiếp hay gặp:**
- **Xem auto-config nào được áp dụng hoặc bị bỏ qua:** chạy với `--debug` (in conditions evaluation report) hoặc endpoint actuator `/actuator/conditions`.
- **Tắt một auto-config:** `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)`.
- **Khởi động chậm, làm gì:** đo bằng `ApplicationStartup` (`BufferingApplicationStartup` + `/actuator/startup`); giảm phạm vi scan, lazy init có chọn lọc, không làm việc nặng trong `@PostConstruct`, CDS hoặc AOT cache, native image. Xem [Khởi động nhanh](#sn-startup).
- **Đặt logic khởi động ở đâu:** `ApplicationRunner` hoặc lắng nghe `ApplicationReadyEvent`, thay vì `@PostConstruct` (lúc đó context chưa sẵn sàng hoàn toàn, proxy như `@Transactional` có thể chưa áp dụng).
- **Fat jar chạy thế nào:** `java -jar` gọi `JarLauncher` của Spring Boot (khai báo trong `MANIFEST.MF`), nó nạp các jar thư viện nằm trong `BOOT-INF/lib` rồi gọi `main` của bạn.

### English

```java
@SpringBootApplication          // = @Configuration + @EnableAutoConfiguration + @ComponentScan
public class App { public static void main(String[] args) { SpringApplication.run(App.class, args); } }
```

**The main steps when `SpringApplication.run()` is called:**

1. **Create the `SpringApplication`:** infer the application type (Servlet, Reactive or non-web) from the libraries on the classpath; load the `ApplicationContextInitializer`s and `ApplicationListener`s declared in `META-INF/spring.factories` files.
2. **Prepare the `Environment`:** read configuration in priority order: command-line arguments > environment variables > `application-{profile}.yml` > `application.yml`...; determine the active **profiles**.
3. **Print the banner**, then **create the appropriate `ApplicationContext`** (for Servlet web apps, `AnnotationConfigServletWebServerApplicationContext`).
4. **Load bean definitions**, without creating objects yet:
   - **Component scanning** from the main class's package: find `@Component`, `@Service`, `@Repository`, `@Controller`, `@Configuration`.
   - **Auto-configuration:** `@EnableAutoConfiguration` reads the class list in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Boot 4 splits it into many small modules). Each class applies only when its **conditions** hold: `@ConditionalOnClass` (a library is on the classpath), `@ConditionalOnMissingBean` (**you haven't declared that bean yourself**), `@ConditionalOnProperty`... That's why adding `spring-boot-starter-data-jpa` gives you a `DataSource` and `EntityManagerFactory` automatically, and why beans you declare yourself **override** the defaults.
5. **`refresh()` the context**, the heaviest part:
   - Run `BeanFactoryPostProcessor`s (processing `@Configuration`, resolving `${...}` placeholders).
   - Register `BeanPostProcessor`s (the ones that create **proxies** for `@Transactional`, `@Async` and AOP, and process `@Autowired`).
   - **Create the singleton beans** (non-lazy): instantiate, inject dependencies, call `@PostConstruct` / `afterPropertiesSet`, apply proxies. See [Bean lifecycle](#spring-2).
   - **Start the embedded web server** (Tomcat by default) during `onRefresh`.
6. **Run `ApplicationRunner`s and `CommandLineRunner`s** (your startup logic: warming caches, checking connections).
7. Publish **`ApplicationReadyEvent`**; the application is ready. Actuator readiness switches to `ACCEPTING_TRAFFIC`, so Kubernetes starts sending requests.

**Events in order:** `ApplicationStartingEvent` → `ApplicationEnvironmentPreparedEvent` → `ApplicationContextInitializedEvent` → `ApplicationPreparedEvent` → `ContextRefreshedEvent` → `ApplicationStartedEvent` → `ApplicationReadyEvent` (or `ApplicationFailedEvent` on failure).

**Common follow-ups:**
- **See which auto-configurations applied or were skipped:** run with `--debug` (prints the conditions evaluation report) or use the `/actuator/conditions` endpoint.
- **Disable an auto-configuration:** `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)`.
- **Slow startup, what to do:** measure with `ApplicationStartup` (`BufferingApplicationStartup` + `/actuator/startup`); narrow scanning, selective lazy init, no heavy work in `@PostConstruct`, CDS or the AOT cache, native images. See [Fast startup](#sn-startup).
- **Where to put startup logic:** an `ApplicationRunner` or an `ApplicationReadyEvent` listener rather than `@PostConstruct` (at that point the context isn't fully ready, and proxies such as `@Transactional` may not be applied yet).
- **How a fat jar runs:** `java -jar` invokes Spring Boot's `JarLauncher` (declared in `MANIFEST.MF`), which loads the library jars from `BOOT-INF/lib` and then calls your `main`.

@@@ spring-3 | @Transactional hoạt động bên trong thế nào, và khi nào nó âm thầm không có tác dụng? / How does @Transactional work internally, and when does it silently fail? | spring | | override
### Tiếng Việt

**Cơ chế: AOP proxy.** Khi khởi động, một `BeanPostProcessor` thấy bean có `@Transactional` thì **bọc bean bằng proxy** (CGLIB tạo class con; hoặc JDK dynamic proxy nếu dùng interface). Các bean khác được inject **proxy**, không phải object gốc.

**Luồng một lời gọi:**
```
Caller → Proxy → TransactionInterceptor
            1. Đọc thuộc tính: propagation, isolation, readOnly, timeout, rollbackFor
            2. PlatformTransactionManager (JpaTransactionManager / DataSourceTransactionManager)
               .getTransaction(): lấy kết nối từ pool, setAutoCommit(false), gắn vào ThreadLocal
               (TransactionSynchronizationManager) để repository và JdbcTemplate trên CÙNG thread dùng chung kết nối
            3. Gọi method thật của bean
            4. Thành công → commit (Hibernate flush trước) · RuntimeException/Error → rollback · checked exception → VẪN commit
            5. Trả kết nối về pool, chạy callback afterCommit (ví dụ @TransactionalEventListener)
```

**Vì transaction gắn vào ThreadLocal**, nên code chạy ở **thread khác** (`@Async`, `CompletableFuture.supplyAsync`, `parallelStream`) **không** thuộc transaction đó.

**Các trường hợp âm thầm không có tác dụng:**

| Bẫy | Vì sao | Cách sửa |
|---|---|---|
| **Gọi nội bộ** `this.method()` | Lời gọi không đi qua proxy | Tách sang bean khác, hoặc inject chính mình (`@Lazy`) |
| Method **private** (hoặc `final`, `static`) | Proxy không override được | Để public; đặt ở lớp service |
| **Checked exception** | Mặc định chỉ rollback với unchecked | `rollbackFor = Exception.class` |
| **Bắt exception** bên trong rồi không ném lại | Proxy không thấy lỗi, nên commit | Ném lại, hoặc `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` |
| Gọi từ object tự `new` | Không phải Spring bean, không có proxy | Inject từ container |
| Chạy ở thread khác | Transaction gắn với thread | Mở transaction riêng ở thread đó |
| Bảng MySQL MyISAM | Engine không hỗ trợ transaction | Dùng InnoDB |
| Nhiều `TransactionManager` | Chọn sai manager | `@Transactional("ordersTxManager")` |

**Bẫy về hiệu năng và đúng đắn:**
- **Transaction quá dài:** gọi HTTP, gửi email hay gọi LLM bên trong transaction **giữ kết nối DB** suốt thời gian đó, dễ cạn pool. Gọi bên ngoài transaction, hoặc dùng outbox.
- **Gửi Kafka hay email trong transaction**, sau đó rollback, thì sự kiện vẫn đã đi. Dùng `@TransactionalEventListener(phase = AFTER_COMMIT)` hoặc [outbox](#microservices-4).
- **`readOnly = true`** cho method chỉ đọc: Hibernate bỏ dirty checking và flush, có thể định tuyến sang read replica.
- **Lazy loading ngoài transaction** gây `LazyInitializationException`; đừng dựa vào Open Session In View (`spring.jpa.open-in-view=false`), hãy fetch đủ dữ liệu trong transaction.
- Đặt `@Transactional` ở **tầng service** (ranh giới nghiệp vụ), không đặt ở controller hay repository rời rạc.

Xem thêm [Propagation và isolation](#spring-4).

**Câu trả lời mẫu:** *"Spring bọc bean bằng proxy; `TransactionInterceptor` lấy kết nối qua `PlatformTransactionManager`, gắn vào ThreadLocal, gọi method, rồi commit hoặc rollback. Vì dựa vào proxy và ThreadLocal nên nó không có tác dụng khi gọi nội bộ trong class, với method private, khi chạy ở thread khác, và mặc định không rollback với checked exception. Tôi cũng giữ transaction ngắn, không gọi service ngoài bên trong."*

### English

**The mechanism: an AOP proxy.** At startup, a `BeanPostProcessor` sees a bean with `@Transactional` and **wraps it in a proxy** (CGLIB generates a subclass, or a JDK dynamic proxy when using interfaces). Other beans get the **proxy** injected, not the original object.

**The flow of one call:**
```
Caller → Proxy → TransactionInterceptor
            1. Read the attributes: propagation, isolation, readOnly, timeout, rollbackFor
            2. PlatformTransactionManager (JpaTransactionManager / DataSourceTransactionManager)
               .getTransaction(): take a connection from the pool, setAutoCommit(false), bind it to a ThreadLocal
               (TransactionSynchronizationManager) so repositories and JdbcTemplate on the SAME thread share the connection
            3. Call the bean's real method
            4. Success → commit (Hibernate flushes first) · RuntimeException/Error → rollback · checked exception → STILL commits
            5. Return the connection to the pool and run afterCommit callbacks (e.g. @TransactionalEventListener)
```

**Because the transaction is bound to a ThreadLocal**, code running on **another thread** (`@Async`, `CompletableFuture.supplyAsync`, `parallelStream`) is **not** part of it.

**Cases where it silently does nothing:**

| Trap | Why | Fix |
|---|---|---|
| **Self-invocation** `this.method()` | The call doesn't go through the proxy | Move it to another bean, or inject yourself (`@Lazy`) |
| **Private** (or `final`, `static`) methods | The proxy can't override them | Make them public; put them in the service layer |
| **Checked exceptions** | By default only unchecked ones trigger rollback | `rollbackFor = Exception.class` |
| **Catching the exception** inside without rethrowing | The proxy never sees the error, so it commits | Rethrow, or call `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` |
| Calling an object you created with `new` | Not a Spring bean, no proxy | Inject it from the container |
| Running on another thread | The transaction is bound to the thread | Open a separate transaction on that thread |
| MySQL MyISAM tables | The engine doesn't support transactions | Use InnoDB |
| Several `TransactionManager`s | The wrong manager is used | `@Transactional("ordersTxManager")` |

**Performance and correctness traps:**
- **Long transactions:** making HTTP calls, sending emails or calling an LLM inside a transaction **holds a DB connection** the whole time and can exhaust the pool. Call outside the transaction, or use an outbox.
- **Sending to Kafka or email inside a transaction** that later rolls back means the event already went out. Use `@TransactionalEventListener(phase = AFTER_COMMIT)` or the [outbox](#microservices-4).
- **`readOnly = true`** for read-only methods: Hibernate skips dirty checking and flushing, and routing to a read replica becomes possible.
- **Lazy loading outside the transaction** causes `LazyInitializationException`; don't rely on Open Session In View (`spring.jpa.open-in-view=false`); fetch what you need inside the transaction.
- Put `@Transactional` on the **service layer** (the business boundary), not scattered on controllers or repositories.

See also [Propagation and isolation](#spring-4).

**A model answer:** *"Spring wraps the bean in a proxy; the `TransactionInterceptor` obtains a connection via the `PlatformTransactionManager`, binds it to a ThreadLocal, calls the method, then commits or rolls back. Because it relies on proxies and ThreadLocals, it does nothing for self-invocation, private methods or other threads, and by default it doesn't roll back on checked exceptions. I also keep transactions short and never call external services inside them."*

@@@ db-query-optimization | Tối ưu một câu SQL chậm thế nào? (index, bỏ SELECT *, EXPLAIN, slow query log, phi chuẩn hóa) / How do you optimize a slow SQL query? (indexes, dropping SELECT *, EXPLAIN, slow query logs, denormalization) | data | sql,performance,index,goldman-sachs | qa | SQL
### Tiếng Việt

**Quy trình: tìm, đo, sửa, đo lại.**

**1. Tìm query chậm (đừng đoán):**
- **PostgreSQL:** extension `pg_stat_statements` (xếp theo tổng thời gian, không chỉ thời gian mỗi lần: query 5 ms chạy 1 triệu lần còn tệ hơn query 2 giây chạy 10 lần); `log_min_duration_statement = 500ms` để ghi log query chậm.
- **MySQL:** `slow_query_log` + `long_query_time`, công cụ `pt-query-digest` để gom nhóm.
- APM hoặc tracing (span SQL dài), Hibernate statistics (đếm số query mỗi request để phát hiện N+1).

**2. Đọc execution plan:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, o.total, c.name
FROM orders o JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'PAID' AND o.created_at >= now() - interval '7 days'
ORDER BY o.created_at DESC LIMIT 50;
```
Tìm: **`Seq Scan`** trên bảng lớn; số dòng **ước lượng lệch xa** số dòng thật (thống kê cũ, chạy `ANALYZE`); `Sort` tốn bộ nhớ hoặc tràn ra đĩa; `Nested Loop` với số vòng rất lớn; `Rows Removed by Filter` cao. `EXPLAIN ANALYZE` **chạy thật câu lệnh**, nên cẩn thận với `UPDATE`/`DELETE` (bọc trong transaction rồi rollback).

**3. Các cách sửa, theo thứ tự hay dùng:**

| Cách | Chi tiết |
|---|---|
| **Index cột trong WHERE, JOIN, ORDER BY** | Composite index theo thứ tự: cột lọc **bằng** trước, cột **khoảng hoặc sắp xếp** sau: `(status, created_at DESC)`. Index khóa ngoại dùng để JOIN (`orders.customer_id`); PostgreSQL **không tự tạo** index cho khóa ngoại |
| **Covering index** | `INCLUDE (total)` để trả kết quả chỉ từ index (index-only scan), không phải đọc bảng |
| **Partial index** | `WHERE status = 'PENDING'` khi chỉ truy vấn một phần nhỏ dữ liệu |
| **Bỏ `SELECT *`** | Chỉ lấy cột cần: ít I/O và dữ liệu qua mạng, cho phép index-only scan, không vỡ khi bảng thêm cột; trong JPA dùng **projection** (DTO hoặc record) |
| **Viết điều kiện "sargable"** | Không bọc cột trong hàm: `WHERE DATE(created_at) = ...` không dùng được index, nên viết `created_at >= :d AND created_at < :d + 1`; tránh `LIKE '%abc'`, ép kiểu ngầm, `OR` trên nhiều cột (thử `UNION`) |
| **Phân trang theo keyset** | `WHERE (created_at, id) < (:lastCreated, :lastId) ORDER BY ... LIMIT 50` thay vì `OFFSET 100000` (phải đọc và bỏ 100.000 dòng) |
| **Sửa N+1** | `JOIN FETCH`, `@EntityGraph`, batch fetching. Xem [N+1](#jpa-16) |
| **Thao tác theo lô** | Batch insert/update, tránh gọi query trong vòng lặp |
| **Cập nhật thống kê** | `ANALYZE`; `VACUUM` với bảng bị update/delete nhiều (PostgreSQL) |
| **Phi chuẩn hóa** | Lưu sẵn cột tính toán (`order_total`, `comment_count`), bảng tổng hợp, **materialized view** cho báo cáo; đổi lại việc ghi phức tạp hơn. Xem [Chuẩn hóa](#sql-normalization) |
| **Partitioning** | Bảng rất lớn theo thời gian: partition theo tháng để query chỉ quét partition liên quan, xóa dữ liệu cũ bằng drop partition |
| **Cache, read replica** | Khi query đã tối ưu mà tải đọc vẫn cao |

**4. Cái giá của index:** mỗi index làm **ghi chậm hơn** (insert/update phải cập nhật index) và tốn dung lượng. Xóa index không dùng (`pg_stat_user_indexes` với `idx_scan = 0`). Tạo index trên bảng production dùng `CREATE INDEX CONCURRENTLY` để không khóa bảng.

**5. Đo lại** với dữ liệu và tải giống production; ghi lại kết quả trước và sau.

**Câu chuyện mẫu:** *"API danh sách đơn chậm 2,5 giây. `pg_stat_statements` cho thấy query lọc theo `status` và `created_at` quét toàn bảng 30 triệu dòng. Tôi thêm composite index `(status, created_at DESC) INCLUDE (total)`, đổi `SELECT *` sang projection, và chuyển `OFFSET` sang keyset pagination. Query còn khoảng 15 ms, CPU database giảm rõ."*

### English

**The process: find, measure, fix, measure again.**

**1. Find the slow queries (don't guess):**
- **PostgreSQL:** the `pg_stat_statements` extension (sort by total time, not just per-call time: a 5 ms query run a million times is worse than a 2-second query run 10 times); `log_min_duration_statement = 500ms` to log slow queries.
- **MySQL:** `slow_query_log` + `long_query_time`, and `pt-query-digest` to group them.
- APM or tracing (long SQL spans), Hibernate statistics (counting queries per request to spot N+1).

**2. Read the execution plan:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, o.total, c.name
FROM orders o JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'PAID' AND o.created_at >= now() - interval '7 days'
ORDER BY o.created_at DESC LIMIT 50;
```
Look for: a **`Seq Scan`** on a large table; **estimated rows far from actual rows** (stale statistics, run `ANALYZE`); a `Sort` that uses lots of memory or spills to disk; a `Nested Loop` with a huge number of iterations; a high `Rows Removed by Filter`. `EXPLAIN ANALYZE` **actually runs the statement**, so be careful with `UPDATE`/`DELETE` (wrap them in a transaction and roll back).

**3. Fixes, roughly in order of use:**

| Fix | Details |
|---|---|
| **Index WHERE, JOIN and ORDER BY columns** | Composite indexes ordered with **equality** columns first and **range or sort** columns after: `(status, created_at DESC)`. Index foreign keys used in JOINs (`orders.customer_id`); PostgreSQL **doesn't create** foreign-key indexes automatically |
| **Covering indexes** | `INCLUDE (total)` so results come from the index alone (an index-only scan) without reading the table |
| **Partial indexes** | `WHERE status = 'PENDING'` when you only query a small slice of the data |
| **Drop `SELECT *`** | Fetch only the needed columns: less I/O and network data, index-only scans become possible, and nothing breaks when columns are added; in JPA use **projections** (DTOs or records) |
| **Write "sargable" conditions** | Don't wrap columns in functions: `WHERE DATE(created_at) = ...` can't use the index, so write `created_at >= :d AND created_at < :d + 1`; avoid `LIKE '%abc'`, implicit casts, and `OR` across columns (try `UNION`) |
| **Keyset pagination** | `WHERE (created_at, id) < (:lastCreated, :lastId) ORDER BY ... LIMIT 50` instead of `OFFSET 100000` (which reads and discards 100,000 rows) |
| **Fix N+1** | `JOIN FETCH`, `@EntityGraph`, batch fetching. See [N+1](#jpa-16) |
| **Batch operations** | Batch inserts/updates; avoid queries inside loops |
| **Refresh statistics** | `ANALYZE`; `VACUUM` for heavily updated or deleted tables (PostgreSQL) |
| **Denormalization** | Precomputed columns (`order_total`, `comment_count`), summary tables, **materialized views** for reports; in exchange writes get more complex. See [Normalization](#sql-normalization) |
| **Partitioning** | Very large time-based tables: partition by month so queries scan only relevant partitions, and drop partitions to delete old data |
| **Caching, read replicas** | When the query is already optimized but read load is still high |

**4. The cost of indexes:** every index **slows writes** (inserts and updates must maintain it) and takes space. Drop unused indexes (`pg_stat_user_indexes` with `idx_scan = 0`). On production tables, use `CREATE INDEX CONCURRENTLY` to avoid locking the table.

**5. Measure again** with production-like data and load, and record the before and after.

**A sample story:** *"The order-list API took 2.5 seconds. `pg_stat_statements` showed the query filtering on `status` and `created_at` scanning all 30 million rows. I added a composite index `(status, created_at DESC) INCLUDE (total)`, replaced `SELECT *` with a projection, and moved from `OFFSET` to keyset pagination. The query dropped to about 15 ms and database CPU fell noticeably."*

@@@ sec-token-lifecycle | OAuth và JWT khác nhau thế nào? Token hết hạn ra sao, thu hồi JWT được không, refresh token hoạt động thế nào? / OAuth vs JWT, how token expiry works, whether JWTs can be revoked, and how refresh tokens work? | security | oauth,jwt,refresh-token,api-gateway,goldman-sachs | qa | Auth & token
### Tiếng Việt

**OAuth và JWT không cùng loại nên không thay thế nhau:**
- **OAuth 2.0** là **giao thức ủy quyền**: quy định cách một ứng dụng **xin và nhận** quyền truy cập (access token) thay mặt user, qua các flow như Authorization Code + PKCE, Client Credentials. **OpenID Connect (OIDC)** xây trên OAuth để thêm **xác thực** (ID token cho biết user là ai).
- **JWT** là **định dạng token**: `header.payload.signature`, chứa claims (`sub`, `exp`, `iss`, `aud`, `scope`) và chữ ký. OAuth **có thể** dùng JWT làm access token, hoặc dùng token "mờ" (opaque) phải hỏi lại server.

| | JWT (tự chứa thông tin) | Opaque token |
|---|---|---|
| Kiểm tra | **Tại chỗ**: kiểm tra chữ ký bằng public key (JWKS) và `exp` | Gọi **introspection** tới authorization server (hoặc tra cache hay DB) |
| Hiệu năng | Không cần gọi mạng | Thêm một lời gọi mỗi request (thường có cache) |
| Thu hồi | **Khó** | **Dễ**: xóa ở server |
| Nội dung | Ai cũng đọc được payload (chỉ mã hóa base64url, **không** phải encryption) | Không lộ thông tin |

**Token hết hạn thế nào:** JWT có claim **`exp`** (thời điểm hết hạn, Unix time). Mỗi service hoặc gateway kiểm tra `exp` khi verify (cho phép **lệch đồng hồ** vài chục giây). Hết hạn thì trả **401**, client dùng refresh token lấy token mới. Không có lời gọi server nào "làm token hết hạn": nó hết hạn vì thời gian.

**Có thu hồi JWT được không?** Bản chất JWT **stateless**, nên server không thể "xóa" một token đã phát. Các cách:
1. **Access token sống ngắn** (5–15 phút): bị lộ thì thiệt hại giới hạn. **Đây là cách chính.**
2. **Thu hồi refresh token** ở server: user không lấy được access token mới, nên tối đa vài phút sau là mất quyền.
3. **Danh sách chặn (denylist)** theo `jti` (id của token) trong Redis, TTL bằng thời gian sống còn lại của token: thu hồi tức thì nhưng **thêm trạng thái** và một lần tra Redis mỗi request.
4. **Token version / thời điểm "không hợp lệ trước"** theo user: lưu `tokens_valid_after` trong DB hoặc cache; token có `iat` cũ hơn bị từ chối (dùng khi đổi mật khẩu, "đăng xuất mọi thiết bị").
5. **Đổi khóa ký**: vô hiệu hóa **mọi** token; dùng khi lộ khóa.

**Refresh token flow:**
```
1. Đăng nhập (Authorization Code + PKCE) → nhận access token (15 phút) + refresh token (vài ngày, lưu ở server)
2. Gọi API với access token
3. API trả 401 (hết hạn) → client gửi refresh token tới /token (grant_type=refresh_token)
4. Server kiểm tra refresh token còn hợp lệ, chưa bị thu hồi → phát access token MỚI + refresh token MỚI
5. Refresh token cũ bị vô hiệu ngay (ROTATION)
```
- **Refresh token rotation + phát hiện dùng lại:** nếu một refresh token **đã dùng** lại được gửi lên, nghĩa là có thể đã bị đánh cắp, nên thu hồi **cả chuỗi token** đó và buộc đăng nhập lại.
- Lưu ở đâu: web nên để refresh token trong **cookie `HttpOnly`, `Secure`, `SameSite`** (JavaScript không đọc được, chống XSS) hoặc dùng mẫu **BFF** (backend giữ token, trình duyệt chỉ có session cookie); mobile dùng **Keychain / Keystore**. **Không** để trong `localStorage`.
- Refresh token là chuỗi ngẫu nhiên mờ, **lưu dạng hash** trong DB, gắn với user, thiết bị, hạn dùng.

**Xác thực ở API gateway:**
- Gateway kiểm tra JWT (chữ ký qua JWKS có cache, `exp`, `iss`, `aud`), rate limit, rồi chuyển request kèm thông tin user (header như `X-User-Id`, hoặc chuyển tiếp token). Ở Opswat là mô hình **forward auth**.
- **Service phía sau vẫn phải kiểm tra quyền** trên tài nguyên (user chỉ được xem tài khoản của mình), và chỉ tin header từ gateway khi mạng nội bộ được bảo vệ (mTLS, network policy). Nếu không, ai gọi thẳng vào service cũng giả được header.
- Gọi giữa các service: dùng **Client Credentials** hoặc token exchange, mỗi service một danh tính và scope tối thiểu.

**Câu trả lời mẫu:** *"OAuth là giao thức để cấp quyền, JWT là một định dạng token. Tôi dùng JWT access token sống ngắn, khoảng 15 phút, để service kiểm tra tại chỗ, kèm refresh token lưu ở server, có rotation và phát hiện dùng lại. JWT không thu hồi tức thì được, nên tôi dựa vào TTL ngắn và thu hồi refresh token; khi thật sự cần chặn ngay, ví dụ tài khoản bị xâm phạm, thì dùng denylist theo `jti` hoặc token version trong Redis."*

### English

**OAuth and JWT aren't the same kind of thing, so they don't replace each other:**
- **OAuth 2.0** is an **authorization protocol**: it defines how an application **requests and receives** access (an access token) on a user's behalf, through flows such as Authorization Code + PKCE and Client Credentials. **OpenID Connect (OIDC)** builds on OAuth to add **authentication** (an ID token saying who the user is).
- **JWT** is a **token format**: `header.payload.signature`, holding claims (`sub`, `exp`, `iss`, `aud`, `scope`) and a signature. OAuth **can** use JWTs as access tokens, or use "opaque" tokens that must be checked with the server.

| | JWT (self-contained) | Opaque token |
|---|---|---|
| Validation | **Locally**: verify the signature with a public key (JWKS) and check `exp` | Call **introspection** on the authorization server (or look it up in a cache or DB) |
| Performance | No network call | One extra call per request (usually cached) |
| Revocation | **Hard** | **Easy**: delete it on the server |
| Contents | Anyone can read the payload (only base64url-encoded, **not** encrypted) | Reveals nothing |

**How token expiry works:** a JWT has an **`exp`** claim (the expiry time in Unix time). Each service or the gateway checks `exp` when verifying (allowing a few tens of seconds of **clock skew**). Once expired it returns **401**, and the client uses the refresh token to get a new one. No server call "expires" the token: time does.

**Can JWTs be revoked?** JWTs are **stateless** by nature, so the server can't "delete" an issued token. The options:
1. **Short-lived access tokens** (5–15 minutes): a leaked token does limited damage. **This is the main approach.**
2. **Revoke the refresh token** on the server: the user can't get new access tokens, so access ends within minutes at most.
3. **A denylist** by `jti` (the token id) in Redis, with a TTL equal to the token's remaining lifetime: immediate revocation, but it **adds state** and a Redis lookup per request.
4. **A per-user token version / "not valid before" time:** store `tokens_valid_after` in the DB or cache; tokens with an older `iat` are rejected (for password changes and "log out of all devices").
5. **Rotate the signing key**: invalidates **every** token; used when the key leaks.

**The refresh token flow:**
```
1. Log in (Authorization Code + PKCE) → receive an access token (15 minutes) + a refresh token (days, stored server-side)
2. Call APIs with the access token
3. An API returns 401 (expired) → the client sends the refresh token to /token (grant_type=refresh_token)
4. The server checks the refresh token is valid and not revoked → issues a NEW access token + a NEW refresh token
5. The old refresh token is invalidated immediately (ROTATION)
```
- **Refresh token rotation + reuse detection:** if an **already used** refresh token shows up again, it may have been stolen, so revoke **the whole token family** and force a new login.
- Where to store it: on the web, keep the refresh token in an **`HttpOnly`, `Secure`, `SameSite` cookie** (JavaScript can't read it, protecting against XSS) or use the **BFF** pattern (the backend holds the tokens and the browser only gets a session cookie); on mobile use the **Keychain / Keystore**. **Never** in `localStorage`.
- A refresh token is a random opaque string, **stored hashed** in the DB, tied to a user, a device and an expiry.

**Authentication at the API gateway:**
- The gateway verifies the JWT (signature via a cached JWKS, `exp`, `iss`, `aud`), rate limits, then forwards the request with user info (headers such as `X-User-Id`, or the token itself). At Opswat this was the **forward auth** model.
- **Downstream services must still check authorization** on resources (users may only see their own accounts), and should trust gateway headers only when the internal network is protected (mTLS, network policies). Otherwise anyone calling a service directly could forge the headers.
- Service-to-service calls: use **Client Credentials** or token exchange, with one identity per service and minimal scopes.

**A model answer:** *"OAuth is the protocol for granting access; JWT is a token format. I use short-lived JWT access tokens, around 15 minutes, so services can validate them locally, plus server-stored refresh tokens with rotation and reuse detection. JWTs can't be revoked instantly, so I rely on short TTLs and refresh-token revocation; when I really need to block immediately, say for a compromised account, I use a `jti` denylist or a token version in Redis."*

@@@ hr-culture-fit | Câu hỏi culture fit: áp lực và deadline, làm việc với team toàn cầu, định hướng phát triển. / Culture-fit questions: pressure and deadlines, working with global teams, career growth plans. | hr | hr,behavioral,culture-fit,goldman-sachs | qa | HR screening
### Tiếng Việt

**1. "Bạn xử lý áp lực và deadline thế nào?"**

Interviewer muốn thấy bạn **có hệ thống** (ưu tiên, chia nhỏ, báo sớm), không phải "tôi làm thêm giờ".

- **Khung:** làm rõ điều gì thật sự quan trọng → chia nhỏ việc, ước lượng → **báo rủi ro sớm** cho stakeholder kèm các lựa chọn (giảm phạm vi, thêm người, lùi hạn) → tập trung vào phần có giá trị nhất → giữ chất lượng ở những chỗ không được thỏa hiệp (test, bảo mật) → rút kinh nghiệm.
- **Mẫu:** *"Ở [DXC], khách hàng [bảo hiểm] cần tính năng [X] trước đợt kiểm tra compliance, còn 2 tuần trong khi ước lượng là 3 tuần. Tôi chia thành phần bắt buộc cho kỳ kiểm tra và phần có thể làm sau, trao đổi với PM ngay trong ngày thứ hai, và thống nhất giao phần bắt buộc đúng hạn. Tôi tự động hóa phần test hồi quy để không phải test tay mỗi lần thay đổi. Chúng tôi giao đúng hạn, phần còn lại xong trong sprint tiếp theo. Bài học của tôi là báo rủi ro càng sớm thì càng có nhiều lựa chọn."*
- Xem thêm [Deadline có nguy cơ trễ](#behavioral-6).

**2. "Bạn có kinh nghiệm làm việc với team toàn cầu không?"**

- Nói **cụ thể**: làm với khách hàng hoặc đồng nghiệp ở đâu (DXC: khách hàng bảo hiểm Shinhan Life, MetLife; Opswat: công ty Mỹ, team nhiều nước), lệch múi giờ bao nhiêu, công cụ (Jira, Confluence, Slack, Teams).
- **Thói quen làm việc tốt:**
  - Giao tiếp **bất đồng bộ** rõ ràng: viết ticket, PR description, tài liệu thiết kế đầy đủ để người ở múi giờ khác làm tiếp được mà không phải chờ hỏi.
  - Tận dụng **giờ trùng nhau** cho việc cần thảo luận trực tiếp; chuẩn bị agenda trước, gửi tóm tắt sau họp.
  - **Xác nhận lại** yêu cầu bằng văn bản để tránh hiểu lầm về ngôn ngữ và văn hóa; hỏi lại khi chưa chắc.
  - Tôn trọng khác biệt văn hóa trong cách góp ý: thẳng thắn hay tế nhị.
- **Mẫu:** *"Ở [Opswat], team tôi phối hợp với [đồng nghiệp ở Mỹ], lệch khoảng 12–14 giờ. Tôi viết PR và tài liệu đủ chi tiết để họ review trong ngày của họ, và dùng khoảng giờ trùng buổi sáng cho các buổi thảo luận thiết kế. Nhờ vậy một vòng review gần như không bị mất thêm một ngày."*

**3. "Định hướng phát triển của bạn là gì?" / "5 năm nữa bạn ở đâu?"**

- Cho thấy **tham vọng hợp lý, gắn với vị trí đang ứng tuyển**; tránh "muốn làm manager ngay" hay "chưa nghĩ tới".
- **Khung:** ngắn hạn (1–2 năm): làm chủ hệ thống và domain, đóng góp tốt ở mức senior → trung hạn (3–5 năm): **senior/staff engineer** dẫn dắt thiết kế kỹ thuật, mentoring, hoặc tech lead → luôn học: ví dụ domain tài chính, hệ thống phân tán, AI trong backend.
- **Mẫu:** *"Trong 1–2 năm tới, tôi muốn hiểu sâu domain [giao dịch / thanh toán] và hệ thống của team, và trở thành người team tin tưởng giao những phần quan trọng. Dài hơn, tôi muốn đi theo hướng kỹ thuật: dẫn dắt thiết kế hệ thống, review kiến trúc, mentoring kỹ sư trẻ. Tôi chọn [công ty] vì ở đây có hệ thống quy mô lớn, yêu cầu tính đúng cao, đúng thứ tôi muốn học."*

**4. "Why Goldman Sachs?" (hoặc ngân hàng / công ty tài chính nói chung)**
- Kết nối 3 điểm: **công ty** (hệ thống tài chính quy mô lớn, yêu cầu tính đúng đắn, độ trễ thấp và bảo mật cao), **vị trí** (khớp với kỹ năng Java, Spring, concurrency, database), **bản thân** (kinh nghiệm hệ thống bảo hiểm có dữ liệu nhạy cảm ở DXC, bảo mật ở Opswat; muốn học domain tài chính).
- Tìm hiểu trước: mảng mà team làm (trading, risk, payments, Marcus...), sản phẩm hoặc dự án mã nguồn mở của họ (ví dụ thư viện Eclipse Collections do Goldman Sachs khởi xướng). Xem [Vì sao muốn vào công ty này](#hr-screening-3).

### English

**1. "How do you handle pressure and deadlines?"**

The interviewer wants to see you're **systematic** (prioritizing, breaking work down, flagging early), not "I work overtime".

- **Framework:** clarify what truly matters → break the work down and estimate → **flag risk early** to stakeholders with options (cut scope, add people, move the date) → focus on the most valuable part → keep quality where it can't be compromised (tests, security) → learn from it.
- **Sample:** *"At [DXC], an [insurance] client needed feature [X] before a compliance audit; we had 2 weeks against a 3-week estimate. I split it into what the audit required and what could wait, raised it with the PM on day two, and we agreed to deliver the required part on time. I automated the regression tests so we didn't have to test by hand after every change. We delivered on time and finished the rest the next sprint. My lesson: the earlier you flag a risk, the more options you have."*
- See also [A deadline at risk](#behavioral-6).

**2. "Do you have experience working with global teams?"**

- Be **specific**: who you worked with and where (DXC: insurance clients such as Shinhan Life and MetLife; Opswat: a US company with a multinational team), the time-zone gap, the tools (Jira, Confluence, Slack, Teams).
- **Good working habits:**
  - Clear **asynchronous** communication: complete tickets, PR descriptions and design docs so someone in another time zone can continue without waiting to ask.
  - Use the **overlapping hours** for things that need live discussion; send an agenda before and a summary after.
  - **Confirm requirements in writing** to avoid language and cultural misunderstandings; ask when unsure.
  - Respect cultural differences in giving feedback: direct or indirect.
- **Sample:** *"At [Opswat], my team worked with [colleagues in the US], about 12–14 hours apart. I wrote PRs and docs detailed enough for them to review during their day, and used the overlapping morning hours for design discussions. That way a review round rarely cost us an extra day."*

**3. "What are your career growth plans?" / "Where do you see yourself in 5 years?"**

- Show **reasonable ambition tied to the role you're applying for**; avoid "I want to be a manager right away" or "I haven't thought about it".
- **Framework:** short term (1–2 years): master the system and domain and contribute strongly at senior level → medium term (3–5 years): a **senior/staff engineer** leading technical design and mentoring, or a tech lead → always learning: for example the financial domain, distributed systems, AI in backends.
- **Sample:** *"Over the next 1–2 years I want to understand the [trading / payments] domain and the team's systems deeply, and become someone the team trusts with critical parts. Longer term I want to grow on the technical track: leading system design, reviewing architecture, mentoring junior engineers. I chose [company] because it has large-scale systems with high correctness requirements, exactly what I want to learn."*

**4. "Why Goldman Sachs?" (or a bank / financial firm in general)**
- Connect three points: **the company** (large-scale financial systems demanding correctness, low latency and strong security), **the role** (matching your Java, Spring, concurrency and database skills), **you** (experience with sensitive-data insurance systems at DXC and security at Opswat; wanting to learn the financial domain).
- Research beforehand: the team's area (trading, risk, payments, Marcus...), and their products or open-source work (for example Eclipse Collections, a library Goldman Sachs originated). See [Why do you want to join our company](#hr-screening-3).
