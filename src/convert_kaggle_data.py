"""
Convert Kaggle Data Science Interview Questions to Interview Coach Bot format
"""

import pandas as pd
import json
import os

def convert_kaggle_to_interview_format():
    """Convert the downloaded Kaggle dataset to our interview format"""
    
    # Read the deep learning questions CSV
    csv_path = "./data/kaggle_datasets/deeplearning_questions.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Dataset file not found: {csv_path}")
        return
    
    # Read the CSV
    df = pd.read_csv(csv_path)
    print(f"📊 Loaded {len(df)} questions from Kaggle dataset")
    
    # Load existing questions
    existing_questions_path = "./data/questions.json"
    with open(existing_questions_path, 'r') as f:
        existing_data = json.load(f)
    
    # Create enhanced dataset
    enhanced_data = existing_data.copy()
    
    # Add sample answers for the Kaggle questions (you can improve these)
    sample_answers = {
        "What is padding": "Padding is adding zeros or other values to input data to maintain spatial dimensions after convolution operations.",
        "Sigmoid Vs Softmax": "Sigmoid outputs values between 0-1 for binary classification, while Softmax outputs probability distribution for multiclass classification.",
        "What is PoS Tagging": "Part-of-Speech tagging is the process of marking up words in text with their corresponding part of speech.",
        "What is tokenization": "Tokenization is the process of breaking down text into individual tokens or words for natural language processing.",
        "What is topic modeling": "Topic modeling is an unsupervised learning technique to discover abstract topics in a collection of documents.",
        "What is back propagation": "Backpropagation is an algorithm for training neural networks by calculating gradients and updating weights backwards through the network.",
        "What is the idea behind GANs": "Generative Adversarial Networks use two competing neural networks - a generator and discriminator - to create realistic synthetic data.",
        "What is the Computational Graph": "A computational graph represents mathematical operations as nodes and data flow as edges, used in automatic differentiation.",
        "What is sigmoid What does it do": "Sigmoid is an activation function that maps input values to a range between 0 and 1, commonly used in binary classification."
    }
    
    # Add more categories
    if "Deep Learning Engineer" not in enhanced_data:
        enhanced_data["Deep Learning Engineer"] = {"easy": [], "medium": [], "hard": []}
    
    # Convert Kaggle questions
    for _, row in df.iterrows():
        question_text = str(row['DESCRIPTION']).strip()
        
        # Get answer from our sample answers or create a generic one
        answer_text = sample_answers.get(question_text, f"This is a technical question about {question_text.lower()}. Please provide a detailed explanation with examples.")
        
        # Assign difficulty based on question complexity (you can improve this logic)
        if any(word in question_text.lower() for word in ['what is', 'define', 'basic']):
            difficulty = "easy"
        elif any(word in question_text.lower() for word in ['difference', 'compare', 'vs']):
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        question_obj = {
            "question": question_text,
            "answer": answer_text
        }
        
        # Add to Deep Learning Engineer category
        enhanced_data["Deep Learning Engineer"][difficulty].append(question_obj)
    
    # Also add some to ML Engineer for variety (ensure structure exists)
    if "ML Engineer" in enhanced_data:
        # Add a few questions to ML Engineer as well
        for i, (_, row) in enumerate(df.head(5).iterrows()):
            question_text = str(row['DESCRIPTION']).strip()
            answer_text = sample_answers.get(question_text, f"Technical explanation for {question_text.lower()}")
            
            question_obj = {
                "question": question_text,
                "answer": answer_text
            }
            
            enhanced_data["ML Engineer"]["medium"].append(question_obj)
    
    # Save enhanced dataset
    output_path = "./data/questions_enhanced.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Enhanced dataset saved to: {output_path}")
    
    # Print summary
    print("\n📈 Dataset Summary:")
    for role, difficulties in enhanced_data.items():
        total = sum(len(questions) for questions in difficulties.values())
        print(f"🎯 {role}: {total} questions")
        for difficulty, questions in difficulties.items():
            if questions:  # Only show if there are questions
                print(f"   {difficulty}: {len(questions)} questions")

if __name__ == "__main__":
    convert_kaggle_to_interview_format()
