import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to call backend

def get_db_connection():
    conn = sqlite3.connect('cards.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Flask backend is running!"

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        data = request.json
        score = int(data.get("score", 0))
        age = int(data.get("age", 0))
        income = int(data.get("income", 0))

        conn = get_db_connection()
        cards = conn.execute(
            'SELECT * FROM cards WHERE min_score <= ? AND min_income <= ? AND age_req <= ?',
            (score, income, age)
        ).fetchall()
        conn.close()

        recommendations = [dict(card) for card in cards]
        return jsonify(recommendations)
    else:
        return jsonify({"message": "Send a POST request with score, age, and income."})
    
if __name__ == '__main__':
    app.run(debug=True)
