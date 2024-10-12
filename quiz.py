from flask import Flask, render_template, request
import random, html, requests
from colorama import Fore, Style, init

app = Flask(__name__)

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
    category_id = request.form.get('category')
    difficulty= request.form.get("difficulty").lower()
    number = 5
    
    questions= fetch_question(category_id,difficulty,number)
    if 'results' in questions and questions['results']:
        return render_template('questions.html', questions=questions['results'])
    else:
        return "No questions found for the selected category and difficulty."

@app.route('/submit', methods=['POST'])
def submit_quiz():
    score=0
    questions = request.form.getlist('question')
    correct_answer = request.form.getlist('correct_answer')

    for i in range(len(questions)):
        user_answer = request.form.getlist(f'answer_{i}')
        if user_answer == correct_answer[i]:
            score+=1
            
    return f"Your score is {score} out of {len(questions)}"
    
if __name__ == "__main__":
    app.run(debug=True)



