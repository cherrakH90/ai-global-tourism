from flask import Flask, render_template, jsonify, request
import os
import sys

# ============================================================
# إنشاء تطبيق Flask
# ============================================================
app = Flask(__name__)

# ============================================================
# (اختياري) إجبار إيقاف الخادم القديم على المنفذ 7000
# ============================================================
if sys.platform.startswith('linux') or sys.platform == 'darwin':
    os.system("fuser -k 7000/tcp > /dev/null 2>&1")
elif sys.platform.startswith('win'):
    os.system("for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :7000') do taskkill /f /pid %a >nul 2>&1")

# ============================================================
# المسار الرئيسي (الصفحة الرئيسية)
# ============================================================
@app.route('/')
def home():
    """تقديم الواجهة الرئيسية للتطبيق"""
    return render_template('index.html')

# ============================================================
# API معالجة الذكاء الاصطناعي والملاحة
# ============================================================
@app.route('/api/ai-process', methods=['POST'])
def ai_process():
    """
    استقبال طلب من العميل (الـ JavaScript) ومعالجة الاستعلام
    وإرجاع رد نصي مناسب حسب اللغة المختارة.
    """
    data = request.json or {}
    query = data.get('query', '').strip()
    lang = data.get('lang', 'ar')

    if not query:
        return jsonify({"status": "error", "reply": "الرجاء إدخال استعلام صحيح."})

    # توليد الرد بناءً على اللغة
    if lang == 'fr':
        reply = f"Hologramme AI analyse la destination: {query}. Navigation satellite 3D activée."
    elif lang == 'en':
        reply = f"Hologram AI processing destination: {query}. 3D Satellite navigation active."
    else:  # العربية
        reply = f"الروبوت الهولوغرامي يحلل الموقع العالمي: {query}. تم عرض الخريطة والملاحة الفضائية 3D."

    return jsonify({
        "status": "success",
        "query": query,
        "reply": reply
    })

# ============================================================
# تشغيل الخادم (للاستخدام المحلي فقط، لا يُستخدم في Vercel)
# ============================================================
if __name__ == '__main__':
    # عند التشغيل المباشر للملف، يُشغل الخادم على المنفذ 7000
    app.run(host='0.0.0.0', port=7000, debug=True)
