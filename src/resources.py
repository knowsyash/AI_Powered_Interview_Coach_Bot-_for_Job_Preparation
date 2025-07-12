def get_tip(score):
    if score >= 0.8:
        return "✅ Excellent! Your answer is very close to the ideal one."
    elif score >= 0.5:
        return "⚠️ Decent attempt. You covered some key points, but you can elaborate more."
    else:
        return "❌ Needs improvement. Try to study the core concept and include relevant keywords."
