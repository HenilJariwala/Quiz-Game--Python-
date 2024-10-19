CREATE DATABASE quiz_game;

USE quiz_game;

CREATE TABLE users(
id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(200),
age int,
score int);