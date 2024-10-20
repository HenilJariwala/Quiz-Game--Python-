CREATE DATABASE quiz_game;

USE quiz_game;

CREATE TABLE users(
id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(200),
age INT,
score INT);

ALTER TABLE users
ADD question_count INT,
ADD quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
