# تحويل رابط Streamlit إلى APK أندرويد

هذا المجلد يحتوي مشروع Android Studio بسيط يفتح رابط التطبيق داخل WebView.

## قبل البناء
1. انشر التطبيق أولاً على Streamlit Cloud.
2. خذ الرابط النهائي مثل:
   `https://your-app-name.streamlit.app`
3. افتح الملف:
   `android_wrapper_template/app/src/main/res/values/strings.xml`
4. بدّل قيمة `streamlit_url` بالرابط الحقيقي.

## البناء
1. افتح مجلد `android_wrapper_template` في Android Studio.
2. دع Android Studio ينشئ ملفات Gradle الناقصة تلقائياً إذا طلب.
3. اختر **Build > Build APK(s)**.

## ملاحظات
- هذا APK يغلف نسخة الويب داخل تطبيق أندرويد.
- الأداء يعتمد على سرعة الإنترنت لأن التطبيق الأساسي Streamlit ويب.
- لو أردت تطبيق Native كامل، يجب إعادة بناء الواجهة كتطبيق Flutter أو React Native.
