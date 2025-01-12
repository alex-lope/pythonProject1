from flask import Flask, render_template, request
from utils.preprocessing import preprocess_input_text, validate_input
from utils.prediction import predict_with_model
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import os

# initialize Flask app
app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret')

# load models and vectorizers
def load_pickle_model(file_path, model_name):

    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"{model_name} file not found.")
        return None

def load_keras_model(file_path, model_name):

    try:
        return load_model(file_path)
    except Exception as e:
        print(f"Error loading {model_name}: {e}")
        return None


def vectorize_for_inference(text, vectorizer, vectorizer_type):
    processed_text = preprocess_input_text(text)

    if vectorizer_type == 'tfidf':
        return vectorizer.transform([processed_text])
    elif vectorizer_type == 'sequence':
        vectorized_text = vectorizer([processed_text]).numpy()
        return pad_sequences(vectorized_text, maxlen=300, padding='post')
    else:
        raise ValueError("Invalid vectorizer_type. Use 'tfidf' or 'sequence'.")


# load SVM model
try:
    with open("models/svm_model.pkl", "rb") as svm_file:
        svm_model = pickle.load(svm_file)
except FileNotFoundError:
    print("SVM model file not found.")
    svm_model = None

# load TF-IDF vectorizer
try:
    with open("models/tfidf_vectorizer.pkl", "rb") as tfidf_file:
        tfidf_vectorizer = pickle.load(tfidf_file)
except FileNotFoundError:
    print("TF-IDF vectorizer file not found.")
    tfidf_vectorizer = None

# load RNN model
try:
    rnn_model = load_model("models/rnn_model.keras")
except Exception as e:
    print(f"Error loading RNN model: {e}")
    rnn_model = None

# load CNN model
try:
    cnn_model = load_model("models/cnn_model.keras")
except Exception as e:
    print(f"Error loading CNN model: {e}")
    cnn_model = None

# load TextVectorization layer
try:
    loaded_vectorizer_model = load_model("models/text_vectorizer.keras")
    text_vectorizer = loaded_vectorizer_model.layers[0]
except Exception as e:
    print(f"Error loading TextVectorization layer: {e}")
    text_vectorizer = None

# initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get user input
        student_name = request.form.get('student_name', 'Unknown')
        student_id = request.form.get('student_id', 'Unknown')
        raw_text = request.form.get('text_input', '')

        # validate input
        is_valid, error_message = validate_input(raw_text)
        if not is_valid:
            return render_template('index.html', error=error_message)

        # preprocess the input text
        processed_text = preprocess_input_text(raw_text)

        # process and predict
        svm_pred_class, svm_pred_prob = predict_with_model(raw_text, svm_model, tfidf_vectorizer, 'tfidf')
        rnn_pred_class, rnn_pred_prob = predict_with_model(raw_text, rnn_model, text_vectorizer, 'sequence')
        cnn_pred_class, cnn_pred_prob = predict_with_model(raw_text, cnn_model, text_vectorizer, 'sequence')

        # ensemble prediction logic
        predictions = [svm_pred_class, rnn_pred_class, cnn_pred_class]
        ensemble_pred_class = 'unsuccessful' if all(pred == 'unsuccessful' for pred in predictions) else 'successful'

        #  calculate word count, sentiment, and readability
        word_count = len(processed_text.split())
        sentiment_score = analyzer.polarity_scores(raw_text)['compound']
        readability_score = textstat.flesch_kincaid_grade(raw_text)

        # render results
        return render_template(
            'index.html',
            student_name=student_name,
            student_id=student_id,
            raw_text=raw_text,
            word_count=len(raw_text.split()),
            sentiment_score=sentiment_score,
            readability_score=readability_score,
            svm_class=svm_pred_class, svm_prob=svm_pred_prob,
            rnn_class=rnn_pred_class, rnn_prob=rnn_pred_prob,
            cnn_class=cnn_pred_class, cnn_prob=cnn_pred_prob,
            ensemble_class=ensemble_pred_class
        )
    return render_template('index.html')


# help route
@app.route('/help', methods=['GET'])
def help_page():
    return render_template('help.html')


@app.route('/download_report', methods=['POST'])
def download_report():
    # Collect data from the form
    student_name = request.form['student_name']
    student_id = request.form['student_id']
    raw_text = request.form['raw_text']
    word_count = request.form['word_count']
    sentiment_score = request.form['sentiment_score']
    readability_score = request.form['readability_score']
    svm_class = request.form['svm_class']
    svm_prob = request.form['svm_prob']
    rnn_class = request.form['rnn_class']
    rnn_prob = request.form['rnn_prob']
    cnn_class = request.form['cnn_class']
    cnn_prob = request.form['cnn_prob']
    ensemble_class = request.form['ensemble_class']

    # sanitize student name for file name
    sanitized_name = re.sub(r'[^\w\s-]', '', student_name)
    sanitized_name = sanitized_name.strip().replace(' ', '_')

    # create the report
    report = f"""
    Graduation Success Model Report
    ===============================
    Student Name: {student_name}
    Student ID: {student_id}

    Results
    -------
    Input Text: {raw_text}
    Word Count: {word_count}
    Sentiment Score: {sentiment_score}
    Readability Score: {readability_score}
    SVM Prediction: {svm_class} (Probability: {float(svm_prob):.2f})
    RNN Prediction: {rnn_class} (Probability: {float(rnn_prob):.2f})
    CNN Prediction: {cnn_class} (Probability: {float(cnn_prob):.2f})
    Ensemble Prediction: {ensemble_class}
    """

    # create a file path including student name and ID
    file_path = f"reports/{sanitized_name}_report.txt"

    # save to the file
    try:
        with open(file_path, 'w') as file:
            file.write(report)
        return f"Report saved successfully! You can find it at {file_path}."
    except Exception as e:
        return f"Error saving report: {e}"

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'its-been-years-2017')

# run the app
if __name__ == '__main__':
    app.run(debug=False)
