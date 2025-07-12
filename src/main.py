from question_selector import load_questions
from evaluator import evaluate_answer
from resources import get_tip
from logger import log_response

print("=== Interview Coach Bot ===")

# Step 1: Choose Role
available_roles = ["Data Scientist", "ML Engineer", "Web Developer"]

print("\nAvailable roles:")
for i, role_name in enumerate(available_roles):
    print(f"{i + 1}. {role_name}")

while True:
    try:
        role_choice = int(input("Choose a role (1/2/3): "))
        if 1 <= role_choice <= len(available_roles):
            role = available_roles[role_choice - 1]
            break
        else:
            print("❌ Invalid choice. Please choose 1, 2, or 3.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Step 2: Choose Difficulty
while True:
    difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
    if difficulty in ["easy", "medium", "hard"]:
        break
    else:
        print("❌ Please enter one of: easy, medium, or hard.")

# Step 3: Load Questions
questions = load_questions(role, difficulty)

# Step 4: Start Interview Loop
all_scores = []
attempted = 0

for i, q in enumerate(questions):
    print(f"\nQ{i+1}: {q['question']}")
    user_answer = input("Your Answer: ").strip()
    
    if user_answer:
        score = evaluate_answer(user_answer, q["answer"])
        tip = get_tip(score)
        print(f"Similarity Score: {round(score, 2)}")
        print("Feedback:", tip)

        log_response(q["question"], user_answer, score, tip)

        all_scores.append(score)
        attempted += 1
    else:
        print("⚠️ Skipped.")

# Step 5: Show Session Summary
print("\n===== SESSION SUMMARY =====")
print(f"Total Questions    : {len(questions)}")
print(f"Attempted          : {attempted}")

if attempted > 0:
    avg_score = sum(all_scores) / attempted
    print(f"Average Score      : {round(avg_score, 2)}")

    if avg_score >= 0.75:
        print("Performance        : ✅ Excellent")
    elif avg_score >= 0.5:
        print("Performance        : ⚠️ Average")
    else:
        print("Performance        : ❌ Needs Improvement")
else:
    print("No questions were attempted.")
print("===========================")
