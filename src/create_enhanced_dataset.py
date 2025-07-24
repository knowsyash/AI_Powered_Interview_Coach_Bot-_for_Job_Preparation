"""
Simple converter for Kaggle Data Science Interview Questions
"""

import pandas as pd
import json

def create_enhanced_questions():
    """Create an enhanced questions file with Kaggle data"""
    
    # Read the Kaggle dataset
    csv_path = "./data/kaggle_datasets/deeplearning_questions.csv"
    df = pd.read_csv(csv_path)
    print(f"📊 Processing {len(df)} questions from Kaggle")
    
    # Sample answers for common deep learning questions
    answers_map = {
        "What is padding": "Padding adds zeros around input data to maintain spatial dimensions after convolution operations.",
        "Sigmoid Vs Softmax": "Sigmoid is used for binary classification (output 0-1), Softmax for multi-class (probability distribution).",
        "What is PoS Tagging": "Part-of-Speech tagging assigns grammatical categories (noun, verb, adjective) to words in text.",
        "What is tokenization": "Tokenization splits text into individual words, phrases, or meaningful elements for processing.",
        "What is topic modeling": "Topic modeling discovers abstract topics in document collections using unsupervised learning methods.",
        "What is back propagation": "Backpropagation calculates gradients and updates neural network weights by propagating errors backward.",
        "What is the idea behind GANs": "GANs use two competing networks (generator vs discriminator) to create realistic synthetic data.",
        "What is the Computational Graph": "A computational graph represents operations as nodes and data flow as edges for efficient gradient computation.",
        "What is sigmoid What does it do": "Sigmoid activation function maps inputs to (0,1) range, useful for binary classification output layers."
    }
    
    # Create new enhanced structure
    enhanced_questions = {
        "Data Scientist": {
            "easy": [
                {
                    "question": "What is overfitting?",
                    "answer": "Overfitting occurs when a model learns training data too well, including noise, reducing generalization ability."
                },
                {
                    "question": "What is the difference between supervised and unsupervised learning?",
                    "answer": "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data."
                },
                {
                    "question": "What is cross-validation?",
                    "answer": "Cross-validation evaluates model performance by splitting data into training and validation sets multiple times."
                }
            ],
            "medium": [],
            "hard": []
        },
        "ML Engineer": {
            "easy": [
                {
                    "question": "What is model deployment?",
                    "answer": "Model deployment makes trained models available for real-world use through APIs, web services, or applications."
                },
                {
                    "question": "What is feature engineering?",
                    "answer": "Feature engineering creates, transforms, and selects relevant features from raw data to improve model performance."
                }
            ],
            "medium": [],
            "hard": []
        },
        "Deep Learning Engineer": {
            "easy": [],
            "medium": [],
            "hard": []
        },
        "Web Developer": {
            "easy": [
                {
                    "question": "What is responsive design?",
                    "answer": "Responsive design ensures websites work well on various devices and screen sizes using flexible layouts."
                }
            ],
            "medium": [],
            "hard": []
        }
    }
    
    # Process Kaggle questions and add them to Deep Learning Engineer
    for _, row in df.iterrows():
        question = str(row['DESCRIPTION']).strip()
        
        # Get answer from our map or create a generic one
        answer = answers_map.get(question, f"This question requires understanding of {question.lower()}. Provide a detailed technical explanation.")
        
        # Simple difficulty assignment
        if any(keyword in question.lower() for keyword in ['what is', 'define']):
            difficulty = "easy"
        elif any(keyword in question.lower() for keyword in ['vs', 'difference', 'compare']):
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        question_obj = {
            "question": question,
            "answer": answer
        }
        
        enhanced_questions["Deep Learning Engineer"][difficulty].append(question_obj)
    
    # Add some questions to other categories too
    # Add a few DL questions to ML Engineer (medium level)
    sample_dl_questions = [
        {
            "question": "What is backpropagation?",
            "answer": "Backpropagation calculates gradients and updates neural network weights by propagating errors backward through layers."
        },
        {
            "question": "What is the difference between CNN and RNN?",
            "answer": "CNNs process spatial data like images using convolutions, while RNNs handle sequential data with memory mechanisms."
        }
    ]
    
    enhanced_questions["ML Engineer"]["medium"].extend(sample_dl_questions)
    
    # Save the enhanced dataset
    output_path = "./data/questions_enhanced.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_questions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Enhanced dataset saved to: {output_path}")
    
    # Print summary
    print("\n📈 Enhanced Dataset Summary:")
    for role, difficulties in enhanced_questions.items():
        total = sum(len(questions) for questions in difficulties.values())
        if total > 0:
            print(f"🎯 {role}: {total} total questions")
            for difficulty, questions in difficulties.items():
                if questions:
                    print(f"   {difficulty}: {len(questions)} questions")

if __name__ == "__main__":
    create_enhanced_questions()
