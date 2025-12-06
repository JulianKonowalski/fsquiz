CREATE DATABASE tmp;
\c tmp;

DROP DATABASE IF EXISTS proton;
CREATE DATABASE proton;
\c proton;

DROP DATABASE TMP;

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32)
);

CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    event_id INT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    year INT NOT NULL
);

CREATE TABLE question_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(16) UNIQUE NOT NULL
);

INSERT INTO question_types (name) VALUES
    ('single-choice'),
    ('multi-choice'),
    ('input'),
    ('input-range');

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INT NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    type_id INT NOT NULL REFERENCES question_types(id) ON DELETE RESTRICT,
    text TEXT UNIQUE NOT NULL
);

CREATE TABLE question_answers (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL
);

CREATE TABLE question_images (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    path VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE solutions (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    text TEXT NOT NULL
);

CREATE TABLE solution_images (
    id SERIAL PRIMARY KEY,
    solution_id INT NOT NULL REFERENCES solutions(id) ON DELETE CASCADE,
    path VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    username VARCHAR(16) UNIQUE NOT NULL
);

CREATE TABLE user_answers (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id INT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    answer_id INT NOT NULL REFERENCES question_answers(id) ON DELETE CASCADE
);