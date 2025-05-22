"""
Train a sentiment analysis model on a labeled tweet dataset.

Main steps:
1. Download and load the dataset
2. Clean the text data
3. Vectorize using TF-IDF
4. Split into training and test sets
5. Train a logistic regression model
6. Evaluate performance
7. Save the model and the vectorizer for later use
"""

# === Library imports ===

# Data manipulation
import gdown
import pandas as pd

# Visualisation (optionnal but useful)
import matplotlib.pyplot as plt
import seaborn as sns

# Text vectorization
from sklearn.feature_extraction.text import TfidfVectorizer

# Data splitting
from sklearn.model_selection import train_test_split

# Machine learning model
from sklearn.linear_model import LogisticRegression

# Evaluation metrics
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Save models
import pickle

# Text preprocessing
from utils import clean_text

# === Step 1: Download and load the dataset ===

# Google Drive public file ID and download target
file_id = "1VrM1g88xG94SOIUo8JAg0-J2yby6kYjE"
output = "data.csv"

print("\n📥 Downloading dataset from Google Drive...")
gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)
print("✅ Dataset downloaded.\n")

# Read the CSV into a DataFrame
df = pd.read_csv(output)

print("📝 Preview of the dataset:")
print(df.head(), "\n")

print("📊 Available columns:")
print(df.columns)
print("\n")

print("📈 Class distribution (positive/negative tweets):")
print(df['label'].value_counts(), "\n")

print("🔍 Missing values in the dataset:")
print(df.isna().sum(), "\n")

# === Step 2: Text cleaning ===

print("🧹 Cleaning text data...")
df['clean_text'] = df['text'].apply(clean_text)
print("✅ Text cleaned.\n")

# === Step 3: TF-IDF Vectorization ===

print("🧠 Vectorizing text using TF-IDF...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))  # Unigrams + bigrames
# max_features=5000 : limite la dimension pour éviter le sur-apprentissage.
# ngram_range=(1,2) : prend en compte des paires de mots (ex : "très bien", "pas content").
X = vectorizer.fit_transform(df['clean_text'])
y = df['label']
print("✅ Text vectorized.\n")


# === Step 4: Train/Test Split ===

print("✂️ Splitting data: 80% train / 20% test...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("✅ Data split complete.\n")

# === Step 5: Train the Logistic Regression model ===

print("⚙️ Training logistic regression model...")
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)
print("✅ Model trained.\n")

# === Step 6: Model Evaluation ===

print("📏 Model evaluation:\n")

y_pred = model.predict(X_test)

print("✅ Accuracy:", round(accuracy_score(y_test, y_pred), 4), "\n")

print("✅ Classification report:\n")
print(classification_report(y_test, y_pred))

print("✅ Confusion matrix (text):\n")
print(pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted']), "\n")

# === Step 7: Confusion Matrix Visualization ===

print("📊 Visualizing confusion matrix...\n")

cm = confusion_matrix(y_test, y_pred)
labels = ['Negative', 'Positive']

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show() 


# === Step 8: Save the model and vectorizer ===

print("💾 Saving trained model to 'sentiment_analysis_model.pkl'...")
with open("sentiment_analysis_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("✅ Model saved.\n")

print("💾 Saving TF-IDF vectorizer to 'sentiment_analysis_vectorizer.pkl'...")
with open('sentiment_analysis_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print("✅ Vectorizer saved.\n")

print("🎉 Training complete! The model is now ready to be used in an API or web app.\n")
