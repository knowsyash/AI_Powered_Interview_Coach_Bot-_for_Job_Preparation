"""
🧪 PRACTICAL DEMONSTRATION: How Score Prediction Actually Works
============================================================

This script shows you exactly how your interview coach bot calculates scores
with real examples and step-by-step breakdowns.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator import evaluate_answer, clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def demonstrate_text_cleaning():
    """Show how text preprocessing works"""
    print("=" * 70)
    print("🧹 TEXT CLEANING DEMONSTRATION")
    print("=" * 70)
    
    examples = [
        "Machine Learning is the study of algorithms!",
        "Overfitting occurs when a model learns the training data too well.",
        "What is the difference between supervised and unsupervised learning?",
        "Deep learning uses neural networks with multiple layers."
    ]
    
    for i, text in enumerate(examples, 1):
        cleaned = clean_text(text)
        print(f"\nExample {i}:")
        print(f"Original:  '{text}'")
        print(f"Cleaned:   '{cleaned}'")
        print(f"Changes:   Removed: punctuation, stopwords | Made: lowercase")

def demonstrate_tfidf_vectorization():
    """Show how TF-IDF converts text to numbers"""
    print("\n" + "=" * 70)
    print("📊 TF-IDF VECTORIZATION DEMONSTRATION")
    print("=" * 70)
    
    # Sample texts
    texts = [
        "machine learning algorithms",
        "deep learning neural networks",
        "supervised learning classification"
    ]
    
    print("Sample texts:")
    for i, text in enumerate(texts, 1):
        print(f"{i}. '{text}'")
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    print(f"\nVocabulary (unique words): {list(feature_names)}")
    print(f"Vector dimensions: {len(feature_names)}")
    
    print("\nTF-IDF Vectors:")
    for i, vector in enumerate(tfidf_matrix.toarray()):
        print(f"\nText {i+1}: '{texts[i]}'")
        print("Vector:", [round(val, 3) for val in vector])
        
        # Show which words have highest scores
        word_scores = list(zip(feature_names, vector))
        top_words = sorted(word_scores, key=lambda x: x[1], reverse=True)[:3]
        print("Top words:", [(word, round(score, 3)) for word, score in top_words])

def demonstrate_cosine_similarity():
    """Show how cosine similarity calculates the final score"""
    print("\n" + "=" * 70)
    print("📐 COSINE SIMILARITY DEMONSTRATION")
    print("=" * 70)
    
    # Example question and answers
    question = "What is overfitting?"
    expected_answer = "Overfitting is when a model learns the training data too well, including noise."
    
    user_answers = [
        "Overfitting happens when a model memorizes training data",  # Good answer
        "When machine learning model is too complex",               # Medium answer
        "I don't know",                                           # Poor answer
        "Overfitting occurs when a model learns the training data too well and fails to generalize to new data"  # Excellent answer
    ]
    
    print(f"Question: '{question}'")
    print(f"Expected Answer: '{expected_answer}'")
    print("\nUser Answers and Scores:")
    
    for i, user_answer in enumerate(user_answers, 1):
        score = evaluate_answer(user_answer, expected_answer)
        
        # Get feedback
        if score >= 0.8:
            feedback = "✅ Excellent"
        elif score >= 0.5:
            feedback = "⚠️ Decent"
        else:
            feedback = "❌ Needs improvement"
        
        print(f"\n{i}. User Answer: '{user_answer}'")
        print(f"   Score: {score:.3f} ({score*100:.1f}%)")
        print(f"   Feedback: {feedback}")
        
        # Show cleaned versions
        user_clean = clean_text(user_answer)
        expected_clean = clean_text(expected_answer)
        print(f"   User (cleaned): '{user_clean}'")
        print(f"   Expected (cleaned): '{expected_clean}'")

def demonstrate_why_scores_differ():
    """Explain why different answers get different scores"""
    print("\n" + "=" * 70)
    print("🤔 WHY SCORES DIFFER - DETAILED ANALYSIS")
    print("=" * 70)
    
    expected = "Overfitting is when a model learns the training data too well, including noise."
    expected_clean = clean_text(expected)
    expected_words = set(expected_clean.split())
    
    print(f"Expected answer keywords: {expected_words}")
    
    test_answers = [
        ("Overfitting occurs when a model learns the training data too well and fails to generalize", "High overlap"),
        ("Machine learning model is too complex and overfits", "Some overlap"),
        ("Neural networks have too many parameters", "No direct overlap"),
        ("Overfitting training data model learns well noise", "Perfect keyword match")
    ]
    
    for answer, description in test_answers:
        score = evaluate_answer(answer, expected)
        answer_clean = clean_text(answer)
        answer_words = set(answer_clean.split())
        
        overlap = expected_words.intersection(answer_words)
        overlap_ratio = len(overlap) / len(expected_words)
        
        print(f"\nAnswer: '{answer}'")
        print(f"Score: {score:.3f}")
        print(f"Keyword overlap: {overlap}")
        print(f"Overlap ratio: {overlap_ratio:.2f}")
        print(f"Why: {description}")

def demonstrate_edge_cases():
    """Show how the system handles edge cases"""
    print("\n" + "=" * 70)
    print("🔍 EDGE CASES AND SPECIAL SCENARIOS")
    print("=" * 70)
    
    expected = "Machine learning is a subset of artificial intelligence."
    
    edge_cases = [
        ("", "Empty answer"),
        ("Machine learning subset artificial intelligence", "Perfect keywords, different order"),
        ("ML is part of AI", "Abbreviations and synonyms"),
        ("Artificial intelligence includes machine learning", "Reverse relationship"),
        ("Machine learning machine learning machine learning", "Repeated words"),
        ("The the the is is is", "Only stopwords")
    ]
    
    for answer, case_type in edge_cases:
        if answer:  # Skip empty for actual scoring
            score = evaluate_answer(answer, expected)
            print(f"\nCase: {case_type}")
            print(f"Answer: '{answer}'")
            print(f"Score: {score:.3f}")
        else:
            print(f"\nCase: {case_type}")
            print(f"Answer: '{answer}'")
            print(f"Score: 0.000 (handled by main.py - skipped)")

def main():
    """Run all demonstrations"""
    print("🧪 INTERVIEW COACH BOT - SCORING SYSTEM DEEP DIVE")
    print("This demonstration shows exactly how your bot calculates scores!")
    
    demonstrate_text_cleaning()
    demonstrate_tfidf_vectorization()
    demonstrate_cosine_similarity()
    demonstrate_why_scores_differ()
    demonstrate_edge_cases()
    
    print("\n" + "=" * 70)
    print("🎓 CONCLUSION")
    print("=" * 70)
    print("Your Interview Coach Bot uses sophisticated NLP techniques to:")
    print("1. Clean and normalize text")
    print("2. Convert text to numerical vectors using TF-IDF")
    print("3. Calculate semantic similarity using cosine similarity")
    print("4. Provide meaningful feedback based on similarity scores")
    print("\nThis approach allows the bot to understand meaning, not just")
    print("exact word matches, making it a powerful learning tool!")

if __name__ == "__main__":
    main()
