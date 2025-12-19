from learning_platform.user_service import get_connection


def save_progress(user_id, level_code, correct, wrong, total):
    conn = get_connection()
    cur = conn.cursor()

    percent = int((correct / total) * 100) if total else 0

    cur.execute("""
        SELECT id FROM progress
        WHERE user_id = %s AND level_code = %s
    """, (user_id, level_code))

    row = cur.fetchone()

    if row:
        cur.execute("""
            UPDATE progress
            SET correct = %s,
                wrong = %s,
                total = %s,
                percent = %s
            WHERE user_id = %s AND level_code = %s
        """, (correct, wrong, total, percent, user_id, level_code))
    else:
        cur.execute("""
            INSERT INTO progress (user_id, level_code, correct, wrong, total, percent)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, level_code, correct, wrong, total, percent))

    conn.commit()
    conn.close()


def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT level_code, correct, wrong, total, percent, created_at
        FROM progress
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows
