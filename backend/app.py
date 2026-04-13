from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'users.db'


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS userLogins (
        sub TEXT PRIMARY KEY,
        email TEXT,
        name TEXT,
        raw_json TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/api/save_user', methods=['POST', 'OPTIONS'])
def save_user():
    if request.method == 'OPTIONS':
        return ('', 200)

    data = request.json
    sub = data.get('sub')
    email = data.get('email')
    name = data.get('name')
    raw_json = str(data)
    print(f"Received user data: sub={sub}, email={email}, name={name}")
    if not sub:
        return jsonify({'error': 'Missing sub'}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO userLogins (sub, email, name, raw_json) VALUES (?, ?, ?, ?)',
              (sub, email, name, raw_json))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
