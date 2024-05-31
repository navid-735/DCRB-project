


CREATE DATABASE IF NOT EXISTS localFile;

USE localFile;

CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(255) UNIQUE,
    file_name VARCHAR(255),
    file_type ENUM('directory', 'file', 'html', 'txt', 'py', 'jpg', 'png'),
    file_size INT,
    file_content LONGTEXT 
);
