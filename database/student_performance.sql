CREATE DATABASE IF NOT EXISTS student_performance;
USE student_performance;
CREATE TABLE students(
 student_id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 department VARCHAR(100),
 semester INT
);
CREATE TABLE subjects(
 subject_id INT AUTO_INCREMENT PRIMARY KEY,
 subject_name VARCHAR(100) NOT NULL,
 credits INT DEFAULT 3
);
CREATE TABLE attendance(
 attendance_id INT AUTO_INCREMENT PRIMARY KEY,
 student_id INT, subject_id INT, percentage DECIMAL(5,2),
 FOREIGN KEY(student_id) REFERENCES students(student_id),
 FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
);
CREATE TABLE marks(
 mark_id INT AUTO_INCREMENT PRIMARY KEY,
 student_id INT, subject_id INT,
 internal DECIMAL(5,2), assignment DECIMAL(5,2), exam DECIMAL(5,2),
 FOREIGN KEY(student_id) REFERENCES students(student_id),
 FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
);
CREATE TABLE performance(
 performance_id INT AUTO_INCREMENT PRIMARY KEY,
 student_id INT, gpa DECIMAL(4,2), grade VARCHAR(10),
 FOREIGN KEY(student_id) REFERENCES students(student_id)
);
CREATE TABLE predictions(
 prediction_id INT AUTO_INCREMENT PRIMARY KEY,
 student_id INT, predicted_class VARCHAR(20), probability DECIMAL(6,4),
 predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(student_id) REFERENCES students(student_id)
);
CREATE TABLE IF NOT EXISTS users(
 user_id INT AUTO_INCREMENT PRIMARY KEY,
 username VARCHAR(50) NOT NULL UNIQUE,
 password VARCHAR(255) NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO students(name,department,semester) VALUES
('Anu','CSE',2),('Rahul','CSE',3);
INSERT IGNORE INTO users(username,password) VALUES('admin','admin123');
