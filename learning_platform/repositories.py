from typing import List, Optional
from db import execute_query
from models import User, Course, Lesson, Question, Answer


# Пользователи

def get_user_by_username(username: str) -> Optional[User]:
    row = execute_query(
        "SELECT * FROM users WHERE username = %s",
        (username,), fetchone=True
    )
    if row:
        return User(**row)
    return None


def create_user(username: str, password_hash: str, full_name: str, role: str = "student") -> User:
    execute_query(
        """
        INSERT INTO users (username, password_hash, full_name, role)
        VALUES (%s, %s, %s, %s)
        """,
        (username, password_hash, full_name, role),
        commit=True
    )
    row = execute_query(
        "SELECT * FROM users WHERE username = %s",
        (username,), fetchone=True
    )
    return User(**row)


def validate_user(username: str, password_hash: str) -> Optional[User]:
    row = execute_query(
        "SELECT * FROM users WHERE username = %s AND password_hash = %s",
        (username, password_hash),
        fetchone=True
    )
    if row:
        return User(**row)
    return None


# Курсы

def get_all_courses() -> List[Course]:
    rows = execute_query(
        "SELECT * FROM courses ORDER BY id",
        fetchall=True
    )
    return [Course(**row) for row in rows]


def get_lessons_by_course(course_id: int) -> List[Lesson]:
    rows = execute_query(
        "SELECT * FROM lessons WHERE course_id = %s ORDER BY order_index, id",
        (course_id,),
        fetchall=True
    )
    return [Lesson(**row) for row in rows]


def get_lesson_by_id(lesson_id: int) -> Optional[Lesson]:
    row = execute_query(
        "SELECT * FROM lessons WHERE id = %s",
        (lesson_id,),
        fetchone=True
    )
    if row:
        return Lesson(**row)
    return None


# Тесты

def get_questions_by_lesson(lesson_id: int) -> List[Question]:
    rows = execute_query(
        "SELECT * FROM questions WHERE lesson_id = %s",
        (lesson_id,),
        fetchall=True
    )
    return [Question(**row) for row in rows]


def get_answers_by_question(question_id: int) -> List[Answer]:
    rows = execute_query(
        "SELECT * FROM answers WHERE question_id = %s",
        (question_id,),
        fetchall=True
    )
    return [Answer(**row) for row in rows]


def create_test_attempt(user_id: int, lesson_id: int, max_score: int) -> int:
    # возвращаем id попытки
    row = execute_query(
        """
        INSERT INTO test_attempts (user_id, lesson_id, max_score)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (user_id, lesson_id, max_score),
        fetchone=True
    )
    return row["id"]


def finish_test_attempt(attempt_id: int, score: int):
    execute_query(
        """
        UPDATE test_attempts
        SET score = %s, finished_at = NOW()
        WHERE id = %s
        """,
        (score, attempt_id),
        commit=True
    )


def save_attempt_answer(attempt_id: int, question_id: int, answer_id: int, is_correct: bool):
    execute_query(
        """
        INSERT INTO attempt_answers (attempt_id, question_id, selected_answer_id, is_correct)
        VALUES (%s, %s, %s, %s)
        """,
        (attempt_id, question_id, answer_id, is_correct),
        commit=True
    )


def get_results_by_user(user_id: int):
    return execute_query(
        """
        SELECT ta.id, l.title AS lesson_title, ta.score, ta.max_score, ta.started_at, ta.finished_at
        FROM test_attempts ta
        JOIN lessons l ON l.id = ta.lesson_id
        WHERE ta.user_id = %s
        ORDER BY ta.started_at DESC
        """,
        (user_id,),
        fetchall=True
    )
