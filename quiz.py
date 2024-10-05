import random 
from colorama import Fore, Style, init
import requests

def get_categories():
    category_url="https://opentdb.com/api_category.php"
    response=requests.get(category_url)
    if response.status_code ==  200:
        data = response.json()
        return data.get('trivia_categories', [])
    else:
        print("Failed to fetch categories")
        return []


def display_categories():
    categories=get_categories()
    for i,category in enumerate(categories):
        print(f"{i+1}.{category['name']}")


def choose_categories(categories):
   
    try:
        choice=int(input("\nEnter the category number: ")) -1
        if 0< choice< len(categories):
            return categories[choice]['id'], categories[choice]['name']
        else:
            print("Invalid choice")
            return None
    except ValueError:
        print("Enter a Valid number!")
        return None
   
def fetch_question(category,difficulty):
    
    base_url = "https://opentdb.com/api_count.php"
    params = {
        "amount":1,
        "category":category,
        "difficulty":difficulty.lower(),
        "type": "multiple"
    }
    
    response = requests.get(base_url,params=params)
    if response.status_code == 200:
        data=response.json()
        return data.get('results',[])
    else:
        print("Failed to fetch questions")
        return []
    
def run_quiz(category,difficulty):
    score=1
    
    while 1 <= score <= 50:  # Keep running the quiz while the score is between 1 and 50
        question = fetch_question(category, difficulty)
        if not question:
            print("No Questions availaible")
        
        print(f"\nQuestion: {Fore.YELLOW}{question[0    ]['question']}{Style.RESET_ALL} ")
    
        options = [question['incorrect_answers']] + [question['correct_answer']]
        random.shuffle(options)
        
        
        for i, option in enumerate(options,start=1):
            print(f"{i}.{option}")
            
        try:
            user_answer=int(input("\nChoose the correct option (1-4): ")) - 1
            if 0 <= user_answer < len(options):
                if options[user_answer] == question['correct_answer']:
                    print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                    score += 10  # Increase score for correct answer
                else:
                    print(f"{Fore.RED}Wrong!{Style.RESET_ALL} The correct answer was: {question['correct_answer']}")
                    score -= 5  # Decrease score for incorrect answer
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL} You lose 5 points.")
                score -= 5
        except ValueError:
            print(f"{Fore.RED}Invalid input!{Style.RESET_ALL} You lose 5 points.")
            score -= 5
        
        # Show the current score
        print(f"Your current score: {score}")

        # Stop the quiz if the score goes outside the range
        if score < 1 or score > 50:
            break
    
    
        
def main():
    
    categories = get_categories()
    display_categories()
    category_id, category_name = choose_categories(categories)
   
    print("Now select the difficulty level") 
    difficulty = ["Easy", "Medium", "Hard"] 
    for i, level in enumerate(difficulty, start=1):
        print(f"{i}. {difficulty[i-1]}")
    
    try:
        level_choice = int(input("Enter the number for difficulty level: ")) - 1
    
        if level_choice < 0 or level_choice >= len(difficulty):
            print("Invalid difficulty selection. Exiting quiz.")  # Input validation
            return
    except ValueError:
        print("Invalid input for difficulty level. Exiting quiz.")  # Input validation for non-integer values
        return

    print(f"Selected category : {difficulty[level_choice]}")
    
    url = "https://opentdb.com/api_count.php?category=" + str(category_id)
    response = requests.get(url)
    

    if response.status_code == 200:
        data = response.json
        if 'overall' in data:
        num = data['overall']  # For example, if 'overall' is a key in the response
        else:
        num = "Key not found in response"    
        print(num)
    else:
        print(f"Failed to get data. Status code: {response.status_code}")
    
    run_quiz(category=category_id, difficulty=difficulty[level_choice]) 

if __name__ == "__main__":
    main()



