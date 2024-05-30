import os
import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='localFile',
            user='root',  # Update with your MySQL username
            password='Matin@735'  # Update with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

def insert_file_data(cursor, file_path, file_name, file_type, file_content):
    try:
        cursor.execute("""
            INSERT INTO files (file_path, file_name, file_type, file_content)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE file_content = VALUES(file_content)
        """, (file_path, file_name, file_type, file_content))
    except Error as e:
        print(f"Error: {e}")

def load_files_to_db(root_dir):
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            insert_file_data(cursor, dir_path, dirname, 'directory', '')

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                file_content = file.read()
            insert_file_data(cursor, file_path, filename, 'file', file_content)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    # Set your directory path here
    root_directory = r"C:\Users\Navid Matin\Desktop\Project\project"
    load_files_to_db(root_directory)
