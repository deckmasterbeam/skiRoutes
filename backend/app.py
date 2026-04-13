from flask import Flask, request, jsonify
import json
from user_store import init_db, insert_login

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response


init_db()

@app.route('/api/save_user', methods=['POST', 'OPTIONS'])
def save_user():
    if request.method == 'OPTIONS':
        return ('', 200)

    data = request.json
    sub = data.get('sub')
    email = data.get('email')
    name = data.get('name')
    raw_json = json.dumps(data, sort_keys=True)
    print(f"Received user data: sub={sub}, email={email}, name={name}")
    if not sub:
        return jsonify({'error': 'Missing sub'}), 400
    insert_login(sub, email, name, raw_json)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
