from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to call backend

# Example credit card dataset
cards = [
    {"name": "Starter Credit Card", "min_score": 500, "min_income": 0, "age_req": 18, "ref": "https://example.com/starter"},
    {"name": "Student Rewards Card", "min_score": 600, "min_income": 1000, "age_req": 18, "ref": "https://example.com/student"},
    {"name": "Platinum Rewards Card", "min_score": 700, "min_income": 3000, "age_req": 21, "ref": "https://example.com/platinum"}
]

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    score = int(data.get("score", 0))
    age = int(data.get("age", 0))
    income = int(data.get("income", 0))

    recommendations = []
    for card in cards:
        if score >= card["min_score"] and income >= card["min_income"] and age >= card["age_req"]:
            recommendations.append(card)

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
