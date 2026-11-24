@@@ ai-tools-13 | Bạn dùng công cụ AI coding trong công việc thế nào? / How do you use AI coding tools in your work? | ai | | override
### Tiếng Việt

Đây là câu **gần như chắc chắn bị hỏi** ở vòng technical và vòng manager năm 2026. Interviewer muốn biết hai điều: bạn có **tận dụng AI để làm nhanh hơn** không, và bạn có **giữ được chất lượng và trách nhiệm** với code không.

**Khung trả lời (khoảng 60–90 giây):**
1. **Công cụ:** kể đúng công cụ bạn dùng thật (Claude Code, Cursor, GitHub Copilot, ChatGPT...), dùng ở mức nào: autocomplete, chat, hay agent tự sửa nhiều file và chạy test.
2. **Dùng cho việc gì:** đọc hiểu codebase lạ, viết test, boilerplate, refactor, migration, viết tài liệu, debug với log và stack trace, review PR, viết script.
3. **Quy trình:** yêu cầu agent **lập kế hoạch trước**, chia việc nhỏ, có lệnh kiểm chứng rõ ràng (test, build, lint), review diff trước khi commit.
4. **Kiểm soát:** tự review mọi dòng; không merge code mình không giải thích được; không đưa secret hay dữ liệu khách hàng vào; tuân thủ chính sách công ty.
5. **Kết quả cụ thể:** một con số hoặc ví dụ thật.
6. **Giới hạn:** nơi bạn không dùng AI hoặc dùng rất cẩn thận (logic thanh toán, bảo mật, thiết kế kiến trúc).

**Câu trả lời mẫu (thay phần trong ngoặc bằng chuyện thật):**
*"Tôi dùng [Claude Code / Cursor] hằng ngày, chủ yếu ở chế độ agent. Với việc mới, tôi cho agent đọc code liên quan và đề xuất kế hoạch trước; tôi sửa kế hoạch rồi mới cho nó viết code, theo từng bước nhỏ, mỗi bước chạy test. Repo có file hướng dẫn chung (lệnh build, quy ước code, những thư mục không được đụng), nên agent ít sai hơn. Ví dụ ở [Opswat], tôi dùng agent để [viết integration test với Testcontainers cho 12 API cũ / migrate X sang Y], xong trong [2 ngày] thay vì khoảng [1 tuần]. Nhưng tôi vẫn review từng diff: đã có lần agent [gọi một method không tồn tại / bỏ qua một case null], test của tôi bắt được. Với phần nhạy cảm như xác thực hay tiền, tôi viết hoặc kiểm tra kỹ bằng tay."*

**Tránh:**
- "Tôi không dùng AI": nghe như lạc hậu, trừ khi công ty cấm và bạn giải thích được.
- "AI viết hết, tôi chỉ chấp nhận": nghe như không chịu trách nhiệm.
- Nói chung chung, không có ví dụ hay con số.

### English

This question is **almost certain to come up** in technical and manager rounds in 2026. The interviewer wants to know two things: whether you **use AI to move faster**, and whether you **keep quality and ownership** of the code.

**Answer framework (about 60–90 seconds):**
1. **Tools:** name the tools you really use (Claude Code, Cursor, GitHub Copilot, ChatGPT...) and at which level: autocomplete, chat, or an agent that edits many files and runs tests.
2. **What for:** understanding unfamiliar codebases, writing tests, boilerplate, refactoring, migrations, documentation, debugging from logs and stack traces, reviewing PRs, writing scripts.
3. **Process:** ask the agent for **a plan first**, split work into small steps, give clear verification commands (tests, build, lint), review the diff before committing.
4. **Control:** review every line yourself; never merge code you can't explain; don't paste secrets or customer data; follow company policy.
5. **Concrete outcome:** one real number or example.
6. **Limits:** where you don't use AI or use it very carefully (payment logic, security, architecture decisions).

**A model answer (replace the bracketed parts with your real story):**
*"I use [Claude Code / Cursor] daily, mostly in agent mode. For new work I have the agent read the relevant code and propose a plan first; I correct the plan and only then let it write code, in small steps, running the tests after each one. The repo has a shared instructions file (build commands, coding conventions, folders not to touch), so the agent makes fewer mistakes. For example, at [Opswat] I used an agent to [write Testcontainers integration tests for 12 legacy APIs / migrate X to Y], finishing in [2 days] instead of about [a week]. But I still review every diff: once the agent [called a method that doesn't exist / skipped a null case], and my tests caught it. For sensitive parts such as authentication or money, I write or check things carefully by hand."*

**Avoid:**
- "I don't use AI": it sounds out of date, unless your company forbids it and you can explain that.
- "AI writes everything and I just accept it": it sounds like you don't take ownership.
- Vague answers with no example or number.

@@@ ai-dev-vibe-coding | Vibe coding là gì? Khác gì với AI-assisted engineering? Khi nào chấp nhận được? / What is vibe coding, how does it differ from AI-assisted engineering, and when is it acceptable? | ai | vibe-coding,ai-dev | qa | AI-assisted development
### Tiếng Việt

**Vibe coding** (thuật ngữ do Andrej Karpathy đặt đầu năm 2025): mô tả bằng lời điều mình muốn, để AI viết toàn bộ code, **chấp nhận kết quả mà không đọc kỹ code**, lỗi thì dán thông báo lỗi lại cho AI sửa, đánh giá bằng việc "chạy được và trông ổn".

**AI-assisted engineering** (hay "agentic engineering"): vẫn dùng AI viết phần lớn code, nhưng **kỹ sư chịu trách nhiệm**: đặt yêu cầu và thiết kế, review diff, có test kiểm chứng, hiểu code trước khi merge.

| | Vibe coding | AI-assisted engineering |
|---|---|---|
| Ai hiểu code | Không ai thật sự hiểu | Kỹ sư hiểu và giải thích được |
| Kiểm chứng | Chạy thử, nhìn bằng mắt | Test tự động, review, CI, lint, scan bảo mật |
| Thiết kế | Để AI tự quyết | Kỹ sư quyết kiến trúc, AI triển khai |
| Tốc độ ban đầu | Rất nhanh | Nhanh |
| Bảo trì về sau | Khó, nợ kỹ thuật tăng nhanh | Bền vững |
| Rủi ro | Lỗ hổng bảo mật, lỗi logic ẩn, code trùng lặp | Được kiểm soát |

**Khi nào vibe coding chấp nhận được:**
- Prototype, demo, thử nghiệm ý tưởng sẽ vứt đi.
- Script dùng một lần, công cụ cá nhân, trang nội bộ không chạm dữ liệu nhạy cảm.
- Học một công nghệ mới, khám phá API.

**Khi nào không:**
- Code production, đặc biệt là xác thực, phân quyền, thanh toán, dữ liệu cá nhân, xử lý đồng thời.
- Code nhóm sẽ bảo trì lâu dài.
- Hệ thống có yêu cầu compliance (audit, bảo mật).

**Rủi ro điển hình của code AI không được review:** thiếu kiểm tra quyền (IDOR), SQL ghép chuỗi, secret viết cứng trong code, bắt và nuốt exception, gọi API hoặc thư viện **không tồn tại**, cài **package tên gần giống** package thật (slopsquatting), test chỉ kiểm tra mock chứ không kiểm tra hành vi, thêm abstraction không cần thiết.

**Câu trả lời mẫu:** *"Tôi vibe code cho prototype hoặc script cá nhân để thử nhanh. Với code production thì tôi dùng AI như một lập trình viên rất nhanh cần được giám sát: tôi quyết định thiết kế, AI triển khai theo từng bước nhỏ, mọi thay đổi phải qua test và review của tôi. Tiêu chí là tôi phải giải thích được mọi dòng trước khi merge."*

### English

**Vibe coding** (a term coined by Andrej Karpathy in early 2025): describe what you want in words, let the AI write all the code, **accept the result without reading it closely**, paste error messages back for the AI to fix, and judge success by "it runs and looks fine".

**AI-assisted engineering** (or "agentic engineering"): AI still writes most of the code, but **the engineer stays accountable**: setting requirements and design, reviewing diffs, verifying with tests, and understanding the code before merging.

| | Vibe coding | AI-assisted engineering |
|---|---|---|
| Who understands the code | Nobody really | The engineer understands it and can explain it |
| Verification | Try it and eyeball it | Automated tests, review, CI, linting, security scans |
| Design | Left to the AI | The engineer decides the architecture; the AI implements |
| Initial speed | Very fast | Fast |
| Long-term maintenance | Hard; technical debt grows fast | Sustainable |
| Risks | Security holes, hidden logic bugs, duplicated code | Under control |

**When vibe coding is acceptable:**
- Prototypes, demos, throwaway experiments.
- One-off scripts, personal tools, internal pages that touch no sensitive data.
- Learning a new technology or exploring an API.

**When it isn't:**
- Production code, especially authentication, authorization, payments, personal data and concurrency.
- Code a team will maintain for a long time.
- Systems with compliance requirements (audit, security).

**Typical risks of unreviewed AI code:** missing authorization checks (IDOR), string-concatenated SQL, hard-coded secrets, caught-and-swallowed exceptions, calls to APIs or libraries **that don't exist**, installing **packages with names similar to real ones** (slopsquatting), tests that only check mocks rather than behaviour, and unnecessary abstractions.

**A model answer:** *"I vibe code prototypes or personal scripts to try things quickly. For production code I treat AI as a very fast developer who needs supervision: I decide the design, the AI implements in small steps, and every change goes through tests and my review. My rule is that I must be able to explain every line before it's merged."*

@@@ ai-dev-agentic-tools | AI coding agent (Claude Code, Cursor, Copilot agent) hoạt động thế nào? Khác autocomplete và chat ra sao? / How do AI coding agents (Claude Code, Cursor, Copilot agent mode) work, and how do they differ from autocomplete and chat? | ai | agentic-coding,ai-dev | qa | AI-assisted development
### Tiếng Việt

**Các mức độ hỗ trợ của AI trong lập trình:**

| Mức | Cách hoạt động | Ví dụ | Bạn kiểm soát |
|---|---|---|---|
| **Autocomplete** | Gợi ý vài dòng tiếp theo khi gõ | Copilot inline, Cursor Tab | Từng dòng |
| **Chat** | Hỏi đáp, dán code vào, copy kết quả ra | ChatGPT, Claude chat | Từng đoạn |
| **Agent trong IDE hoặc terminal** | Tự đọc file, sửa nhiều file, **chạy lệnh** (build, test), đọc kết quả, lặp lại cho tới khi xong | Claude Code, Cursor Agent, Copilot agent mode, Codex | Từng nhiệm vụ, duyệt từng thao tác hoặc diff |
| **Agent chạy nền / bất đồng bộ** | Nhận issue, tự làm trên máy cloud, mở pull request | Copilot coding agent, Claude Code trên web, Codex cloud | Review PR |

**Vòng lặp của một coding agent** (giống agent nói chung: suy luận, hành động, quan sát):
```
Nhiệm vụ → đọc code liên quan (grep, mở file) → lập kế hoạch → sửa file
        → chạy test / build / lint → đọc lỗi → sửa tiếp → ... → báo kết quả + diff
```
Agent dùng **tool**: đọc và ghi file, tìm kiếm, chạy shell, gọi web, và các **MCP server** (Jira, GitHub, database, trình duyệt).

**Vì sao agent mạnh hơn chat:** nó **tự kiểm chứng** bằng cách chạy test và đọc lỗi thật, thay vì đoán. Nên chất lượng phụ thuộc lớn vào việc repo có **test tốt và lệnh kiểm chứng rõ ràng** hay không.

**Kiểm soát an toàn:**
- **Chế độ quyền:** hỏi trước khi sửa file hoặc chạy lệnh; tự duyệt các lệnh an toàn (chạy test); chặn lệnh nguy hiểm (`rm -rf`, `git push --force`, gọi production).
- **Sandbox, container, git worktree** để agent không phá môi trường thật.
- Không cấp **credential production** cho agent; dùng tài khoản và dữ liệu test.
- Mọi thay đổi đi qua **git**: dễ xem diff, dễ revert.

**Điểm yếu cần biết:**
- Context window có hạn: phiên làm việc dài làm agent "quên" hoặc lẫn lộn, nên chia nhỏ và bắt đầu phiên mới cho việc mới.
- Có thể tự tin sửa sai chỗ, xóa test cho "pass", hoặc làm quá phạm vi yêu cầu.
- Kém với yêu cầu mơ hồ, logic nghiệp vụ ngầm không có trong code.

### English

**Levels of AI assistance in programming:**

| Level | How it works | Examples | You control |
|---|---|---|---|
| **Autocomplete** | Suggests the next few lines as you type | Copilot inline, Cursor Tab | Each line |
| **Chat** | Q&A; paste code in, copy results out | ChatGPT, Claude chat | Each snippet |
| **Agents in the IDE or terminal** | Read files, edit many files, **run commands** (build, test), read the output, and loop until done | Claude Code, Cursor Agent, Copilot agent mode, Codex | Each task, approving each action or diff |
| **Background / asynchronous agents** | Take an issue, work on a cloud machine, open a pull request | Copilot coding agent, Claude Code on the web, Codex cloud | The PR review |

**A coding agent's loop** (the same as agents in general: reason, act, observe):
```
Task → read relevant code (grep, open files) → plan → edit files
     → run tests / build / lint → read errors → fix → ... → report the result + diff
```
The agent uses **tools**: reading and writing files, search, a shell, the web, and **MCP servers** (Jira, GitHub, databases, a browser).

**Why agents beat chat:** they **verify themselves** by running tests and reading real errors instead of guessing. So quality depends heavily on whether the repo has **good tests and clear verification commands**.

**Safety controls:**
- **Permission modes:** ask before editing files or running commands; auto-approve safe commands (running tests); block dangerous ones (`rm -rf`, `git push --force`, calls to production).
- **Sandboxes, containers, git worktrees** so the agent can't damage the real environment.
- Never give the agent **production credentials**; use test accounts and test data.
- Every change goes through **git**: easy to inspect the diff, easy to revert.

**Weaknesses to know:**
- The context window is limited: long sessions make the agent "forget" or mix things up, so split work and start a fresh session for a new task.
- It can confidently edit the wrong place, delete tests to make them "pass", or go beyond the requested scope.
- It struggles with vague requirements and implicit business logic that isn't in the code.

@@@ ai-dev-workflow | Quy trình làm việc hiệu quả với AI coding agent trên một tính năng thật là gì? / What's an effective workflow for building a real feature with an AI coding agent? | ai | ai-workflow,agentic-coding | qa | AI-assisted development
### Tiếng Việt

**Quy trình 5 bước: Khám phá, Lập kế hoạch, Triển khai, Kiểm chứng, Hoàn tất.**

**1. Khám phá (explore):** cho agent đọc code liên quan **trước khi viết gì**. *"Đọc `OrderService`, `PaymentClient` và các test liên quan. Giải thích luồng tạo đơn hiện tại. Chưa sửa gì."* Bạn kiểm tra xem agent hiểu đúng chưa.

**2. Lập kế hoạch (plan):** yêu cầu kế hoạch cụ thể: sửa file nào, thêm class gì, migration DB, test nào, rủi ro gì. **Bạn sửa kế hoạch**; đây là chỗ bạn đưa vào hiểu biết về kiến trúc và nghiệp vụ. Với việc lớn, lưu kế hoạch thành file (spec) trong repo.

**3. Triển khai theo bước nhỏ (implement):** mỗi bước là một thay đổi có thể review được (vài file). Cách hiệu quả là **TDD với AI**: viết (hoặc cho agent viết) test trước, xác nhận test **fail đúng lý do**, rồi mới cho agent viết code để test pass, và dặn **không được sửa test**.

**4. Kiểm chứng (verify):** agent chạy test, build, lint, type check. Bạn **đọc diff**: logic đúng chưa, có xử lý lỗi và case biên, có làm quá phạm vi, có lặp code đã có sẵn không. Với UI hoặc API thì chạy thử thật.

**5. Hoàn tất (commit):** commit nhỏ, message rõ; agent có thể viết mô tả PR, nhưng bạn kiểm tra lại. Mở **phiên mới** cho việc tiếp theo để context sạch.

**Cách viết yêu cầu tốt (prompt cho coding agent):**
```text
Mục tiêu: thêm API hủy đơn POST /api/orders/{id}/cancel.
Bối cảnh: theo pattern của OrderController.confirm(); trạng thái trong OrderStatus.
Ràng buộc: chỉ hủy khi PENDING hoặc CONFIRMED; phát sự kiện OrderCancelled qua outbox;
           không đổi schema bảng orders; không thêm thư viện mới.
Xong khi: ./mvnw test pass; có test cho cả 3 trạng thái và trường hợp đơn của user khác (403).
Trước khi code: đưa kế hoạch cho tôi duyệt.
```
Bao gồm: **mục tiêu, bối cảnh (file, pattern có sẵn), ràng buộc, tiêu chí hoàn thành, cách kiểm chứng**.

**Khi agent đi sai hướng:** dừng sớm, đừng cố sửa bằng nhiều lượt chat. Revert (`git checkout`), làm rõ yêu cầu hoặc kế hoạch, rồi chạy lại trong phiên mới. Sửa vòng vo trong một phiên dài thường càng tệ hơn.

**Việc AI làm rất tốt:** viết test cho code có sẵn, boilerplate (DTO, mapper, cấu hình), refactor cơ học, migration phiên bản thư viện, đọc hiểu code lạ, viết script, debug từ stack trace, viết tài liệu.
**Việc cần bạn dẫn dắt nhiều:** thiết kế kiến trúc, logic nghiệp vụ phức tạp, đồng thời và giao dịch, bảo mật, tối ưu hiệu năng (phải đo).

### English

**A 5-step workflow: Explore, Plan, Implement, Verify, Commit.**

**1. Explore:** have the agent read the relevant code **before writing anything**. *"Read `OrderService`, `PaymentClient` and their tests. Explain the current order-creation flow. Don't change anything yet."* You check that it understood correctly.

**2. Plan:** ask for a concrete plan: which files change, which classes are added, DB migrations, which tests, what risks. **You correct the plan**; this is where you bring in your architectural and business knowledge. For large work, save the plan as a file (a spec) in the repo.

**3. Implement in small steps:** each step is a reviewable change (a few files). An effective approach is **TDD with AI**: write the tests first (or have the agent write them), confirm they **fail for the right reason**, then let the agent write code until they pass, telling it **not to modify the tests**.

**4. Verify:** the agent runs tests, build, lint and type checks. You **read the diff**: is the logic right, are errors and edge cases handled, did it go beyond scope, did it duplicate code that already exists? For UIs or APIs, try them for real.

**5. Commit:** small commits with clear messages; the agent can draft the PR description, but you check it. Start a **fresh session** for the next task so the context stays clean.

**Writing a good request (a prompt for a coding agent):**
```text
Goal: add a cancel-order API, POST /api/orders/{id}/cancel.
Context: follow the pattern of OrderController.confirm(); statuses live in OrderStatus.
Constraints: only cancel when PENDING or CONFIRMED; publish OrderCancelled via the outbox;
             don't change the orders table schema; no new libraries.
Done when: ./mvnw test passes; tests cover all 3 statuses and another user's order (403).
Before coding: give me a plan to approve.
```
It covers the **goal, context (files, existing patterns), constraints, definition of done, and how to verify**.

**When the agent goes in the wrong direction:** stop early instead of fixing it through many chat turns. Revert (`git checkout`), clarify the requirements or plan, and rerun in a fresh session. Going around in circles in one long session usually makes things worse.

**What AI does very well:** tests for existing code, boilerplate (DTOs, mappers, configuration), mechanical refactors, library version migrations, understanding unfamiliar code, scripts, debugging from stack traces, documentation.
**What needs your strong guidance:** architecture, complex business logic, concurrency and transactions, security, performance tuning (which needs measurement).

@@@ ai-dev-context | Context engineering cho AI coding agent là gì? (CLAUDE.md, AGENTS.md, rules, MCP) / What is context engineering for AI coding agents? (CLAUDE.md, AGENTS.md, rules, MCP) | ai | context-engineering,agentic-coding | qa | AI-assisted development
### Tiếng Việt

**Ý chính:** chất lượng output của agent phụ thuộc vào **đúng thông tin ở đúng lúc** trong context window, hơn là vào câu chữ khéo léo của prompt. **Context engineering** là việc thiết kế những gì agent được thấy.

**1. File hướng dẫn trong repo** (agent tự đọc mỗi phiên):
- `CLAUDE.md` (Claude Code), `AGENTS.md` (chuẩn mở, nhiều công cụ đọc), `.cursor/rules` (Cursor), `.github/copilot-instructions.md` (Copilot).
- Nên có: **lệnh build, test, lint, chạy local**; kiến trúc và cấu trúc thư mục ngắn gọn; quy ước code (đặt tên, xử lý lỗi, logging); **những điều cấm** (không sửa file migration đã chạy, không thêm dependency khi chưa hỏi); cách viết test.
- Ngắn gọn, cụ thể, commit vào repo để **cả nhóm dùng chung** và review như code. Mỗi lần agent mắc lỗi lặp lại thì thêm một dòng hướng dẫn.

```markdown
# Order service
## Commands
- Build/test: `./mvnw verify` · Single test: `./mvnw test -Dtest=OrderServiceTest`
## Conventions
- Hexagonal: domain/ has no Spring imports. Controllers only map DTOs.
- Errors: throw DomainException; mapped to ProblemDetail in GlobalExceptionHandler.
- Events go through the outbox table, never kafkaTemplate directly.
## Don't
- Edit applied Flyway migrations; add a new V__ file instead.
- Add dependencies without asking.
```

**2. Cung cấp đúng context cho từng việc:** chỉ file, class, test liên quan; dán stack trace hoặc log thật; đưa link tài liệu API hoặc spec; ví dụ một chỗ làm đúng pattern để agent bắt chước.

**3. Mở rộng khả năng bằng tool:**
- **MCP server:** cho agent đọc Jira ticket, GitHub issue, schema database (chỉ đọc), tài liệu nội bộ, điều khiển trình duyệt để kiểm tra UI.
- **Skills / slash commands / prompt dùng lại:** đóng gói quy trình lặp lại (tạo migration, viết release note, review theo checklist).
- **Hooks:** tự chạy formatter hoặc lint sau mỗi lần sửa file, chặn lệnh nguy hiểm.

**4. Giữ context sạch:**
- Context càng dài, chất lượng càng giảm và càng tốn token. **Mỗi việc một phiên**, xóa hoặc tóm tắt khi chuyển việc.
- Dùng **subagent** cho việc tìm kiếm hoặc đọc nhiều file: subagent đọc rồi chỉ trả về tóm tắt, context chính không bị đầy.
- Lưu kế hoạch hoặc tiến độ ra file để phiên sau đọc lại, thay vì dựa vào lịch sử chat.

**5. Bảo mật context:** không đưa secret hay dữ liệu thật của khách hàng vào; `.env` nằm ngoài phạm vi agent đọc; nhớ rằng nội dung từ web, issue hay tài liệu có thể chứa **prompt injection**.

### English

**The key idea:** an agent's output quality depends on having **the right information at the right time** in its context window, more than on clever prompt wording. **Context engineering** is designing what the agent gets to see.

**1. Instruction files in the repo** (the agent reads them every session):
- `CLAUDE.md` (Claude Code), `AGENTS.md` (an open convention many tools read), `.cursor/rules` (Cursor), `.github/copilot-instructions.md` (Copilot).
- Include: **build, test, lint and run-locally commands**; a brief architecture and folder layout; conventions (naming, error handling, logging); **prohibitions** (don't edit applied migrations, don't add dependencies without asking); how to write tests.
- Keep them short and specific, and commit them so **the whole team shares them** and reviews them like code. Whenever the agent repeats a mistake, add a line.

```markdown
# Order service
## Commands
- Build/test: `./mvnw verify` · Single test: `./mvnw test -Dtest=OrderServiceTest`
## Conventions
- Hexagonal: domain/ has no Spring imports. Controllers only map DTOs.
- Errors: throw DomainException; mapped to ProblemDetail in GlobalExceptionHandler.
- Events go through the outbox table, never kafkaTemplate directly.
## Don't
- Edit applied Flyway migrations; add a new V__ file instead.
- Add dependencies without asking.
```

**2. Give the right context for each task:** only the relevant files, classes and tests; paste real stack traces or logs; link API docs or specs; point to one place that follows the pattern correctly so the agent can copy it.

**3. Extend capabilities with tools:**
- **MCP servers:** let the agent read Jira tickets, GitHub issues, the database schema (read-only), internal docs, or drive a browser to check the UI.
- **Skills / slash commands / reusable prompts:** package repeated workflows (creating a migration, writing release notes, reviewing against a checklist).
- **Hooks:** run the formatter or linter automatically after each file edit, block dangerous commands.

**4. Keep the context clean:**
- The longer the context, the lower the quality and the higher the token cost. **One task per session**; clear or summarize when switching.
- Use **subagents** for searching or reading many files: the subagent reads and returns only a summary, so the main context doesn't fill up.
- Save plans or progress to a file for the next session to read, instead of relying on chat history.

**5. Context security:** no secrets or real customer data; keep `.env` out of the agent's reach; remember that content from the web, issues or documents may contain **prompt injection**.

@@@ ai-dev-review | Làm sao review và kiểm soát chất lượng code do AI sinh ra? / How do you review and control the quality of AI-generated code? | ai | code-review,ai-dev,security | qa | AI-assisted development
### Tiếng Việt

**Nguyên tắc:** code do AI viết được **đối xử như code của một đồng nghiệp mới rất nhanh nhưng hay tự tin sai**. Bạn là người chịu trách nhiệm khi merge.

**Các lỗi hay gặp ở code AI và cách phát hiện:**

| Lỗi | Ví dụ | Cách phát hiện |
|---|---|---|
| **API hoặc thư viện "ảo"** | Gọi method không tồn tại, dùng option cấu hình sai phiên bản | Compile, test, đọc tài liệu chính thức |
| **Package giả mạo** (slopsquatting) | Thêm dependency có tên gần giống package thật | Kiểm tra từng dependency mới; dùng dependency scanning |
| **Lỗ hổng bảo mật** | Thiếu kiểm tra quyền (IDOR), SQL ghép chuỗi, log lộ token, secret viết cứng | SAST (SonarQube, Semgrep), secret scanning, review checklist bảo mật |
| **Test vô nghĩa** | Test chỉ kiểm tra mock được gọi; hoặc **sửa assertion cho khớp code sai**; xóa test để "pass" | Đọc test kỹ như đọc code; mutation testing (PIT) |
| **Xử lý lỗi kém** | `catch (Exception e) {}`, trả `null`, không timeout khi gọi ra ngoài | Review, lint rule |
| **Làm quá phạm vi** | Sửa file không liên quan, đổi format cả file, thêm abstraction thừa | Diff nhỏ; giới hạn phạm vi trong yêu cầu |
| **Trùng lặp** | Viết lại util đã có trong codebase | Biết codebase; đưa ví dụ có sẵn vào context |
| **Sai về đồng thời hoặc giao dịch** | Race condition, gọi HTTP trong transaction | Review kỹ, load test |

**Checklist review diff do AI tạo:**
1. Diff có **đúng và chỉ đúng** phạm vi yêu cầu không?
2. Tôi **giải thích được** từng thay đổi không?
3. Case biên: null, rỗng, trùng, đồng thời, lỗi mạng, dữ liệu lớn?
4. Quyền và bảo mật: user có được làm thao tác này không? Input có được validate?
5. Test có kiểm tra **hành vi** không, và có fail nếu logic sai không?
6. Dependency mới có thật sự cần, có uy tín không?
7. Hiệu năng: N+1, vòng lặp gọi DB, thiếu index?

**Lớp tự động trong CI (không phân biệt code người hay AI viết):** build và test bắt buộc, coverage, lint và formatter, SAST, secret scanning, dependency scanning (Dependabot, Snyk), có thể thêm **AI review bot** cho PR làm lớp thứ hai, nhưng **không thay cho người review**.

**Quy định nhóm hợp lý:** PR do agent mở vẫn cần người review; người mở PR chịu trách nhiệm như code mình viết; ghi rõ phần nào AI tạo nếu công ty yêu cầu; không dùng AI với dữ liệu hoặc code bị cấm theo hợp đồng khách hàng.

### English

**Principle:** treat AI-written code **like code from a new colleague who is very fast but often confidently wrong**. You're the one accountable when it's merged.

**Common flaws in AI code and how to catch them:**

| Flaw | Example | How to catch it |
|---|---|---|
| **"Phantom" APIs or libraries** | Calls a method that doesn't exist, uses a config option from the wrong version | Compile, test, read the official docs |
| **Fake packages** (slopsquatting) | Adds a dependency whose name resembles a real package | Check every new dependency; use dependency scanning |
| **Security holes** | Missing authorization (IDOR), string-built SQL, logs leaking tokens, hard-coded secrets | SAST (SonarQube, Semgrep), secret scanning, a security review checklist |
| **Meaningless tests** | Tests that only verify a mock was called; or **assertions edited to match buggy code**; tests deleted to "pass" | Read tests as carefully as code; mutation testing (PIT) |
| **Poor error handling** | `catch (Exception e) {}`, returning `null`, no timeouts on outbound calls | Review, lint rules |
| **Scope creep** | Edits unrelated files, reformats whole files, adds needless abstractions | Small diffs; limit scope in the request |
| **Duplication** | Rewrites a utility that already exists in the codebase | Know the codebase; put existing examples in context |
| **Concurrency or transaction mistakes** | Race conditions, HTTP calls inside a transaction | Careful review, load tests |

**A checklist for reviewing AI-generated diffs:**
1. Does the diff cover **exactly and only** the requested scope?
2. Can I **explain** every change?
3. Edge cases: null, empty, duplicates, concurrency, network failures, large data?
4. Permissions and security: may this user perform this action? Is input validated?
5. Do the tests check **behaviour**, and would they fail if the logic were wrong?
6. Is every new dependency truly needed and reputable?
7. Performance: N+1 queries, DB calls in loops, missing indexes?

**Automated layers in CI (regardless of whether a human or AI wrote the code):** mandatory build and tests, coverage, linting and formatting, SAST, secret scanning, dependency scanning (Dependabot, Snyk), and optionally an **AI review bot** on PRs as a second layer, but **not a replacement for human review**.

**Sensible team rules:** PRs opened by agents still need human review; whoever opens the PR is accountable as if they wrote it; label AI-generated parts if the company requires it; don't use AI with data or code that customer contracts forbid.

@@@ ai-dev-team | Đưa AI vào quy trình phát triển của cả nhóm (SDLC) thế nào? Đo hiệu quả ra sao? / How do you bring AI into a team's development process (SDLC), and how do you measure the impact? | ai | ai-workflow,sdlc,team | qa | AI-assisted development
### Tiếng Việt

**AI ở từng giai đoạn của SDLC:**

| Giai đoạn | Cách dùng AI |
|---|---|
| Yêu cầu, thiết kế | Phân tích yêu cầu, liệt kê case biên, viết nháp spec hoặc ADR, so sánh phương án; **con người quyết định** |
| Code | Agent trong IDE hoặc terminal; agent chạy nền nhận issue nhỏ và mở PR |
| Test | Sinh unit và integration test, dữ liệu test, test case từ acceptance criteria |
| Review | AI review bot trên PR (lớp thứ hai), tóm tắt PR lớn |
| CI/CD | Agent chạy **headless** trong pipeline: sửa lỗi lint, cập nhật dependency, viết release note; phân tích nguyên nhân build fail |
| Vận hành | Tóm tắt log và alert, gợi ý nguyên nhân sự cố, viết nháp postmortem |
| Tài liệu, onboarding | Giải thích codebase cho người mới, sinh và cập nhật tài liệu |

**Triển khai cho nhóm, theo bước:**
1. **Chính sách trước:** công cụ được phép, dữ liệu nào được gửi đi (code của khách hàng? dữ liệu cá nhân?), bản enterprise không dùng dữ liệu để huấn luyện, quản lý secret.
2. **Thí điểm** với một nhóm nhỏ, việc rõ ràng (viết test, migration).
3. **Chuẩn hóa context:** file hướng dẫn chung (`AGENTS.md` / `CLAUDE.md`), prompt và skill dùng chung, MCP server nội bộ được duyệt.
4. **Củng cố lưới an toàn:** test, CI, scan bảo mật, quy định review, vì code được tạo ra nhanh hơn rất nhiều.
5. Chia sẻ kinh nghiệm thường xuyên (cách dùng hay, lỗi hay gặp).

**Đo hiệu quả, đừng đo bằng số dòng code:**
- **DORA:** lead time cho thay đổi, tần suất deploy, change failure rate, thời gian khôi phục.
- Cycle time của PR, thời gian review, số bug lọt ra production, độ phủ test.
- Khảo sát trải nghiệm developer.
- Chi phí công cụ và token so với thời gian tiết kiệm được.
- Cảnh giác: tốc độ tăng nhưng **change failure rate cũng tăng** nghĩa là chất lượng đang giảm; PR to hơn làm review chậm đi và tạo nút thắt mới.

**Rủi ro của cả nhóm:** kỹ năng của junior không phát triển nếu chỉ chấp nhận output; codebase không nhất quán; phụ thuộc vào một nhà cung cấp; rò rỉ dữ liệu.

### English

**AI at each SDLC stage:**

| Stage | How AI is used |
|---|---|
| Requirements, design | Analysing requirements, listing edge cases, drafting specs or ADRs, comparing options; **humans decide** |
| Coding | Agents in the IDE or terminal; background agents take small issues and open PRs |
| Testing | Generating unit and integration tests, test data, test cases from acceptance criteria |
| Review | AI review bots on PRs (a second layer), summaries of large PRs |
| CI/CD | **Headless** agents in the pipeline: fixing lint errors, updating dependencies, writing release notes; analysing why a build failed |
| Operations | Summarizing logs and alerts, suggesting incident causes, drafting postmortems |
| Docs, onboarding | Explaining the codebase to newcomers, generating and updating documentation |

**Rolling it out to a team, step by step:**
1. **Policy first:** approved tools, what data may be sent out (customer code? personal data?), enterprise plans that don't train on your data, secret management.
2. **Pilot** with a small team on clear work (writing tests, migrations).
3. **Standardize context:** a shared instructions file (`AGENTS.md` / `CLAUDE.md`), shared prompts and skills, approved internal MCP servers.
4. **Strengthen the safety net:** tests, CI, security scans and review rules, because code is now produced much faster.
5. Share lessons regularly (good practices, common mistakes).

**Measuring impact, not by lines of code:**
- **DORA:** lead time for changes, deployment frequency, change failure rate, time to restore.
- PR cycle time, review time, bugs escaping to production, test coverage.
- Developer experience surveys.
- Tool and token costs versus time saved.
- Watch out: if speed rises but **the change failure rate rises too**, quality is slipping; bigger PRs slow review and create a new bottleneck.

**Team-level risks:** juniors' skills stop growing if they only accept output; the codebase becomes inconsistent; dependence on a single vendor; data leakage.

@@@ ai-dev-multi-agent | Subagent, chạy nhiều agent song song và agent trong CI dùng thế nào? / How do you use subagents, multiple agents in parallel, and agents in CI? | ai | multi-agent,agentic-coding,ci | qa | AI-assisted development
### Tiếng Việt

**1. Subagent:** agent chính giao một việc phụ cho agent con có **context riêng**. Subagent đọc nhiều file, tìm kiếm, phân tích, rồi chỉ trả về **bản tóm tắt**, nên context của agent chính không bị đầy.
- Hợp với: khảo sát codebase ("tìm mọi chỗ gọi PaymentClient"), review độc lập (một subagent chỉ đọc diff để tìm lỗi, không thấy quá trình viết nên không "tự chấm bài mình"), nghiên cứu tài liệu.
- Có thể định nghĩa subagent chuyên biệt: "security reviewer", "test writer", mỗi cái có hướng dẫn và quyền tool riêng.

**2. Nhiều agent song song:** chạy vài agent cùng lúc cho **những việc độc lập**.
- Mỗi agent làm trên một **git worktree** (thư mục làm việc riêng của cùng repo, nhánh riêng) để không ghi đè lên nhau.
- Ví dụ: agent A viết tính năng, agent B viết test cho module khác, agent C cập nhật tài liệu. Hoặc thử **2–3 cách giải** cho cùng một vấn đề rồi chọn cách tốt nhất.
- Giới hạn thật: **bạn** vẫn phải review tất cả, nên nút thắt chuyển sang khâu review. Chỉ chạy song song số việc bạn review kịp.

**3. Mẫu "người viết và người kiểm":** một agent viết code, một agent khác (context sạch) review hoặc viết test, rồi agent đầu sửa theo nhận xét. Bắt được nhiều lỗi hơn một agent tự kiểm.

**4. Agent trong CI/CD (chế độ headless, không tương tác):**
```yaml
# Ví dụ khái niệm: GitHub Actions gọi agent khi có comment "@agent fix" trên PR
on: issue_comment
jobs:
  agent:
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write }   # quyền tối thiểu
    steps:
      - uses: actions/checkout@v4
      - run: <coding-agent-cli> -p "Fix the failing tests in this PR. Do not modify tests." --allowed-tools "Edit,Bash(./mvnw test)"
```
- Use case: tự review PR, sửa lỗi lint hoặc test vỡ, cập nhật dependency, phân loại issue, sinh release note.
- **An toàn:** quyền tối thiểu, chỉ cho phép một số lệnh, không có secret production, kết quả phải đi qua PR và người review. Cẩn thận **prompt injection** từ nội dung issue hoặc PR do người ngoài viết.

**Khi nào không nên dùng multi-agent:** việc nhỏ, việc phụ thuộc chặt vào nhau (sửa cùng file), hoặc khi chi phí token và công review lớn hơn lợi ích.

### English

**1. Subagents:** the main agent delegates a side task to a child agent with **its own context**. The subagent reads many files, searches and analyses, then returns only **a summary**, so the main agent's context doesn't fill up.
- Good for: surveying a codebase ("find every call to PaymentClient"), independent review (a subagent reads only the diff to find bugs; it didn't see the writing process, so it isn't "grading its own work"), researching documentation.
- You can define specialized subagents, such as a "security reviewer" or a "test writer", each with its own instructions and tool permissions.

**2. Multiple agents in parallel:** run several agents at once on **independent tasks**.
- Each agent works in its own **git worktree** (a separate working directory of the same repo, on its own branch) so they don't overwrite each other.
- Examples: agent A builds a feature, agent B writes tests for another module, agent C updates docs. Or try **2–3 solutions** to the same problem and pick the best.
- The real limit: **you** still review everything, so the bottleneck moves to review. Only run as many parallel tasks as you can review.

**3. The "writer and checker" pattern:** one agent writes the code, another (with a clean context) reviews it or writes tests, and the first one fixes the feedback. This catches more bugs than one agent checking itself.

**4. Agents in CI/CD (headless, non-interactive mode):**
```yaml
# Conceptual example: GitHub Actions invokes an agent on a "@agent fix" PR comment
on: issue_comment
jobs:
  agent:
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write }   # least privilege
    steps:
      - uses: actions/checkout@v4
      - run: <coding-agent-cli> -p "Fix the failing tests in this PR. Do not modify tests." --allowed-tools "Edit,Bash(./mvnw test)"
```
- Use cases: automatic PR review, fixing lint errors or broken tests, dependency updates, issue triage, release notes.
- **Safety:** least privilege, an allow-list of commands, no production secrets, and results must go through a PR and a human reviewer. Beware **prompt injection** from issue or PR content written by outsiders.

**When not to use multi-agent setups:** small tasks, tightly coupled work (editing the same files), or when token costs and review effort outweigh the benefit.
