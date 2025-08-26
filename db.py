import sqlite3

DB_PATH = "data/lab_notebook.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(title, date, category, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO entries (title, date, category, content) VALUES (?, ?, ?, ?)",
              (title, date, category, content))
    conn.commit()
    conn.close()

def get_entries(search_query=None, category=None, date=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = "SELECT id, title, date, category, content FROM entries WHERE 1=1"
    params = []
    if search_query:
        query += " AND (title LIKE ? OR content LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    if category and category != "All":
        query += " AND category=?"
        params.append(category)
    if date:
        query += " AND date=?"
        params.append(date)
    query += " ORDER BY date DESC"
    c.execute(query, tuple(params))
    results = c.fetchall()
    conn.close()
    return results

def get_entry_by_id(entry_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, date, category, content FROM entries WHERE id=?", (entry_id,))
    result = c.fetchone()
    conn.close()
    return result
