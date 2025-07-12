from datetime import datetime

def log_response(question, user_answer, score, feedback):
    with open("logs/session_log.txt", "a", encoding="utf-8") as f:
        f.write("---- New Response ----\n")
        f.write(f"Timestamp : {datetime.now()}\n")
        f.write(f"Question  : {question}\n")
        f.write(f"Answer    : {user_answer}\n")
        f.write(f"Score     : {round(score, 2)}\n")
        f.write(f"Feedback  : {feedback}\n\n")
