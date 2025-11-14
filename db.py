import sqlite3, os

DB_PATH = os.path.join("data", "game.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            high_score INTEGER,
            total_stars INTEGER,
            games_played INTEGER,
            total_aliens INTEGER,
            total_meteors INTEGER
        )
    """)

    cur.execute("SELECT COUNT(*) FROM stats")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO stats VALUES (1, 0, 0, 0, 0, 0)")
    conn.commit()
    conn.close()

def load_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM stats WHERE id=1")
    data = cur.fetchone()
    conn.close()

    return {
        "high_score": data[1],
        "total_stars": data[2],
        "games_played": data[3],
        "total_aliens": data[4],
        "total_meteors": data[5]
    }

def save_stats(high, stars, aliens, meteors):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE stats SET
            high_score = ?,
            total_stars = total_stars + ?,
            games_played = games_played + 1,
            total_aliens = total_aliens + ?,
            total_meteors = total_meteors + ?
        WHERE id = 1
    """, (high, stars, aliens, meteors))
    conn.commit()
    conn.close()
