"""Split src.md + extra.md into articles and write data.json.

Run inside src/:  python3 build.py && python3 bundle.py
"""
import json, re, unicodedata, collections

CATS = [
    ('guide', 'Hướng dẫn'), ('company', 'Công ty'), ('hr', 'HR & giới thiệu'),
    ('java', 'Java & JVM'), ('go', 'Go'), ('spring', 'Spring & Database'),
    ('arch', 'Microservices & System Design'), ('devops', 'CI/CD, Cloud & AWS'),
    ('security', 'Security'), ('coding', 'Coding, DSA & SQL'), ('behavioral', 'Behavioral & AI'),
]
CAT_LABEL = dict(CATS)
H2_CAT = [  # prefix of the ## heading -> category
    ('Cách dùng', 'guide'), ('HR screening', 'hr'),
    ('Technical: Java', 'java'), ('Technical: Spring', 'spring'),
    ('Technical: microservices', 'arch'), ('Technical: CI/CD', 'devops'),
    ('Technical: coding', 'coding'), ('Behavioral', 'behavioral'),
    ('Câu hỏi cho interviewer', 'guide'),
]
SUB = {  # ### heading -> topic tag (also the article id prefix)
    'Collections và ngôn ngữ': 'java-core', 'Java 8 đến 21': 'java-modern',
    'JVM và bộ nhớ': 'jvm', 'Concurrency': 'concurrency',
    'Spring và Spring Boot': 'spring', 'Database': 'database',
    'JPA và Hibernate': 'jpa', 'Microservices': 'microservices',
    'Kafka và messaging': 'kafka', 'System design': 'system-design',
    'CI/CD': 'cicd', 'Docker và Kubernetes': 'docker-k8s', 'Cloud': 'cloud',
    'Coding': 'coding', 'SQL': 'sql', 'Behavioral': 'behavioral',
    'AI-assisted development': 'ai-tools',
}
EXTRA_TAGS = [(r'Opswat', 'opswat'), (r'DXC', 'dxc'), (r'\bKafka\b', 'kafka'),
              (r'Kubernetes|kubectl', 'kubernetes'), (r'Docker', 'docker')]


def slug(s):
    s = unicodedata.normalize('NFD', s.replace('đ', 'd').replace('Đ', 'D'))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


articles = []


def add(a):
    a['body'] = a['body'].strip('\n')
    txt = re.sub(r'```.*?```', ' ', a['body'], flags=re.S)
    txt = '\n'.join(l for l in txt.split('\n')
                    if not l.lstrip().startswith('|') and not l.startswith('###'))
    txt = re.sub(r'(?m)^\s*(?:[-*]|\d+\.)\s+(?:\[ \]\s*)?', '', txt)
    txt = re.sub(r'\]\([^)]*\)', ']', txt)
    txt = re.sub(r'[*_`#>\[\]|\\]', '', txt)
    a['excerpt'] = re.sub(r'\s+', ' ', txt).strip()[:220]
    tags = list(dict.fromkeys(t for t in a['tags'] if t))
    if a['kind'] == 'qa':
        for pat, t in EXTRA_TAGS:
            if t not in tags and re.search(pat, a['title'] + ' ' + a['body']):
                tags.append(t)
    a['tags'] = tags
    a['catLabel'] = CAT_LABEL[a['cat']]
    a.setdefault('tip', '')
    a.setdefault('num', None)
    articles.append(a)


# ---------- src.md ----------
lines = open('src.md', encoding='utf-8').read().split('\n')
h2 = h3 = cat = None
intro, pre = [], []
cur = guide = None
part_tip = {}


def flush():
    global cur, guide
    if cur: add(cur)
    if guide and guide['body'].strip(): add(guide)
    cur = guide = None


def flush_intro():
    global intro
    body = '\n'.join(intro).strip()
    if body and h2:
        if cat == 'guide':
            add(dict(id=slug(h2), title=h2, cat=cat, section='', tags=['huong-dan'],
                     body=body, kind='guide'))
        else:
            add(dict(id=slug(h2), title='Tổng quan: ' + h2, cat=cat, section='Tổng quan',
                     tags=['tong-quan'], body=body, kind='guide'))
            tips = [p for p in body.split('\n\n') if p.startswith('*') and not p.startswith('**')]
            if tips: part_tip[h2] = tips[0]
    intro = []


for line in lines:
    if line.startswith('## '):
        flush(); flush_intro()
        h2 = line[3:].strip(); h3 = None; pre = []
        cat = next(c for p, c in H2_CAT if h2.startswith(p))
        continue
    if h2 is None:
        continue
    if line.startswith('### '):
        flush()
        h3 = line[4:].strip(); pre = []
        if h3 not in SUB:
            guide = dict(id=slug(h3), title=h3, cat=cat, section=h3, kind='guide', body='',
                         tags=['huong-dan'] + (['cicd'] if 'pipeline' in h3 else []))
        continue
    m = re.match(r'^\*\*Q(\d+)\. (.+?)\*\*\s*$', line)
    if m:
        flush()
        sub = SUB.get(h3, 'hr-screening' if cat == 'hr' else cat)
        cur = dict(id=f'{sub}-{m.group(1)}', title=m.group(2), cat=cat,
                   section=h3 or 'HR screening', tags=[sub], body='', kind='qa',
                   num=int(m.group(1)), tip='\n'.join(pre).strip(), h2=h2)
        continue
    if cur is not None: cur['body'] += line + '\n'
    elif guide is not None: guide['body'] += line + '\n'
    elif h3 is not None: pre.append(line)
    else: intro.append(line)
flush(); flush_intro()

# the coding/behavioral tips sit in the part intro, which is flushed after its Qs: backfill
for a in articles:
    h = a.pop('h2', None)
    if a['kind'] == 'qa' and not a['tip']:
        a['tip'] = part_tip.get(h, '')

# merge "Câu hỏi cho interviewer" intro into the questions article
by = {a['id']: a for a in articles}
iv = by.get('cau-hoi-cho-interviewer-va-checklist')
if iv:
    q = by['cau-hoi-nen-hoi']
    q['body'] = iv['body'] + '\n\n' + q['body']
    q['title'] = 'Câu hỏi nên hỏi ngược interviewer'
    articles.remove(iv)

# ---------- extra.md ----------
import glob
raw = '\n'.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob('extra*.md')))
for chunk in raw.split('@@@ ')[1:]:
    head, body = chunk.split('\n', 1)
    parts = [x.strip() for x in head.split('|')]
    aid, title, cat, tags, kind = parts[:5]
    section = parts[5] if len(parts) > 5 else ''
    base = ['huong-dan'] if cat == 'guide' else (['cong-ty'] if cat == 'company' else [])
    add(dict(id=aid, title=title, cat=cat, section=section, kind=kind,
             tags=base + tags.split(','), body=body))

coding_tip = next((t for h, t in part_tip.items() if h.startswith('Technical: coding')), '')
for a in articles:
    if a['kind'] == 'qa' and a['cat'] == 'coding' and not a['tip']:
        a['tip'] = coding_tip

# ---------- order + checks ----------
order = {c: i for i, (c, _) in enumerate(CATS)}
gpri = {'plan': 0, 'cach-dung-tai-lieu': 1, 'cicd-fix': 2}
articles.sort(key=lambda a: (order[a['cat']], gpri.get(a['id'], 5), a['kind'] != 'guide'))
ids = [a['id'] for a in articles]
dups = [i for i, n in collections.Counter(ids).items() if n > 1]
assert not dups, dups
bad = [(a['id'], l) for a in articles for l in re.findall(r'\]\(#([a-z0-9-]+)\)', a['body']) if l not in ids]
assert not bad, bad

json.dump({'cats': CATS, 'articles': articles}, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(articles), 'articles,', sum(a['kind'] == 'qa' for a in articles), 'questions')
