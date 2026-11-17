@@@ pg-acid-wal | How does PostgreSQL guarantee atomicity and durability after a crash? | spring | database,postgresql,acid,transaction | qa | PostgreSQL internals
"Through the **write-ahead log**. Every change is written to the WAL and flushed to disk at commit before the data pages themselves are written. After a crash, Postgres replays the WAL from the last checkpoint: committed transactions are redone, and changes from uncommitted ones are simply never visible, because MVCC marks them by transaction ID as aborted.

So durability means 'the WAL record is on disk', and atomicity comes from all-or-nothing visibility by transaction ID. Trading durability for speed is possible with `synchronous_commit = off`, which risks losing the last few hundred milliseconds of commits but not corruption.

Many NoSQL systems relax ACID across documents or partitions to gain horizontal scale and availability; that's the BASE trade-off. For money, both atomicity and durability are non-negotiable."

Tham khảo thêm: [Database: ACID Properties](https://minhnhat97kg.github.io/docsify/content/database-acid-properties/vi.md)

@@@ pg-mvcc | What is MVCC, and why does PostgreSQL need VACUUM? | spring | database,postgresql,mvcc,vacuum | qa | PostgreSQL internals
"With MVCC, readers don't block writers and writers don't block readers. Each row version stores `xmin`, the transaction that created it, and `xmax`, the one that deleted it. An `UPDATE` doesn't overwrite; it writes a new version and marks the old one dead. Each transaction sees the versions valid for its snapshot.

Dead versions take space and slow scans: that's **bloat**. **VACUUM** marks their space reusable; `VACUUM FULL` rewrites the table and returns space to the OS but takes an exclusive lock, so I prefer `pg_repack` in production. **Autovacuum** runs this automatically; on large, busy tables I lower its scale factors so it runs more often.

It also prevents **transaction ID wraparound**: IDs are 32-bit, so old rows must be frozen, or Postgres eventually stops accepting writes. Long-running transactions block cleanup, so I monitor them. Related trivia: `COUNT(*)` is slower than you'd expect because visibility must be checked per row, and frequently updating one small column still creates whole new row versions."

Tham khảo thêm: [MVCC & Dead Tuples](https://minhnhat97kg.github.io/docsify/content/database-mvcc-dead-tuples/vi.md), [Vacuum & Autovacuum](https://minhnhat97kg.github.io/docsify/content/database-vacuum-autovacuum-garbage-collection/vi.md)

@@@ pg-isolation | Read committed vs repeatable read vs serializable in PostgreSQL? | spring | database,postgresql,isolation,transaction | qa | PostgreSQL internals
"PostgreSQL's default is **read committed**: each statement sees data committed before it started, so two reads in one transaction can differ, and phantoms can appear.

**Repeatable read** in Postgres is snapshot isolation: the whole transaction sees one snapshot, which also prevents phantoms for reads. But it allows **write skew**: two transactions each read a condition, such as 'at least one doctor on call', and update different rows, breaking the invariant together.

**Serializable** adds conflict detection (SSI) and aborts one transaction with a serialization error, so the application must retry.

To avoid anomalies without serializable: lock the rows that guard the invariant with `SELECT ... FOR UPDATE`, use a conditional update, add a unique or exclusion constraint, or use advisory locks. MySQL InnoDB's repeatable read behaves differently, using gap locks, so I name the database when answering."

Tham khảo thêm: [Database - Isolation Levels](https://minhnhat97kg.github.io/docsify/content/database-isolation-level-read-committed-vs-serializable/vi.md)

@@@ pg-indexes | Beyond B-tree: when do you use Hash, GIN, GiST or partial indexes? | spring | database,postgresql,indexing | qa | PostgreSQL internals
"**B-tree** is the default: equality, ranges, sorting, prefix `LIKE 'abc%'`. With `INCLUDE` columns it enables index-only scans.

**Hash**: equality only, rarely worth it over B-tree.

**GIN**, an inverted index: for values that contain many keys, such as JSONB containment (`@>`), arrays, and full-text search. Reads are fast; inserts are slower because one row updates many entries, which `fastupdate` mitigates.

**GiST**: for geometric and range data, such as PostGIS 'nearest ATM', range overlap, and exclusion constraints.

**pg_trgm** with GIN or GiST makes `LIKE '%abc%'` and fuzzy search usable.

**Partial indexes** index only the rows you query, such as `WHERE status = 'PENDING'`: smaller and faster. And an index on a column with a function needs a matching expression index."

Tham khảo thêm: [Indexing: B-Tree](https://minhnhat97kg.github.io/docsify/content/database-indexing-b-tree-the-default-workhorse/vi.md), [Indexing: GIN & GiST](https://minhnhat97kg.github.io/docsify/content/database-indexing-gin-gist-advanced-indexing/vi.md)

@@@ pg-partitioning | When and how do you partition a large table? | spring | database,postgresql,partitioning,performance | qa | PostgreSQL internals
"When a table grows to hundreds of millions of rows and most queries hit a recent slice, or old data must be dropped regularly.

- **Range** partitioning by time, such as monthly for transactions or logs, is the most common.
- **Hash** partitioning by ID spreads load evenly when there's no natural range.
- **List** partitioning by tenant or region.

Benefits: **partition pruning**, where queries with the partition key touch only relevant partitions; dropping an old partition instead of a huge `DELETE` that bloats the table; and smaller indexes per partition.

Pitfalls: a primary key or unique constraint must include the partition key, since Postgres has no global indexes; queries without the partition key scan every partition; and too many partitions slow planning. I automate creating future partitions with `pg_partman` or a scheduled job."

Tham khảo thêm: [Table Partitioning](https://minhnhat97kg.github.io/docsify/content/database-table-partitioning-range-hash/vi.md)

@@@ pg-pooling | Why use PgBouncer if the app already has a connection pool? | spring | database,postgresql,connection-pool,performance | qa | PostgreSQL internals
"Each Postgres connection is a separate OS process using several MB of memory, so a few hundred connections already hurt. With 50 application pods each running a HikariCP pool of 20, you'd have 1,000 connections. PgBouncer sits in between and multiplexes many client connections onto a small number of server connections.

Modes:

- **Session pooling:** a server connection per client session; safe but saves little.
- **Transaction pooling:** a server connection only for the duration of a transaction; the usual choice for high concurrency.
- **Statement pooling:** rarely used.

In transaction mode, session state doesn't survive between transactions: `SET` commands, advisory locks and, historically, server-side prepared statements, causing 'prepared statement does not exist' errors. PgBouncer 1.21+ can track protocol-level prepared statements; otherwise disable them in the driver. On AWS, RDS Proxy plays the same role."

Tham khảo thêm: [Database - Connection Pool](https://minhnhat97kg.github.io/docsify/content/database-connection-pool/vi.md)

@@@ sql-tricky | Tricky SQL questions: EXISTS vs IN, NULL, deleting 10 million rows. | spring | sql,database,performance | qa | SQL nâng cao
"- **EXISTS vs IN:** modern planners often turn both into the same semi-join. The real trap is `NOT IN` with a subquery that can return NULL: it returns no rows at all. I use `NOT EXISTS`.
- **NULL = NULL** is unknown, not true; use `IS NULL` or `IS DISTINCT FROM`. `COUNT(col)` skips NULLs; `COUNT(*)` doesn't.
- **Alias in WHERE:** not allowed, because `WHERE` is evaluated before `SELECT`; the logical order is FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- **SARGable predicates:** `WHERE created_at >= '2026-01-01'` can use an index; `WHERE YEAR(created_at) = 2026` can't.
- **Deleting 10 million rows:** delete in batches of a few thousand by primary key with short pauses, so locks, WAL volume and replication lag stay small; or, if most of the table goes, copy the rows to keep into a new table and swap; or drop a partition.
- **Fast locally, slow in production:** different data volume and distribution, stale statistics, different plans, or parameter-sensitive plans. Check with `EXPLAIN (ANALYZE, BUFFERS)` on production-like data."

Tham khảo thêm: [Database - Advanced SQL Concepts](https://minhnhat97kg.github.io/docsify/content/database-advance-2/vi.md), [Database - Query Optimization](https://minhnhat97kg.github.io/docsify/content/database-optimization/vi.md)

@@@ db-replication-sharding | Replication and sharding: how do you choose a shard key? | arch | database,replication,sharding,system-design | qa | System design
"**Replication** copies data for availability and read scale. Leader-follower is the norm. Synchronous replication means no data loss on failover but higher write latency; asynchronous is faster but can lose the last writes and creates replica lag. Many setups use one synchronous standby plus asynchronous replicas.

**Sharding** splits data horizontally across databases for write scale. The shard key decides everything:

- High cardinality and even distribution, to avoid hot shards.
- Matches the main access pattern, so most queries hit one shard: user ID or tenant ID for user-centric apps.
- Avoid monotonically increasing keys with range sharding, since all new writes land on one shard.

Costs: cross-shard queries and transactions, rebalancing, and global unique IDs (Snowflake-style IDs or UUIDv7). I shard only after indexing, caching, replicas and partitioning are exhausted."

Tham khảo thêm: [Database System Design: Scalability & Reliability](https://minhnhat97kg.github.io/docsify/content/database-system-design/vi.md)

@@@ pgvector | How would you add vector search with PostgreSQL? | spring | database,postgresql,ai,vector-search | qa | PostgreSQL internals
"The `pgvector` extension stores embeddings as a `vector(n)` column and supports distance operators: cosine `<=>`, which suits text embeddings, L2 `<->`, and inner product.

Two approximate indexes:

- **HNSW:** a layered graph; better recall and speed, but slower to build and more memory. Tunable with `m` and `ef_construction` at build time and `ef_search` at query time.
- **IVFFlat:** clusters vectors into lists; faster to build, but needs data before building and lower recall.

Why pgvector instead of a dedicated vector database: one system to run, vectors filtered and joined with relational data in one query, and transactions. A dedicated store becomes worth it at very large scale or for advanced features. Use cases: semantic search, recommendations, and anomaly detection by finding transactions similar to known fraud."

Tham khảo thêm: [Vector Search & HNSW Index](https://minhnhat97kg.github.io/docsify/content/database-vector-search-hnsw-index/vi.md)
