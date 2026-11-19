@@@ sql-joins | Các loại JOIN trong SQL khác nhau thế nào? / What are the types of SQL JOIN and how do they differ? | data | sql,join | qa | SQL
### Tiếng Việt

Giả sử có bảng `customers(id, name)` và `orders(id, customer_id, amount)`.

| JOIN | Trả về | Ví dụ dùng |
|---|---|---|
| **INNER JOIN** | Chỉ các dòng **khớp ở cả hai bảng** | Đơn hàng kèm tên khách |
| **LEFT JOIN** | **Mọi dòng bảng trái**, bảng phải không khớp thì là `NULL` | Mọi khách hàng, kể cả chưa có đơn |
| **RIGHT JOIN** | Ngược lại của LEFT | Hiếm dùng, thường viết lại thành LEFT |
| **FULL OUTER JOIN** | Mọi dòng của cả hai bảng | Đối soát hai nguồn dữ liệu. **MySQL không hỗ trợ**: dùng LEFT JOIN UNION RIGHT JOIN |
| **CROSS JOIN** | Tích Descartes: mọi tổ hợp | Sinh lịch (mọi ngày × mọi nhân viên) |
| **SELF JOIN** | Bảng join với chính nó | Nhân viên và quản lý trong cùng bảng `employees` |

```sql
-- Khách chưa từng đặt hàng (anti-join), cách 1:
SELECT c.* FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;

-- Cách 2, thường rõ nghĩa hơn:
SELECT c.* FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

**Bẫy hay gặp:** điều kiện trên bảng phải đặt ở `WHERE` sẽ **biến LEFT JOIN thành INNER JOIN**:

```sql
-- SAI: khách không có đơn bị loại, vì o.amount là NULL
SELECT c.name, o.amount FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.amount > 100;

-- ĐÚNG: đưa điều kiện vào ON
SELECT c.name, o.amount FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.amount > 100;
```

**Hiệu năng:** database chọn thuật toán join (nested loop, hash join, merge join) theo kích thước bảng và index. Cột dùng để join (`orders.customer_id`) nên có **index**. Kiểm tra bằng `EXPLAIN`.

### English

Assume tables `customers(id, name)` and `orders(id, customer_id, amount)`.

| JOIN | Returns | Example use |
|---|---|---|
| **INNER JOIN** | Only rows that **match in both tables** | Orders with the customer's name |
| **LEFT JOIN** | **Every row of the left table**, `NULL` where the right side doesn't match | Every customer, including those without orders |
| **RIGHT JOIN** | The mirror of LEFT | Rarely used, usually rewritten as LEFT |
| **FULL OUTER JOIN** | Every row of both tables | Reconciling two data sources. **MySQL doesn't support it**: use LEFT JOIN UNION RIGHT JOIN |
| **CROSS JOIN** | Cartesian product: every combination | Generating a schedule (every day × every employee) |
| **SELF JOIN** | A table joined with itself | Employees and their managers in one `employees` table |

```sql
-- Customers who never ordered (an anti-join), option 1:
SELECT c.* FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;

-- Option 2, often clearer:
SELECT c.* FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

**A common trap:** a condition on the right-hand table placed in `WHERE` **turns a LEFT JOIN into an INNER JOIN**:

```sql
-- WRONG: customers without orders are dropped, because o.amount is NULL
SELECT c.name, o.amount FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.amount > 100;

-- RIGHT: move the condition into ON
SELECT c.name, o.amount FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.amount > 100;
```

**Performance:** the database picks a join algorithm (nested loop, hash join, merge join) based on table sizes and indexes. Join columns (`orders.customer_id`) should be **indexed**. Check with `EXPLAIN`.

@@@ sql-normalization | Chuẩn hóa dữ liệu (1NF, 2NF, 3NF) là gì? Khi nào nên phi chuẩn hóa? / What is normalization (1NF, 2NF, 3NF), and when should you denormalize? | data | sql,database-design | qa | SQL
### Tiếng Việt

**Mục tiêu của chuẩn hóa:** mỗi thông tin chỉ lưu **một chỗ**, để tránh dư thừa và tránh dữ liệu mâu thuẫn khi cập nhật.

| Dạng | Quy tắc | Vi phạm ví dụ | Sửa |
|---|---|---|---|
| **1NF** | Mỗi ô chứa **giá trị đơn**, không có nhóm lặp | Cột `phones = "090..., 091..."` | Tách bảng `customer_phones` |
| **2NF** | 1NF, và mọi cột phụ thuộc vào **toàn bộ** khóa chính (với khóa ghép) | `order_items(order_id, product_id, product_name)`: `product_name` chỉ phụ thuộc `product_id` | Đưa `product_name` sang bảng `products` |
| **3NF** | 2NF, và **không phụ thuộc bắc cầu** (cột không khóa phụ thuộc cột không khóa khác) | `employees(id, dept_id, dept_name)`: `dept_name` phụ thuộc `dept_id` | Tách bảng `departments` |
| BCNF | Mọi phụ thuộc hàm đều có vế trái là khóa ứng viên | Hiếm gặp khi phỏng vấn | |

Thực tế hầu hết thiết kế OLTP dừng ở **3NF**.

**Phi chuẩn hóa (denormalization):** cố ý lưu trùng dữ liệu để **đọc nhanh hơn**, đổi lại việc ghi phức tạp hơn.

Ví dụ hợp lý:
- Lưu `total_amount` trong `orders` thay vì cộng `order_items` mỗi lần đọc.
- Lưu **giá tại thời điểm mua** (`unit_price`) trong `order_items`. Đây thực ra là dữ liệu lịch sử, không phải trùng lặp: giá sản phẩm sau này đổi thì đơn cũ vẫn phải giữ giá cũ.
- Bảng báo cáo hoặc read model (CQRS), materialized view, document trong NoSQL.

**Cách giữ dữ liệu phi chuẩn hóa đúng:** cập nhật trong cùng transaction, dùng trigger, hoặc cập nhật bất đồng bộ qua sự kiện (chấp nhận eventual consistency).

**Câu trả lời mẫu:** *"Tôi thiết kế ở 3NF cho dữ liệu giao dịch, rồi phi chuẩn hóa có chủ đích ở chỗ đã đo được truy vấn đọc là điểm nghẽn."*

### English

**The goal of normalization:** store each fact in **one place**, to avoid redundancy and inconsistent data on updates.

| Form | Rule | Violation example | Fix |
|---|---|---|---|
| **1NF** | Each cell holds a **single value**, no repeating groups | A column `phones = "090..., 091..."` | Split into a `customer_phones` table |
| **2NF** | 1NF, and every column depends on the **whole** primary key (for composite keys) | `order_items(order_id, product_id, product_name)`: `product_name` depends only on `product_id` | Move `product_name` to a `products` table |
| **3NF** | 2NF, and **no transitive dependencies** (a non-key column depending on another non-key column) | `employees(id, dept_id, dept_name)`: `dept_name` depends on `dept_id` | Split out a `departments` table |
| BCNF | Every functional dependency's left side is a candidate key | Rare in interviews | |

In practice most OLTP designs stop at **3NF**.

**Denormalization:** deliberately storing duplicate data to **read faster**, at the cost of more complex writes.

Reasonable examples:
- Storing `total_amount` on `orders` instead of summing `order_items` on every read.
- Storing the **price at purchase time** (`unit_price`) in `order_items`. That's really historical data, not duplication: if the product price changes later, old orders must keep the old price.
- Reporting tables or read models (CQRS), materialized views, documents in NoSQL.

**How to keep denormalized data correct:** update it in the same transaction, use triggers, or update it asynchronously through events (accepting eventual consistency).

**A model answer:** *"I design transactional data in 3NF, then denormalize deliberately where I've measured that read queries are the bottleneck."*

@@@ sql-window | Window function là gì? Cho ví dụ ROW_NUMBER, RANK, LAG, tổng lũy kế. / What are window functions? Give examples of ROW_NUMBER, RANK, LAG and running totals. | data | sql,window-function | qa | SQL
### Tiếng Việt

**Window function** tính toán trên một "cửa sổ" các dòng liên quan, nhưng **không gộp dòng** như `GROUP BY`: mỗi dòng vẫn giữ nguyên và có thêm một cột kết quả.

Cú pháp: `hàm() OVER (PARTITION BY ... ORDER BY ... [khung])`
- `PARTITION BY`: chia nhóm (giống GROUP BY nhưng không gộp).
- `ORDER BY`: thứ tự trong mỗi nhóm.

**Xếp hạng, với bảng lương mẫu 100, 90, 90, 80:**

| Hàm | Kết quả | Đặc điểm |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 | Luôn khác nhau, bằng nhau thì thứ tự tùy ý |
| `RANK()` | 1, 2, 2, **4** | Bằng nhau cùng hạng, **bỏ số** sau đó |
| `DENSE_RANK()` | 1, 2, 2, **3** | Bằng nhau cùng hạng, **không bỏ số** |

```sql
-- Top 3 lương mỗi phòng ban
SELECT * FROM (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees e
) t WHERE rnk <= 3;

-- Đơn hàng mới nhất của mỗi khách (lấy đúng 1 dòng)
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders o
) t WHERE rn = 1;

-- So với tháng trước: LAG lấy giá trị dòng trước, LEAD lấy dòng sau
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM monthly_revenue;

-- Tổng lũy kế số dư theo thời gian, cho từng tài khoản
SELECT account_id, created_at, amount,
       SUM(amount) OVER (PARTITION BY account_id ORDER BY created_at
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance
FROM transactions;

-- Trung bình trượt 7 ngày
AVG(amount) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

**Lưu ý:** không lọc trực tiếp kết quả window function trong `WHERE` được, vì WHERE chạy trước. Phải bọc bằng subquery hoặc CTE như ví dụ trên. MySQL hỗ trợ window function từ phiên bản 8.0.

### English

A **window function** computes over a "window" of related rows but **doesn't collapse rows** like `GROUP BY`: every row stays and gets an extra result column.

Syntax: `function() OVER (PARTITION BY ... ORDER BY ... [frame])`
- `PARTITION BY`: splits rows into groups (like GROUP BY without collapsing).
- `ORDER BY`: the order within each group.

**Ranking, with sample salaries 100, 90, 90, 80:**

| Function | Result | Behaviour |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 | Always distinct; ties are ordered arbitrarily |
| `RANK()` | 1, 2, 2, **4** | Ties share a rank, **numbers are skipped** afterwards |
| `DENSE_RANK()` | 1, 2, 2, **3** | Ties share a rank, **no gaps** |

```sql
-- Top 3 salaries per department
SELECT * FROM (
  SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees e
) t WHERE rnk <= 3;

-- Each customer's latest order (exactly one row)
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders o
) t WHERE rn = 1;

-- Month-over-month change: LAG reads the previous row, LEAD the next one
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM monthly_revenue;

-- Running balance over time, per account
SELECT account_id, created_at, amount,
       SUM(amount) OVER (PARTITION BY account_id ORDER BY created_at
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance
FROM transactions;

-- 7-day moving average
AVG(amount) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

**Note:** you can't filter on a window function's result directly in `WHERE`, because WHERE runs first. Wrap it in a subquery or CTE as above. MySQL supports window functions from version 8.0.

@@@ nosql-types | Có những loại NoSQL nào? Khi nào chọn SQL, khi nào chọn NoSQL? / What types of NoSQL databases are there, and when do you choose SQL vs NoSQL? | data | nosql,database-design | qa | NoSQL
### Tiếng Việt

| Loại | Ví dụ | Mô hình dữ liệu | Hợp với |
|---|---|---|---|
| **Key-value** | Redis, DynamoDB | Key → giá trị | Cache, session, rate limit, truy cập theo khóa cực nhanh |
| **Document** | MongoDB, Couchbase | Document JSON lồng nhau | Dữ liệu có cấu trúc linh hoạt: catalog sản phẩm, profile, CMS |
| **Wide-column** | Cassandra, ScyllaDB, HBase | Partition key + nhiều cột, sắp xếp theo clustering key | Ghi cực nhiều, dữ liệu theo thời gian: log, sự kiện, IoT, tin nhắn |
| **Graph** | Neo4j, Amazon Neptune | Node và cạnh | Quan hệ nhiều tầng: mạng xã hội, gợi ý, phát hiện gian lận |
| **Search** | Elasticsearch, OpenSearch | Inverted index | Tìm kiếm full-text, lọc nhiều tiêu chí, log analytics |
| **Time-series** | InfluxDB, TimescaleDB, Prometheus | Điểm dữ liệu theo thời gian | Metrics, dữ liệu cảm biến |

**SQL hay NoSQL:**

| Chọn **SQL** (PostgreSQL, MySQL) khi | Chọn **NoSQL** khi |
|---|---|
| Dữ liệu **có quan hệ**, cần JOIN | Truy cập chủ yếu theo **một khóa**, không cần JOIN |
| Cần **ACID nhiều bảng**: tiền, đơn hàng, tồn kho | Cần **scale ghi ngang** vượt khả năng một máy |
| Truy vấn đa dạng, chưa biết trước | **Mẫu truy vấn biết trước**, ổn định |
| Ràng buộc dữ liệu chặt (khóa ngoại, unique) | Schema thay đổi thường xuyên |
| Báo cáo, aggregate phức tạp | Độ trễ rất thấp ở quy mô rất lớn |

**Thực tế thường kết hợp (polyglot persistence):** PostgreSQL làm nguồn sự thật, Redis làm cache, Elasticsearch để tìm kiếm, Cassandra hoặc ClickHouse cho sự kiện khối lượng lớn. Dữ liệu đồng bộ giữa chúng qua sự kiện hoặc CDC.

**Lưu ý:** ranh giới đã mờ đi. PostgreSQL có JSONB và full-text search; MongoDB có transaction nhiều document từ bản 4.0. Mặc định chọn PostgreSQL, chỉ chọn NoSQL khi có lý do cụ thể.

### English

| Type | Examples | Data model | Fits |
|---|---|---|---|
| **Key-value** | Redis, DynamoDB | Key → value | Caches, sessions, rate limiting, very fast lookups by key |
| **Document** | MongoDB, Couchbase | Nested JSON documents | Flexible structures: product catalogs, profiles, CMS |
| **Wide-column** | Cassandra, ScyllaDB, HBase | Partition key + many columns, sorted by clustering key | Very write-heavy, time-ordered data: logs, events, IoT, messages |
| **Graph** | Neo4j, Amazon Neptune | Nodes and edges | Multi-hop relationships: social networks, recommendations, fraud detection |
| **Search** | Elasticsearch, OpenSearch | Inverted index | Full-text search, multi-criteria filtering, log analytics |
| **Time-series** | InfluxDB, TimescaleDB, Prometheus | Timestamped data points | Metrics, sensor data |

**SQL or NoSQL:**

| Choose **SQL** (PostgreSQL, MySQL) when | Choose **NoSQL** when |
|---|---|
| Data is **relational** and needs JOINs | Access is mostly by **one key**, no JOINs |
| You need **multi-table ACID**: money, orders, stock | You need to **scale writes horizontally** beyond one machine |
| Queries are varied and not known in advance | **Query patterns are known** and stable |
| Strict constraints (foreign keys, unique) | The schema changes often |
| Reporting, complex aggregates | Very low latency at very large scale |

**In practice they're combined (polyglot persistence):** PostgreSQL as the source of truth, Redis as a cache, Elasticsearch for search, Cassandra or ClickHouse for high-volume events. Data is synchronized between them through events or CDC.

**Note:** the lines have blurred. PostgreSQL has JSONB and full-text search; MongoDB has multi-document transactions since 4.0. Default to PostgreSQL and choose NoSQL only for a concrete reason.

@@@ nosql-mongodb | Thiết kế dữ liệu trong MongoDB thế nào: embed hay reference? / How do you model data in MongoDB: embed or reference? | data | nosql,mongodb | qa | NoSQL
### Tiếng Việt

**Nguyên tắc:** thiết kế theo **cách ứng dụng đọc dữ liệu**, không theo chuẩn hóa. Dữ liệu được đọc cùng nhau thì nên lưu cùng nhau.

**Embed (lồng vào nhau) khi:**
- Quan hệ **một-ít** (1–vài chục) và luôn đọc cùng nhau: địa chỉ của khách, các dòng trong một đơn hàng.
- Dữ liệu con **không có ý nghĩa khi đứng riêng**.
- Lợi ích: một lần đọc lấy đủ dữ liệu, và cập nhật **atomic trong một document**.

```json
{ "_id": "order_1", "customerId": "c_9", "status": "PAID",
  "items": [ { "sku": "A1", "qty": 2, "price": 150000 },
             { "sku": "B7", "qty": 1, "price": 90000 } ] }
```

**Reference (lưu id) khi:**
- Quan hệ **một-rất-nhiều** hoặc không giới hạn: bình luận của một bài viết phổ biến, log của một thiết bị.
- Dữ liệu con được dùng **ở nhiều nơi** và cập nhật độc lập (thông tin sản phẩm).
- Document có nguy cơ vượt **giới hạn 16 MB**.
- Truy vấn kết hợp bằng `$lookup` (chậm hơn JOIN) hoặc đọc hai lần từ ứng dụng.

**Kiến thức hay bị hỏi:**
- **Index:** single field, compound (theo quy tắc ESR: Equality, Sort, Range), multikey cho mảng, TTL index để tự xóa dữ liệu hết hạn.
- **Transaction:** từ 4.0 có transaction nhiều document (từ 4.2 trên sharded cluster), nhưng chậm hơn; thiết kế tốt thường chỉ cần atomic trong một document.
- **Replica set:** một primary nhận ghi, các secondary sao chép; primary chết thì bầu lại tự động. `writeConcern: majority` để không mất dữ liệu đã xác nhận.
- **Sharding:** chọn **shard key** có độ phân tán cao và khớp với truy vấn chính; key tăng dần như timestamp làm dồn ghi vào một shard.

**Khi nào không dùng MongoDB:** dữ liệu quan hệ chặt, nhiều JOIN, cần ràng buộc toàn vẹn mạnh (kế toán, sổ cái).

### English

**Principle:** model for **how the application reads the data**, not for normalization. Data that's read together should be stored together.

**Embed when:**
- The relationship is **one-to-few** (one to a few dozen) and always read together: a customer's addresses, the lines of an order.
- The child data **has no meaning on its own**.
- Benefits: one read returns everything, and updates are **atomic within one document**.

```json
{ "_id": "order_1", "customerId": "c_9", "status": "PAID",
  "items": [ { "sku": "A1", "qty": 2, "price": 150000 },
             { "sku": "B7", "qty": 1, "price": 90000 } ] }
```

**Reference (store an id) when:**
- The relationship is **one-to-very-many** or unbounded: comments on a popular post, a device's logs.
- The child data is **used in many places** and updated independently (product details).
- A document risks exceeding the **16 MB limit**.
- Combine data with `$lookup` (slower than a JOIN) or with two reads in the application.

**Frequently asked details:**
- **Indexes:** single-field, compound (following the ESR rule: Equality, Sort, Range), multikey for arrays, TTL indexes to expire data automatically.
- **Transactions:** multi-document transactions since 4.0 (on sharded clusters since 4.2), but they're slower; a good model usually needs atomicity within one document only.
- **Replica sets:** one primary takes writes, secondaries replicate; if the primary dies, a new one is elected automatically. Use `writeConcern: majority` so acknowledged writes aren't lost.
- **Sharding:** pick a **shard key** with high cardinality that matches the main queries; a monotonically increasing key such as a timestamp funnels all writes to one shard.

**When not to use MongoDB:** tightly relational data, lots of JOINs, strong integrity requirements (accounting, ledgers).

@@@ nosql-cassandra | Cassandra hoạt động thế nào? Thiết kế bảng ra sao? / How does Cassandra work, and how do you design its tables? | data | nosql,cassandra,axon | qa | NoSQL
### Tiếng Việt

*Axon liệt kê Cassandra trong yêu cầu backend ở TP.HCM, nên chủ đề này đáng ôn kỹ.*

**Kiến trúc:** cụm **không có master**, mọi node ngang hàng. Dữ liệu chia theo **partition key** trên một vòng consistent hashing, mỗi partition được nhân bản ra `RF` node (thường RF = 3).

**Vì sao ghi rất nhanh (LSM tree):** ghi vào **commit log** (append tuần tự) và **memtable** trong RAM là xong. Memtable đầy thì flush thành **SSTable** bất biến trên đĩa; định kỳ **compaction** gộp các SSTable. Không có đọc-trước-khi-ghi.

**Tunable consistency:** chọn mức nhất quán cho từng truy vấn: `ONE`, `QUORUM`, `ALL`, `LOCAL_QUORUM`. Nếu **R + W > RF** (ví dụ đọc QUORUM và ghi QUORUM với RF = 3, tức 2 + 2 > 3) thì luôn đọc được bản ghi mới nhất.

**Thiết kế bảng: query-first.** Không có JOIN, không nên query ngoài khóa, nên **mỗi truy vấn thường một bảng**, chấp nhận lưu trùng dữ liệu.

```sql
-- Truy vấn: "lấy 50 sự kiện mới nhất của một thiết bị trong một ngày"
CREATE TABLE events_by_device (
    device_id  uuid,
    day        date,
    event_time timestamp,
    event_id   timeuuid,
    payload    text,
    PRIMARY KEY ((device_id, day), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC, event_id DESC);

SELECT * FROM events_by_device WHERE device_id = ? AND day = ? LIMIT 50;
```

- **Partition key** `(device_id, day)`: quyết định dữ liệu nằm ở node nào; truy vấn **bắt buộc** có đủ partition key.
- **Clustering columns** `event_time, event_id`: sắp xếp dữ liệu trong partition, cho phép truy vấn khoảng.
- Thêm `day` vào partition key để **chia nhỏ (bucketing)**, tránh một partition phình quá lớn. Nên giữ partition dưới khoảng 100 MB.

**Bẫy hay gặp:**
- **Tombstone:** xóa không xóa ngay mà ghi dấu xóa; xóa nhiều làm đọc chậm. Tránh dùng Cassandra như hàng đợi (ghi rồi xóa liên tục).
- **Hot partition:** partition key phân bố kém (ví dụ chỉ dùng `day`) dồn tải vào vài node.
- `ALLOW FILTERING` và secondary index: tránh trong truy vấn chính vì phải quét nhiều node.
- Transaction rất hạn chế: chỉ có **lightweight transaction** (`IF NOT EXISTS`, dùng Paxos) và chậm.

**Hợp với:** ghi rất nhiều, truy vấn biết trước, cần chịu lỗi cao và chạy nhiều data center: dữ liệu thiết bị, log, tin nhắn, timeline.

### English

*Axon lists Cassandra in its backend requirements in Ho Chi Minh City, so this topic is worth studying properly.*

**Architecture:** a **masterless** cluster where every node is a peer. Data is distributed by **partition key** on a consistent-hashing ring, and each partition is replicated to `RF` nodes (usually RF = 3).

**Why writes are so fast (LSM tree):** a write goes to the **commit log** (a sequential append) and an in-memory **memtable**, and that's it. When the memtable fills, it's flushed to an immutable **SSTable** on disk; **compaction** periodically merges SSTables. There's no read-before-write.

**Tunable consistency:** choose a consistency level per query: `ONE`, `QUORUM`, `ALL`, `LOCAL_QUORUM`. If **R + W > RF** (for example QUORUM reads and QUORUM writes with RF = 3, so 2 + 2 > 3), reads always see the latest write.

**Table design is query-first.** There are no JOINs and you shouldn't query outside the key, so it's typically **one table per query**, accepting duplicated data.

```sql
-- Query: "get the 50 latest events of one device on one day"
CREATE TABLE events_by_device (
    device_id  uuid,
    day        date,
    event_time timestamp,
    event_id   timeuuid,
    payload    text,
    PRIMARY KEY ((device_id, day), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC, event_id DESC);

SELECT * FROM events_by_device WHERE device_id = ? AND day = ? LIMIT 50;
```

- **Partition key** `(device_id, day)`: decides which nodes hold the data; queries **must** supply the full partition key.
- **Clustering columns** `event_time, event_id`: order data within the partition and allow range queries.
- Adding `day` to the partition key **buckets** the data so one partition doesn't grow too large. Keep partitions under roughly 100 MB.

**Common traps:**
- **Tombstones:** deletes aren't immediate; they write a deletion marker, and many deletes slow reads down. Don't use Cassandra as a queue (constant write-then-delete).
- **Hot partitions:** a poorly distributed partition key (for example `day` alone) concentrates load on a few nodes.
- `ALLOW FILTERING` and secondary indexes: avoid them on main queries because they scan many nodes.
- Transactions are very limited: only **lightweight transactions** (`IF NOT EXISTS`, using Paxos), and they're slow.

**Fits:** very write-heavy workloads with known queries that need high fault tolerance and multiple data centers: device data, logs, messages, timelines.

@@@ cache-patterns | Có những chiến lược cache nào? Cache-aside, read-through, write-through, write-behind khác nhau ra sao? / What caching strategies exist? How do cache-aside, read-through, write-through and write-behind differ? | data | cache,redis | qa | Cache
### Tiếng Việt

| Chiến lược | Đọc | Ghi | Ưu | Nhược |
|---|---|---|---|---|
| **Cache-aside** (lazy loading) | App đọc cache; miss thì app đọc DB rồi **tự ghi vào cache** | App ghi DB rồi **xóa** key trong cache | Phổ biến nhất, cache chết thì app vẫn chạy, chỉ cache dữ liệu thật sự được đọc | Lần đọc đầu luôn miss; dễ lệch dữ liệu nếu xử lý sai thứ tự |
| **Read-through** | App chỉ hỏi cache; **cache tự** nạp từ DB khi miss | (kết hợp với chiến lược ghi khác) | Code app gọn | Cần thư viện hoặc cache hỗ trợ loader |
| **Write-through** | | App ghi vào cache, **cache ghi đồng bộ** xuống DB | Cache luôn mới | Ghi chậm hơn (ghi hai nơi); cache chứa cả dữ liệu ít đọc |
| **Write-behind** (write-back) | | Ghi vào cache, **ghi xuống DB sau**, theo lô và bất đồng bộ | Ghi rất nhanh, gom lô giảm tải DB | **Mất dữ liệu** nếu cache chết trước khi ghi xuống DB |
| **Refresh-ahead** | Cache **tự làm mới** key nóng trước khi hết hạn | | Không có độ trễ miss cho key nóng | Tốn tài nguyên làm mới cả key không còn ai đọc |

**Cache-aside, cách viết đúng:**

```java
Product get(long id) {
    String key = "product:" + id;
    Product p = redis.get(key);
    if (p != null) return p;                 // hit
    p = repository.findById(id);             // miss → đọc DB
    redis.set(key, p, Duration.ofMinutes(10).plusSeconds(random(0, 60))); // TTL có jitter
    return p;
}

@Transactional
void update(Product p) {
    repository.save(p);                       // 1. ghi DB trước
    // 2. xóa cache SAU KHI commit (TransactionSynchronization hoặc @TransactionalEventListener)
    redis.delete("product:" + p.getId());
}
```

**Vì sao xóa cache thay vì cập nhật cache khi ghi?** Hai request ghi đồng thời có thể cập nhật cache theo thứ tự ngược với DB, để lại giá trị cũ trong cache. Xóa thì lần đọc sau sẽ nạp lại giá trị đúng từ DB. Ngoài ra không tốn công tính lại giá trị không ai đọc.

**Trong Spring:** `@Cacheable`, `@CachePut`, `@CacheEvict` với Caffeine (cache cục bộ) hoặc Redis. Nhớ rằng chúng cũng dựa trên proxy, nên gọi nội bộ trong cùng class sẽ không đi qua cache.

### English

| Strategy | Read | Write | Pros | Cons |
|---|---|---|---|---|
| **Cache-aside** (lazy loading) | App reads the cache; on a miss, the app reads the DB and **populates the cache itself** | App writes the DB, then **deletes** the cache key | Most common, the app still works if the cache dies, only data that's actually read gets cached | First read always misses; data can diverge if ordering is handled wrongly |
| **Read-through** | App only asks the cache; **the cache itself** loads from the DB on a miss | (combined with some write strategy) | Simpler application code | Needs a library or cache with loader support |
| **Write-through** | | App writes to the cache, and **the cache writes synchronously** to the DB | Cache is always fresh | Slower writes (two places); cache also holds rarely read data |
| **Write-behind** (write-back) | | Write to the cache, **write to the DB later**, in asynchronous batches | Very fast writes, batching reduces DB load | **Data loss** if the cache dies before flushing to the DB |
| **Refresh-ahead** | The cache **refreshes** hot keys before they expire | | No miss latency for hot keys | Wastes resources refreshing keys nobody reads anymore |

**Cache-aside done right:**

```java
Product get(long id) {
    String key = "product:" + id;
    Product p = redis.get(key);
    if (p != null) return p;                 // hit
    p = repository.findById(id);             // miss → read the DB
    redis.set(key, p, Duration.ofMinutes(10).plusSeconds(random(0, 60))); // TTL with jitter
    return p;
}

@Transactional
void update(Product p) {
    repository.save(p);                       // 1. write the DB first
    // 2. delete the cache AFTER COMMIT (TransactionSynchronization or @TransactionalEventListener)
    redis.delete("product:" + p.getId());
}
```

**Why delete the cache instead of updating it on writes?** Two concurrent writers can update the cache in the opposite order from the database, leaving a stale value in the cache. Deleting means the next read reloads the correct value from the DB. It also avoids computing values nobody reads.

**In Spring:** `@Cacheable`, `@CachePut`, `@CacheEvict` with Caffeine (a local cache) or Redis. Remember they're proxy-based too, so internal calls within the same class bypass the cache.

@@@ cache-problems | Cache penetration, cache breakdown (stampede) và cache avalanche là gì? Xử lý thế nào? / What are cache penetration, cache breakdown (stampede) and cache avalanche, and how do you handle them? | data | cache,redis,performance | qa | Cache
### Tiếng Việt

| Vấn đề | Chuyện gì xảy ra | Cách xử lý |
|---|---|---|
| **Penetration** (xuyên thủng) | Truy vấn key **không tồn tại cả trong DB** (ví dụ `id = -1`, bot dò id). Cache không bao giờ có, nên mọi request đều xuống DB | **Cache giá trị rỗng** với TTL ngắn (30–60 giây); **Bloom filter** chặn trước các id chắc chắn không tồn tại; validate input, rate limit |
| **Breakdown / stampede** (một key nóng hết hạn) | Một key **cực nóng** hết hạn, hàng nghìn request cùng miss và **cùng lúc** đập xuống DB | **Mutex hoặc single-flight**: chỉ một request được nạp lại, các request khác chờ hoặc dùng giá trị cũ; **logical expiry** (không đặt TTL thật, lưu thời điểm hết hạn trong value, hết hạn thì một thread làm mới nền còn các request khác vẫn trả giá trị cũ); refresh-ahead |
| **Avalanche** (tuyết lở) | **Nhiều key hết hạn cùng lúc** (ví dụ cùng nạp lúc khởi động với cùng TTL), hoặc **cả cụm Redis chết**: DB bị dồn tải và sập | **TTL có jitter** (10 phút cộng ngẫu nhiên 0–60 giây); Redis HA (Sentinel hoặc Cluster); **cache nhiều tầng** (Caffeine cục bộ + Redis); **circuit breaker và rate limit** để bảo vệ DB; warm-up cache trước giờ cao điểm |

**Ví dụ single-flight với khóa Redis:**

```java
Product get(long id) {
    Product p = redis.get(key(id));
    if (p != null) return p;
    String lock = "lock:" + key(id);
    if (redis.setIfAbsent(lock, "1", Duration.ofSeconds(5))) {   // chỉ một request giành được khóa
        try {
            p = repository.findById(id);
            redis.set(key(id), p, ttlWithJitter());
            return p;
        } finally { redis.delete(lock); }
    }
    Thread.sleep(50);            // request khác chờ ngắn rồi đọc lại cache
    return get(id);              // (thực tế giới hạn số lần thử)
}
```

Trong một instance, `Caffeine` với `LoadingCache` đã tự gộp các lần nạp đồng thời cho cùng key. Khóa Redis chỉ cần khi có nhiều instance.

### English

| Problem | What happens | How to handle it |
|---|---|---|
| **Penetration** | Requests for keys that **don't exist in the database either** (e.g. `id = -1`, bots probing ids). The cache never has them, so every request hits the DB | **Cache empty results** with a short TTL (30–60 seconds); a **Bloom filter** blocks ids that definitely don't exist; validate input, rate limit |
| **Breakdown / stampede** (one hot key expires) | An **extremely hot** key expires, and thousands of requests miss and hit the DB **at the same moment** | **A mutex or single-flight**: only one request reloads, the others wait or use the old value; **logical expiry** (no real TTL; store the expiry time inside the value, and when it passes, one thread refreshes in the background while other requests keep returning the old value); refresh-ahead |
| **Avalanche** | **Many keys expire at once** (e.g. all loaded at startup with the same TTL), or **the whole Redis cluster goes down**: the DB is flooded and fails | **TTL with jitter** (10 minutes plus a random 0–60 seconds); Redis HA (Sentinel or Cluster); **multi-level caching** (local Caffeine + Redis); **circuit breakers and rate limits** to protect the DB; warm the cache before peak hours |

**Single-flight example with a Redis lock:**

```java
Product get(long id) {
    Product p = redis.get(key(id));
    if (p != null) return p;
    String lock = "lock:" + key(id);
    if (redis.setIfAbsent(lock, "1", Duration.ofSeconds(5))) {   // only one request wins the lock
        try {
            p = repository.findById(id);
            redis.set(key(id), p, ttlWithJitter());
            return p;
        } finally { redis.delete(lock); }
    }
    Thread.sleep(50);            // other requests wait briefly, then read the cache again
    return get(id);              // (in practice, cap the number of attempts)
}
```

Within one instance, Caffeine's `LoadingCache` already collapses concurrent loads of the same key. A Redis lock is only needed across several instances.

@@@ cache-consistency | Làm sao giữ cache và database nhất quán? / How do you keep the cache and the database consistent? | data | cache,consistency,redis | qa | Cache
### Tiếng Việt

Cache và DB là hai hệ thống, nên **không có nhất quán tuyệt đối** nếu không có transaction chung. Mục tiêu là giữ khoảng lệch **ngắn và có giới hạn**.

**So sánh các thứ tự ghi:**

| Cách | Vấn đề |
|---|---|
| Cập nhật cache, rồi cập nhật DB | DB lỗi thì cache chứa giá trị **chưa từng tồn tại** |
| Cập nhật DB, rồi **cập nhật** cache | Hai lần ghi đồng thời có thể để cache theo thứ tự sai, tức **giá trị cũ** |
| Xóa cache, rồi cập nhật DB | Giữa hai bước, một request đọc nạp lại **giá trị cũ** vào cache |
| **Cập nhật DB, rồi xóa cache** | **Tốt nhất**, vẫn còn một khe hở nhỏ (xem bên dưới) |

**Khe hở còn lại của "cập nhật DB rồi xóa cache":** request A đọc miss và lấy giá trị cũ từ DB; request B cập nhật DB rồi xóa cache; A ghi giá trị cũ vào cache. Khe hở này hiếm vì đọc DB thường nhanh hơn ghi, nhưng vẫn có thể xảy ra.

**Các cách thu hẹp tiếp:**
1. **TTL là lưới an toàn:** mọi key đều có TTL, nên dữ liệu sai tự hết hạn.
2. **Delayed double delete:** xóa cache, cập nhật DB, rồi **xóa thêm lần nữa sau vài trăm ms** (bất đồng bộ).
3. **Xóa qua CDC:** Debezium đọc binlog/WAL của DB rồi phát sự kiện, consumer xóa cache. Không bỏ sót kể cả khi app chết giữa chừng, và **tách việc xóa cache khỏi code nghiệp vụ**. Xóa thất bại thì retry từ Kafka.
4. **Version hoặc timestamp:** lưu version trong value; chỉ ghi vào cache nếu version mới hơn (dùng Lua script để so sánh và ghi atomic).
5. **Không cache** dữ liệu bắt buộc mới tuyệt đối: số dư khi trừ tiền, tồn kho lúc đặt hàng. Đọc thẳng DB, hoặc dùng Redis làm nguồn sự thật có kiểm soát (như flash sale) rồi đối soát.

**Cache cục bộ trên nhiều instance (Caffeine):** mỗi instance có bản riêng, nên khi dữ liệu đổi phải **broadcast invalidation** (Redis pub/sub hoặc Kafka) tới mọi instance, hoặc chỉ dùng TTL rất ngắn.

**Câu trả lời mẫu:** *"Tôi dùng cache-aside: ghi DB, xóa cache sau commit, mọi key có TTL kèm jitter. Với dữ liệu quan trọng, tôi xóa cache qua CDC để không bỏ sót, và không cache những giá trị cần nhất quán mạnh như số dư."*

### English

The cache and the database are two systems, so **there's no perfect consistency** without a shared transaction. The goal is to keep the window of inconsistency **short and bounded**.

**Comparing write orders:**

| Approach | Problem |
|---|---|
| Update the cache, then the DB | If the DB write fails, the cache holds a value **that never existed** |
| Update the DB, then **update** the cache | Two concurrent writes can leave the cache in the wrong order, i.e. a **stale value** |
| Delete the cache, then update the DB | Between the two steps, a read can reload the **old value** into the cache |
| **Update the DB, then delete the cache** | **Best**, though a small gap remains (see below) |

**The remaining gap in "update DB, then delete cache":** request A misses and reads the old value from the DB; request B updates the DB and deletes the cache; A then writes the old value into the cache. It's rare because DB reads are usually faster than writes, but it can happen.

**Ways to narrow it further:**
1. **TTL as a safety net:** every key has a TTL, so wrong data expires on its own.
2. **Delayed double delete:** delete the cache, update the DB, then **delete again a few hundred ms later** (asynchronously).
3. **Invalidation via CDC:** Debezium reads the DB's binlog/WAL and emits events, and a consumer deletes cache keys. Nothing is missed even if the app dies midway, and **cache invalidation is decoupled from business code**. Failed deletes are retried from Kafka.
4. **Versions or timestamps:** store a version in the value and only write to the cache if the version is newer (a Lua script compares and writes atomically).
5. **Don't cache** data that must be absolutely fresh: a balance when charging, stock at checkout. Read the DB directly, or use Redis as a controlled source of truth (as in a flash sale) and reconcile.

**Local caches across many instances (Caffeine):** each instance has its own copy, so on changes you must **broadcast invalidations** (Redis pub/sub or Kafka) to every instance, or use only very short TTLs.

**A model answer:** *"I use cache-aside: write the DB, delete the cache after commit, and every key has a TTL with jitter. For important data I invalidate through CDC so nothing is missed, and I don't cache values that need strong consistency, such as balances."*

@@@ redis-structures | Redis có những kiểu dữ liệu nào? Dùng cho bài toán gì? Vì sao Redis nhanh? / What data types does Redis have, what are they used for, and why is Redis fast? | data | redis,cache | qa | Cache
### Tiếng Việt

| Kiểu | Lệnh tiêu biểu | Dùng cho |
|---|---|---|
| **String** | `SET key val EX 60 NX`, `INCR`, `GET` | Cache object (JSON), bộ đếm, **khóa phân tán** (`SET NX PX`), rate limit |
| **Hash** | `HSET user:1 name An`, `HINCRBY` | Object nhiều field, cập nhật từng field mà không đọc ghi lại cả object |
| **List** | `LPUSH`, `RPOP`, `BLPOP`, `LRANGE` | Hàng đợi đơn giản, N mục mới nhất (feed, log gần đây) |
| **Set** | `SADD`, `SISMEMBER`, `SINTER` | Tập không trùng: tag, người đã like, giao hai tập (bạn chung) |
| **Sorted Set** | `ZADD`, `ZRANGE ... REV`, `ZRANGEBYSCORE` | **Bảng xếp hạng**, hàng đợi ưu tiên hoặc theo thời gian, **sliding-window rate limit** |
| **Bitmap** | `SETBIT`, `BITCOUNT` | Điểm danh theo ngày, người dùng hoạt động (1 bit mỗi user) |
| **HyperLogLog** | `PFADD`, `PFCOUNT` | **Đếm số phần tử khác nhau** gần đúng với khoảng 12 KB, sai số khoảng 0,81% (lượt xem duy nhất) |
| **Stream** | `XADD`, `XREADGROUP`, `XACK` | Log sự kiện có consumer group, thay Kafka cho tải nhỏ |
| **Geo** | `GEOADD`, `GEOSEARCH` | Tìm điểm gần nhất (tài xế, cửa hàng) |

**Vì sao Redis nhanh:**
- Dữ liệu nằm **hoàn toàn trong RAM**.
- Thực thi lệnh trên **một thread chính**: không tốn chi phí khóa hay chuyển ngữ cảnh, và **mỗi lệnh là atomic**. Từ Redis 6 có thêm I/O thread cho đọc ghi mạng, nhưng lệnh vẫn chạy tuần tự.
- I/O multiplexing (epoll) phục vụ hàng chục nghìn kết nối.
- Cấu trúc dữ liệu được tối ưu (listpack, skiplist cho sorted set).

**Hệ quả của single-thread:** **một lệnh chậm chặn tất cả**. Tránh `KEYS *` (dùng `SCAN`), tránh `HGETALL` hay `SMEMBERS` trên tập rất lớn, tránh **big key** (value hàng MB) và xóa big key bằng `UNLINK` thay cho `DEL`.

**Atomic nhiều bước:** dùng **Lua script** (chạy atomic, không bị chen ngang) hoặc `MULTI/EXEC`. Ví dụ trừ tồn kho chỉ khi còn hàng phải nằm trong một Lua script.

### English

| Type | Typical commands | Used for |
|---|---|---|
| **String** | `SET key val EX 60 NX`, `INCR`, `GET` | Caching objects (JSON), counters, **distributed locks** (`SET NX PX`), rate limiting |
| **Hash** | `HSET user:1 name An`, `HINCRBY` | Multi-field objects, updating one field without rewriting the whole object |
| **List** | `LPUSH`, `RPOP`, `BLPOP`, `LRANGE` | Simple queues, latest-N items (feeds, recent logs) |
| **Set** | `SADD`, `SISMEMBER`, `SINTER` | Unique collections: tags, users who liked, set intersections (mutual friends) |
| **Sorted Set** | `ZADD`, `ZRANGE ... REV`, `ZRANGEBYSCORE` | **Leaderboards**, priority or time-ordered queues, **sliding-window rate limiting** |
| **Bitmap** | `SETBIT`, `BITCOUNT` | Daily check-ins, active users (one bit per user) |
| **HyperLogLog** | `PFADD`, `PFCOUNT` | **Approximate distinct counts** in about 12 KB with about 0.81% error (unique views) |
| **Stream** | `XADD`, `XREADGROUP`, `XACK` | An event log with consumer groups, replacing Kafka for small loads |
| **Geo** | `GEOADD`, `GEOSEARCH` | Nearest-point search (drivers, stores) |

**Why Redis is fast:**
- Data lives **entirely in RAM**.
- Commands execute on **one main thread**: no locking or context-switch overhead, and **every command is atomic**. Redis 6 added I/O threads for network reads and writes, but commands still run sequentially.
- I/O multiplexing (epoll) serves tens of thousands of connections.
- Data structures are optimized (listpacks, skiplists for sorted sets).

**Consequence of the single thread:** **one slow command blocks everything**. Avoid `KEYS *` (use `SCAN`), avoid `HGETALL` or `SMEMBERS` on very large collections, avoid **big keys** (multi-MB values), and delete big keys with `UNLINK` instead of `DEL`.

**Multi-step atomicity:** use a **Lua script** (runs atomically, nothing interleaves) or `MULTI/EXEC`. For example, decrementing stock only when items remain must happen inside one Lua script.

@@@ redis-ha | Redis lưu dữ liệu xuống đĩa và chạy HA thế nào? Khi bộ nhớ đầy thì sao? / How does Redis persist data and run highly available, and what happens when memory is full? | data | redis,high-availability | qa | Cache
### Tiếng Việt

**Persistence, hai cơ chế:**

| | RDB (snapshot) | AOF (append-only file) |
|---|---|---|
| Cách làm | Định kỳ fork process, chụp toàn bộ dữ liệu ra file | Ghi **mọi lệnh ghi** vào cuối file |
| Mất dữ liệu khi sập | Mất từ lần chụp cuối (có thể vài phút) | Với `appendfsync everysec`: mất **tối đa khoảng 1 giây** |
| Khởi động lại | Nhanh | Chậm hơn (phải chạy lại lệnh); có AOF rewrite để thu gọn |
| Hợp với | Backup, khôi phục nhanh | Cần ít mất dữ liệu |

Thực tế thường bật **cả hai** (Redis 7 dùng AOF nhiều phần, có phần nền dạng RDB). Với cache thuần thì có thể tắt persistence.

**High availability:**
- **Replication:** một master, nhiều replica, sao chép **bất đồng bộ**, nên master chết có thể mất vài lệnh ghi cuối. `WAIT` giúp giảm rủi ro nhưng không đảm bảo tuyệt đối.
- **Sentinel:** theo dõi master; master chết thì Sentinel **tự promote** một replica và báo client địa chỉ mới. Dùng khi dữ liệu vừa trong một máy.
- **Redis Cluster:** chia dữ liệu thành **16.384 hash slot** trên nhiều master (mỗi master có replica), scale cả đọc lẫn ghi. Lệnh nhiều key chỉ chạy được khi các key **cùng slot**: dùng **hash tag** `{user:1}:profile`, `{user:1}:cart`.
- Dịch vụ quản lý: AWS ElastiCache hoặc MemoryDB, Azure Cache.

**Khi đầy bộ nhớ (`maxmemory`), theo `maxmemory-policy`:**

| Policy | Hành vi |
|---|---|
| `noeviction` (mặc định) | Lệnh ghi bị **báo lỗi** |
| `allkeys-lru` | Xóa key **ít được dùng gần đây nhất** trong mọi key. **Chọn cho cache** |
| `allkeys-lfu` | Xóa key **ít được dùng thường xuyên nhất**. Tốt khi có key nóng ổn định |
| `volatile-lru`, `volatile-lfu`, `volatile-ttl` | Chỉ xóa trong các key **có TTL** |
| `allkeys-random` | Xóa ngẫu nhiên |

LRU và LFU của Redis là **gần đúng** (lấy mẫu một số key) để tiết kiệm bộ nhớ.

**Lưu ý:** **không dùng Redis làm nguồn sự thật duy nhất cho dữ liệu quan trọng** như tiền hay đơn hàng, vì replication bất đồng bộ có thể mất dữ liệu khi failover. Nếu có dùng (ví dụ đếm tồn kho flash sale), phải có đối soát với DB.

### English

**Persistence, two mechanisms:**

| | RDB (snapshot) | AOF (append-only file) |
|---|---|---|
| How | Periodically forks and dumps the whole dataset to a file | Appends **every write command** to a file |
| Data loss on crash | Everything since the last snapshot (possibly minutes) | With `appendfsync everysec`: **at most about 1 second** |
| Restart | Fast | Slower (commands are replayed); AOF rewrite keeps it compact |
| Fits | Backups, fast recovery | Minimal data loss |

In practice both are often enabled (Redis 7 uses a multi-part AOF with an RDB-format base). For a pure cache, persistence can be turned off.

**High availability:**
- **Replication:** one master, several replicas, replicated **asynchronously**, so a master failure can lose the last few writes. `WAIT` reduces the risk but doesn't guarantee anything.
- **Sentinel:** monitors the master; if it dies, Sentinel **automatically promotes** a replica and tells clients the new address. Used when the data fits on one machine.
- **Redis Cluster:** splits data into **16,384 hash slots** across several masters (each with replicas), scaling both reads and writes. Multi-key commands only work when the keys are **in the same slot**: use **hash tags** such as `{user:1}:profile`, `{user:1}:cart`.
- Managed services: AWS ElastiCache or MemoryDB, Azure Cache.

**When memory is full (`maxmemory`), per `maxmemory-policy`:**

| Policy | Behaviour |
|---|---|
| `noeviction` (default) | Writes **return an error** |
| `allkeys-lru` | Evicts the **least recently used** key among all keys. **The choice for a cache** |
| `allkeys-lfu` | Evicts the **least frequently used** key. Good when hot keys are stable |
| `volatile-lru`, `volatile-lfu`, `volatile-ttl` | Evict only among keys **with a TTL** |
| `allkeys-random` | Evicts at random |

Redis's LRU and LFU are **approximate** (they sample keys) to save memory.

**Note:** **don't use Redis as the only source of truth for important data** like money or orders, because asynchronous replication can lose data on failover. If you do (for example a flash-sale stock counter), reconcile against the database.

@@@ cache-local-vs-distributed | Cache cục bộ (Caffeine) và cache phân tán (Redis) khác nhau thế nào? Khi nào dùng cả hai? / Local cache (Caffeine) vs distributed cache (Redis): how do they differ, and when do you use both? | data | cache,redis,caffeine | qa | Cache
### Tiếng Việt

| | Cache cục bộ (Caffeine, Guava, `ConcurrentHashMap`) | Cache phân tán (Redis, Memcached) |
|---|---|---|
| Vị trí | Trong heap của **từng instance** | Server riêng, **dùng chung** cho mọi instance |
| Tốc độ | **Nhanh nhất** (nano đến micro giây), không qua mạng, không serialize | Khoảng 0,1–1 ms, qua mạng và serialize |
| Nhất quán giữa instance | **Mỗi instance một bản**, có thể lệch nhau | Một bản chung |
| Dung lượng | Giới hạn bởi heap, cache lớn làm GC nặng | Lớn, scale riêng |
| Còn sau khi restart app | Mất | Còn |
| Hợp với | Dữ liệu nhỏ, **rất nóng, ít đổi**: cấu hình, danh mục, quyền | Dữ liệu cần dùng chung: session, giỏ hàng, rate limit, khóa, cache object lớn |

**Cache hai tầng (L1 Caffeine + L2 Redis):**

```
Request → L1 (Caffeine, TTL 30 giây) → miss → L2 (Redis, TTL 10 phút) → miss → DB
```

- Giảm mạnh số lần gọi Redis cho key cực nóng, và **chống avalanche** khi Redis gặp sự cố.
- **Vấn đề:** dữ liệu đổi thì L1 ở các instance khác vẫn giữ bản cũ. Cách xử lý: L1 có TTL ngắn, và **broadcast invalidation** qua Redis pub/sub hoặc Kafka để mọi instance xóa key khỏi L1.

**Caffeine cấu hình mẫu:**

```java
LoadingCache<Long, Product> cache = Caffeine.newBuilder()
    .maximumSize(10_000)                       // giới hạn số phần tử (thuật toán W-TinyLFU)
    .expireAfterWrite(Duration.ofSeconds(30))
    .refreshAfterWrite(Duration.ofSeconds(20)) // làm mới nền, request vẫn nhận giá trị cũ
    .recordStats()                             // đo hit rate
    .build(id -> repository.findById(id).orElseThrow());
```

**Đo hiệu quả:** theo dõi **hit rate**, độ trễ, lượng bộ nhớ, số key bị loại. Hit rate thấp nghĩa là cache không có tác dụng: hoặc sai key, hoặc TTL quá ngắn, hoặc dữ liệu vốn không được đọc lặp lại.

### English

| | Local cache (Caffeine, Guava, `ConcurrentHashMap`) | Distributed cache (Redis, Memcached) |
|---|---|---|
| Location | In the heap of **each instance** | A separate server, **shared** by all instances |
| Speed | **Fastest** (nano- to microseconds), no network, no serialization | About 0.1–1 ms, over the network with serialization |
| Consistency across instances | **Each instance has its own copy**, copies can diverge | One shared copy |
| Capacity | Limited by the heap; large caches add GC pressure | Large, scaled independently |
| Survives app restarts | No | Yes |
| Fits | Small, **very hot, rarely changing** data: configuration, catalogs, permissions | Data that must be shared: sessions, carts, rate limits, locks, large object caches |

**Two-level cache (L1 Caffeine + L2 Redis):**

```
Request → L1 (Caffeine, TTL 30 s) → miss → L2 (Redis, TTL 10 min) → miss → DB
```

- Greatly reduces Redis calls for extremely hot keys, and **protects against avalanches** when Redis has problems.
- **The issue:** when data changes, L1 on other instances still holds the old copy. The fix: a short L1 TTL plus **broadcast invalidation** via Redis pub/sub or Kafka so every instance evicts the key from L1.

**Sample Caffeine configuration:**

```java
LoadingCache<Long, Product> cache = Caffeine.newBuilder()
    .maximumSize(10_000)                       // bounded size (W-TinyLFU algorithm)
    .expireAfterWrite(Duration.ofSeconds(30))
    .refreshAfterWrite(Duration.ofSeconds(20)) // background refresh, requests still get the old value
    .recordStats()                             // measure hit rate
    .build(id -> repository.findById(id).orElseThrow());
```

**Measure effectiveness:** track **hit rate**, latency, memory use and evictions. A low hit rate means the cache isn't helping: the key is wrong, the TTL is too short, or the data simply isn't read repeatedly.
