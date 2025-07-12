import json
import os

def load_questions(role, difficulty):
    file_path = os.path.join("src", "questions.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if role not in data:
        raise ValueError(f"Role '{role}' not found.")
    if difficulty not in data[role]:
        raise ValueError(f"Difficulty '{difficulty}' not found for role '{role}'.")
    
    return data[role][difficulty]
