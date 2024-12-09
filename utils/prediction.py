from tensorflow.keras.preprocessing.sequence import pad_sequences
from utils.preprocessing import preprocess_input_text, validate_input
import numpy as np

def predict_with_model(text, model, vectorizer, vectorizer_type):

    # preprocess the input text
    processed_text = preprocess_input_text(text)

    # vectorize the text
    if vectorizer_type == 'tfidf':
        vectorized_text = vectorizer.transform([processed_text])
    elif vectorizer_type == 'sequence':
        vectorized_text = vectorizer([processed_text]).numpy()
        vectorized_text = pad_sequences(vectorized_text, maxlen=300, padding='post')
    else:
        raise ValueError("Unknown vectorizer type. Use 'tfidf' or 'sequence'.")

    # get prediction probabilities
    if hasattr(model, "predict_proba"):  # SVM
        prob = model.predict_proba(vectorized_text)[0][1]
    else:  # RNN and CNN
        prob = model.predict(vectorized_text).ravel()[0]

    # determine the predicted class
    predicted_class = 'successful' if prob > 0.5 else 'unsuccessful'

    return predicted_class, prob
