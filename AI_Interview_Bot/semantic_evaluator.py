import numpy as np
import os
import joblib
from sentence_transformers import SentenceTransformer

class SemanticAnswerEvaluator:
    def __init__(self):
        self.model = None
        self.embedder = None
        
    def load_model(self):
        print("Loading Lite LLM embedding model (all-MiniLM-L6-v2)...")
        # Keep it small and lightweight for Render deployment
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'real_dataset_score', 'semantic_rf_model.joblib')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Semantic model not found at {model_path}")
            
        self.model = joblib.load(model_path)
        print("Semantic Evaluation Model loaded successfully.")
        
    def evaluate_answer(self, question, answer, reference_answer=None):
        if self.model is None or self.embedder is None:
            raise ValueError("Model not loaded. Call load_model() first.")
            
        # 1. Embed the user's answer
        # The embedding captures the true context and meaning of the text
        embedding = self.embedder.encode([answer])
        
        # 2. Predict the score (1-10 scale) using the semantic RF regressor
        predicted_score = float(self.model.predict(embedding)[0])
        
        # 3. Generate generic feedback based on the predicted score
        if predicted_score >= 8.0:
            feedback = "Excellent answer. You clearly conveyed your ideas with strong context and high relevance to the question."
        elif predicted_score >= 6.0:
            feedback = "Good answer. It was relevant and made sense, but could benefit from more specific details or clearer structure."
        else:
            feedback = "Your answer missed key concepts or lacked sufficient detail. Try to directly address the core of the question."
            
        return {
            'predicted_score': predicted_score,
            'feedback': feedback,
            'details': {
                'score': predicted_score
            }
        }
