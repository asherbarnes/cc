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
                try:
                    conn.executescript(script)
                except sqlite3.OperationalError as e:
                    # if the seed refers to a column not present in the existing table,
                    # attempt a targeted migration for the known 'rec_score' column and retry.
                    msg = str(e).lower()
                    if 'no column named rec_score' in msg:
                        app.logger.info("Migration: adding missing 'rec_score' column to cards table")
                        try:
                            conn.execute("ALTER TABLE cards ADD COLUMN rec_score INTEGER DEFAULT NULL;")
                            conn.executescript(script)
                        except Exception:
                            app.logger.exception("Retrying seed after adding column failed")
                            raise
                    else:
                        # unknown operational error, re-raise so startup fails visibly
                        raise
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

        # If no cards matched, return empty list quickly
        if not cards:
            return jsonify([])

        # Prepare numeric values and compute mins/maxes for normalization
        rec_values = []
        fee_values = []
        prepared = []
        for card in cards:
            # Use rec_score if present otherwise fall back to min_score
            rec = card["rec_score"] if card["rec_score"] is not None else card["min_score"]
            fee = float(card["annual_fee"] or 0.0)
            rec_values.append(rec)
            fee_values.append(fee)
            prepared.append({
                "row": card,
                "rec": float(rec),
                "fee": fee
            })

        min_rec = min(rec_values) if rec_values else 0.0
        max_rec = max(rec_values) if rec_values else 0.0
        max_fee = max(fee_values) if fee_values else 0.0

        # User-influenced factors (capped)
        user_score_factor = min(max(score / 850.0, 0.0), 1.0)   # higher score => more weight on rec_score
        income_factor = min(max(income / 150000.0, 0.0), 1.0)   # higher income => more weight on annual_fee

        # Weights for combining components
        SCORE_WEIGHT = 0.65
        FEE_WEIGHT = 0.35

        ranked = []
        for p in prepared:
            # normalized rec_score (0..1)
            if max_rec > min_rec:
                rec_norm = (p["rec"] - min_rec) / (max_rec - min_rec)
            else:
                rec_norm = 0.5  # neutral if no range

            # normalized fee (0..1)
            fee_norm = (p["fee"] / max_fee) if max_fee > 0 else 0.0

            # final score: give rec_score more importance for users with higher credit scores,
            # and give fee more importance for users with higher incomes.
            final_score = (SCORE_WEIGHT * rec_norm * user_score_factor) + (FEE_WEIGHT * fee_norm * income_factor)

            ranked.append((final_score, p["row"]))

        # sort by final_score desc, break ties by better cashback_max then lower apr_min
        ranked.sort(key=lambda t: (t[0], float(t[1]["cashback_max"] or 0.0), -float(t[1]["apr_min"] or 0.0)), reverse=True)

        recommendations = []
        for _, card in ranked:
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

if __name__ == '__main__':
    # bind explicitly to localhost and keep default port 5000
    app.run(host='127.0.0.1', debug=True)
