def interpret_p_value(p_val, test_name="هذا الاختبار", alpha=0.05):
    """Generate a readable AI insight based on p-value."""
    if p_val < alpha:
        return f"✨ **تحليل الذكاء الاصطناعي:** بناءً على قيمة الاحتمالية (P-value = {p_val:.4f}) والتي هي أصغر من {alpha}، يرى النموذج أن هناك فرقاً أو علاقة **ذات دلالة إحصائية قوية**. هذا يعني أن النتائج التي حصلنا عليها ليست صدفة."
    else:
        return f"💡 **تحليل الذكاء الاصطناعي:** بناءً على قيمة الاحتمالية (P-value = {p_val:.4f}) والتي هي أكبر من {alpha}، يرى النموذج أنه **لا توجد أدلة كافية** لإثبات وجود فرق أو علاقة ذات دلالة إحصائية في {test_name}. قد تكون النتائج ناتجة عن الصدفة."

def interpret_correlation(r_val, p_val, x_name, y_name):
    """Generate AI insight for correlation."""
    direction = "طردية (موجبة)" if r_val > 0 else "عكسية (سالبة)"
    strength = "قوية جداً" if abs(r_val) >= 0.8 else "قوية" if abs(r_val) >= 0.6 else "متوسطة" if abs(r_val) >= 0.4 else "ضعيفة"
    
    insight = f"🔍 **مساعدك البحثي:** يظهر التحليل علاقة ارتباط **{direction} {strength}** بين المتغيرين '{x_name}' و '{y_name}' (معامل الارتباط = {r_val:.2f}). "
    
    if p_val < 0.05:
        insight += "بما أن قيمة الاحتمالية أقل من 0.05، فهذه العلاقة تعتبر موثوقة إحصائياً."
    else:
        insight += "لكن قيمة الاحتمالية عالية، مما يعني أن هذه العلاقة قد تكون غير دالة إحصائياً ولا يُعتمد عليها."
        
    return insight

def interpret_regression(r2_val, rmse_val):
    """Generate AI insight for regression models."""
    if r2_val >= 0.8:
        strength = "ممتازة جداً"
    elif r2_val >= 0.6:
        strength = "جيدة"
    elif r2_val >= 0.4:
        strength = "متوسطة إلى ضعيفة"
    else:
        strength = "ضعيفة جداً"
        
    return f"🤖 **رؤية الذكاء الاصطناعي للنموذج:** يوضح مقياس (R²) أن النموذج يفسر **{r2_val*100:.1f}%** من التباين في البيانات، وهي نسبة **{strength}**. أما خطأ التنبؤ التقريبي (RMSE) فيبلغ {rmse_val:.4f}."
