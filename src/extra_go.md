@@@ go-channels | Buffered vs unbuffered channels: how do they behave? | go | go,concurrency,channel | qa | Go concurrency
"An unbuffered channel is a synchronization point: a send blocks until a receiver takes the value, so both goroutines meet. A buffered channel decouples them up to its capacity: sends block only when the buffer is full, receives only when it's empty.

The rules I keep in mind:

- Sending to or receiving from a **nil** channel blocks forever.
- Sending to a **closed** channel panics; receiving from it returns the zero value immediately, with `ok == false`.
- Only the sender should close a channel, and only once.
- `for v := range ch` ends when the channel is closed and drained.

I use unbuffered channels when I want a handoff guarantee, and a small buffer to absorb bursts. A large buffer that hides a slow consumer is a smell: it only delays back-pressure."

Tham khảo thêm: [Golang: Worker Pool with Context Cancellation](https://minhnhat97kg.github.io/docsify/content/golang-buffered-unbuffered-channel/vi.md)

@@@ go-worker-pool | Implement a worker pool that stops cleanly on cancellation. | go | go,concurrency,context,coding | qa | Go concurrency
Một job channel, N worker đọc bằng `range`, `WaitGroup` để chờ, và `select` trên `ctx.Done()` để dừng sớm. Đây là bài code Go hay gặp nhất.

```go
func Run(ctx context.Context, jobs []Job, workers int) []Result {
    in := make(chan Job)
    out := make(chan Result)
    var wg sync.WaitGroup

    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := range in {
                select {
                case out <- process(ctx, j):
                case <-ctx.Done():
                    return
                }
            }
        }()
    }

    go func() {
        defer close(in)
        for _, j := range jobs {
            select {
            case in <- j:
            case <-ctx.Done():
                return
            }
        }
    }()

    go func() { wg.Wait(); close(out) }()

    var results []Result
    for r := range out {
        results = append(results, r)
    }
    return results
}
```

"The producer closes `in`, so workers' `range` loops end. A separate goroutine closes `out` after all workers finish, so the collector's loop ends. Every blocking send also selects on `ctx.Done()`, so nothing leaks on cancellation. In production I'd use `errgroup.WithContext` with `SetLimit`, which does the same with less code."

Tham khảo thêm: [Golang: Worker Pool with Context Cancellation](https://minhnhat97kg.github.io/docsify/content/golang-buffered-unbuffered-channel/vi.md)

@@@ go-context | How does the context package work? | go | go,context,concurrency | qa | Go concurrency
"A `context.Context` carries a cancellation signal, a deadline and request-scoped values down a call tree. Cancelling a parent cancels all its children, never the other way round.

- `WithCancel` for manual cancellation, `WithTimeout` for a relative duration, `WithDeadline` for an absolute time. Always `defer cancel()` to release resources.
- A child can't outlive its parent: if the child's timeout is longer than the parent's, the parent's deadline wins.
- `context.Background()` is the root for main and tests; `context.TODO()` marks code where I haven't decided which context to pass yet. They behave the same.

Rules: pass it as the first parameter named `ctx`, never store it in a struct, and use values only for request metadata such as trace IDs, not for optional parameters. Database drivers and HTTP clients take the context, so a request timeout really stops the query."

Tham khảo thêm: [Golang: Context Package](https://minhnhat97kg.github.io/docsify/content/golang-context-package/vi.md)

@@@ go-defer | defer, panic and recover: what are the traps? | go | go,error-handling | qa | Go language
"Deferred calls run in LIFO order when the function returns, which is why closing resources in reverse order of opening works naturally.

Two traps:

- **Arguments are evaluated when `defer` executes**, not when the deferred call runs. `defer fmt.Println(i)` prints the value at that moment; wrap it in a closure to see the final value.
- **Named results can be modified by a deferred closure**, which is how you turn a recovered panic into a returned error.

`panic` is for programmer errors and truly unrecoverable states. `recover` only works inside a deferred function in the same goroutine. I use it at boundaries, for example HTTP middleware that turns a panic into a 500 so one bad request doesn't crash the server. It's not a substitute for `if err != nil`: errors are values in Go, and hiding them behind panics makes control flow invisible. A panic in a goroutine you started isn't caught by the caller's recover."

Tham khảo thêm: [Golang: Defer, Panic, Recover](https://minhnhat97kg.github.io/docsify/content/golang-defer-panic-recover/vi.md)

@@@ go-goroutine-leak | What is a goroutine leak and how do you find it? | go | go,concurrency,memory-leak | qa | Go concurrency
"A goroutine that blocks forever and is never collected. Goroutines aren't garbage collected while blocked, so memory and goroutine count grow until the service degrades.

Common causes: sending on a channel nobody reads, for example after the caller timed out; reading from a channel nobody closes; a missing `ctx.Done()` case in a `select`; and HTTP response bodies that are never closed.

Fixes: give every blocking operation a way out through `select` on `ctx.Done()`; use a buffered channel of size 1 when a single result may be abandoned; make sure the owner closes channels.

Detection: watch `runtime.NumGoroutine()` or the `go_goroutines` metric, take a goroutine profile with `pprof` to see where they're blocked, and use `go.uber.org/goleak` in tests to fail when a test leaves goroutines behind."

Tham khảo thêm: [Golang: Goroutine Leak](https://minhnhat97kg.github.io/docsify/content/golang-gorountine-leak/vi.md)

@@@ go-interface-nil | How are interfaces represented, and why can a nil error be non-nil? | go | go,internals,interface | qa | Go language
"An interface value is two words: a type pointer (the `itab`, or just the type for the empty interface) and a data pointer. It's nil only when **both** are nil.

The classic bug: a function returns `*MyError` that is nil, but its return type is `error`. The interface now holds type `*MyError` and a nil data pointer, so `err != nil` is true and the caller treats success as failure.

```go
func find() error {
    var e *MyError = nil
    return e // non-nil interface!
}
```

The fix is to return a literal `nil` on success, and to declare return types as `error`, never as concrete error pointers. Same idea: `var i interface{} = (*int)(nil)` gives `i == nil` false."

Tham khảo thêm: [Golang - Interface Internals](https://minhnhat97kg.github.io/docsify/content/golang-interface/vi.md)

@@@ go-map | How does a Go map work, and how do you make it concurrency-safe? | go | go,internals,map,concurrency | qa | Go language
"A map is a hash table of buckets, each holding up to 8 key-value pairs, with overflow buckets on collision. When the load factor gets too high it grows by doubling and evacuates entries incrementally during later writes, so no single write pays the full cost. Since Go 1.24 the runtime uses a Swiss-table design, but the behaviour you observe is the same. Iteration order is deliberately randomized.

Maps are not safe for concurrent writes, and the runtime crashes with 'concurrent map writes' rather than corrupting data silently. That was a deliberate choice to keep the common single-goroutine case fast.

Options: a plain map with `sync.RWMutex`, which I use in most cases; `sync.Map`, which is optimized for keys written once and read many times, or for goroutines touching disjoint keys; or sharding the map across several mutexes for heavy contention. The Java equivalent of the first option is `Collections.synchronizedMap`, and of the last is `ConcurrentHashMap`."

Tham khảo thêm: [Golang - Map Internals & Thread Safety](https://minhnhat97kg.github.io/docsify/content/golang-map-internals-thread-safety/vi.md)

@@@ go-slices | Explain slice internals and the append gotcha. | go | go,internals,slice | qa | Go language
"A slice is a header of three fields: a pointer to an underlying array, a length and a capacity. Slicing creates a new header over the same array, so two slices can share memory.

`append` writes in place if there's capacity, otherwise it allocates a bigger array and copies. The gotcha: appending to a sub-slice that still has spare capacity overwrites elements of the original slice.

```go
a := []int{1, 2, 3, 4}
b := a[:2]
b = append(b, 99) // a is now [1 2 99 4]
```

Fixes: use a full slice expression `a[:2:2]` to cap the capacity, or `copy` into a new slice. Another trap is holding a small slice of a huge array, which keeps the whole array alive; copy what you need. When I know the final size, I preallocate with `make([]T, 0, n)` to avoid repeated growth."

Tham khảo thêm: [Golang - Slices Internals](https://minhnhat97kg.github.io/docsify/content/golang-slices/vi.md)

@@@ go-stack-heap | Stack vs heap in Go: what is escape analysis? | go | go,internals,memory,performance | qa | Go runtime
"The compiler decides where each value lives. If it can prove a value doesn't outlive the function, it goes on the goroutine's stack, which is cheap to allocate and freed automatically. Otherwise it 'escapes' to the heap and the garbage collector must manage it.

Typical reasons to escape: returning a pointer to a local variable, storing it in an interface, capturing it in a closure that outlives the call, or a size unknown at compile time.

I check with `go build -gcflags='-m'`. In hot paths, fewer heap allocations means less GC work, so I preallocate, reuse buffers with `sync.Pool`, and avoid needless pointers. But I only optimize after a benchmark with `-benchmem` or a profile shows allocations matter. Goroutine stacks start small, around 2 KB, and grow by copying, which is why goroutines are cheap."

Tham khảo thêm: [Golang - Stack & Heap](https://minhnhat97kg.github.io/docsify/content/golang-stack-heap/vi.md)

@@@ go-gc | How does Go's garbage collector work, compared with the JVM? | go | go,gc,performance,jvm | qa | Go runtime
"Go uses a concurrent, non-generational, non-compacting tri-color mark-and-sweep collector. Most marking runs alongside the program with a write barrier, and stop-the-world pauses are typically well under a millisecond.

Tuning has two main knobs: `GOGC`, default 100, which triggers a cycle when the heap grows by that percentage over the live heap; and `GOMEMLIMIT`, a soft memory cap that makes the GC work harder as the process approaches the limit, useful in containers.

Compared with the JVM: Java's collectors such as G1 and ZGC are generational and can compact, which suits allocation-heavy workloads, but have many tuning options. Go trades raw throughput for low latency and simplicity, and relies on escape analysis to keep many values off the heap. In both, the best GC tuning is allocating less."

Tham khảo thêm: [Golang - Garbage Collector](https://minhnhat97kg.github.io/docsify/content/golang-gc/vi.md)

@@@ go-sync | Mutex vs RWMutex vs atomic: when do you use each? | go | go,concurrency,mutex,atomic | qa | Go concurrency
"`sync/atomic` for a single word: counters, flags, or swapping a pointer to an immutable config. It's lock-free and fastest, but can't protect an invariant that spans several fields.

`sync.Mutex` for any critical section that touches several fields or does compound read-modify-write. Keep the section short and never do I/O while holding it.

`sync.RWMutex` when reads greatly outnumber writes and the read section isn't tiny; for very short sections, its extra bookkeeping can make it slower than a plain mutex.

Example: a balance update that checks and then subtracts must be one critical section, or a single atomic compare-and-swap loop; two separate atomic operations still race. And the Go proverb applies: often it's cleaner to give one goroutine ownership of the state and communicate with it through channels."

Tham khảo thêm: [Golang - Mutex vs Atomic vs RWMutex](https://minhnhat97kg.github.io/docsify/content/golang-mutex-vs-atomic-vs-rwmutex/vi.md)

@@@ go-race | Race condition vs data race: how do you detect and fix them? | go | go,concurrency,race-condition | qa | Go concurrency
"A **data race** is two goroutines accessing the same memory at the same time, at least one writing, without synchronization; the result is undefined. A **race condition** is a logic bug where the outcome depends on timing, even if every access is synchronized, for example check-then-act: read the balance, decide, then write.

Classic example: two withdrawals both read 100, both subtract 80, and both write 20: a lost update.

Detection: run tests and staging builds with `go test -race`, which instruments memory access and reports data races with stack traces. It only catches races that actually happen during the run, so tests need concurrency.

Fixes: protect the whole check-and-act with a mutex, use atomic compare-and-swap, or push the check into the database with a conditional `UPDATE ... WHERE balance >= amount` or a row lock, because in a multi-instance service an in-process lock isn't enough."

Tham khảo thêm: [Concurrency: Race Condition](https://minhnhat97kg.github.io/docsify/content/golang-race-condition/vi.md)

@@@ go-money | How do you handle money in code and in the database? | go | go,money,fintech,precision,database | qa | Go language
"Never use floating point: 0.1 + 0.2 isn't 0.3 in binary.

Two safe options: store integers in the smallest unit, such as cents or đồng, which is fast and exact; or use a decimal type, `shopspring/decimal` in Go or `BigDecimal` in Java, created from strings, never from floats. In PostgreSQL I use `NUMERIC(19,4)` or `BIGINT` for minor units, and I store the currency code next to the amount.

Rounding rules matter: I round once at the end, use the rounding mode the business specifies, often banker's rounding (half-even) to avoid systematic bias, and multiply before dividing.

Splitting is the classic follow-up: dividing 100 among three people gives 33.33 three times and loses a cent. The fix is to allocate the remainder deterministically, so one person gets 33.34 and the total is exact."

Tham khảo thêm: [Golang - Money Handling & Precision](https://minhnhat97kg.github.io/docsify/content/golang-money-handling-precision/vi.md)

@@@ go-design | How do SOLID and interfaces look in idiomatic Go? | go | go,solid,design,interface | qa | Go language
"Go has no classes or inheritance, so SOLID shows up through small packages and implicit interfaces.

- **Accept interfaces, return structs:** the consumer defines the small interface it needs, such as `type UserStore interface { Get(ctx, id) (User, error) }`, next to where it's used. The producer returns a concrete type. This keeps interfaces small (interface segregation) and lets tests pass fakes (dependency inversion).
- **Embedding isn't inheritance:** it's composition with method promotion. There's no polymorphism through the embedded type, and the outer type isn't a subtype of it.
- **Single responsibility:** avoid `utils` and `common` packages; name packages for what they provide.
- **Open/closed:** add a new payment method by implementing an interface, not by extending a `switch`.

Wiring happens explicitly in `main`; most Go teams avoid DI frameworks."

Tham khảo thêm: [Golang - SOLID Design Principles](https://minhnhat97kg.github.io/docsify/content/golang-solid-design-principles/vi.md)
