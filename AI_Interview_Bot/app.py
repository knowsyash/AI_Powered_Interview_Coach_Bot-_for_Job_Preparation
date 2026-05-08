from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import pandas as pd
import os
import nltk
from dataset_loader import DatasetLoader
from semantic_evaluator import SemanticAnswerEvaluator
from reference_answer_loader import ReferenceAnswerLoader


# Download NLTK data at startup
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']:
    try:
        nltk.download(resource, quiet=True)
    except:
        pass

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

class InterviewBotSession:
    def __init__(self, category='webdev'):
        self.category = category
        self.questions = []
        self.scores = []
        self.answers = []
        self.current_question_idx = 0
        self.current_question = None
        
        # Load the new Lite LLM semantic evaluator
        self.semantic_evaluator = SemanticAnswerEvaluator()
        try:
            self.semantic_evaluator.load_model()
        except Exception as e:
            print(f"Error initializing evaluators: {e}")
            # Set rf_evaluator to None if model loading fails
            self.rf_evaluator = None
            
        # Load questions
        self._load_questions()
    
    def _load_questions(self):
        """Load questions based on category"""
        # Get dataset based on category
        dataset_map = {
            'webdev': 'webdev_interview_qa.csv',
            'python': 'stackoverflow_training_data.csv',
            'java': 'stackoverflow_training_data.csv',
            'csharp': 'stackoverflow_training_data.csv',
            'javascript': 'stackoverflow_training_data.csv',
            'database': 'stackoverflow_training_data.csv',
            'behavioral': 'interview_data_with_scores.csv'  # Using proper behavioral dataset with competency data
        }
        
        csv_file = dataset_map.get(self.category, 'webdev_interview_qa.csv')
        
        # Try multiple possible paths for flexibility (local and deployed)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(base_dir, 'dataset', csv_file),
            os.path.join(base_dir, '..', 'dataset', csv_file),
            os.path.join('dataset', csv_file),
            os.path.join(base_dir, 'real_dataset_score', csv_file),
            os.path.join(base_dir, '..', 'real_dataset_score', csv_file),
            os.path.join('real_dataset_score', csv_file)
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Filter by technology if Stack Overflow data
            if self.category in ['python', 'java', 'csharp', 'javascript', 'database']:
                if 'tags' in df.columns:
                    # Filter by technology tag in stackoverflow data
                    tech_map = {
                        'python': 'python',
                        'java': 'java',
                        'csharp': 'c#',
                        'javascript': 'javascript',
                        'database': 'sql'
                    }
                    tech_tag = tech_map.get(self.category, self.category)
                    df = df[df['tags'].str.contains(tech_tag, case=False, na=False)]
            
            # Load questions
            for _, row in df.iterrows():
                # Handle different column names across datasets
                answer_col = None
                if 'answer' in df.columns:
                    answer_col = 'answer'
                elif 'user_answer' in df.columns:
                    answer_col = 'user_answer'
                
                # Get answer value safely
                answer_value = ''
                if answer_col:
                    ans = row.get(answer_col)
                    if pd.notna(ans):
                        answer_value = str(ans)
                
                # Get human score from either column name
                human_score = 0
                if 'human_score' in df.columns and pd.notna(row.get('human_score')):
                    human_score = float(row.get('human_score'))
                elif 'score' in df.columns and pd.notna(row.get('score')):
                    human_score = float(row.get('score'))
                
                q_data = {
                    'question': row['question'],
                    'answer': answer_value,
                    'competency': row.get('competency', ''),
                    'human_score': human_score,
                    'has_reference': bool(answer_value)
                }
                self.questions.append(q_data)
            
            # Shuffle and select subset
            random.shuffle(self.questions)
            num_questions = min(5, len(self.questions))
            self.questions = self.questions[:num_questions]
    
    def get_next_question(self):
        """Get the next question"""
        if self.current_question_idx < len(self.questions):
            self.current_question = self.questions[self.current_question_idx]
            return self.current_question['question']
        return None
    
    def evaluate_answer(self, answer, experience_level='junior', strictness='normal', hint_used=False, received_hint=None):
        """Evaluate the user's answer using the advanced Semantic Embedding model"""
        if not self.current_question:
            return None
        
        self.current_answer = answer
        
        # Check for copied hint
        if received_hint and isinstance(received_hint, str):
            clean_hint = received_hint.replace("Think about: ", "").replace("Hint from reference: ", "").strip().lower()
            clean_ans = answer.strip().lower()
            
            # If they just pasted the hint or the hint makes up most of their answer
            if clean_hint and (clean_hint in clean_ans or clean_ans in clean_hint) and len(clean_ans) > 10:
                final_score_10 = 0.0
                feedback = "FOUL: Copied directly from hint! 0 Marks. You must write your own original answer."
                self.scores.append(final_score_10)
                self.answers.append({
                    'question': self.current_question['question'],
                    'answer': answer,
                    'score': final_score_10,
                    'feedback': feedback
                })
                return {
                    'score': final_score_10,
                    'feedback': feedback,
                    'reference_answer': self.current_question.get('answer', 'No reference answer available.'),
                    'is_foul': True
                }
        
        # Evaluate using the semantic model
        if self.semantic_evaluator:
            result = self.semantic_evaluator.evaluate_answer(
                self.current_question['question'],
                answer
            )
            final_score = result['predicted_score']
            feedback = f"Semantic Analysis Score: {final_score:.2f}/10.0\n\n{result['feedback']}"
        else:
            # Fallback if model fails to load
            final_score = 5.0
            feedback = "Score: 5.0/10.0\n\nUnable to evaluate answer: Semantic model not loaded."

        # Apply strict caps for extremely short answers
        word_count = len(answer.split())
        score_caps = []
        if word_count < 8:
            score_caps.append(3.0)
            feedback += "\n\nAnswer too short; score capped."
        elif word_count < 15:
            score_caps.append(4.5)

        if score_caps:
            final_score = min(final_score, *score_caps)
        
        # Apply modifiers
        if strictness == 'strict':
            final_score *= 0.90
        elif strictness == 'lenient':
            final_score = min(10.0, final_score * 1.10)
            
        if experience_level == 'senior':
            final_score *= 0.85
            feedback += "\n\nNote: Graded with Senior-level expectations."
        elif experience_level == 'mid':
            final_score *= 0.95
            
        if hint_used:
            final_score *= 0.90
            feedback += "\n\nNote: -10% penalty applied for using a hint."

        # Keep on 10-point scale as requested
        final_score_10 = round(final_score, 1)

        # Store score
        self.scores.append(final_score_10)
        self.answers.append({
            'question': self.current_question['question'],
            'answer': answer,
            'score': final_score_10,
            'feedback': feedback
        })
        
        return {
            'score': final_score_10,
            'feedback': feedback,
            'reference_answer': self.current_question.get('answer', 'No reference answer available.')
        }
    
    def move_to_next(self):
        """Move to the next question"""
        self.current_question_idx += 1
        return self.current_question_idx < len(self.questions)
    
    def get_summary(self):
        """Get session summary"""
        if not self.scores:
            return {
                'total_questions': len(self.questions),
                'attempted': 0,
                'average_score': 0,
                'message': 'No questions attempted yet.'
            }
        
        avg_score = sum(self.scores) / len(self.scores)
        
        return {
            'category': self.category.upper(),
            'total_questions': len(self.questions),
            'attempted': len(self.scores),
            'average_score': f"{avg_score:.2f}",
            'highest_score': f"{max(self.scores):.2f}",
            'lowest_score': f"{min(self.scores):.2f}",
            'performance': 'Excellent' if avg_score >= 8 else 'Good' if avg_score >= 6 else 'Needs Improvement'
        }

# Global session storage
sessions = {}

@app.route('/get_question', methods=['GET'])
def get_question():
    category = request.args.get('category', 'webdev')
    session = InterviewBotSession(category)
    question = session.get_next_question()
    if question:
        # Store the session for evaluation
        session_id = str(random.randint(1000, 9999))
        sessions[session_id] = session
        return jsonify({'question': question, 'session_id': session_id})
    else:
        return jsonify({'error': 'No questions available for this category.'}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    session_id = data.get('session_id')
    experience_level = data.get('experienceLevel', 'junior')
    strictness = data.get('strictness', 'normal')
    hint_used = data.get('hintUsed', False)
    received_hint = data.get('receivedHint', None)

    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID.'}), 400

    session = sessions[session_id]
    
    # The current question is already set in the session when get_question was called
    # We just need to make sure the question from the request matches the one in the session
    if not session.current_question or session.current_question['question'] != question:
        return jsonify({'error': 'Question mismatch.'}), 400

    result = session.evaluate_answer(answer, experience_level, strictness, hint_used, received_hint)

    if result:
        # Move to the next question in the session
        session.move_to_next()
        return jsonify({
            'score': result['score'],
            'feedback': result['feedback'],
            'reference_answer': result.get('reference_answer'),
            'is_foul': result.get('is_foul', False)
        })
    else:
        return jsonify({'error': 'Could not evaluate answer.'}), 500

@app.route('/skip', methods=['POST'])
def skip_question():
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID.'}), 400
        
    session = sessions[session_id]
    
    if not session.current_question:
        return jsonify({'error': 'No active question.'}), 400
        
    # Record a 0 score for skipping
    session.scores.append(0)
    session.answers.append({
        'question': session.current_question['question'],
        'answer': '[SKIPPED]',
        'score': 0,
        'feedback': 'Question skipped by user.'
    })
    
    # Move to the next question
    session.move_to_next()
    
    return jsonify({
        'success': True,
        'message': 'Question skipped.'
    })

@app.route('/get_hint', methods=['POST'])
def get_hint():
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session ID.'}), 400
        
    session = sessions[session_id]
    if not session.current_question:
        return jsonify({'error': 'No active question.'}), 400
        
    ref_answer = str(session.current_question.get('answer', ''))
    
    # Generate a hint by taking the first ~15 words of the reference answer
    words = ref_answer.split()
    if len(words) > 15:
        hint_text = " ".join(words[:15]) + "..."
    else:
        hint_text = ref_answer
        
    # If the reference answer is empty or missing, provide a generic fallback
    if not hint_text.strip():
        hint_text = "Break the problem into smaller concepts and address them one by one."
        
    return jsonify({'hint': f"Think about: {hint_text}"})


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint to wake up the Render server and check status"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    # Hugging Face Spaces expects the app to run on port 7860
    app.run(host='0.0.0.0', port=7860, debug=False)
