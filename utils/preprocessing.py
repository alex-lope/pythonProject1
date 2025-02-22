import re
import html
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_input_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    text = html.unescape(text)
    text = re.sub(r'<.*?>', "", text)  # remove HTML tags
    text = text.strip().lower()  # strip and lowercase
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    preprocessed_text = ' '.join(
        [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])  # lemmatizer
    return preprocessed_text

def validate_input(text):
    if not text.strip():  # check if text is empty
        return False, "Input cannot be empty. Please provide some text."

    sanitized_text = re.sub(r'<.*?>', '', text)
    word_count = len(sanitized_text.split())
    if word_count > 500:
        return False, f"Input exceeds the 500-word limit. Your input contains {word_count} words."

    if re.search(r'<script.*?>.*?</script>', text, re.IGNORECASE):
        return False, "Input contains potentially malicious content (e.g., <script> tags)."

    return True, None

