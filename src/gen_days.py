"""Generate extra_days.md (the 14-day roadmap) from data.json.

Run inside src/:  python3 build.py && python3 gen_days.py && python3 build.py && python3 bundle.py
(the first build produces data.json so question titles can be looked up).
"""
import json

A = {a['id']: a for a in json.load(open('data.json', encoding='utf-8'))['articles']}


def q(aid):
    t = A[aid]['title'].split(' / ')[0]
    return f'- [ ] [{t}](#{aid})'


def ids(prefix=None, section=None, explicit=(), exclude=()):
    out = list(explicit)
    for a in A.values():
        if a['kind'] != 'qa' or a['id'] in out or a['id'] in exclude:
            continue
        if prefix and any(a['id'].startswith(p) for p in prefix):
            out.append(a['id'])
        elif section and a['section'] in section:
            out.append(a['id'])
    return out


def lc(num, slug, title, level):
    return f'- [ ] [{num}. {title}](https://leetcode.com/problems/{slug}/) ({level})'


DAYS = [
    dict(n=1, title='Java core', goal='Collections, HashMap, String, OOP, exception, generics.',
         theory=[ids(prefix=['java-core-', 'jc-'], exclude=['jc-sync-vs-lock', 'jc-jmm', 'jc-thread-safety'])],
         coding=[lc(1, 'two-sum', 'Two Sum', 'Easy'), lc(49, 'group-anagrams', 'Group Anagrams', 'Medium'),
                 lc(3, 'longest-substring-without-repeating-characters', 'Longest Substring Without Repeating Characters', 'Medium'),
                 lc(347, 'top-k-frequent-elements', 'Top K Frequent Elements', 'Medium')],
         topic='Arrays & hashing'),
    dict(n=2, title='JVM & concurrency', goal='Bộ nhớ JVM, GC, class loader, thread pool, virtual threads, Java 8–21.',
         theory=[ids(prefix=['jvm-', 'concurrency-', 'java-modern-', 'jn-'], explicit=['jc-jmm', 'jc-thread-safety', 'jc-sync-vs-lock'])],
         coding=['- [ ] Làm lại 347 trong 10 phút (min-heap kích thước k)',
                 lc(692, 'top-k-frequent-words', 'Top K Frequent Words', 'Medium') + ' · lời giải: [heap ngược chiều](#dsa-top-k-words)',
                 lc(242, 'valid-anagram', 'Valid Anagram', 'Easy'),
                 lc(238, 'product-of-array-except-self', 'Product of Array Except Self', 'Medium'),
                 lc(128, 'longest-consecutive-sequence', 'Longest Consecutive Sequence', 'Medium'),
                 lc(141, 'linked-list-cycle', 'Linked List Cycle', 'Easy') + ' · lời giải: [Floyd](#dsa-linked-list-cycle)'],
         topic='Arrays & hashing'),
    dict(n=3, title='Spring & Spring Boot', goal='IoC, bean lifecycle, @Transactional, AOP, auto-configuration, Security, MVC.',
         theory=[ids(prefix=['spring-', 'sp-', 'sn-'])],
         coding=[lc(125, 'valid-palindrome', 'Valid Palindrome', 'Easy'),
                 lc(167, 'two-sum-ii-input-array-is-sorted', 'Two Sum II', 'Medium'),
                 lc(15, '3sum', '3Sum', 'Medium')],
         topic='Two pointers', evening='CI/CD lab bước 1–2: CI cơ bản và quality gate ([hướng dẫn](#cicd-fix))'),
    dict(n=4, title='Database, JPA & SQL', goal='Index, locking, isolation, N+1, PostgreSQL internals, SQL.',
         theory=[ids(prefix=['database-', 'jpa-', 'pg-', 'sql-', 'nosql-'], explicit=['db-query-optimization', 'pgvector'])],
         coding=[lc(121, 'best-time-to-buy-and-sell-stock', 'Best Time to Buy and Sell Stock', 'Easy'),
                 lc(424, 'longest-repeating-character-replacement', 'Longest Repeating Character Replacement', 'Medium'),
                 lc(567, 'permutation-in-string', 'Permutation in String', 'Medium')],
         topic='Sliding window', evening='CI/CD lab bước 3: multi-stage Dockerfile, push image lên GHCR'),
    dict(n=5, title='Microservices & Kafka', goal='Saga, outbox, idempotency, resilience, REST, Kafka.',
         theory=[ids(prefix=['request-flow', 'sync-async-code', 'microservices-', 'kafka-', 'rabbitmq-', 'dt-', 'arch-rest', 'arch-cb-open'])],
         coding=[lc(20, 'valid-parentheses', 'Valid Parentheses', 'Easy'),
                 lc(678, 'valid-parenthesis-string', 'Valid Parenthesis String', 'Medium') + ' · lời giải: [khoảng lo/hi](#dsa-valid-paren-star)',
                 lc(155, 'min-stack', 'Min Stack', 'Medium'),
                 lc(739, 'daily-temperatures', 'Daily Temperatures', 'Medium')],
         topic='Stack', evening='CI/CD lab bước 4: deploy lên kind, manual approval'),
    dict(n=6, title='Go', goal='Concurrency, context, map, slice, interface, GC, xử lý tiền (quan trọng cho Grab).',
         theory=[ids(prefix=['go-'])],
         coding=[lc(704, 'binary-search', 'Binary Search', 'Easy'),
                 lc(33, 'search-in-rotated-sorted-array', 'Search in Rotated Sorted Array', 'Medium'),
                 lc(153, 'find-minimum-in-rotated-sorted-array', 'Find Minimum in Rotated Sorted Array', 'Medium')],
         topic='Binary search', evening='CI/CD lab bước 5: probes, rollback, secrets'),
    dict(n=7, title='Mock 1 & ôn lại', goal='Mock 90 phút bằng tiếng Anh cho Ngày 1–6, ghi âm, lập danh sách lỗ hổng.',
         theory=[], extra=['- [ ] Nhắn "mock Java core" hoặc "mock Spring" để luyện hỏi đáp với Claude',
                           '- [ ] Ôn lại mọi câu chưa đánh dấu "đã thuộc" của Ngày 1–6',
                           '- [ ] Viết ra 5 lỗ hổng lớn nhất để vá trong tuần 2'],
         coding=[lc(206, 'reverse-linked-list', 'Reverse Linked List', 'Easy'),
                 lc(24, 'swap-nodes-in-pairs', 'Swap Nodes in Pairs', 'Medium') + ' · lời giải: [dummy node](#dsa-swap-pairs)',
                 lc(21, 'merge-two-sorted-lists', 'Merge Two Sorted Lists', 'Easy'),
                 lc(141, 'linked-list-cycle', 'Linked List Cycle', 'Easy')],
         topic='Linked list'),
    dict(n=8, title='System design 1', goal='Khung trả lời 45 phút, caching, CDN, scale database, consistent hashing.',
         theory=[ids(explicit=['sd-checklist', 'lld-rate-limiter', 'sd-estimation', 'sd-scale-up-out', 'sd-stateless-stateful', 'sd-stateful-scaling', 'sd-load-balancer', 'sd-availability', 'sd-autoscaling', 'sd-queue-backpressure', 'sd-bottleneck', 'system-design-17', 'system-design-18', 'system-design-19',
                                'system-design-20', 'sd-cdn', 'sd-consistent-hashing', 'db-replication-sharding'],
                     prefix=['cache-', 'redis-'])],
         extra=['- [ ] Tự vẽ URL shortener và rate limiter trong 35 phút mỗi bài, nói to bằng tiếng Anh'],
         coding=[lc(19, 'remove-nth-node-from-end-of-list', 'Remove Nth Node From End of List', 'Medium'),
                 lc(2, 'add-two-numbers', 'Add Two Numbers', 'Medium'),
                 lc(146, 'lru-cache', 'LRU Cache', 'Medium')],
         topic='Linked list'),
    dict(n=9, title='System design 2', goal='Bài quy mô lớn (ride matching, ví, flash sale), lock, consistency, kiến trúc dự án cũ.',
         theory=[ids(explicit=['system-design-16', 'sd-ride-matching', 'sd-wallet', 'sd-double-entry', 'sd-flash-sale',
                                'sd-distributed-lock', 'sd-eventual', 'sd-strangler', 'arch-hexagonal', 'arch-principles'])],
         extra=['- [ ] Vẽ sơ đồ kiến trúc Opswat, chuẩn bị 3 quyết định thiết kế bảo vệ được'],
         coding=[lc(226, 'invert-binary-tree', 'Invert Binary Tree', 'Easy'),
                 lc(104, 'maximum-depth-of-binary-tree', 'Maximum Depth of Binary Tree', 'Easy'),
                 lc(102, 'binary-tree-level-order-traversal', 'Binary Tree Level Order Traversal', 'Medium')],
         topic='Trees'),
    dict(n=10, title='CI/CD, Docker, K8s & AWS', goal='Pipeline, deploy strategies, probes, AWS cơ bản, xử lý sự cố.',
         theory=[ids(prefix=['net-', 'cicd-', 'docker-', 'k8s-', 'cloud-', 'aws-', 'troubleshoot-'])],
         coding=[lc(98, 'validate-binary-search-tree', 'Validate Binary Search Tree', 'Medium'),
                 lc(235, 'lowest-common-ancestor-of-a-binary-search-tree', 'Lowest Common Ancestor of a BST', 'Medium'),
                 lc(230, 'kth-smallest-element-in-a-bst', 'Kth Smallest Element in a BST', 'Medium')],
         topic='Trees'),
    dict(n=11, title='Security & testing', goal='JWT, OAuth, OWASP, mã hóa, mTLS, phân quyền, test pyramid (quan trọng cho Axon).',
         theory=[ids(prefix=['sec-', 'eng-testing'])],
         coding=[lc(56, 'merge-intervals', 'Merge Intervals', 'Medium'),
                 lc(57, 'insert-interval', 'Insert Interval', 'Medium'),
                 lc(215, 'kth-largest-element-in-an-array', 'Kth Largest Element in an Array', 'Medium')],
         topic='Intervals & heap'),
    dict(n=12, title='Behavioral & AI', goal='8 câu chuyện STAR bằng chuyện thật, AI tools, Agile.',
         theory=[ids(prefix=['behavioral-', 'ai-', 'eng-sdlc-agile'])],
         extra=['- [ ] Điền hết các chỗ [...] bằng chuyện thật, mỗi câu chuyện nói trong 2 phút'],
         coding=[lc(200, 'number-of-islands', 'Number of Islands', 'Medium'),
                 lc(133, 'clone-graph', 'Clone Graph', 'Medium'),
                 lc(207, 'course-schedule', 'Course Schedule', 'Medium')],
         topic='Graphs'),
    dict(n=13, title='HR & Mock 2', goal='Mock đầy đủ theo quy trình công ty sắp phỏng vấn: HR, technical, manager.',
         theory=[ids(prefix=['hr-screening-', 'hr-culture-fit', 'hr-questions-to-ask'])],
         extra=['- [ ] Mock full với Claude: 30 phút HR, 60 phút technical, 30 phút behavioral',
                '- [ ] Sửa 3 điểm yếu nhất sau buổi mock'],
         coding=[lc(70, 'climbing-stairs', 'Climbing Stairs', 'Easy'),
                 lc(198, 'house-robber', 'House Robber', 'Medium'),
                 lc(322, 'coin-change', 'Coin Change', 'Medium')],
         topic='Dynamic programming'),
    dict(n=14, title='Ôn nhẹ', goal='Không học mới. Ôn câu chưa thuộc, chuẩn bị tinh thần và câu hỏi ngược.',
         theory=[], extra=['- [ ] Đọc lại [checklist trước ngày phỏng vấn](#checklist-truoc-ngay-phong-van)',
                           '- [ ] Chuẩn bị [câu hỏi hỏi ngược interviewer](#cau-hoi-nen-hoi)',
                           '- [ ] Đọc trang công ty sắp phỏng vấn trong mục Công ty',
                           '- [ ] Self-introduction 90 giây, nói lại 3 lần',
                           '- [ ] Ngủ sớm'],
         coding=['- [ ] Làm lại 3 bài bị vấp nhiều nhất trong 13 ngày qua'],
         topic='Ôn lại'),
]

out = []
for d in DAYS:
    body = [f'**Mục tiêu:** {d["goal"]}', '']
    theory = [x for group in d['theory'] for x in group]
    if theory:
        body += [f'### Lý thuyết ({len(theory)} câu)', '',
                 '*Bật nút luyện tập, tự nói bằng tiếng Anh 60–90 giây rồi mới xem câu trả lời mẫu.*', '']
        body += [q(i) for i in theory] + ['']
    if d.get('extra'):
        body += ['### Việc cần làm', ''] + d['extra'] + ['']
    body += [f'### Coding: {d["topic"]}', '', '*Chỉ Easy và Medium. Bấm giờ, nói to complexity, code Java không autocomplete.*', '']
    body += d['coding'] + ['']
    if d.get('evening'):
        body += ['### Buổi tối', '', f'- [ ] {d["evening"]}', '']
    body += ['### Chốt ngày', '', '- [ ] Ghi âm 2 câu khó nhất, nghe lại',
             '- [ ] Đánh dấu "đã thuộc" cho các câu nói trôi chảy',
             '- [ ] Ghi lại câu còn vấp và bài coding bị kẹt']
    out.append(f'@@@ day-{d["n"]} | Day {d["n"]}: {d["title"]} | plan | lo-trinh | guide | Day {d["n"]}\n' + '\n'.join(body) + '\n')

open('extra_days.md', 'w', encoding='utf-8').write('\n'.join(out))
print('wrote', len(DAYS), 'days')
