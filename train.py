import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load CSV dataset
df = pd.read_csv("usp_drug_classification.csv")
df['drug_example_clean'] = df['drug_example'].astype(str).str.lower().str.strip()

# Label: all 1 (drug)
df['is_drug'] = 1

# Features and target
X = df['drug_example_clean']
y = df['is_drug']

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# Train RandomForestClassifier (all positive examples)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_tfidf, y)

# Save model and vectorizer
joblib.dump(clf, "drug_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Training complete! Only drugs in dataset, model ready.")
