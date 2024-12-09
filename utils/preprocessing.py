import re

def preprocess_input_text(text):
    text = text.replace('\n', ' ')  # replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)  # strip extra spaces
    text = text.strip()  # strip leading/trailing spaces
    return text

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
