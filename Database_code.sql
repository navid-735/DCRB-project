CREATE DATABASE IF NOT EXISTS localFile;

USE localFile;

CREATE TABLE IF NOT EXISTS files (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_path VARCHAR(255) NOT NULL UNIQUE,
    file_name VARCHAR(255) NOT NULL,
    file_type ENUM('directory', 'file') NOT NULL,
    file_content TEXT
);
