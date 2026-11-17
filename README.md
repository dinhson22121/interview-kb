# Backend Interview KB

Kho kiến thức tĩnh để ôn phỏng vấn Senior Backend (Java/Go) cho nhiều công ty: câu hỏi kèm câu trả lời mẫu theo chủ đề (Java & JVM, Spring & Database, Microservices & System Design, CI/CD & Cloud, Coding/DSA/SQL, HR, Behavioral), trang riêng cho từng công ty (EPAM, mgm, Grab, Axon), kế hoạch ôn 2 tuần.

Tính năng: lọc theo chủ đề và tag, tìm kiếm (phím `/`), chế độ luyện tập ẩn câu trả lời, đánh dấu đã thuộc (lưu trong trình duyệt), dark mode, phím `j`/`k` để chuyển câu.

## Cấu trúc

- `index.html` — trang đã build; GitHub Pages phục vụ trực tiếp file này
- `src/src.md` — câu hỏi và câu trả lời chính
- `src/extra.md` — bài bổ sung: kế hoạch, công ty, DSA, system design. Mỗi bài bắt đầu bằng `@@@ id | tiêu đề | chủ đề | tags | guide/qa | section`
- `src/build.py` — tách Markdown thành bài, gắn tag, kiểm tra link nội bộ, xuất `data.json`
- `src/template.html` — giao diện
- `src/bundle.py` — nhúng dữ liệu và thư viện `marked` vào `index.html`

## Thêm công ty hoặc câu hỏi mới

Thêm một khối `@@@` vào `src/extra.md` (chủ đề `company` cho trang công ty), rồi build lại:

```bash
cd src
npm i marked@12.0.2      # lần đầu
python3 build.py && python3 bundle.py
git add -A && git commit -m "update content" && git push
```
