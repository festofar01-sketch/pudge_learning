import hashlib
from learning_platform.db import fetch_one, execute
from learning_platform.models import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ----------------- Регистрация -----------------

def register_user(username: str, raw_password: str, full_name: str):
    # Проверяем, есть ли такой username
    row = fetch_one("SELECT id FROM users WHERE username = %s", (username,))
    if row:
        raise ValueError("user exists")

    password_hash = hash_password(raw_password)

    # СОЗДАЁМ через execute(), НЕ через cur.execute()
    execute(
        "INSERT INTO users (username, password_hash, full_name) VALUES (%s, %s, %s)",
        (username, password_hash, full_name)
    )

    # Делаем повторный SELECT
    row = fetch_one(
        "SELECT id, username, full_name, created_at FROM users WHERE username = %s",
        (username,)
    )

    return User(
        id=row["id"],
        username=row["username"],
        password_hash=password_hash,
        full_name=row["full_name"],
        created_at=row["created_at"]
    )



# ----------------- Логин -----------------

def login_user(username: str, raw_password: str):
    password_hash = hash_password(raw_password)

    row = fetch_one(
        """
        SELECT id, username, password_hash, full_name, created_at
        FROM users
        WHERE username = %s AND password_hash = %s
        """,
        (username, password_hash)
    )

    if not row:
        return None

    return User(
        id=row["id"],
        username=row["username"],
        password_hash=row["password_hash"],
        full_name=row["full_name"],
        created_at=row["created_at"]
    )

def check_login(username, raw_password):
    row = fetch_one("SELECT * FROM users WHERE username = %s", (username,))

    if not row:
        return None

    user = User(**row)

    if user.blocked:
        raise ValueError("Пользователь заблокирован")

    if user.password_hash != hash_password(raw_password):
        return None

    return user
