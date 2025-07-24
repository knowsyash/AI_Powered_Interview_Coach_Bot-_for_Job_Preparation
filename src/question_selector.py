import json
import os

def load_questions(role, difficulty):
    # Try enhanced dataset first, fallback to original
    enhanced_path = os.path.join("data", "questions_enhanced.json")
    original_path = os.path.join("data", "questions.json")
    
    file_path = enhanced_path if os.path.exists(enhanced_path) else original_path
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if role not in data:
        raise ValueError(f"Role '{role}' not found.")
    if difficulty not in data[role]:
        raise ValueError(f"Difficulty '{difficulty}' not found for role '{role}'.")
    
    questions = data[role][difficulty]
    if not questions:
        raise ValueError(f"No questions found for {role} - {difficulty} level.")
    
    return questions
