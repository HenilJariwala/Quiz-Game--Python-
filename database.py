import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_connection():
    try:
        # Create a connection to the MySQL database
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
        print("Connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def insert_quiz_result(username, age, score,question_count):
    connection = create_connection()
    cursor = connection.cursor()

    sql_query = "INSERT INTO users (username, age, score, question_count) VALUES (%s, %s, %s,%s)"
    data = (username, age, score, question_count)

    try:
        cursor.execute(sql_query, data)
        connection.commit()
        print("Quiz result inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()
        
# Example usage
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        # Do something with the connection
        conn.close()  # Don't forget to close the connection when done!
