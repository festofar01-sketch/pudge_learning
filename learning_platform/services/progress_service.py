from learning_platform.user_service import get_cursor


def save_progress(user_id, level_code, correct, wrong, total):
    cur = get_cursor()
    percent = int((correct / total) * 100) if total else 0

    # проверяем, есть ли уже запись
    cur.execute("""
        SELECT id FROM progress
        WHERE user_id = %s AND level_code = %s
    """, (user_id, level_code))

    row = cur.fetchone()

    if row:
        # UPDATE
        cur.execute("""
            UPDATE progress
            SET correct = %s,
                wrong = %s,
                total = %s,
                percent = %s,
                created_at = NOW()
            WHERE user_id = %s AND level_code = %s
        """, (correct, wrong, total, percent, user_id, level_code))
    else:
        # INSERT
        cur.execute("""
            INSERT INTO progress (user_id, level_code, correct, wrong, total, percent)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, level_code, correct, wrong, total, percent))


def get_user_progress(user_id):
    cur = get_cursor()
    cur.execute("""
        SELECT level_code, correct, wrong, total, percent, created_at
        FROM progress
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    return cur.fetchall()
