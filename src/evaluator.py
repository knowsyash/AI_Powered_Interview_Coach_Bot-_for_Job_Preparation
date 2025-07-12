from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import string

# Make sure NLTK stopwords are downloaded (you did this in Step 2)
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Lowercase, remove punctuation, and stopwords
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    filtered = [w for w in tokens if w not in stop_words]
    return ' '.join(filtered)

def evaluate_answer(user_answer, correct_answer):
    # Clean both answers
    user_clean = clean_text(user_answer)
    correct_clean = clean_text(correct_answer)

    # Vectorize both using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_clean, correct_clean])

    # Compute cosine similarity
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return score  # between 0 and 1
