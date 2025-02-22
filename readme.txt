Graduation Success Classification Model
Overview
The Graduation Success Classification Model is a Flask-based web application that classifies student writing samples as "successful" or "unsuccessful." This application leverages machine learning models (SVM, RNN, and CNN) with an ensemble approach to enhance prediction accuracy. Additional features include text preprocessing, sentiment analysis, readability scoring, and a report generation function.

Features
	•	Input Processing: Users input a writing sample (up to 500 words).
	•	Preprocessing: The system removes HTML tags, lowercases text, removes punctuation, and lemmatizes words.
	•	Model Predictions: Predictions from SVM, RNN, CNN, and an ensemble classifier.
	•	Readability & Sentiment Analysis: Calculates readability scores and sentiment polarity.
	•	Interactive Web Interface: Built with Flask, featuring user-friendly navigation.
	•	Help Feature: Provides users with guidance on how to use the system.
	•	Report Generation: Allows users to save predictions and scores as a text file.

Installation
Prerequisites
	•	Python 3.9+
	•	Flask
	•	TensorFlow
	•	Scikit-learn
	•	Matplotlib
	•	Pandas
	•	Textstat
	•	VADER Sentiment Analysis
	•	NLTK
Setup Instructions
	1	Clone the repository: git clone https://github.com/your-repository/graduation-success-model.git
	2	cd graduation-success-model
	3	Create a virtual environment (recommended): python -m venv venv
	4	source venv/bin/activate  # On Windows use: venv\Scripts\activate
	5	Install dependencies: pip install -r requirements.txt
	6	Download necessary NLP resources: import nltk
	7	nltk.download('stopwords')
	8	nltk.download('wordnet')
	9	Run the application: python app.py
	10	Access the application in a browser: http://127.0.0.1:5000/

Usage
	1	Enter Student Information
	◦	Type or paste the student name and ID.
	2	Input Text
	◦	Copy and paste a writing sample (maximum 500 words).
	3	Click 'Classify'
	◦	The application will process the text and display:
	▪	Word count
	▪	Sentiment score
	▪	Readability score
	▪	Predictions from SVM, RNN, CNN, and ensemble method
	4	Generate a Report
	◦	Click 'Print Report' to save the results as a text file.
	5	View Help
	◦	Click 'Help' for instructions on how to use the system.

File Structure
Graduation-Success-Model/
│-- app.py  # Flask application
│-- requirements.txt  # Dependencies
│-- models/  # Contains trained ML models
│-- utils/
│   │-- preprocessing.py  # Text preprocessing utilities
│   │-- prediction.py  # Model inference functions
│-- templates/
│   │-- index.html  # Main user interface
│-- static/
│   │-- styles.css  # Stylesheet for UI
│-- logs/  # Application logs
│-- reports/  # Directory for saving reports

Security Measures
	•	Input Validation: Ensures text is sanitized, limits length, and prevents script injection.
	•	Restricted File Access: Prevents unauthorized access to model files.
	•	Logging: Logs system activity and potential issues.

Troubleshooting
Common Issues & Fixes
Issue
Possible Cause
Solution
Flask app not running
Missing dependencies
Run pip install -r requirements.txt
Results not displaying
Empty input field
Ensure all fields are filled before clicking 'Classify'
Report not saving
Insufficient permissions
Ensure the /reports/ directory has write access


License
None required.

Contact
For issues or questions, please reach out via GitHub Issues or Alex_Lope.
