import os
import mysql.connector
from mysql.connector import Error
from bs4 import BeautifulSoup


#THE LAST CODE FOR LOADING THE CONTENT OF THE LOCAL FILE INTO THE DATABASE
#HOW EVER IT WAS A TOUGH TIME BUT YOU MADE IT AND THAT IS A GREAT POINT SO DONT GET NERVOUS AND JUST DO SOMETHING GREAT AND THAT IS IT FOR NOW 
#WISH YOU BEST OF LUCK AND FULL OF JOY AND THAT IS 



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

def get_file_type(file_name):
    extension = os.path.splitext(file_name)[1][1:].lower()  # Get the file extension without the dot
    if extension in ['html', 'txt', 'py', 'jpg', 'png']:
        return extension
    return 'file'  # General file type for unknown extensions

def insert_file(file_path, file_name, file_type, file_size, file_content):
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()
    query = "INSERT INTO files (file_path, file_name, file_type, file_size, file_content) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (file_path, file_name, file_type, file_size, file_content))
        connection.commit()
    except Error as e:
        print(f"Error inserting file into database: {e}")
    finally:
        cursor.close()
        connection.close()


"""
def load_files_from_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            dir_path = os.path.join(root, name)
            insert_file(dir_path, name, 'directory', 0, '')  # Pass empty string for file content
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_type = get_file_type(file_name)
            file_size = os.path.getsize(file_path)
            file_content = ""
            if file_type in ['html', 'txt', 'py']:  # Read content only for these file types
                try:
                    with open(file_path, 'r', errors='ignore') as file:
                        file_content = file.read()
                        print(f"Read content from {file_path}: {file_content[:100]}...")  # Print first 100 characters of content
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
            insert_file(file_path, file_name, file_type, file_size, file_content)


def load_files_from_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            dir_path = os.path.join(root, name)
            insert_file(dir_path, name, 'directory', 0, '')  # Pass empty string for file content
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_type = get_file_type(file_name)
            file_size = os.path.getsize(file_path)
            file_content = ""
            if file_type in ['html', 'txt', 'py']:  # Read content only for these file types
                try:
                    with open(file_path, 'rb') as file:
                        file_content = file.read().decode('utf-8')

                        print(f"Read content from {file_path}: {file_content[:100]}...")  # Print first 100 characters of content
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
            insert_file(file_path, file_name, file_type, file_size, file_content)
"""

def load_files_from_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            dir_path = os.path.join(root, name)
            insert_file(dir_path, name, 'directory', 0, '')  # Pass empty string for file content
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_type = get_file_type(file_name)
            file_size = os.path.getsize(file_path)
            file_content = ""
            if file_type in ['html', 'txt', 'py']:  # Read content only for these file types
                try:
                    with open(file_path, 'rb') as file:
                        soup = BeautifulSoup(file, 'html.parser')
                        file_content = soup.get_text()
                        print(f"Read content from {file_path}: {file_content[:100]}...")  # Print first 100 characters of content
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
            insert_file(file_path, file_name, file_type, file_size, file_content)


# Set your directory path
directory = "C:\\Users\\Navid Matin\\Desktop\\Project"
load_files_from_directory(directory)
