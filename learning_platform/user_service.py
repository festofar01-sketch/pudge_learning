import psycopg2
import hashlib


# ============================================
#               ПОДКЛЮЧЕНИЕ К БД
# ============================================
conn = psycopg2.connect(
    dbname="pudge_learning",
    user="postgres",
    password="Ramil2007",
    host="localhost",
    port="5432"
)
conn.autocommit = True


def get_cursor():
    return conn.cursor()


# ============================================
#               ХЭШ ПАРОЛЕЙ
# ============================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ============================================
#                 ЛОГИН
# ============================================
def check_login(username, password):
    cur = get_cursor()

    cur.execute("SELECT id, username, password_hash FROM users WHERE username=%s", (username,))
    row = cur.fetchone()

    if not row:
        return None

    user_id, uname, pass_hash = row

    if hash_password(password) == pass_hash:
        class User:
            def __init__(self, id, username):
                self.id = id
                self.username = username

        return User(user_id, uname)

    return None


# ============================================
#               РЕГИСТРАЦИЯ
# ============================================
def register_user(username, password, fullname=None):
    cur = get_cursor()

    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cur.fetchone():
        raise ValueError("User exists")

    cur.execute(
        "INSERT INTO users (username, password_hash, full_name) VALUES (%s, %s, %s)",
        (username, hash_password(password), fullname)
    )
    return True


# ============================================
#           ОБНОВЛЕНИЕ ЛОГИНА
# ============================================
def update_username(user_id, new_username):
    cur = get_cursor()

    cur.execute("SELECT id FROM users WHERE username=%s", (new_username,))
    if cur.fetchone():
        return False

    cur.execute(
        "UPDATE users SET username=%s WHERE id=%s",
        (new_username, user_id)
    )
    return True


# ============================================
#           ОБНОВЛЕНИЕ ПОЛНОГО ИМЕНИ
# ============================================
def update_fullname(user_id, new_fullname):
    cur = get_cursor()
    cur.execute(
        "UPDATE users SET full_name=%s WHERE id=%s",
        (new_fullname, user_id)
    )
    return True


# ============================================
#            ОБНОВЛЕНИЕ ПАРОЛЯ
# ============================================
def update_password(user_id, new_password):
    cur = get_cursor()
    cur.execute(
        "UPDATE users SET password_hash=%s WHERE id=%s",
        (hash_password(new_password), user_id)
    )
    return True


# ============================================
#              УДАЛЕНИЕ АККАУНТА
# ============================================
def delete_user(user_id):
    cur = get_cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    return True


# ============================================
#          ЗАГРУЗКА УРОВНЕЙ И ВОПРОСОВ
# ============================================
def load_levels():
    cur = get_cursor()
    cur.execute("SELECT code, name FROM levels ORDER BY id")
    return cur.fetchall()


def load_questions_by_level_and_task(level_code, task_level):
    cur = get_cursor()

    cur.execute(
        "SELECT id FROM levels WHERE code=%s",
        (level_code,)
    )
    row = cur.fetchone()
    if not row:
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
    return result

# ============================================
#          СИНТАКСИС (Собери предложение)
# ============================================

def load_syntax_questions_by_level(level_code):
    cur = get_cursor()

    cur.execute("""
        SELECT id, sentence, words, correct_order
        FROM syntax_questions
        WHERE level_code = %s
        ORDER BY id
    """, (level_code,))

    questions = []
    for qid, sentence, words, correct_order in cur.fetchall():
        questions.append({
            "id": qid,
            "sentence": sentence,
            "words": words,                 # text[] → list[str]
            "correct_order": correct_order  # text[] → list[str]
        })

    return questions

