@@@ jc-abstraction-encapsulation | Abstraction vs encapsulation: can you have encapsulation without abstraction? | java | java-core,oop,epam | qa | Java core (EPAM rapid-fire)
"**Abstraction** is about *what* an object exposes: it hides implementation details behind a simple contract, such as an interface `PaymentGateway.charge()` that hides whether it calls Stripe or a bank. **Encapsulation** is about *protecting state*: fields are private and changed only through methods that keep invariants valid.

Yes, you can have encapsulation without abstraction. A class with private fields and plain getters and setters is encapsulated, but it abstracts nothing: callers still see and depend on every detail of its data. Good design uses both: a small public interface, and private state that only the class itself can change consistently."

@@@ jc-string-pool | What is the String constant pool, and where do strings live? | java | java-core,string,jvm,epam | qa | Java core (EPAM rapid-fire)
"String literals are interned in the string pool, which since Java 7 lives in the **heap**, not PermGen. `String a = "hi"; String b = "hi";` gives one object, so `a == b` is true. `new String("hi")` always creates a new heap object, so `==` is false while `equals` is true. `intern()` returns the pooled instance.

Practical points: always compare strings with `equals`; compile-time constants such as `"a" + "b"` are folded into one literal, while runtime concatenation creates new objects. Sharing pooled strings is safe precisely because `String` is immutable."

@@@ jc-interface-private | Can an interface have private methods? Why would it? | java | java-core,java-modern,epam | qa | Java core (EPAM rapid-fire)
"Yes, since Java 9, an interface can have `private` and `private static` methods. Java 8 added `default` and `static` methods, which made interfaces carry real code, and private methods let those default methods share helper logic without duplicating it and without exposing the helper as part of the public contract.

Interface fields are still implicitly `public static final`, and an interface still can't hold instance state. If several default methods need shared mutable state, it's a sign an abstract class is the better fit."

@@@ jc-ocp-violation | Is it ever acceptable to violate the Open/Closed Principle? | java | java-core,solid,design,epam | qa | Java core (EPAM rapid-fire)
"Yes, when the cost of the abstraction is higher than the benefit. In a small codebase, a prototype or a one-off fix, adding a `case` to an existing `switch` is simpler and clearer than introducing a strategy interface with one implementation. YAGNI applies.

I apply OCP where variation is real and recurring: payment methods, pricing rules, notification channels, plugins. A useful trigger is the rule of three: the third time I edit the same `switch` for a new variant, I extract an interface. Sealed interfaces with exhaustive `switch` in Java 21 are a middle ground: modification is explicit, and the compiler shows every place that must change."

@@@ jc-finally | Can a finally block override an exception thrown in try? | java | java-core,exception,epam | qa | Java core (EPAM rapid-fire)
"Yes. If `finally` executes a `return` or throws a new exception, the original exception from `try` is silently discarded. That's a well-known bug source, so `return` inside `finally` is considered bad practice and many linters flag it.

Related details: `finally` runs even when `try` returns, but the return value of a primitive is already computed, so changing the variable in `finally` doesn't change what's returned. It doesn't run if the JVM exits with `System.exit` or crashes. For resources I use try-with-resources, which closes them automatically and keeps exceptions thrown by `close()` as **suppressed** exceptions instead of losing the original."

@@@ jc-collection-map | Why doesn't Map extend Collection? HashMap vs TreeMap? | java | java-core,collections,epam | qa | Java core (EPAM rapid-fire)
"`Collection` models a group of single elements with `add(E)`; a `Map` models key-value pairs, so `add(E)` has no natural meaning. Instead, `Map` exposes collection views: `keySet()`, `values()` and `entrySet()`.

**HashMap vs TreeMap:**

| | HashMap | TreeMap |
|---|---|---|
| Structure | Hash table of buckets | Red-black tree |
| Order | None | Sorted by key (natural or `Comparator`) |
| get/put | O(1) average, O(log n) worst | O(log n) |
| Null key | One allowed | Not allowed (throws `NullPointerException` because it must compare keys), unless a custom comparator handles null |
| Extra API | — | `firstKey`, `floorKey`, `subMap`, range queries |

`LinkedHashMap` keeps insertion or access order, which is how a simple LRU cache is built."

@@@ sp-without-sba | Can a Spring Boot app run without @SpringBootApplication? | spring | spring,spring-boot,epam | qa | Spring (EPAM rapid-fire)
"Yes. `@SpringBootApplication` is just a convenience meta-annotation combining three annotations: `@SpringBootConfiguration` (a specialized `@Configuration`), `@EnableAutoConfiguration`, and `@ComponentScan` of the class's package and sub-packages. Putting those three on the main class, or configuring components explicitly, works the same, and `SpringApplication.run(...)` starts the app either way.

A common follow-up: beans in packages outside the main class's package aren't found, because component scanning starts from that package. Fix it by moving the main class to the root package or setting `scanBasePackages`."

@@@ sp-dispatcher | What is DispatcherServlet? Walk through the Spring MVC request flow. | spring | spring,spring-mvc,epam | qa | Spring (EPAM rapid-fire)
"`DispatcherServlet` is the **front controller**: every HTTP request enters through it. The flow:

1. Servlet filters run first, including the Spring Security filter chain.
2. `DispatcherServlet` asks the `HandlerMapping` which controller method matches the URL and HTTP method.
3. Interceptors' `preHandle` run.
4. A `HandlerAdapter` invokes the method, resolving arguments such as `@PathVariable`, `@RequestParam` and `@RequestBody` (via `HttpMessageConverter`s, for example Jackson for JSON) and running validation.
5. The return value is written as the response body for `@RestController`, or resolved to a view by a `ViewResolver` for server-rendered pages.
6. Exceptions go to `HandlerExceptionResolver`s, which is where `@ControllerAdvice` with `@ExceptionHandler` plugs in.

In Spring Boot it's auto-configured; you rarely touch it directly."

@@@ sp-param-path | @RequestParam vs @PathVariable: can you use both in one method? | spring | spring,spring-mvc,rest,epam | qa | Spring (EPAM rapid-fire)
"`@PathVariable` binds a segment of the URL path and identifies a resource: `/users/{id}`. `@RequestParam` binds a query string parameter, typically optional, for filtering, sorting or paging: `/users?status=active&page=2`.

Yes, they combine naturally:

```java
@GetMapping("/users/{id}/orders")
public Page<OrderDto> orders(@PathVariable long id,
                             @RequestParam(defaultValue = "0") int page,
                             @RequestParam(required = false) String status) { ... }
```

REST convention: identity in the path, optional modifiers in the query. `@RequestParam` is required by default, so missing values give a 400 unless I set `required = false` or a default."

@@@ sp-profiles | How do you configure different databases per environment? | spring | spring,spring-boot,configuration,epam | qa | Spring (EPAM rapid-fire)
"With **Spring profiles**. Common settings go in `application.yml`, environment-specific ones in `application-dev.yml`, `application-prod.yml` and so on, and the active profile is chosen at startup with `spring.profiles.active` or the `SPRING_PROFILES_ACTIVE` environment variable. Beans can also be limited with `@Profile("dev")`.

In practice, I keep secrets such as database passwords out of these files entirely: they come from environment variables, Kubernetes Secrets, or a secret manager, and the same image runs in every environment with only configuration changing. Spring Boot's property precedence lets environment variables override file values, which is how that works without code changes."

@@@ arch-rest | What are REST principles? Is REST always stateless? | arch | rest,api-design,epam | qa | Microservices (EPAM rapid-fire)
"REST constraints: client-server separation; **statelessness**, where every request carries everything needed to process it; cacheable responses; a uniform interface built on resources, URIs, standard HTTP methods and representations; and a layered system, so clients don't know if they talk to a proxy, gateway or the real server. Code on demand is optional.

Statelessness is about **the server not keeping client session state between requests**. A REST API can still identify a user on every request with a token such as a JWT; that's stateless because the token travels with each request. Storing a server-side session tied to a cookie technically breaks the constraint and makes horizontal scaling harder, since requests then need sticky sessions or a shared session store like Redis. The business data itself, in the database, is of course state; the constraint is only about conversational state."

@@@ arch-cb-open | What happens if a circuit breaker stays open too long? | arch | microservices,resilience,circuit-breaker,epam | qa | Microservices (EPAM rapid-fire)
"A circuit breaker has three states. **Closed:** calls pass and failures are counted. **Open:** calls fail fast without reaching the dependency. **Half-open:** after a wait duration, a few trial calls are allowed; success closes it, failure opens it again.

If it stays open too long, the dependency may have recovered while we keep rejecting requests, which turns a short outage into a long one for users. Causes: a wait duration that's too long, or a half-open trial that's too strict or keeps hitting a cold dependency.

Tuning in Resilience4j: a reasonable `waitDurationInOpenState`, a small `permittedNumberOfCallsInHalfOpenState`, a sliding window and threshold based on real traffic, and slow-call thresholds. While open, return a **fallback**, such as cached data or a degraded response, and **alert** on state changes so humans know the dependency is down."

@@@ eng-testing | TDD vs BDD, and what is the test pyramid? | devops | testing,tdd,bdd,epam | qa | Engineering practice (EPAM rapid-fire)
"**TDD**: write a failing unit test, write the minimum code to pass, refactor: red, green, refactor. It drives design toward small, testable units.

**BDD**: describes behaviour in business language, often Given/When/Then scenarios with Cucumber, so product people and engineers agree on acceptance criteria.

**Test pyramid**: many fast unit tests at the base, fewer integration tests in the middle (database, messaging, using Testcontainers), and very few slow end-to-end or UI tests at the top. An inverted pyramid, mostly UI tests, gives slow, flaky pipelines.

Honest answer about my practice: I write tests alongside the code rather than strictly test-first, but I do use TDD for tricky business logic and bug fixes, where a failing test reproduces the bug first."

@@@ eng-sdlc-agile | What is the SDLC, and why is Agile usually preferred over Waterfall? | behavioral | sdlc,agile,process,epam | qa | Engineering practice (EPAM rapid-fire)
"The SDLC is the lifecycle of building software: requirements, design, implementation, testing, deployment and maintenance.

**Waterfall** runs those phases once, in sequence. It suits fixed, well-understood requirements, for example regulated or contract-fixed projects, but changes late in the project are expensive and users see value only at the end.

**Agile** runs short iterations, typically two-week sprints in Scrum, each delivering a working increment, with regular feedback from stakeholders. It handles changing requirements and reduces risk because problems surface early.

At DXC, the insurance clients [mô tả quy trình thật: Scrum 2 tuần, sprint review với khách hàng, ...]. At Opswat we [mô tả]. I've seen hybrid setups too: fixed-scope contracts on the client side, run internally in sprints."

*Ghi chú: câu "Agile practices in your project" phải trả lời bằng dự án thật: độ dài sprint, các buổi họp, ai là PO, công cụ (Jira), cách ước lượng.*

@@@ dsa-rain-water | Trapping Rain Water: how much water is trapped between bars? | coding | dsa,two-pointers,epam | qa | DSA
Nước tại vị trí i bằng `min(maxLeft, maxRight) - height[i]`. Dùng hai con trỏ từ hai đầu: phía nào có max nhỏ hơn thì nước ở phía đó đã được xác định, nên xử lý phía đó rồi tiến vào. Time O(n), space O(1). Cách dễ nói hơn là dùng hai mảng prefix max và suffix max, O(n) space.

```java
int trap(int[] h) {
    int left = 0, right = h.length - 1;
    int leftMax = 0, rightMax = 0, water = 0;
    while (left < right) {
        if (h[left] < h[right]) {
            leftMax = Math.max(leftMax, h[left]);
            water += leftMax - h[left];
            left++;
        } else {
            rightMax = Math.max(rightMax, h[right]);
            water += rightMax - h[right];
            right--;
        }
    }
    return water;
}
```

"Why it's correct: when `h[left] < h[right]`, there is a bar on the right at least as tall as `h[left]`, so the water at `left` is limited only by `leftMax`. Example: `[0,1,0,2,1,0,1,3,2,1,2,1]` traps 6."
