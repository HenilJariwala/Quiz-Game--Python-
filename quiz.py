from flask import Flask, render_template, request, session, redirect, url_for
import requests
from database import insert_quiz_result 

app = Flask(__name__)
app.secret_key = 'quick_secret_quiz'

# Extracting all the categories from the API
def get_categories():
    category_url = "https://opentdb.com/api_category.php"
    response = requests.get(category_url)
    if response.status_code == 200:
        data = response.json()
        return data.get('trivia_categories', [])
    else:
        print("Failed to fetch categories")
        return []

def fetch_question(category_id, difficulty, number):
    base_url = "https://opentdb.com/api.php?"
    question_url = f"{base_url}amount={number}&category={category_id}&difficulty={difficulty}"
    
    response = requests.get(question_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("No questions found")
        return []

@app.route('/')
def quiz():
    categories = get_categories()
    return render_template('quiz.html', categories=categories)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    session.clear()
    category_id = request.form.get('category')
    difficulty = request.form.get("difficulty").lower()
    username = request.form.get('username')
    age = request.form.get('age')
    number = 10
    
    questions = fetch_question(category_id, difficulty, number)

    if 'results' in questions and questions['results']:
        session['question'] = questions['results']
        session['current_question'] = 0  # Initialize current question index
        session['score'] = 0
        session['username'] = username
        session['age'] = age
        
        return redirect(url_for('show_question'))
    else:
        return "No questions found for the selected category and difficulty."

@app.route('/show_question', methods=['GET', 'POST'])
def show_question():
    questions = session.get('question', [])
    current_index = session.get('current_question', 0)

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct_answer')

        # Check if the answer is correct
        if user_answer == correct_answer:
            score = session.get('score', 0) + 1
            session['score'] = score  # Store the updated score in the session
            print("Correct answer!")
        else:
            print("Incorrect answer!")

        # Increment the index to show the next question
        session['current_question'] = current_index + 1
        return redirect(url_for('show_question'))
    
    # Check if there are more questions
    if current_index < len(questions):
        question = questions[current_index]
        return render_template('questions.html', question=question, question_num=current_index + 1)
    else:
        return redirect(url_for('quiz_result'))

@app.route('/quiz_result')
def quiz_result():
    score = session.get('score', 0)
    questions = session.get('question', [])
    username = session.get('username')
    age = session.get('age')
    questions_count = len(questions)
    
    insert_quiz_result(username, age, score, questions_count)
    print(username, age, score, questions_count)
    
    if score <= 5:
        text = "Better Luck Next Time"
    else:
        text = "Congratulations"
    return render_template('quiz_result.html', score=score, Text=text, total_questions=len(questions), username=username, age=age)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
