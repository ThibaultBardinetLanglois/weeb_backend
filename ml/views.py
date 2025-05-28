from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pickle
import json
import numpy as np
import os
from utils import clean_text 



# Load the sentiment analysis and vectorizer model once on server load

# Path to Trained Logistic Regression Model for Sentiment Analysis
SENTIMENT_ANALYSIS_MODEL_PATH = os.path.join(os.path.dirname(__file__), '../sentiment_analysis_model.pkl')

# Loading the model
with open(SENTIMENT_ANALYSIS_MODEL_PATH, 'rb') as f:
    sentiment_analysis_model = pickle.load(f)

# Path to the TF-IDF vectorizer used during training
SENTIMENT_ANALYSIS_VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), '../sentiment_analysis_vectorizer.pkl')

# Loading the vectorization model
with open(SENTIMENT_ANALYSIS_VECTORIZER_PATH, 'rb') as f:
    sentiment_analysis_vectorizer = pickle.load(f)

# Sentiment Analysis Prediction View
@csrf_exempt # allow POST requests without CSRF token (for Postman)
def sentiment_analysis(request):
    """
    Predicts the sentiment of a given text via a POST request.

    Expected request (JSON) :
        {
            "text": "text string to parse"
        }

    Response (JSON) :
        {
            "prediction": 0 fornegatve  # or 1 for positive
        }

    Error codes :
        - 400 : missing or empty field
        - 500 : internal error (e.g. format or vectorization problem)

    Returns:
        JsonResponse: Containing prediction or error.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            text = body["text"]
            
            if not text:
                return JsonResponse({"error": "Champ 'text' manquant"}, status=400)
            
            # Text cleaning and preprocessing
            cleaned = clean_text(text)
            vectorized_text = sentiment_analysis_vectorizer.transform([cleaned])
            
            # Prediction
            prediction = sentiment_analysis_model.predict(vectorized_text)[0]
            
            return JsonResponse({"prediction": int(prediction)})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)