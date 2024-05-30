from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='localFile',
            user='root',  # Replace with your MySQL username
            password='Matin@735'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

def search_files(search_string):
    connection = connect_to_db()
    if not connection:
        return []

    cursor = connection.cursor()
    query = """
        SELECT file_path, file_name, file_type, file_content
        FROM files
        WHERE file_name LIKE %s OR file_content LIKE %s
    """
    try:
        cursor.execute(query, (f"%{search_string}%", f"%{search_string}%"))
        results = cursor.fetchall()
        return results

    except Error as e:
        print(f"Error executing query: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        if search_query:
            search_results = search_files(search_query)
            return render_template('results.html', search_results=search_results, search_query=search_query)
        else:
            return render_template('index.html', error_message="Please enter a search string")
    else:
        return render_template('index.html', error_message=None)

if __name__ == "__main__":
    app.run(debug=True)
