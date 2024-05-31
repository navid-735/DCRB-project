import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
import os

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='localFile',
            user='root',  
            password=''  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
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
        SELECT file_path, file_name, file_type,
            (CASE 
                WHEN file_name LIKE %s THEN 'file_name'
                WHEN file_content LIKE %s THEN 'file_content'
                WHEN file_type = 'directory' THEN 'directory'
            END) AS match_type,
            (CASE 
                WHEN file_content LIKE %s THEN (LENGTH(file_content) - LENGTH(REPLACE(file_content, %s, ''))) / LENGTH(%s)
                ELSE 0
            END) AS occurrences
        FROM files
        WHERE file_name LIKE %s OR file_content LIKE %s
    """
    
    try:
        cursor.execute(query, (f"%{search_string}%", f"%{search_string}%", f"%{search_string}%", search_string, search_string, f"%{search_string}%", f"%{search_string}%"))
        results = cursor.fetchall()
        return results

    except Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def main():
    print("File Search Engine")
    while True:
        search_string = input("Enter search string (or type 'exit' to quit): ")
        if not search_string.strip():
            print("Search string cannot be empty. Please try again.")
            continue
        if search_string.lower() == 'exit':
            break
        results = search_files(search_string)
        if not results:
            print(f"No results found for: {search_string}")
        else:
            headers = ["File Path", "File Name", "File Type", "Match Type", "Occurrences"]
            formatted_results = []
            for row in results:
                file_name = os.path.splitext(row[1])[0]  # Exclude file extension from file name
                formatted_results.append([
                    row[0], file_name, row[2], row[3], int(row[4]) if row[3] == 'file_content' else ''
                ])
            print(tabulate(formatted_results, headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
