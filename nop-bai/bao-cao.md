# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Nguyễn Như Tài |
| MSSV | 2A202602976 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/nntai1111/K4-L3-DAY21-NguyenNhuTai-2A202602976-CI-CD-for-AI-Systems |
| Ngày nộp | 07/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Lần 3 có F1 cao nhất (0.7149), dù accuracy cao nhất lại thuộc về lần 1; accuracy giữa các lần chỉ chênh 3 điểm phần trăm còn F1 chênh 0.11, nên accuracy không phản ánh khả năng nhận diện lớp thu nhập cao. Lần 2 giảm learning_rate nhưng cũng giảm số cây và độ sâu nên bị underfit (F1 0.6051, dưới ngưỡng), cho thấy giảm learning_rate thì phải tăng n_estimators để bù.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Chỉ 24,8% mẫu thuộc lớp thu nhập cao, nên mô hình luôn đoán "thu nhập thấp" vẫn đạt accuracy khoảng 75% dù hoàn toàn vô dụng. F1 của lớp dương kết hợp precision và recall trên chính lớp thiểu số, nên mô hình trên có F1 bằng 0 và bị Quality Gate chặn. Không dùng average="macro" hay "weighted" vì điểm cao của lớp đa số sẽ kéo kết quả lên, che lấp hiệu năng kém trên lớp cần quan tâm.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Không dùng được GCP. | Gói dùng thử tại Việt Nam yêu cầu trả trước. | Chuyển sang AWS: S3 cho DVC, EC2 cho API. |
| Job Train lỗi `AssumeRoleWithWebIdentity`. | Claim `sub` của GitHub OIDC dạng immutable, không khớp trust policy. | Cập nhật trust policy theo đúng claim. |
| Push lên `main` không kích hoạt pipeline. | Repo fork bị tắt workflow theo sự kiện push. | Bật workflow trong tab Actions rồi đẩy lại commit. |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2`) | 0.7354 | 0.8820 |

**Nhận xét:** Gấp đôi dữ liệu làm F1 tăng khoảng 0.02, nhưng holdout chỉ có 124 mẫu lớp dương nên mức chênh này tương ứng vài dự đoán và nằm trong biên độ dao động ngẫu nhiên, do dữ liệu mới cùng phân phối. Điểm chính là commit dữ liệu đã tự động kích hoạt toàn bộ pipeline đến bước triển khai.
