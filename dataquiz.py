from flask import Flask, request, render_template, redirect, url_for
import random

app = Flask(__name__)

# Stop words list
stop_words = {'the', 'a', 'and', 'in', 'of', 'when', 'is', 'by', 'to', 'for'}

# Function to filter out stop words from a list of words
def filter_stop_words(words):
    return [word for word in words if word not in stop_words]

# Updated Question Bank
question_bank = {
    1: {
        "question": "What is the difference between dry bulb and wet bulb temperature in data center cooling?",
        "answer": "Dry bulb temperature measures the ambient air temperature, while wet bulb temperature accounts for humidity and is the lowest temperature air can reach through evaporation."
    },
    # Add other questions...
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
    correct_answer = question_bank[question_id]["answer"].split()

    # Filter out stop words from the user's answer
    filtered_user_answer = filter_stop_words(user_answer)

    score = 0
    result_display = []

    # Check each word in the correct answer and highlight if it was in the user answer
    for word in correct_answer:
        if word.lower() in filtered_user_answer:
            result_display.append(f'<span style="color:green;">{word}</span>')
            score += 1
        else:
            result_display.append(word)

    total_keywords = len(filter_stop_words(correct_answer))

    # Return the result with colored words
    result_html = " ".join(result_display)
    
    return render_template('result.html', score=score, total=total_keywords, correct_answer=result_html)

@app.route('/ask_another')
def ask_another():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
