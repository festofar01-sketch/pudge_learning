import psycopg2
import hashlib
from dataclasses import dataclass


# ============================================
#               НАСТРОЙКИ БД
# ============================================
DB_CONFIG = {
    "dbname": "pudge_learning",
    "user": "postgres",
    "password": "Ramil2007",
    "host": "localhost",
    "port": "5432"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()


# ============================================
#               РОЛИ
# ============================================
ROLES = ("user", "teacher", "admin")


# ============================================
#               МОДЕЛЬ USER
# ============================================
@dataclass
class User:
    id: int
    username: str
    role: str
    full_name: str | None = None


# ============================================
#               ХЭШ ПАРОЛЕЙ
# ============================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ============================================
#                 ЛОГИН
# ============================================
def check_login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, password_hash, role, full_name
        FROM users
        WHERE username = %s
    """, (username,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    user_id, uname, pass_hash, role, full_name = row

    if hash_password(password) != pass_hash:
        return None

    return User(
        id=user_id,
        username=uname,
        role=role,
        full_name=full_name
    )


# ============================================
#               РЕГИСТРАЦИЯ
# ============================================
def register_user(username, password, fullname=None):
    conn, cur = get_cursor()

    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cur.fetchone():
        conn.close()
        raise ValueError("User exists")

    if not fullname:
        fullname = username

    cur.execute("""
        INSERT INTO users (username, password_hash, full_name, role)
        VALUES (%s, %s, %s, 'user')
    """, (username, hash_password(password), fullname))

    conn.commit()
    conn.close()
    return True


# ============================================
#           РАБОТА С ПОЛЬЗОВАТЕЛЯМИ (ADMIN)
# ============================================
def get_all_users():
    conn, cur = get_cursor()
    cur.execute("""
        SELECT id, username, role, full_name
        FROM users
        ORDER BY id
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        User(id=r[0], username=r[1], role=r[2], full_name=r[3])
        for r in rows
    ]


def update_user_role(user_id, role):
    if role not in ROLES:
        raise ValueError("Invalid role")

    conn, cur = get_cursor()
    cur.execute("UPDATE users SET role=%s WHERE id=%s", (role, user_id))
    conn.commit()
    conn.close()


def update_username(user_id, new_username):
    conn, cur = get_cursor()

    cur.execute("SELECT id FROM users WHERE username=%s", (new_username,))
    if cur.fetchone():
        conn.close()
        return False

    cur.execute("UPDATE users SET username=%s WHERE id=%s", (new_username, user_id))
    conn.commit()
    conn.close()
    return True


def update_fullname(user_id, new_fullname):
    conn, cur = get_cursor()
    cur.execute("UPDATE users SET full_name=%s WHERE id=%s", (new_fullname, user_id))
    conn.commit()
    conn.close()
    return True


def update_password(user_id, new_password):
    conn, cur = get_cursor()
    cur.execute(
        "UPDATE users SET password_hash=%s WHERE id=%s",
        (hash_password(new_password), user_id)
    )
    conn.commit()
    conn.close()
    return True


def delete_user(user_id):
    conn, cur = get_cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    conn.close()
    return True


# ============================================
#          УРОВНИ И ВОПРОСЫ (STUDENT)
# ============================================
def load_levels():
    conn, cur = get_cursor()
    cur.execute("SELECT code, name FROM levels ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def load_questions_by_level_and_task(level_code, task_level):
    conn, cur = get_cursor()

    cur.execute("SELECT id FROM levels WHERE code=%s", (level_code,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return []

    level_id = row[0]

    cur.execute("""
        SELECT question, answer1, answer2, answer3, answer4, correct_answer
        FROM questions
        WHERE level_id=%s AND task_level=%s
        ORDER BY id
    """, (level_id, task_level))

    result = []
    for q, a1, a2, a3, a4, correct in cur.fetchall():
        result.append((
            q,
            [
                (a1, correct == 1),
                (a2, correct == 2),
                (a3, correct == 3),
                (a4, correct == 4),
            ]
        ))

    conn.close()
    return result


def load_syntax_questions_by_level(level_code):
    conn, cur = get_cursor()

    cur.execute("""
        SELECT id, sentence, words, correct_order
        FROM syntax_questions
        WHERE level_code=%s
        ORDER BY id
    """, (level_code,))

    questions = []
    for qid, sentence, words, correct_order in cur.fetchall():
        questions.append({
            "id": qid,
            "sentence": sentence,
            "words": words,
            "correct_order": correct_order
        })

    conn.close()
    return questions


# ============================================
#      TEACHER: УПРАВЛЕНИЕ ВОПРОСАМИ
# ============================================
def teacher_get_questions(limit=500):
    conn, cur = get_cursor()
    cur.execute("""
        SELECT q.id, l.code, q.task_level, q.question,
               q.answer1, q.answer2, q.answer3, q.answer4, q.correct_answer
        FROM questions q
        JOIN levels l ON l.id = q.level_id
        ORDER BY q.id DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def teacher_add_question(level_code, task_level, question, a1, a2, a3, a4, correct_answer):
    if correct_answer not in (1, 2, 3, 4):
        raise ValueError("correct_answer must be 1..4")

    conn, cur = get_cursor()

    cur.execute("SELECT id FROM levels WHERE code=%s", (level_code,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise ValueError("Level code not found")

    level_id = row[0]

    cur.execute("""
        INSERT INTO questions
        (level_id, task_level, question, answer1, answer2, answer3, answer4, correct_answer)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (level_id, task_level, question, a1, a2, a3, a4, correct_answer))

    conn.commit()
    conn.close()


def teacher_delete_question(question_id):
    conn, cur = get_cursor()
    cur.execute("DELETE FROM questions WHERE id=%s", (question_id,))
    conn.commit()
    conn.close()


def teacher_update_question(question_id, level_code, task_level, question, a1, a2, a3, a4, correct_answer):
    if correct_answer not in (1, 2, 3, 4):
        raise ValueError("correct_answer must be 1..4")

    conn, cur = get_cursor()

    cur.execute("SELECT id FROM levels WHERE code=%s", (level_code,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise ValueError("Level code not found")

    level_id = row[0]

    cur.execute("""
        UPDATE questions
        SET level_id=%s,
            task_level=%s,
            question=%s,
            answer1=%s,
            answer2=%s,
            answer3=%s,
            answer4=%s,
            correct_answer=%s
        WHERE id=%s
    """, (
        level_id, task_level, question,
        a1, a2, a3, a4,
        correct_answer,
        question_id
    ))

    conn.commit()
    conn.close()


def teacher_search_questions(query_text, limit=200):
    conn, cur = get_cursor()
    cur.execute("""
        SELECT q.id, l.code, q.task_level, q.question,
               q.answer1, q.answer2, q.answer3, q.answer4, q.correct_answer
        FROM questions q
        JOIN levels l ON l.id = q.level_id
        WHERE q.question ILIKE %s
        ORDER BY q.id DESC
        LIMIT %s
    """, (f"%{query_text}%", limit))
    rows = cur.fetchall()
    conn.close()
    return rows


def add_syntax_question(level_code, sentence, words, correct_order):
    conn, cur = get_cursor()
    cur.execute("""
        INSERT INTO syntax_questions (level_code, sentence, words, correct_order)
        VALUES (%s, %s, %s, %s)
    """, (level_code, sentence, words, correct_order))
    conn.commit()
    conn.close()

def teacher_load_questions_by_level_and_task(level_code, task_level):
    """
    Для панели преподавателя.
    Возвращает список: (id, question)
    """
    conn, cur = get_cursor()

    cur.execute("SELECT id FROM levels WHERE code=%s", (level_code,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return []

    level_id = row[0]

    cur.execute("""
        SELECT id, question
        FROM questions
        WHERE level_id=%s AND task_level=%s
        ORDER BY id DESC
    """, (level_id, task_level))

    rows = cur.fetchall()
    conn.close()
    return rows

def teacher_delete_syntax_question(question_id):
    conn, cur = get_cursor()
    cur.execute("DELETE FROM syntax_questions WHERE id=%s", (question_id,))
    conn.commit()
    conn.close()

