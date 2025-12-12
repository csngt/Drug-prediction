from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load model + vectorizer
model = joblib.load("drug_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Load CSV for drug details
df = pd.read_csv("usp_drug_classification.csv")
df['drug_example_clean'] = df['drug_example'].astype(str).str.lower().str.strip()
drug_dict = {row['drug_example_clean']: row.to_dict() for _, row in df.iterrows()}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    example = data.get("drug_example", "").lower().strip()

    if not example:
        return jsonify({"error": "Drug example required"}), 400

    # Check if input exists in CSV dictionary
    if example in drug_dict:
        details = drug_dict[example]
        return jsonify({
            "status": "Drug detected",
            "input": example,
            "details": details
        })
    else:
        # Anything not in CSV → no drug detected
        return jsonify({
            "status": "No drug detected",
            "input": example
        })

@app.route("/")
def home():
    return "Drug Detection API running."

if __name__ == "__main__":
    app.run(debug=True)
