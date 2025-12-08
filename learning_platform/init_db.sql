DROP TABLE IF EXISTS test_attempts CASCADE;
DROP TABLE IF EXISTS answers CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS lessons CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================
-- USERS
-- ============================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================
-- COURSES
-- ============================

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

-- ============================
-- LESSONS
-- ============================

CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    order_index INT DEFAULT 0
);

-- ============================
-- QUESTIONS
-- ============================

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    lesson_id INT REFERENCES lessons(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL
);

-- ============================
-- ANSWERS
-- ============================

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL
);

-- ============================
-- TEST ATTEMPTS
-- ============================

CREATE TABLE test_attempts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    lesson_id INT REFERENCES lessons(id) ON DELETE CASCADE,
    max_score INT NOT NULL,
    current_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================
-- DEMO COURSE + LESSON + QUESTIONS
-- ============================

INSERT INTO courses (title) VALUES ('English Basics');

INSERT INTO lessons (course_id, title, order_index)
VALUES (1, 'Lesson 1', 1);

INSERT INTO questions (lesson_id, question_text) VALUES
(1, 'The word "Cat" means:'),
(1, 'The word "Dog" means:');

INSERT INTO answers (question_id, answer_text, is_correct) VALUES
(1, 'Cat', TRUE),
(1, 'Dog', FALSE),
(1, 'Bird', FALSE),

(2, 'Dog', TRUE),
(2, 'Cat', FALSE),
(2, 'Mouse', FALSE);
