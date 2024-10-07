from flask import Flask, request, jsonify, render_template, redirect, url_for
import random

app = Flask(__name__)

# Stop words list
stop_words = {'the', 'a', 'and', 'in', 'of', 'when', 'is', 'by', 'to', 'for'}

# Function to filter out stop words from a list of words
def filter_stop_words(words):
    return [word for word in words if word not in stop_words]

# Updated Question Bank
question_bank = {
    1: {"question": "What is the difference between dry bulb and wet bulb temperature in data center cooling?",
        "answer": "Dry bulb temperature measures the ambient air temperature, while wet bulb temperature accounts for humidity."},
    # Add more questions here...
}

@app.route('/')
def home():
    question_id = random.choice(list(question_bank.keys()))
    question = question_bank[question_id]["question"]
    return render_template('index.html', question=question, question_id=question_id)

@app.route('/submit', methods=['POST'])
def submit():
    question_id = int(request.form['question_id'])
    user_answer = request.form['answer'].lower().split()
    correct_answer = question_bank[question_id]["answer"].lower().split()
    
    # Scoring logic and comparison goes here...
    return render_template('result.html', user_answer=user_answer, correct_answer=correct_answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
