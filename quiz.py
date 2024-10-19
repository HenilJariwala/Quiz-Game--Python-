from flask import Flask, render_template, request, session, redirect, url_for
import random, html, requests
from colorama import Fore, Style, init


app = Flask(__name__)
app.secret_key = 'quick_secret_quiz'

#extracting all the categories from the API
def get_categories():
    category_url="https://opentdb.com/api_category.php"
    response=requests.get(category_url)
    if response.status_code ==  200:
        data = response.json()
        return data.get('trivia_categories', [])
    else:
        print("Failed to fetch categories")
        return []
  

 
def fetch_question(category_id,difficulty,number):
    
    base_url = "https://opentdb.com/api.php?"
    question_url= f"{base_url}amount={number}&category={category_id}&difficulty={difficulty}"
    
    # print(question_url)
    
    response = requests.get(question_url)
    if response.status_code ==200:
        data =response.json()
        print(data)
        return data
    else:
        print("No questions found")
        return []
      

@app.route('/')  
def quiz():
    categories = get_categories()
    print(categories)
    return render_template('quiz.html',categories=categories)
    
@app.route('/start_quiz',methods=['POST'])
def start_quiz():
    session.clear()
    category_id = request.form.get('category')
    difficulty= request.form.get("difficulty").lower()
    number = 10
    
    questions= fetch_question(category_id,difficulty,number)
   
    
    if 'results' in questions and questions['results']:
        session['question'] = questions['results']
        session['current_question']=0 #initialize current question index
        session['score']=0
        
        return redirect(url_for('show_question'))
    else:
        return "No questions found for the selected category and difficulty."


@app.route('/show_question',methods=['GET', 'POST'])
def show_question():
    questions = session.get('question', [])
    current_index = session.get('question_index', 0)
    
    print(f"Session: {session}")
    print(f"Questions in session: {questions}")  # Check if questions are stored in session
    print(f"Current Index: {current_index}")  # Check current question index
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct_answer')

        # Check if the answer is correct
        if user_answer == correct_answer:
            # Increment the score if the answer is correct
            score = session.get('score', 0) + 1
            session['score'] = score  # Store the updated score in the session
            print("Correct answer!")
        else:
            print("Incorrect answer!")

        # Increment the index to show the next question
        session['question_index'] = current_index + 1
        return redirect(url_for('show_question'))
    
    # Check if there are more questions
    if current_index < len(questions):
        question = questions[current_index]
        return render_template('questions.html', question=question, question_num=current_index + 1)
    else:
        return redirect(url_for('quiz_result'))
    
# def next_question():
#     questions = session.get('questions', [])
#     current_index = session.get('question_index', 0)
    
#     # Process the user's answer
#     user_answer = request.form.get('answer')
#     correct_answer = request.form.get('correct_answer')
    
#     if user_answer == correct_answer:
#         session['score'] += 1  # Increment score if answer is correct
    
#     # Move to the next question
#     current_index += 1
#     session['question_index'] = current_index
    
#     # Check if there are more questions
#     if current_index < len(questions):
#         question = questions[current_index]
#         return render_template('question.html', question=question, question_num=current_index + 1)
#     else:
#         return redirect(url_for('quiz_result'))

@app.route('/quiz_result')
def quiz_result():
    score = session.get('score', 0)
    questions = session.get('question', [])
    
    return f"Your score is {score} out of {len(questions)}"

    
if __name__ == "__main__":
    app.run(debug=True) 



