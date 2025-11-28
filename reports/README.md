# Data Warehouse & DSS Report - LaTeX Project

Báo cáo LaTeX cho đề tài **"Kho dữ liệu & Hệ hỗ trợ quyết định cho bài toán Bank Customer Churn"**.

## 📁 Cấu trúc thư mục

```
DataWarehouse/
├── main.tex              # File LaTeX chính (root document)
├── intro.tex             # Chương 1: Giới thiệu
├── dwh_design.tex        # Chương 2: Thiết kế kho dữ liệu
├── etl.tex               # Chương 3: Quy trình ETL
├── analysis.tex          # Chương 4: Phân tích OLAP và trực quan hóa
├── ml_model.tex          # Chương 5: Mô hình dự đoán churn
├── dss.tex               # Chương 6: Hệ hỗ trợ quyết định
├── conclusion.tex        # Chương 7: Kết luận
├── Images/
│   └── hcmut.png         # Logo trường (dùng cho cover và header)
└── figures/              # Thư mục chứa hình ảnh từ Python project
```

## 🎓 Thông tin báo cáo

- **Môn học**: Kho dữ liệu và Hệ hỗ trợ quyết định
- **Học kỳ**: 242 (2024-2025)
- **Đề tài**: Kho dữ liệu & Hệ hỗ trợ quyết định cho bài toán Bank Customer Churn
- **Dữ liệu**: Kaggle - Bank Customer Churn Modeling

## 📝 Nội dung báo cáo

1. **Giới thiệu**: Đặt vấn đề, mục tiêu, phạm vi, tổng quan dữ liệu
2. **Thiết kế kho dữ liệu**: Star schema, fact table, dimension tables, SQL DDL
3. **Quy trình ETL**: Extract, Transform, Load, feature engineering
4. **Phân tích OLAP và trực quan hóa**: OLAP queries, Python visualizations
5. **Mô hình dự đoán churn**: Logistic Regression, Random Forest, evaluation
6. **Hệ hỗ trợ quyết định**: DSS architecture, decision workflow, strategies
7. **Kết luận**: Tổng kết, bài học, hạn chế, hướng phát triển

## 🔧 Biên dịch báo cáo

### Yêu cầu

- LaTeX distribution (TeX Live, MiKTeX, hoặc MacTeX)
- Các packages: vntex, graphicx, listings, tikz, hyperref, v.v. (đã khai báo trong preamble)

### Cách biên dịch

**Option 1: Sử dụng pdflatex**

```bash
cd DataWarehouse
pdflatex main.tex
pdflatex main.tex  # Chạy lần 2 để cập nhật references
```

**Option 2: Sử dụng latexmk (khuyến nghị)**

```bash
cd DataWarehouse
latexmk -pdf main.tex
```

**Option 3: Sử dụng xelatex (nếu có vấn đề với Vietnamese fonts)**

```bash
cd DataWarehouse
xelatex main.tex
xelatex main.tex
```

### Output

File PDF sẽ được tạo: `main.pdf`

## 🖼️ Hình ảnh và biểu đồ

### Hình ảnh có sẵn

- `Images/hcmut.png`: Logo trường (đã copy từ DataMining template)

### Hình ảnh cần thêm

Các hình ảnh được tham chiếu trong báo cáo (từ Python project `bank_churn_dwh_dss`):

**Đặt vào thư mục `figures/`**:

1. `churn_distribution.png` - Phân bố trạng thái churn
2. `age_distribution.png` - Phân bố tuổi
3. `churn_by_geography.png` - Tỷ lệ churn theo quốc gia
4. `balance_by_churn.png` - So sánh số dư theo churn
5. `churn_by_age_group.png` - Tỷ lệ churn theo nhóm tuổi
6. `churn_by_products.png` - Tỷ lệ churn theo số sản phẩm
7. `confusion_matrix.png` - Confusion matrix của mô hình
8. `feature_importance.png` - Feature importance (Random Forest)
9. `roc_curve.png` - ROC curve

**Cách tạo hình ảnh**:

```bash
# Chạy các script Python trong project bank_churn_dwh_dss
cd ../bank_churn_dwh_dss
python src/visualization/eda_plots.py
python src/visualization/churn_dashboard_plots.py
python src/models/churn_model.py
python src/models/evaluation.py

# Copy hình ảnh sang thư mục DataWarehouse
cp reports/figures/*.png ../DataWarehouse/figures/
```

## ✏️ Chỉnh sửa thông tin cá nhân

Mở file `main.tex` và tìm đến phần cover page (dòng ~210), sửa các placeholder:

```latex
\begin{tabular}{rrlcl}
    \hspace{2.25 cm} & GVHD: & <Tên giảng viên> & & \\
    & SV thực hiện: & <Họ tên sinh viên> & -- & <MSSV> \\
\end{tabular}
```

Thay thế:
- `<Tên giảng viên>` → Tên giảng viên hướng dẫn
- `<Họ tên sinh viên>` → Họ tên của bạn
- `<MSSV>` → Mã số sinh viên của bạn

Nếu có nhiều sinh viên, thêm dòng:

```latex
& & <Họ tên sinh viên 2> & -- & <MSSV 2> \\
```

## 🎨 Đặc điểm của template

- **Cover page**: Giống hệt template DataMining (blue border, HCMUT logo, layout chuẩn)
- **Header/Footer**: Logo + tên trường ở header, tên môn học + số trang ở footer
- **Code highlighting**: Python và SQL code với syntax highlighting đẹp
- **Vietnamese support**: Sử dụng vntex, hỗ trợ tiếng Việt đầy đủ
- **Hyperlinks**: Tất cả references và citations đều clickable

## 📚 Tài liệu tham khảo

Báo cáo đã bao gồm 6 tài liệu tham khảo:
- Kimball & Ross - Data Warehouse Toolkit
- Inmon - Building the Data Warehouse
- Scikit-learn documentation
- Kaggle dataset
- Matplotlib
- Pandas

Có thể thêm/sửa tài liệu tham khảo ở cuối file `main.tex` (section `thebibliography`).

## 🚀 Tips

1. **Biên dịch nhanh**: Sử dụng `latexmk -pvc main.tex` để auto-compile khi có thay đổi
2. **Xem lỗi**: Nếu compile lỗi, kiểm tra file `.log` để xem chi tiết
3. **Missing figures**: Nếu thiếu hình, LaTeX sẽ cảnh báo nhưng vẫn compile được (hiển thị placeholder)
4. **Font issues**: Nếu có lỗi font Vietnamese, thử dùng `xelatex` thay vì `pdflatex`

## 📧 Liên hệ

Nếu có vấn đề với LaTeX template, kiểm tra:
- Đã cài đủ packages chưa
- File hình ảnh đã đặt đúng thư mục chưa
- Encoding của file .tex là UTF-8 chưa

---

**Chúc bạn hoàn thành báo cáo tốt!** 🎓
