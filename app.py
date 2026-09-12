from flask import Flask, request, render_template, redirect
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT,
            clicks INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_short_code(conn, length=6):
    # random instead of using the row id - people could guess /1, /2, /3...
    while True:
        code = ''.join(random.choice(ALPHABET) for _ in range(length))
        exists = conn.execute('SELECT 1 FROM urls WHERE short_code = ?', (code,)).fetchone()
        if exists is None:
            return code

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['url']

        conn = get_db()
        short_code = generate_short_code(conn)
        conn.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        conn.commit()
        conn.close()

        short_url = request.host_url + short_code

    return render_template('index.html', short_url=short_url)

@app.route('/<code>')
def redirect_to_url(code):
    conn = get_db()
    row = conn.execute('SELECT * FROM urls WHERE short_code = ?', (code,)).fetchone()
    if row is None:
        return "Short link not found", 404

    conn.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (code,))
    conn.commit()
    conn.close()
    return redirect(row['original_url'])

@app.route('/stats/<code>')
def stats(code):
    conn = get_db()
    row = conn.execute('SELECT * FROM urls WHERE short_code = ?', (code,)).fetchone()
    conn.close()
    if row is None:
        return "Short link not found", 404

    return render_template('stats.html', row=row)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
