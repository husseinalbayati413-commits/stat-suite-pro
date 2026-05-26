# Stat Suite Pro

منصة احترافية لتحليل البيانات والإحصاء والانحدار والتعلم الآلي باستخدام Streamlit.

## أهم التحسينات
- واجهة احترافية ومتجاوبة مع الهاتف
- Data Lab لتحميل CSV / Excel وتنظيف البيانات وتحويلها وتنزيلها
- صفحة Statistics مطورة تشمل:
  - Descriptive Statistics
  - Normality Tests
  - Confidence Intervals
  - Correlation Analysis
  - Independent / Paired T-Test
  - One-Way ANOVA + Tukey
  - Chi-Square + Cramer's V
  - Outlier Detection
  - Multiple Linear Regression
  - Polynomial Regression
  - VIF, p-values, confidence intervals, residual diagnostics
- صفحة Machine Learning للنماذج الأساسية
- تنزيل النتائج بصيغ CSV / JSON / PDF / Session

## التشغيل محلياً
```bash
pip install -r requirements.txt
streamlit run app.py
```

## الاستخدام على الهاتف
بعد تشغيل التطبيق أو نشره على Streamlit Cloud، افتح الرابط من متصفح الهاتف وسيظهر بشكل متجاوب.

## المجلدات الأساسية
- `app.py` الصفحة الرئيسية
- `pages/` الصفحات الداخلية
- `utils/` الأدوات المساعدة للتحليل والتقارير والثيم
