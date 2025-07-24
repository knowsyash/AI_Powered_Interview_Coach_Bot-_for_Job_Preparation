"""
Kaggle Dataset Loader for Interview Coach Bot
This script helps download and process interview question datasets from Kaggle
"""

import os
import json
import pandas as pd
from pathlib import Path

def setup_kaggle_credentials():
    """Check if Kaggle credentials are properly set up"""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if not kaggle_json.exists():
        print("❌ Kaggle credentials not found!")
        print("Please follow these steps:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Scroll to API section and click 'Create New API Token'")
        print(f"3. Place the downloaded kaggle.json file in: {kaggle_dir}")
        return False
    
    print("✅ Kaggle credentials found!")
    return True

def download_dataset(dataset_name, download_path="./data/kaggle_datasets"):
    """Download a dataset from Kaggle"""
    try:
        import kaggle
        
        # Create download directory
        os.makedirs(download_path, exist_ok=True)
        
        print(f"📥 Downloading dataset: {dataset_name}")
        kaggle.api.dataset_download_files(dataset_name, path=download_path, unzip=True)
        print(f"✅ Dataset downloaded to: {download_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def search_datasets(query="data science interview questions"):
    """Search for datasets on Kaggle"""
    try:
        import kaggle
        
        print(f"🔍 Searching for: {query}")
        datasets = kaggle.api.dataset_list(search=query)
        
        print("\n📋 Found datasets:")
        for i, dataset in enumerate(datasets[:5]):  # Show top 5 results
            print(f"{i+1}. {dataset.ref}")
            print(f"   Title: {dataset.title}")
            print(f"   Size: {dataset.size}")
            print(f"   Downloads: {dataset.downloadCount}")
            print()
            
        return datasets[:5]
        
    except Exception as e:
        print(f"❌ Error searching datasets: {e}")
        return []

def convert_to_interview_format(csv_file_path, output_file="./data/interview_questions_kaggle.json"):
    """Convert Kaggle CSV dataset to our interview format"""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        print(f"📊 Loaded dataset with {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
        # Try to map common column names to our format
        question_cols = ['question', 'Question', 'questions', 'interview_question']
        answer_cols = ['answer', 'Answer', 'answers', 'expected_answer', 'solution']
        difficulty_cols = ['difficulty', 'Difficulty', 'level', 'Level']
        category_cols = ['category', 'Category', 'role', 'Role', 'domain', 'Domain']
        
        # Find matching columns
        question_col = next((col for col in question_cols if col in df.columns), None)
        answer_col = next((col for col in answer_cols if col in df.columns), None)
        difficulty_col = next((col for col in difficulty_cols if col in df.columns), None)
        category_col = next((col for col in category_cols if col in df.columns), None)
        
        if not question_col:
            print("❌ Could not find question column. Available columns:", list(df.columns))
            return False
            
        # Create our format
        interview_data = {}
        
        # Group by category/role if available
        if category_col and category_col in df.columns:
            categories = df[category_col].unique()
        else:
            categories = ["Data Scientist"]  # Default category
            df[category_col] = "Data Scientist"
        
        for category in categories:
            if category not in interview_data:
                interview_data[category] = {"easy": [], "medium": [], "hard": []}
            
            category_data = df[df[category_col] == category] if category_col else df
            
            for _, row in category_data.iterrows():
                question_text = str(row[question_col]).strip()
                answer_text = str(row[answer_col]).strip() if answer_col else "Sample answer for this question."
                
                # Determine difficulty
                if difficulty_col and difficulty_col in df.columns:
                    difficulty = str(row[difficulty_col]).lower()
                    if difficulty not in ["easy", "medium", "hard"]:
                        difficulty = "medium"  # Default
                else:
                    difficulty = "medium"  # Default
                
                question_obj = {
                    "question": question_text,
                    "answer": answer_text
                }
                
                interview_data[category][difficulty].append(question_obj)
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(interview_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Converted dataset saved to: {output_file}")
        
        # Print summary
        for category, difficulties in interview_data.items():
            total = sum(len(questions) for questions in difficulties.values())
            print(f"📈 {category}: {total} questions")
            for diff, questions in difficulties.items():
                print(f"   {diff}: {len(questions)} questions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting dataset: {e}")
        return False

def main():
    """Main function to demonstrate usage"""
    print("=== Kaggle Dataset Loader for Interview Coach Bot ===\n")
    
    # Check credentials
    if not setup_kaggle_credentials():
        return
    
    # Search for datasets
    print("Let's search for Data Science interview datasets...")
    datasets = search_datasets("data science interview")
    
    if datasets:
        print("You can download any of these datasets using:")
        print("download_dataset('dataset-owner/dataset-name')")

if __name__ == "__main__":
    main()
