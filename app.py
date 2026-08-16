from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/ai-process', methods=['POST'])
def ai_process():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'reply': 'يرجى إدخال اسم مدينة أو وجهة سياحية للبحث.'})

    reply = f"مرحباً بك! جاري تحليل البيانات السياحية الخاصة بـ ({query})... سيتم عرض المعالم والنصائح قريباً."
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
