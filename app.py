from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/ai-process', methods=['POST'])
def ai_process():
    data = request.json or {}
    query = data.get('query', '')
    # يمكنك وضع منطق الذكاء الاصطناعي هنا
    return jsonify({"reply": f"الروبوت حلل: {query} بنجاح."})

# لا تضع app.run هنا! Vercel سيتولى التشغيل تلقائياً.
