from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/ai-process', methods=['POST'])
def ai_process():
    data = request.get_json() or {}
    query = data.get('query', '')
    reply = f"مرحباً بك! لقد استلمت وجهتك: {query}. جاري إعداد التقرير السياحي..."
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
