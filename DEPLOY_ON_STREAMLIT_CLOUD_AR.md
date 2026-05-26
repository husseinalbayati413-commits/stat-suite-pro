# تشغيل Stat Suite Pro على Streamlit Cloud

## النتيجة المتوقعة
بعد رفع المشروع على GitHub ثم نشره على Streamlit Community Cloud، سيصبح التطبيق متاحاً برابط عام من الشكل:

`https://اسم-التطبيق.streamlit.app`

وهذا رابط مستقل من منصة معروفة.

## الملفات المطلوبة
- `app.py`
- مجلد `pages/`
- مجلد `utils/`
- `requirements.txt`
- `.streamlit/config.toml`

## خطوات النشر
1. أنشئ مستودع جديد على GitHub.
2. ارفع جميع ملفات هذا المشروع إلى المستودع.
3. ادخل إلى Streamlit Community Cloud.
4. اختر **Create app**.
5. اربط حساب GitHub.
6. اختر المستودع والفرع الرئيسي.
7. حدِّد ملف التشغيل: `app.py`
8. اضغط **Deploy**.

## ملاحظات مهمة
- تم التحقق من سلامة ملفات Python.
- تم التحقق من تثبيت واستيراد الاعتمادات الأساسية بنجاح.
- ملف `.streamlit/config.toml` موجود ومناسب للتشغيل.

## بعد النشر
انسخ رابط التطبيق النهائي، ثم ضعه داخل مشروع الأندرويد الموجود في `android_wrapper_template` داخل القيمة:

`streamlit_url`

ثم افتح المشروع في Android Studio وابنِ ملف APK.
