CREATE DATABASE IF NOT EXISTS fucareer;
USE fucareer;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    reset_otp VARCHAR(10),
    reset_otp_created_at DATETIME,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS cv_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    candidate_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    cover_letter TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS internal_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    visibility VARCHAR(50) NOT NULL DEFAULT 'user'
);

-- Create dedicated MySQL user for the app with FILE privileges (for INTO OUTFILE)
CREATE USER IF NOT EXISTS 'ctf'@'localhost' IDENTIFIED BY 'ctfpassword';
GRANT ALL PRIVILEGES ON fucareer.* TO 'ctf'@'localhost';
GRANT FILE ON *.* TO 'ctf'@'localhost';
FLUSH PRIVILEGES;
