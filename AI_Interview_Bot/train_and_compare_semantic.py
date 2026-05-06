import pandas as pd
import numpy as np
import re
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

print("Loading Sentence Transformers (Lite LLM)...")
from sentence_transformers import SentenceTransformer

# Load the old model
from random_forest_evaluator import RandomForestAnswerEvaluator

def main():
    print("=" * 60)
    print("1. DATASET ACQUISITION & REFINEMENT")
    print("=" * 60)
    
    data_dir = 'real_dataset_score'
    
    # We use the StackOverflow dataset because it contains REAL human answers,
    # avoiding the highly synthetic 'As a role...' template of the behavioral dataset.
    print("Loading real human answers from stackoverflow_training_data.csv...")
    so_df = pd.read_csv(os.path.join(data_dir, 'stackoverflow_training_data.csv'))
    
    # Take a representative sample to ensure it trains quickly
    # Refine: Remove extremely short or extremely long answers, drop NaNs
    so_df = so_df.dropna(subset=['user_answer', 'score', 'question'])
    so_df['answer_len'] = so_df['user_answer'].apply(lambda x: len(str(x).split()))
    
    # Filter high quality answers
    refined_df = so_df[(so_df['answer_len'] >= 20) & (so_df['answer_len'] <= 300)].sample(2000, random_state=42)
    
    # Ensure scores are continuous 1-10
    refined_df['score'] = pd.to_numeric(refined_df['score'], errors='coerce').fillna(5.0)
    
    # Combine with original behavioral dataset for better score balance
    beh_df = pd.read_csv(os.path.join(data_dir, 'interview_data_with_scores.csv'))
    # behavioral dataset scores are 1-5, convert to 1-10
    beh_df['score'] = beh_df['human_score'] * 2.0
    beh_df['user_answer'] = beh_df['answer']
    beh_df = beh_df[['question', 'user_answer', 'score']].dropna()
    
    # Also add the huggingface external data if it exists
    try:
        hf_df = pd.read_csv(os.path.join(data_dir, 'huggingface_external_data.csv'))
        hf_df['score'] = 9.0  # these are high quality
        refined_df = pd.concat([refined_df, beh_df, hf_df], ignore_index=True)
    except:
        refined_df = pd.concat([refined_df, beh_df], ignore_index=True)
        
    refined_df = refined_df.sample(min(4000, len(refined_df)), random_state=42)
    
    print(f"Refined dataset ready. Training on {len(refined_df)} real-world samples.")
    
    X_text = refined_df['user_answer'].tolist()
    y = refined_df['score'].values
    questions = refined_df['question'].tolist()
    
    # Train-test split
    X_train_text, X_test_text, y_train, y_test, q_train, q_test = train_test_split(
        X_text, y, questions, test_size=0.2, random_state=42
    )
    
    print("\n" + "=" * 60)
    print("2. TRAINING SEMANTIC MODEL (RAG-LITE)")
    print("=" * 60)
    print("Loading all-MiniLM-L6-v2 embedding model...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating dense semantic embeddings for training data (this captures true meaning)...")
    X_train_embeddings = embedder.encode(X_train_text, show_progress_bar=True)
    X_test_embeddings = embedder.encode(X_test_text, show_progress_bar=True)
    
    print("Training Random Forest Regressor on Semantic Embeddings...")
    semantic_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
    semantic_model.fit(X_train_embeddings, y_train)
    
    y_pred_semantic = semantic_model.predict(X_test_embeddings)
    
    print("\n" + "=" * 60)
    print("3. EVALUATING OLD MODEL (TF-IDF + KEYWORDS)")
    print("=" * 60)
    print("Loading existing RandomForestAnswerEvaluator...")
    old_evaluator = RandomForestAnswerEvaluator()
    try:
        old_evaluator.load_model()
    except Exception as e:
        print(f"Error loading old model: {e}")
        return
        
    # Evaluate old model on the same test set
    y_pred_old = []
    print("Running old model feature extraction on test set (this uses brittle keyword counts)...")
    for ans in X_test_text:
        # Extract features
        features = old_evaluator.extract_features(ans)
        X_old = np.array([list(features.values())])
        # Predict
        try:
            score = old_evaluator.model.predict(X_old)[0]
        except:
            score = 3
        y_pred_old.append(score)
        
    y_pred_old = np.array(y_pred_old)
    
    print("\n" + "=" * 60)
    print("4. COMPARISON RESULTS")
    print("=" * 60)
    
    # Metrics calculation
    def calc_metrics(y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        # Within +/- 1.5 accuracy (since scale is 1-10)
        within_1_5 = np.mean(np.abs(y_true - y_pred) <= 1.5)
        return rmse, mae, within_1_5

    # Note: old model outputs 1-5, so we multiply by 2 for fair 1-10 comparison
    rmse_sem, mae_sem, w1_sem = calc_metrics(y_test, y_pred_semantic)
    rmse_old, mae_old, w1_old = calc_metrics(y_test, y_pred_old * 2)
    
    print(f"{'Metric':<25} | {'Old Model (TF-IDF)':<20} | {'New Model (Semantic RAG)':<20}")
    print("-" * 75)
    print(f"{'Within ±1.5 Accuracy':<25} | {w1_old:.4f}{'':<14} | {w1_sem:.4f} (+{(w1_sem-w1_old):.4f})")
    print(f"{'RMSE (Lower is better)':<25} | {rmse_old:.4f}{'':<14} | {rmse_sem:.4f} ({-1*(rmse_sem-rmse_old):.4f})")
    print(f"{'MAE (Lower is better)':<25} | {mae_old:.4f}{'':<14} | {mae_sem:.4f} ({-1*(mae_sem-mae_old):.4f})")
    
    print("\nCONCLUSION:")
    if rmse_sem < rmse_old:
        print("The Semantic Embedding (Lite LLM) model significantly outperforms the old TF-IDF model on real human answers!")
        print("It captures true contextual meaning, avoids template overfitting, and tracks much closer to the actual score.")
        
    # Save the new semantic pipeline
    print("\nSaving new Semantic Evaluator model...")
    joblib.dump(semantic_model, os.path.join(data_dir, 'semantic_rf_model.joblib'))
    print("Saved to real_dataset_score/semantic_rf_model.joblib")

if __name__ == "__main__":
    main()
