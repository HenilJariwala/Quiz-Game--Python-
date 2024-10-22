import os
from dotenv import load_dotenv  # type: ignore
from pymongo import MongoClient
from datetime import datetime
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()
def create_connection():
    try:
        # URL-encode username and password
        username = quote_plus(os.getenv('MONGO_USER'))
        password = quote_plus(os.getenv('MONGO_PASSWORD'))
        cluster_url = os.getenv('MONGO_CLUSTER_URL')  # Add cluster URL to .env
        db_name = os.getenv('MONGO_DB')  # Add database name to .env

        # Create a connection to the MongoDB database
        mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/{db_name}?retryWrites=true&w=majority"
        client = MongoClient(mongo_uri)
        print("Connection successful!")
        return client
    except Exception as err:
        print(f"Error: {err}")
        return None

def insert_quiz_result(username, age, score, question_count):
    client = create_connection()
    if client:
        db = client['quiz_game']  # Your database name
        collection = db['users']  # Your collection name

        user_data = {
            "username": username,
            "age": age,
            "score": score,
            "question_count": question_count,
            "quiz_date": datetime.now()  # Set the current date and time
        }

        try:
            collection.insert_one(user_data)
            print("Quiz result inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            client.close()  # Close the connection when done
