# 🤖 AI-Powered Interview Coach Bot

An intelligent interview preparation tool that helps job seekers practice and improve their interview skills through AI-powered question evaluation and feedback.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

The AI-Powered Interview Coach Bot is designed to simulate real interview scenarios for different job roles. It uses Natural Language Processing (NLP) techniques to evaluate your answers against model responses and provides instant feedback to help you improve.

### Supported Job Roles:
- **Data Scientist** - Questions about machine learning, statistics, and data analysis
- **ML Engineer** - Questions about model deployment, MLOps, and engineering practices
- **Web Developer** - Questions about web technologies, responsive design, and development practices

### Difficulty Levels:
- **Easy** - Fundamental concepts and basic questions
- **Medium** - Intermediate level questions (coming soon)
- **Hard** - Advanced concepts and complex scenarios (coming soon)

## ✨ Features

- 🎯 **Role-specific Questions**: Tailored questions for different job positions
- 🧠 **AI-Powered Evaluation**: Uses TF-IDF vectorization and cosine similarity for answer assessment
- 📊 **Real-time Scoring**: Instant feedback with similarity scores (0-1 scale)
- 📝 **Session Logging**: Automatic logging of all responses for review
- 📈 **Performance Analytics**: Session summaries with average scores and performance ratings
- 🎨 **User-friendly Interface**: Clean command-line interface with emojis and clear feedback

## 🔧 Prerequisites

Before running the Interview Coach Bot, ensure you have:

- **Python 3.7+** installed on your system
- **pip** package manager
- Internet connection (for initial NLTK data download)

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/knowsyash/AI_Powered_Interview_Coach_Bot-_for_Job_Preparation.git
cd interview-coach-bot
```

### Step 2: Set Up Python Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```bash
python src/download_nltk.py
```

## 🎮 Usage

### Starting the Interview Session

1. **Navigate to the project directory**:
   ```bash
   cd interview-coach-bot
   ```

2. **Run the main application**:
   ```bash
   python src/main.py
   ```

3. **Follow the interactive prompts**:
   - Choose your target job role (1-3)
   - Select difficulty level (easy/medium/hard)
   - Answer the interview questions
   - Review your performance summary

### Example Session

```
=== Interview Coach Bot ===

Available roles:
1. Data Scientist
2. ML Engineer
3. Web Developer
Choose a role (1/2/3): 1
Choose difficulty (easy/medium/hard): easy

Q1: What is overfitting?
Your Answer: Overfitting occurs when a machine learning model learns the training data too well, including noise and random fluctuations, making it perform poorly on new, unseen data.
Similarity Score: 0.85
Feedback: ✅ Excellent! Your answer is very close to the ideal one.

===== SESSION SUMMARY =====
Total Questions    : 1
Attempted          : 1
Average Score      : 0.85
Performance        : ✅ Excellent
===========================
```

## 📁 Project Structure

```
interview-coach-bot/
│
├── src/                          # Source code directory
│   ├── main.py                   # Main application entry point
│   ├── question_selector.py      # Loads questions based on role/difficulty
│   ├── evaluator.py             # AI evaluation engine using NLP
│   ├── resources.py             # Feedback generation based on scores
│   ├── logger.py                # Session logging functionality
│   ├── download_nltk.py         # NLTK data downloader
│   └── test_tokenizer.py        # Testing utilities
│
├── data/                        # Data directory
│   └── questions.json          # Question database
│
├── logs/                       # Log files
│   └── session_log.txt        # Session history and responses
│
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
└── LINK.txt                 # Additional resources
```

## 🔬 How It Works

### 1. **Question Selection**
- Questions are loaded from `data/questions.json` based on selected role and difficulty
- Questions are structured with both the question text and ideal answer

### 2. **Answer Evaluation Process**
```python
# Text preprocessing
user_answer → clean_text() → remove_stopwords → tokenize

# Vectorization
TF-IDF vectorization of both user answer and ideal answer

# Similarity Calculation
cosine_similarity(user_vector, ideal_vector) → similarity_score (0-1)
```

### 3. **Scoring System**
- **0.8 - 1.0**: ✅ Excellent (Your answer is very close to the ideal one)
- **0.5 - 0.79**: ⚠️ Decent (You covered some key points, but can elaborate more)
- **0.0 - 0.49**: ❌ Needs Improvement (Study the core concept and include relevant keywords)

### 4. **Session Logging**
Every response is automatically logged with:
- Timestamp
- Question asked
- User's answer
- Similarity score
- Feedback provided

## 🎨 Customization

### Adding New Questions

Edit `data/questions.json` to add new questions:

```json
{
  "Data Scientist": {
    "easy": [
      {
        "question": "Your new question here?",
        "answer": "The ideal answer for evaluation."
      }
    ],
    "medium": [
      // Add medium level questions
    ],
    "hard": [
      // Add hard level questions
    ]
  }
}
```

### Adding New Job Roles

1. **Update `questions.json`** with the new role structure
2. **Modify `main.py`** to include the new role in `available_roles` list

### Customizing Feedback

Edit the `get_tip()` function in `src/resources.py` to customize feedback messages and scoring thresholds.

## 🛠️ Troubleshooting

### Common Issues

1. **FileNotFoundError: questions.json not found**
   ```
   Solution: Ensure you're running from the project root directory
   ```

2. **ModuleNotFoundError: No module named 'sklearn'**
   ```bash
   Solution: pip install -r requirements.txt
   ```

3. **NLTK Download Errors**
   ```bash
   Solution: Run python src/download_nltk.py
   ```

4. **Virtual Environment Issues**
   ```bash
   # Deactivate and recreate
   deactivate
   rm -rf venv  # or rmdir /s venv on Windows
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Performance Tips

- For better evaluation accuracy, provide detailed answers with relevant keywords
- Review logged sessions in `logs/session_log.txt` to track improvement
- Practice multiple times with the same questions to see score improvements

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Add new questions** to the database
4. **Improve the evaluation algorithm**
5. **Add new job roles or difficulty levels**
6. **Submit a pull request**

### Areas for Improvement:
- Add more comprehensive question databases
- Implement medium and hard difficulty levels
- Add support for code-based questions
- Integrate voice-to-text for verbal practice
- Add web interface using Flask/Django
- Implement user accounts and progress tracking

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Additional Resources

- [Project Demo](https://chatgpt.com/share/6871f1f4-1cd8-8000-b676-6003ea96d129)
- [Machine Learning Interview Questions](https://github.com/yourusername/ml-interview-questions)
- [Web Development Interview Prep](https://github.com/yourusername/web-dev-interview-prep)

---

**Made with ❤️ for job seekers worldwide**

*Last updated: July 2025*