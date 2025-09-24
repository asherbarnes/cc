import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to call backend

# Use a DB file located next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'cards.db')
SQL_SEED = os.path.join(BASE_DIR, 'cards.sql')

def init_db():
    try:
        if os.path.exists(SQL_SEED):
            with sqlite3.connect(DB_PATH) as conn:
                with open(SQL_SEED, 'r', encoding='utf-8') as f:
                    script = f.read()
                conn.executescript(script)
        else:
            if not os.path.exists(DB_PATH):
                open(DB_PATH, 'a').close()
    except Exception as e:
        # ensure any init error is visible and raised as JSON later
        app.logger.exception("Database initialization failed: %s", e)
        raise

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB at startup (let exceptions propagate so startup fails visibly)
init_db()

@app.route('/')
def home():
    return "Flask backend is running!"

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            score = int(data.get("score", 0))
            age = int(data.get("age", 0))
            income = int(data.get("income", 0))
        except Exception:
            return jsonify({"error": "Invalid input. Provide numeric 'score', 'age', and 'income'."}), 400

        try:
            conn = get_db_connection()
            cards = conn.execute(
                'SELECT * FROM cards WHERE min_score <= ? AND min_income <= ? AND age_req <= ?',
                (score, income, age)
            ).fetchall()
        except Exception as e:
            app.logger.exception("Database query failed: %s", e)
            return jsonify({"error": "Internal server error while querying database."}), 500
        finally:
            try:
                conn.close()
            except Exception:
                pass

        recommendations = []
        for card in cards:
            recommendations.append({
                "name": card["name"],
                "cashback_min": card["cashback_min"],
                "cashback_max": card["cashback_max"],
                "apr_min": card["apr_min"],
                "apr_max": card["apr_max"],
                "annual_fee": card["annual_fee"],
                "ref": card["ref"]
            })
        return jsonify(recommendations)
    else:
        return jsonify({"message": "Send a POST request with score, age, and income."})

# ...existing code...
if __name__ == '__main__':
    # bind explicitly to localhost and keep default port 5000
    app.run(host='127.0.0.1', debug=True)
